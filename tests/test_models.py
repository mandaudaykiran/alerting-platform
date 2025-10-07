import unittest
import sys
import os
from datetime import datetime, timedelta

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.user import User, UserRole
from models.alert import Alert, AlertVisibility, VisibilityType, Severity, DeliveryType
from models.notification import UserAlertPreference, NotificationStatus
from models.team import Team

class TestUserModel(unittest.TestCase):
    
    def setUp(self):
        self.user = User("user1", "John Doe", "john@example.com")
    
    def test_user_creation(self):
        self.assertEqual(self.user.user_id, "user1")
        self.assertEqual(self.user.name, "John Doe")
        self.assertEqual(self.user.email, "john@example.com")
        self.assertEqual(self.user.role, UserRole.USER)
    
    def test_admin_user(self):
        admin = User("admin1", "Admin User", "admin@example.com", UserRole.ADMIN)
        self.assertTrue(admin.is_admin())
        self.assertFalse(self.user.is_admin())
    
    def test_team_management(self):
        self.user.add_to_team("team1")
        self.assertIn("team1", self.user.teams)
        self.assertTrue(self.user.is_in_team("team1"))
        self.assertFalse(self.user.is_in_team("team2"))

class TestAlertModel(unittest.TestCase):
    
    def setUp(self):
        visibility = AlertVisibility(VisibilityType.ORGANIZATION, set())
        self.alert = Alert(
            "alert1", "Test Alert", "Test Message", 
            Severity.INFO, "admin1", visibility
        )
    
    def test_alert_creation(self):
        self.assertEqual(self.alert.title, "Test Alert")
        self.assertEqual(self.alert.severity, Severity.INFO)
        self.assertTrue(self.alert.is_active)
        self.assertFalse(self.alert.is_expired())
    
    def test_alert_expiry(self):
        past_time = datetime.now() - timedelta(days=1)
        visibility = AlertVisibility(VisibilityType.ORGANIZATION, set())
        expired_alert = Alert(
            "alert2", "Expired Alert", "Message",
            Severity.WARNING, "admin1", visibility,
            expiry_time=past_time
        )
        self.assertTrue(expired_alert.is_expired())
    
    def test_alert_visibility(self):
        user = User("user1", "Test User", "test@example.com")
        
        # Organization visibility - should be visible to all
        org_visibility = AlertVisibility(VisibilityType.ORGANIZATION, set())
        org_alert = Alert("alert3", "Org Alert", "Message", Severity.INFO, "admin1", org_visibility)
        self.assertTrue(org_alert.is_visible_to_user(user, set()))
        
        # Team visibility - user not in team
        team_visibility = AlertVisibility(VisibilityType.TEAM, {"team1"})
        team_alert = Alert("alert4", "Team Alert", "Message", Severity.INFO, "admin1", team_visibility)
        self.assertFalse(team_alert.is_visible_to_user(user, set()))
        
        # Team visibility - user in team
        self.assertTrue(team_alert.is_visible_to_user(user, {"team1"}))
        
        # User visibility - specific user
        user_visibility = AlertVisibility(VisibilityType.USER, {"user1"})
        user_alert = Alert("alert5", "User Alert", "Message", Severity.INFO, "admin1", user_visibility)
        self.assertTrue(user_alert.is_visible_to_user(user, set()))
        
        # User visibility - different user
        self.assertFalse(user_alert.is_visible_to_user(User("user2", "Other", "other@example.com"), set()))

class TestNotificationModel(unittest.TestCase):
    
    def setUp(self):
        self.preference = UserAlertPreference("user1", "alert1")
    
    def test_preference_creation(self):
        self.assertEqual(self.preference.user_id, "user1")
        self.assertEqual(self.preference.alert_id, "alert1")
        self.assertEqual(self.preference.status, NotificationStatus.UNREAD)
    
    def test_mark_read(self):
        self.preference.mark_read()
        self.assertEqual(self.preference.status, NotificationStatus.READ)
        self.assertIsNotNone(self.preference.read_at)
    
    def test_snooze(self):
        self.preference.snooze_until_tomorrow()
        self.assertEqual(self.preference.status, NotificationStatus.SNOOZED)
        self.assertIsNotNone(self.preference.snoozed_until)
        self.assertTrue(self.preference.is_snoozed())
    
    def test_reminder_logic(self):
        # Should remind initially (no last reminder time)
        self.assertTrue(self.preference.should_remind(120))
        
        # Update reminder time and check again
        self.preference.update_reminder_time()
        self.assertFalse(self.preference.should_remind(120))  # Just reminded, shouldn't remind again immediately

class TestTeamModel(unittest.TestCase):
    
    def setUp(self):
        self.team = Team("team1", "Engineering")
    
    def test_team_creation(self):
        self.assertEqual(self.team.team_id, "team1")
        self.assertEqual(self.team.name, "Engineering")
        self.assertEqual(self.team.get_member_count(), 0)
    
    def test_member_management(self):
        self.team.add_member("user1")
        self.team.add_member("user2")
        self.assertEqual(self.team.get_member_count(), 2)
        self.assertIn("user1", self.team.member_ids)
        self.assertIn("user2", self.team.member_ids)
        
        self.team.remove_member("user1")
        self.assertEqual(self.team.get_member_count(), 1)
        self.assertNotIn("user1", self.team.member_ids)

if __name__ == '__main__':
    unittest.main()