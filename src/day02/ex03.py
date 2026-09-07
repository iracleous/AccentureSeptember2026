# Dataclass: auto-generates __init__, __repr__, __eq__ but no runtime validation
# field(default_factory=list) prevents mutable default issues

from dataclasses import dataclass, field


@dataclass
class SupportTicket:
    # @dataclass decorator creates __init__, __repr__, __eq__ automatically
    ticket_id: str
    issue: str
    priority: str = "medium"
    tags: list[str] = field(default_factory=list)  # Safe mutable default

    def is_urgent(self) -> bool:
        # Check if priority is critical
        return self.priority == "critical"


if __name__ == "__main__":
    # Create ticket and test equality
    t1 = SupportTicket("T-101", "Cannot reset password", tags=["auth"])
    print(t1)
    print(t1 == SupportTicket("T-101", "Cannot reset password", tags=["auth"]))
    print(t1.is_urgent())

    # Accepts int for priority (no validation) - type hint is not enforced at runtime
    broken = SupportTicket("T-102", "Server down", priority=999)
    print(broken)
