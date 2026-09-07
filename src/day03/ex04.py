# Logging demo: config, loggers, levels, handlers, extra fields, propagation

import logging

# Configure root logger with timestamp, level, logger name, message
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s  %(levelname)-8s  %(name)s - %(message)s",
)

# Get logger and demonstrate log levels (debug, info, warning, error)
logger = logging.getLogger("tickets")
logger.debug("Detailed diagnostic info (dev only)")
logger.info("Ticket service started")
logger.warning("SLA config missing -- falling back to default (60 min)")
logger.error("Could not reach the notifications queue")

# Child logger inherits from parent
child = logging.getLogger("tickets.escalation")
child.info("Escalation worker initialised")

# Extra fields in log records
logger.info("Ticket created", extra={"ticket_id": "T-101", "priority": "high"})

# Create file and stream handlers (for screen) with different levels
file_handler = logging.FileHandler("tickets.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Custom logger with custom handlers and propagation disabled
routed = logging.getLogger("tickets.routed")
routed.setLevel(logging.DEBUG)
routed.handlers.clear()
routed.addHandler(file_handler)
routed.addHandler(stream_handler)
routed.propagate = False  # True for Bubble up to root logger

# Debug goes to file only, info goes to both file and console
routed.debug("Only written to tickets.log")
routed.info("Written to both tickets.log and the console")

# usually
logger = logging.getLogger(__name__)
logger.info("Log message....")
