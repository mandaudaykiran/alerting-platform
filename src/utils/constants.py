"""
Application constants
"""

# Reminder frequencies in minutes
DEFAULT_REMINDER_FREQUENCY = 120  # 2 hours
SNOOZE_DURATION_HOURS = 24

# Delivery types
SUPPORTED_DELIVERY_TYPES = ["in_app"]

# Severity levels
SEVERITY_LEVELS = ["info", "warning", "critical"]

# Visibility types
VISIBILITY_TYPES = ["organization", "team", "user"]

# User roles
USER_ROLES = ["admin", "user"]

# Notification statuses
NOTIFICATION_STATUSES = ["unread", "read", "snoozed"]

# System settings
MAX_ALERTS_PER_USER = 1000
MAX_TEAMS_PER_USER = 10
MAX_USERS_PER_TEAM = 100

# Time formats
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

# Logging
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# API settings
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 1000

# Error messages
ERROR_MESSAGES = {
    "user_not_found": "User not found",
    "alert_not_found": "Alert not found", 
    "team_not_found": "Team not found",
    "permission_denied": "Permission denied",
    "invalid_visibility": "Invalid visibility configuration",
    "delivery_failed": "Notification delivery failed"
}

# Success messages
SUCCESS_MESSAGES = {
    "alert_created": "Alert created successfully",
    "alert_updated": "Alert updated successfully",
    "alert_archived": "Alert archived successfully",
    "notification_sent": "Notification sent successfully",
    "user_preference_updated": "User preference updated successfully"
}