from typing import Dict, List, Optional
from datetime import datetime
import uuid

from models.alert import Alert
from models.user import User
from models.notification import UserAlertPreference, NotificationStatus, NotificationDelivery
from services.delivery.delivery_factory import DeliveryFactory
from patterns.observer import AlertObserver

class NotificationService(AlertObserver):
    def __init__(self, alert_service, delivery_logger=None):
        self.alert_service = alert_service
        self.alert_service.add_observer(self)
        self._user_preferences: Dict[str, Dict[str, UserAlertPreference]] = {}  # user_id -> {alert_id -> preference}
        self._delivery_log: List[NotificationDelivery] = []
        self.delivery_logger = delivery_logger
    
    def on_alert_created(self, alert: Alert):
        print(f"📢 Notification: New alert created - '{alert.title}'")
        self._create_preferences_for_alert(alert)
        self._deliver_initial_notifications(alert)
    
    def on_alert_updated(self, alert: Alert):
        print(f"📢 Notification: Alert updated - '{alert.title}'")
        # Re-deliver to relevant users if needed
        if alert.is_active and not alert.is_expired():
            self._deliver_to_eligible_users(alert)
    
    def on_alert_archived(self, alert: Alert):
        print(f"📢 Notification: Alert archived - '{alert.title}'")
    
    def _create_preferences_for_alert(self, alert: Alert):
        # Create preferences for all eligible users
        eligible_users = self._get_eligible_users_for_alert(alert)
        for user in eligible_users:
            self.get_or_create_preference(user.user_id, alert.alert_id)
    
    def _get_eligible_users_for_alert(self, alert: Alert) -> List[User]:
        eligible_users = []
        all_users = self.alert_service.get_all_users()
        
        for user in all_users:
            user_teams = self.alert_service.get_user_teams(user.user_id)
            if alert.is_visible_to_user(user, user_teams):
                eligible_users.append(user)
        
        return eligible_users
    
    def _deliver_initial_notifications(self, alert: Alert):
        eligible_users = self._get_eligible_users_for_alert(alert)
        for user in eligible_users:
            self.deliver_notification(user, alert, is_initial=True)
    
    def _deliver_to_eligible_users(self, alert: Alert):
        eligible_users = self._get_eligible_users_for_alert(alert)
        for user in eligible_users:
            self.deliver_notification(user, alert)
    
    def get_or_create_preference(self, user_id: str, alert_id: str) -> UserAlertPreference:
        if user_id not in self._user_preferences:
            self._user_preferences[user_id] = {}
        
        if alert_id not in self._user_preferences[user_id]:
            self._user_preferences[user_id][alert_id] = UserAlertPreference(user_id, alert_id)
        
        return self._user_preferences[user_id][alert_id]
    
    def get_user_preference(self, user_id: str, alert_id: str) -> Optional[UserAlertPreference]:
        user_prefs = self._user_preferences.get(user_id, {})
        return user_prefs.get(alert_id)
    
    def mark_as_read(self, user_id: str, alert_id: str):
        preference = self.get_or_create_preference(user_id, alert_id)
        preference.mark_read()
        print(f"📖 User {user_id} marked alert '{alert_id}' as read")
    
    def mark_as_unread(self, user_id: str, alert_id: str):
        preference = self.get_or_create_preference(user_id, alert_id)
        preference.mark_unread()
        print(f"📖 User {user_id} marked alert '{alert_id}' as unread")
    
    def snooze_alert(self, user_id: str, alert_id: str):
        preference = self.get_or_create_preference(user_id, alert_id)
        preference.snooze_until_tomorrow()
        print(f"⏰ User {user_id} snoozed alert '{alert_id}' until tomorrow")
    
    def deliver_notification(self, user: User, alert: Alert, is_initial: bool = False) -> bool:
        if alert.is_expired() or not alert.is_active:
            return False
        
        preference = self.get_or_create_preference(user.user_id, alert.alert_id)
        
        # For initial delivery, always send regardless of reminder timing
        if not is_initial and not preference.should_remind(alert.reminder_frequency):
            return False
        
        # Create delivery channel
        try:
            delivery_channel = DeliveryFactory.create_channel(
                alert.delivery_type,
                delivery_logger=self.delivery_logger
            )
            
            success = delivery_channel.send(user, alert)
            if success:
                preference.update_reminder_time()
                self._log_delivery(user.user_id, alert.alert_id, alert.delivery_type.value)
            
            return success
        except Exception as e:
            print(f"❌ Failed to deliver notification: {e}")
            return False
    
    def _log_delivery(self, user_id: str, alert_id: str, delivery_type: str):
        delivery = NotificationDelivery(
            delivery_id=str(uuid.uuid4()),
            user_id=user_id,
            alert_id=alert_id,
            delivery_type=delivery_type
        )
        self._delivery_log.append(delivery)
    
    def get_user_alerts_with_preferences(self, user_id: str) -> List[dict]:
        alerts = self.alert_service.get_alerts_for_user(user_id)
        result = []
        
        for alert in alerts:
            preference = self.get_or_create_preference(user_id, alert.alert_id)
            result.append({
                'alert': alert,
                'preference': preference,
                'status': preference.status.value,
                'is_snoozed': preference.is_snoozed(),
                'last_reminded': preference.last_reminded_at
            })
        
        # Sort by creation date (newest first)
        result.sort(key=lambda x: x['alert'].created_at, reverse=True)
        return result
    
    def process_reminders(self):
        """Process all pending reminders for all users"""
        print("⏰ Processing reminders...")
        reminder_count = 0
        
        for user_id, alert_prefs in self._user_preferences.items():
            user = self.alert_service.get_user(user_id)
            if not user:
                continue
                
            for alert_id, preference in alert_prefs.items():
                alert = self.alert_service.get_alert(alert_id)
                if alert and alert.reminders_enabled and alert.is_active:
                    if self.deliver_notification(user, alert):
                        reminder_count += 1
        
        print(f"✅ Sent {reminder_count} reminders")
        return reminder_count
    
    def get_delivery_stats(self) -> Dict[str, int]:
        return {
            "total_deliveries": len(self._delivery_log),
            "unique_users": len(self._user_preferences),
            "user_preferences": sum(len(prefs) for prefs in self._user_preferences.values())
        }