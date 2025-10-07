from abc import ABC, abstractmethod
from datetime import datetime

class NotificationState(ABC):
    """State interface for notification status"""
    
    @abstractmethod
    def mark_read(self, preference):
        """Mark notification as read"""
        pass
    
    @abstractmethod
    def mark_unread(self, preference):
        """Mark notification as unread"""
        pass
    
    @abstractmethod
    def snooze(self, preference):
        """Snooze notification"""
        pass
    
    @abstractmethod
    def get_status(self) -> str:
        """Get current status"""
        pass
    
    @abstractmethod
    def can_remind(self) -> bool:
        """Check if reminders can be sent in this state"""
        pass

class UnreadState(NotificationState):
    """State for unread notifications"""
    
    def mark_read(self, preference):
        preference.status = "read"
        preference.read_at = datetime.now()
        preference._state = ReadState()
        print(f"✅ Marked alert {preference.alert_id} as READ")
    
    def mark_unread(self, preference):
        # Already unread, do nothing
        print("ℹ️  Alert is already UNREAD")
    
    def snooze(self, preference):
        preference.snooze_until_tomorrow()
        preference._state = SnoozedState()
        print(f"⏰ Snoozed alert {preference.alert_id} until tomorrow")
    
    def get_status(self) -> str:
        return "unread"
    
    def can_remind(self) -> bool:
        return True
    
    def __str__(self):
        return "UNREAD"

class ReadState(NotificationState):
    """State for read notifications"""
    
    def mark_read(self, preference):
        # Already read, do nothing
        print("ℹ️  Alert is already READ")
    
    def mark_unread(self, preference):
        preference.status = "unread"
        preference.read_at = None
        preference._state = UnreadState()
        print(f"✅ Marked alert {preference.alert_id} as UNREAD")
    
    def snooze(self, preference):
        # Cannot snooze a read notification
        print("❌ Cannot snooze a READ alert")
    
    def get_status(self) -> str:
        return "read"
    
    def can_remind(self) -> bool:
        return False
    
    def __str__(self):
        return "READ"

class SnoozedState(NotificationState):
    """State for snoozed notifications"""
    
    def mark_read(self, preference):
        preference.status = "read"
        preference.read_at = datetime.now()
        preference.snoozed_until = None
        preference._state = ReadState()
        print(f"✅ Marked snoozed alert {preference.alert_id} as READ")
    
    def mark_unread(self, preference):
        preference.status = "unread"
        preference.read_at = None
        preference.snoozed_until = None
        preference._state = UnreadState()
        print(f"✅ Marked snoozed alert {preference.alert_id} as UNREAD")
    
    def snooze(self, preference):
        # Resnooze until tomorrow
        preference.snooze_until_tomorrow()
        print(f"⏰ Resnoozed alert {preference.alert_id} until tomorrow")
    
    def get_status(self) -> str:
        return "snoozed"
    
    def can_remind(self) -> bool:
        return False
    
    def __str__(self):
        return "SNOOZED"