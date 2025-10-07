import unittest
import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.alert_service import AlertService
from services.notification_service import NotificationService
from api.admin_api import AdminAPI
from api.user_api import UserAPI
from api.analytics_api import AnalyticsAPI
from models.user import User, UserRole
from models.alert import Severity, VisibilityType, DeliveryType

class TestAdminAPI(unittest.TestCase):
    
    def setUp(self):
        self.alert_service = AlertService()
        self.admin_api = AdminAPI(self.alert_service)
        
        # Create admin user
        admin_user = User("admin1", "Admin User", "admin@example.com", UserRole.ADMIN)
        self.alert_service.add_user(admin_user)
    
    def test_create_alert(self):
        alert = self.admin_api.create_alert(
            title="API Test Alert",
            message="Testing API",
            severity=Severity.CRITICAL,
            created_by="admin1",
            visibility_type=VisibilityType.ORGANIZATION,
            target_ids=set()
        )
        
        self.assertIsNotNone(alert)
        self.assertEqual(alert.title, "API Test Alert")
        self.assertEqual(alert.severity, Severity.CRITICAL)
    
    def test_list_alerts(self):
        # Create some alerts
        self.admin_api.create_alert(
            title="Alert 1",
            message="Message 1",
            severity=Severity.INFO,
            created_by="admin1",
            visibility_type=VisibilityType.ORGANIZATION,
            target_ids=set()
        )
        
        self.admin_api.create_alert(
            title="Alert 2",
            message="Message 2",
            severity=Severity.WARNING,
            created_by="admin1",
            visibility_type=VisibilityType.ORGANIZATION,
            target_ids=set()
        )
        
        # List all alerts
        all_alerts = self.admin_api.list_alerts()
        self.assertEqual(len(all_alerts), 2)
        
        # List with severity filter
        info_alerts = self.admin_api.list_alerts(severity=Severity.INFO)
        self.assertEqual(len(info_alerts), 1)
        self.assertEqual(info_alerts[0].severity, Severity.INFO)
    
    def test_alert_metrics(self):
        # Create alerts for metrics
        self.admin_api.create_alert(
            title="Info Alert",
            message="Message",
            severity=Severity.INFO,
            created_by="admin1",
            visibility_type=VisibilityType.ORGANIZATION,
            target_ids=set()
        )
        
        self.admin_api.create_alert(
            title="Warning Alert",
            message="Message",
            severity=Severity.WARNING,
            created_by="admin1",
            visibility_type=VisibilityType.TEAM,
            target_ids={"team1"}
        )
        
        metrics = self.admin_api.get_alert_metrics()
        
        self.assertIn('total_alerts', metrics)
        self.assertIn('active_alerts', metrics)
        self.assertIn('severity_breakdown', metrics)
        self.assertIn('visibility_breakdown', metrics)
        
        self.assertEqual(metrics['total_alerts'], 2)
        self.assertGreaterEqual(metrics['active_alerts'], 2)

class TestUserAPI(unittest.TestCase):
    
    def setUp(self):
        self.alert_service = AlertService()
        self.notification_service = NotificationService(self.alert_service)
        self.user_api = UserAPI(self.alert_service, self.notification_service)
        
        # Create users
        self.user1 = User("user1", "User One", "user1@example.com")
        self.user2 = User("user2", "User Two", "user2@example.com")
        
        self.alert_service.add_user(self.user1)
        self.alert_service.add_user(self.user2)
        self.alert_service.add_team("engineering", {"user1"})
        
        # Create alerts
        self.alert_service.create_alert(
            title="Org Alert",
            message="Organization wide alert",
            severity=Severity.INFO,
            created_by="admin1",
            visibility_type=VisibilityType.ORGANIZATION,
            target_ids=set()
        )
        
        self.alert_service.create_alert(
            title="Team Alert",
            message="Engineering team alert",
            severity=Severity.WARNING,
            created_by="admin1",
            visibility_type=VisibilityType.TEAM,
            target_ids={"engineering"}
        )
    
    def test_get_user_alerts(self):
        # User1 should see both alerts
        user1_alerts = self.user_api.get_alerts("user1")
        self.assertEqual(len(user1_alerts), 2)
        
        # User2 should see only org alert
        user2_alerts = self.user_api.get_alerts("user2")
        self.assertEqual(len(user2_alerts), 1)
        
        # Check alert structure
        alert_data = user1_alerts[0]
        self.assertIn('alert_id', alert_data)
        self.assertIn('title', alert_data)
        self.assertIn('status', alert_data)
        self.assertIn('severity', alert_data)
    
    def test_user_actions(self):
        user_alerts = self.user_api.get_alerts("user1")
        alert_id = user_alerts[0]['alert_id']
        
        # Mark as read
        self.user_api.mark_alert_read("user1", alert_id)
        
        # Verify status changed
        updated_alerts = self.user_api.get_alerts("user1")
        read_alert = next((a for a in updated_alerts if a['alert_id'] == alert_id), None)
        self.assertEqual(read_alert['status'], 'read')
        
        # Snooze alert
        alert_id2 = user_alerts[1]['alert_id']
        self.user_api.snooze_alert("user1", alert_id2)
        
        # Check snoozed alerts
        snoozed_alerts = self.user_api.get_snoozed_alerts("user1")
        self.assertEqual(len(snoozed_alerts), 1)
        self.assertEqual(snoozed_alerts[0]['alert_id'], alert_id2)
    
    def test_user_dashboard(self):
        dashboard = self.user_api.get_user_dashboard("user1")
        
        self.assertIn('summary', dashboard)
        self.assertIn('recent_alerts', dashboard)
        self.assertIn('critical_alerts', dashboard)
        self.assertIn('snoozed_alerts', dashboard)
        
        summary = dashboard['summary']
        self.assertIn('total_alerts', summary)
        self.assertIn('unread_alerts', summary)
        self.assertIn('snoozed_alerts', summary)

class TestAnalyticsAPI(unittest.TestCase):
    
    def setUp(self):
        self.alert_service = AlertService()
        self.notification_service = NotificationService(self.alert_service)
        self.analytics_api = AnalyticsAPI(self.alert_service, self.notification_service)
        
        # Create test data
        admin = User("admin1", "Admin", "admin@example.com", UserRole.ADMIN)
        user1 = User("user1", "User1", "user1@example.com")
        user2 = User("user2", "User2", "user2@example.com")
        
        self.alert_service.add_user(admin)
        self.alert_service.add_user(user1)
        self.alert_service.add_user(user2)
        
        self.alert_service.add_team("engineering", {"user1"})
        self.alert_service.add_team("marketing", {"user2"})
        
        # Create alerts
        self.alert_service.create_alert(
            title="Critical Alert",
            message="Critical message",
            severity=Severity.CRITICAL,
            created_by="admin1",
            visibility_type=VisibilityType.ORGANIZATION,
            target_ids=set()
        )
        
        self.alert_service.create_alert(
            title="Team Alert",
            message="Team message",
            severity=Severity.INFO,
            created_by="admin1",
            visibility_type=VisibilityType.TEAM,
            target_ids={"engineering"}
        )
    
    def test_system_metrics(self):
        metrics = self.analytics_api.get_system_metrics()
        
        self.assertIn('alerts', metrics)
        self.assertIn('users', metrics)
        self.assertIn('notifications', metrics)
        self.assertIn('system', metrics)
        
        alerts_metrics = metrics['alerts']
        self.assertIn('total', alerts_metrics)
        self.assertIn('by_severity', alerts_metrics)
        self.assertIn('by_visibility', alerts_metrics)
    
    def test_alert_analytics(self):
        analytics = self.analytics_api.get_alert_analytics()
        
        self.assertIn('time_periods', analytics)
        self.assertIn('severity_trends', analytics)
        self.assertIn('top_alert_creators', analytics)
        self.assertIn('most_active_teams', analytics)
    
    def test_user_analytics(self):
        analytics = self.analytics_api.get_user_analytics()
        
        self.assertIn('user_counts', analytics)
        self.assertIn('engagement', analytics)
        self.assertIn('team_distribution', analytics)
    
    def test_generate_report(self):
        report = self.analytics_api.generate_report("weekly")
        
        self.assertIn('report_type', report)
        self.assertIn('summary', report)
        self.assertIn('alert_analytics', report)
        self.assertIn('user_analytics', report)
        self.assertIn('recommendations', report)
        self.assertEqual(report['report_type'], "weekly")

if __name__ == '__main__':
    unittest.main()