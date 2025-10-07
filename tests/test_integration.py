import unittest
import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.alert_service import AlertService
from services.notification_service import NotificationService
from api.admin_api import AdminAPI
from api.user_api import UserAPI
from models.user import User, UserRole
from models.alert import Severity, VisibilityType, DeliveryType
from datetime import datetime, timedelta

class TestIntegration(unittest.TestCase):
    """
    Integration tests for the complete alerting platform workflow
    """
    
    def setUp(self):
        # Initialize all components
        self.alert_service = AlertService()
        self.notification_service = NotificationService(self.alert_service)
        self.admin_api = AdminAPI(self.alert_service)
        self.user_api = UserAPI(self.alert_service, self.notification_service)
        
        # Create test data
        self.setup_test_data()
    
    def setup_test_data(self):
        """Setup test users, teams, and initial alerts"""
        # Create users
        admin = User("admin1", "System Admin", "admin@company.com", UserRole.ADMIN)
        alice = User("alice", "Alice Developer", "alice@company.com")
        bob = User("bob", "Bob Marketer", "bob@company.com")
        charlie = User("charlie", "Charlie QA", "charlie@company.com")
        
        self.alert_service.add_user(admin)
        self.alert_service.add_user(alice)
        self.alert_service.add_user(bob)
        self.alert_service.add_user(charlie)
        
        # Create teams
        self.alert_service.add_team("engineering", {"alice", "charlie"})
        self.alert_service.add_team("marketing", {"bob"})
        self.alert_service.add_team("qa", {"charlie"})
    
    def test_complete_workflow(self):
        """Test complete workflow from alert creation to user interaction"""
        
        # Step 1: Admin creates various alerts
        print("\n=== Step 1: Admin Creating Alerts ===")
        
        critical_alert = self.admin_api.create_alert(
            title="🚨 PRODUCTION ISSUE",
            message="Database connection timeout errors detected",
            severity=Severity.CRITICAL,
            created_by="admin1",
            visibility_type=VisibilityType.ORGANIZATION,
            target_ids=set(),
            delivery_type=DeliveryType.IN_APP
        )
        
        team_alert = self.admin_api.create_alert(
            title="Sprint Planning",
            message="Engineering team: Sprint planning meeting at 2 PM",
            severity=Severity.INFO,
            created_by="admin1",
            visibility_type=VisibilityType.TEAM,
            target_ids={"engineering"},
            delivery_type=DeliveryType.IN_APP
        )
        
        user_alert = self.admin_api.create_alert(
            title="Performance Review",
            message="Your quarterly performance review is scheduled",
            severity=Severity.INFO,
            created_by="admin1",
            visibility_type=VisibilityType.USER,
            target_ids={"alice"},
            delivery_type=DeliveryType.IN_APP
        )
        
        # Step 2: Check alert visibility for different users
        print("\n=== Step 2: Checking Alert Visibility ===")
        
        alice_alerts = self.user_api.get_alerts("alice")
        bob_alerts = self.user_api.get_alerts("bob")
        charlie_alerts = self.user_api.get_alerts("charlie")
        
        # Alice (Engineering) should see all 3 alerts
        self.assertEqual(len(alice_alerts), 3)
        
        # Bob (Marketing) should see only critical alert
        self.assertEqual(len(bob_alerts), 1)
        
        # Charlie (Engineering + QA) should see critical and team alert
        self.assertEqual(len(charlie_alerts), 2)
        
        # Step 3: User interactions with alerts
        print("\n=== Step 3: User Interactions ===")
        
        # Alice marks critical alert as read
        self.user_api.mark_alert_read("alice", critical_alert.alert_id)
        
        # Alice snoozes team alert
        self.user_api.snooze_alert("alice", team_alert.alert_id)
        
        # Bob tries to interact with team alert (should fail - not visible)
        result = self.user_api.snooze_alert("bob", team_alert.alert_id)
        self.assertFalse(result)  # Should return False since alert not visible to Bob
        
        # Step 4: Check user dashboard and preferences
        print("\n=== Step 4: User Dashboard ===")
        
        alice_dashboard = self.user_api.get_user_dashboard("alice")
        alice_snoozed = self.user_api.get_snoozed_alerts("alice")
        
        # Verify dashboard data
        self.assertEqual(alice_dashboard['summary']['total_alerts'], 3)
        self.assertEqual(alice_dashboard['summary']['snoozed_alerts'], 1)
        self.assertEqual(len(alice_snoozed), 1)
        
        # Step 5: Admin analytics and metrics
        print("\n=== Step 5: Admin Analytics ===")
        
        metrics = self.admin_api.get_alert_metrics()
        system_stats = self.admin_api.get_system_stats()
        
        # Verify metrics
        self.assertEqual(metrics['total_alerts'], 3)
        self.assertIn('severity_breakdown', metrics)
        self.assertIn('visibility_breakdown', metrics)
        
        # Step 6: Archive an alert and verify
        print("\n=== Step 6: Archiving Alert ===")
        
        self.admin_api.archive_alert(team_alert.alert_id)
        
        # Verify archived alert is not visible
        alice_alerts_after_archive = self.user_api.get_alerts("alice")
        active_alerts = [a for a in alice_alerts_after_archive if a['is_active']]
        self.assertEqual(len(active_alerts), 2)  # One alert archived
        
        # Step 7: Comprehensive analytics
        print("\n=== Step 7: Comprehensive Analytics ===")
        
        analytics = self.analytics_api.get_system_metrics()
        alert_analytics = self.analytics_api.get_alert_analytics()
        user_analytics = self.analytics_api.get_user_analytics()
        
        # Verify analytics structure
        self.assertIn('alerts', analytics)
        self.assertIn('users', analytics)
        self.assertIn('time_periods', alert_analytics)
        self.assertIn('user_counts', user_analytics)
        
        print("\n✅ All integration tests passed! Complete workflow is working correctly.")
    
    def test_error_handling(self):
        """Test error handling in various scenarios"""
        
        # Test non-existent user
        non_existent_alerts = self.user_api.get_alerts("non_existent_user")
        self.assertEqual(len(non_existent_alerts), 0)
        
        # Test non-existent alert actions
        result = self.user_api.mark_alert_read("alice", "non_existent_alert")
        self.assertFalse(result)
        
        # Test archiving non-existent alert
        result = self.admin_api.archive_alert("non_existent_alert")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()