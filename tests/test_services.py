import unittest
import sys
import os
from datetime import datetime, timedelta

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.alert_service import AlertService
from services.notification_service import NotificationService
from models.user import User, UserRole
from models.alert import Severity, VisibilityType, DeliveryType

class TestAlertService(unittest.TestCase):
    
    def setUp(self):
        self.alert_service = AlertService()
        
        # Create test users
        self.admin = User("admin1", "Admin User", "admin@example.com", UserRole.ADMIN)
        self.user1 = User("user1", "User One", "user1@example.com")
        self.user2 = User("user2", "User Two", "user2@example.com")
        
        self.alert_service.add_user(self.admin)
        self.alert_service.add_user(self.user1)
        self.alert_service.add_user(self.user2)
        
        # Create teams
        self.alert_service.add_team("engineering", {"user1"})
        self.alert_service.add_team("marketing", {"user2"})
    
    def test_create_alert(self):
        alert = self.alert_service.create_alert(
            title="Test Alert",
            message="Test Message",
            severity=Severity.INFO,
            created_by="admin1",
            visibility_type=VisibilityType.ORGANIZATION,
            target_ids=set()
        )
        
        self.assertIsNotNone(alert)
        self.assertEqual(alert.title, "Test Alert")
        self.assertEqual(alert.created_by, "admin1")
        self.assertIn(alert.alert_id, self.alert_service._alerts)
    
    def test_user_alert_visibility(self):
        # Create organization alert
        self.alert_service.create_alert(
            title="Org Alert",
            message="Message",
            severity=Severity.INFO,
            created_by="admin1",
            visibility_type=VisibilityType.ORGANIZATION,
            target_ids=set()
        )
        
        # Create team alert
        self.alert_service.create_alert(
            title="Team Alert",
            message="Message",
            severity=Severity.INFO,
            created_by="admin1",
            visibility_type=VisibilityType.TEAM,
            target_ids={"engineering"}
        )
        
        # User1 should see both alerts (org + engineering team)
        user1_alerts = self.alert_service.get_alerts_for_user("user1")
        self.assertEqual(len(user1_alerts), 2)
        
        # User2 should see only org alert
        user2_alerts = self.alert_service.get_alerts_for_user("user2")
        self.assertEqual(len(user2_alerts), 1)
    
    def test_archive_alert(self):
        alert = self.alert_service.create_alert(
            title="Test Alert",
            message="Test Message",
            severity=Severity.INFO,
            created_by="admin1",
            visibility_type=VisibilityType.ORGANIZATION,
            target_ids=set()
        )
        
        self.assertTrue(alert.is_active)
        self.alert_service.archive_alert(alert.alert_id)
        
        archived_alert = self.alert_service.get_alert(alert.alert_id)
        self.assertFalse(archived_alert.is_active)
    
    def test_list_alerts_with_filters(self):
        # Create alerts with different severities
        self.alert_service.create_alert(
            title="Info Alert",
            message="Message",
            severity=Severity.INFO,
            created_by="admin1",
            visibility_type=VisibilityType.ORGANIZATION,
            target_ids=set()
        )
        
        self.alert_service.create_alert(
            title="Warning Alert",
            message="Message",
            severity=Severity.WARNING,
            created_by="admin1",
            visibility_type=VisibilityType.ORGANIZATION,
            target_ids=set()
        )
        
        # Test severity filter
        info_alerts = self.alert_service.list_all_alerts(severity=Severity.INFO)
        self.assertEqual(len(info_alerts), 1)
        self.assertEqual(info_alerts[0].severity, Severity.INFO)
        
        # Test status filter
        active_alerts = self.alert_service.list_all_alerts(status="active")
        self.assertEqual(len(active_alerts), 2)

class TestNotificationService(unittest.TestCase):
    
    def setUp(self):
        self.alert_service = AlertService()
        self.notification_service = NotificationService(self.alert_service)
        
        # Create test users
        self.user1 = User("user1", "User One", "user1@example.com")
        self.user2 = User("user2", "User Two", "user2@example.com")
        
        self.alert_service.add_user(self.user1)
        self.alert_service.add_user(self.user2)
        self.alert_service.add_team("engineering", {"user1"})
    
    def test_user_preference_management(self):
        # Create an alert
        alert = self.alert_service.create_alert(
            title="Test Alert",
            message="Test Message",
            severity=Severity.INFO,
            created_by="admin1",
            visibility_type=VisibilityType.ORGANIZATION,
            target_ids=set()
        )
        
        # Get or create preference
        preference = self.notification_service.get_or_create_preference("user1", alert.alert_id)
        self.assertEqual(preference.user_id, "user1")
        self.assertEqual(preference.alert_id, alert.alert_id)
        
        # Mark as read
        self.notification_service.mark_as_read("user1", alert.alert_id)
        updated_preference = self.notification_service.get_user_preference("user1", alert.alert_id)
        self.assertEqual(updated_preference.status.value, "read")
        
        # Snooze alert
        self.notification_service.snooze_alert("user1", alert.alert_id)
        snoozed_preference = self.notification_service.get_user_preference("user1", alert.alert_id)
        self.assertEqual(snoozed_preference.status.value, "snoozed")
        self.assertTrue(snoozed_preference.is_snoozed())
    
    def test_get_user_alerts_with_preferences(self):
        # Create alerts
        alert1 = self.alert_service.create_alert(
            title="Alert 1",
            message="Message 1",
            severity=Severity.INFO,
            created_by="admin1",
            visibility_type=VisibilityType.ORGANIZATION,
            target_ids=set()
        )
        
        alert2 = self.alert_service.create_alert(
            title="Alert 2",
            message="Message 2",
            severity=Severity.WARNING,
            created_by="admin1",
            visibility_type=VisibilityType.TEAM,
            target_ids={"engineering"}
        )
        
        # User1 should see both alerts
        user1_alerts = self.notification_service.get_user_alerts_with_preferences("user1")
        self.assertEqual(len(user1_alerts), 2)
        
        # Check structure of returned data
        for alert_data in user1_alerts:
            self.assertIn('alert', alert_data)
            self.assertIn('preference', alert_data)
            self.assertIn('status', alert_data)
            self.assertIn('is_snoozed', alert_data)
    
    def test_observer_pattern(self):
        # Test that notification service is properly observing alert service
        initial_observer_count = self.alert_service.get_observer_count()
        
        # Create a new notification service (should register as observer)
        new_notification_service = NotificationService(self.alert_service)
        self.assertEqual(self.alert_service.get_observer_count(), initial_observer_count + 1)
        
        # Create alert should trigger observer
        alert = self.alert_service.create_alert(
            title="Observer Test",
            message="Testing observer pattern",
            severity=Severity.INFO,
            created_by="admin1",
            visibility_type=VisibilityType.ORGANIZATION,
            target_ids=set()
        )

if __name__ == '__main__':
    unittest.main()