# Pydantic model with runtime validation, constraints, and custom validators

from pydantic import BaseModel, Field, ValidationError, field_validator

PRIORITIES = {"low", "medium", "high", "critical"}


class SupportTicket(BaseModel):
    # Validates types, applies Field constraints (gt=0), and custom validators
    ticket_id: str
    issue: str
    priority: str = "medium"
    sla_minutes: int = Field(default=60, gt=0, description="Minutes until SLA breach")
    tags: list[str] = Field(default_factory=list)
    assignee: str | None = None

    @field_validator("priority")  # Custom validation for priority enum
    @classmethod
    def priority_must_be_known(cls, value: str) -> str:
        if value not in PRIORITIES:
            raise ValueError(
                f"priority must be one of {sorted(PRIORITIES)}, got {value!r}"
            )
        return value


if __name__ == "__main__":
    # Valid ticket with string-to-int coercion for sla_minutes
    ticket = SupportTicket(
        ticket_id="T-201", issue="Checkout crashes", sla_minutes="30", tags=["payments"]
    )
    print(ticket)
    # serialization to dict (model_dump) and JSON (model_dump_json)
    print(ticket.model_dump())
    print(ticket.model_dump_json())

    # Type error: priority expects str, got int
    try:
        SupportTicket(ticket_id="T-202", issue="Server down", priority=999)
    except ValidationError as e:
        print(f"Rejected -- bad type for priority:\n{e}")

    # Constraint violation: sla_minutes must be > 0 (Field constraint)
    try:
        SupportTicket(ticket_id="T-203", issue="Bad SLA", sla_minutes=-5)
    except ValidationError as e:
        print(f"Rejected -- sla_minutes must be > 0:\n{e}")

    # Custom validator: priority must match PRIORITIES set
    try:
        SupportTicket(ticket_id="T-204", issue="Typo'd priority", priority="urgent")
    except ValidationError as e:
        print(f"Rejected -- custom validator caught an unknown priority:\n{e}")


    # Print the JSON schema for the SupportTicket model for seeing the use of field descriptions
    print(SupportTicket.model_json_schema())
