from datetime import datetime
from enum import Enum
from typing import Set, Optional
from dataclasses import dataclass

class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class DeliveryType(Enum):
    IN_APP = "in_app"
    EMAIL = "email"
    SMS = "sms"

class VisibilityType(Enum):
    ORGANIZATION = "organization"
    TEAM = "team"
    USER = "user"

@dataclass
class AlertVisibility:
    type: VisibilityType
    target_ids: Set[str]  # team_ids or user_ids

class Alert:
    def __init__(
        self,
        alert_id: str,
        title: str,
        message: str,
        severity: Severity,
        created_by: str,
        visibility: AlertVisibility,
        delivery_type: DeliveryType = DeliveryType.IN_APP,
        reminder_frequency: int = 120,  # minutes
        start_time: Optional[datetime] = None,
        expiry_time: Optional[datetime] = None
    ):
        self.alert_id = alert_id
        self.title = title
        self.message = message
        self.severity = severity
        self.created_by = created_by
        self.visibility = visibility
        self.delivery_type = delivery_type
        self.reminder_frequency = reminder_frequency
        self.start_time = start_time or datetime.now()
        self.expiry_time = expiry_time
        self.is_active = True
        self.reminders_enabled = True
        self.created_at = datetime.now()
    
    def is_expired(self) -> bool:
        if self.expiry_time:
            return datetime.now() > self.expiry_time
        return False
    
    def is_visible_to_user(self, user: 'User', user_teams: Set[str]) -> bool:
        if not self.is_active or self.is_expired():
            return False
        
        if self.visibility.type == VisibilityType.ORGANIZATION:
            return True
        elif self.visibility.type == VisibilityType.TEAM:
            return any(team_id in user_teams for team_id in self.visibility.target_ids)
        elif self.visibility.type == VisibilityType.USER:
            return user.user_id in self.visibility.target_ids
        return False
    
    def archive(self):
        self.is_active = False
    
    def update(
        self,
        title: Optional[str] = None,
        message: Optional[str] = None,
        severity: Optional[Severity] = None,
        expiry_time: Optional[datetime] = None,
        reminders_enabled: Optional[bool] = None
    ):
        if title is not None:
            self.title = title
        if message is not None:
            self.message = message
        if severity is not None:
            self.severity = severity
        if expiry_time is not None:
            self.expiry_time = expiry_time
        if reminders_enabled is not None:
            self.reminders_enabled = reminders_enabled
    
    def __repr__(self):
        return f"Alert(id={self.alert_id}, title={self.title}, severity={self.severity.value})"
    
    def __str__(self):
        status = "ACTIVE" if self.is_active else "ARCHIVED"
        return f"{self.title} [{self.severity.value}] - {status}"