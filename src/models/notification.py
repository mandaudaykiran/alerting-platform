from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

class NotificationStatus(Enum):
    UNREAD = "unread"
    READ = "read"
    SNOOZED = "snoozed"

class UserAlertPreference:
    def __init__(self, user_id: str, alert_id: str):
        self.user_id = user_id
        self.alert_id = alert_id
        self.status = NotificationStatus.UNREAD
        self.snoozed_until: Optional[datetime] = None
        self.last_reminded_at: Optional[datetime] = None
        self.read_at: Optional[datetime] = None
        self.created_at = datetime.now()
    
    def mark_read(self):
        self.status = NotificationStatus.READ
        self.read_at = datetime.now()
    
    def mark_unread(self):
        self.status = NotificationStatus.UNREAD
        self.read_at = None
    
    def snooze_until_tomorrow(self):
        tomorrow = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        self.status = NotificationStatus.SNOOZED
        self.snoozed_until = tomorrow
    
    def is_snoozed(self) -> bool:
        if self.status != NotificationStatus.SNOOZED or not self.snoozed_until:
            return False
        return datetime.now() < self.snoozed_until
    
    def should_remind(self, reminder_frequency: int) -> bool:
        if self.status == NotificationStatus.READ or self.is_snoozed():
            return False
        
        if not self.last_reminded_at:
            return True
        
        time_since_last_reminder = datetime.now() - self.last_reminded_at
        return time_since_last_reminder.total_seconds() >= reminder_frequency * 60
    
    def update_reminder_time(self):
        self.last_reminded_at = datetime.now()
    
    def __repr__(self):
        return f"UserAlertPreference(user={self.user_id}, alert={self.alert_id}, status={self.status.value})"

class NotificationDelivery:
    def __init__(self, delivery_id: str, user_id: str, alert_id: str, delivery_type: str):
        self.delivery_id = delivery_id
        self.user_id = user_id
        self.alert_id = alert_id
        self.delivery_type = delivery_type
        self.delivered_at = datetime.now()
        self.delivery_status = "sent"
    
    def __repr__(self):
        return f"NotificationDelivery(user={self.user_id}, alert={self.alert_id}, type={self.delivery_type})"