"""
Seed data for testing and demonstration
"""

import sys
import os
from datetime import datetime, timedelta

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.user import User, UserRole
from models.alert import Severity, VisibilityType, DeliveryType

def seed_sample_data(alert_service, notification_service):
    """
    Seed the system with sample data for testing
    """
    print("🌱 Seeding sample data...")
    
    # Create sample users
    users = [
        User("admin1", "Alice Admin", "alice.admin@company.com", UserRole.ADMIN),
        User("user1", "Bob Developer", "bob.developer@company.com"),
        User("user2", "Charlie Designer", "charlie.designer@company.com"),
        User("user3", "Dana Tester", "dana.tester@company.com"),
        User("user4", "Eve Marketer", "eve.marketer@company.com"),
        User("user5", "Frank Manager", "frank.manager@company.com")
    ]
    
    for user in users:
        alert_service.add_user(user)
    
    print(f"✅ Created {len(users)} users")
    
    # Create sample teams
    teams = {
        "engineering": {"user1", "user3"},  # Bob (Developer), Dana (Tester)
        "design": {"user2"},                # Charlie (Designer)
        "marketing": {"user4"},             # Eve (Marketer)
        "management": {"user5"},            # Frank (Manager)
        "qa": {"user3"},                    # Dana (Tester)
        "product": {"user2", "user5"}       # Charlie (Designer), Frank (Manager)
    }
    
    for team_id, user_ids in teams.items():
        alert_service.add_team(team_id, user_ids)
    
    print(f"✅ Created {len(teams)} teams")
    
    # Create sample alerts
    sample_alerts = [
        {
            "title": "🚨 SYSTEM MAINTENANCE",
            "message": "Emergency maintenance required for database servers. All teams please save your work.",
            "severity": Severity.CRITICAL,
            "visibility": VisibilityType.ORGANIZATION,
            "targets": set()
        },
        {
            "title": "New Feature Deployment",
            "message": "Version 2.1.0 has been deployed to production. Engineering team monitor for issues.",
            "severity": Severity.INFO,
            "visibility": VisibilityType.TEAM,
            "targets": {"engineering", "qa"}
        },
        {
            "title": "Design System Update",
            "message": "New design system components available. Please review the updated guidelines.",
            "severity": Severity.INFO,
            "visibility": VisibilityType.TEAM, 
            "targets": {"design", "product"}
        },
        {
            "title": "Q4 Marketing Campaign",
            "message": "Q4 marketing campaign launches next week. Marketing team finalize preparations.",
            "severity": Severity.WARNING,
            "visibility": VisibilityType.TEAM,
            "targets": {"marketing"}
        },
        {
            "title": "Performance Reviews",
            "message": "Q3 performance reviews are now available. Please complete by end of week.",
            "severity": Severity.INFO,
            "visibility": VisibilityType.USER,
            "targets": {"user1", "user2", "user3", "user4"}  # All individual contributors
        },
        {
            "title": "Budget Planning Meeting",
            "message": "Annual budget planning meeting scheduled for department heads.",
            "severity": Severity.INFO,
            "visibility": VisibilityType.USER,
            "targets": {"user5"}  # Only managers
        },
        {
            "title": "Security Training",
            "message": "Mandatory security training must be completed by all employees.",
            "severity": Severity.WARNING,
            "visibility": VisibilityType.ORGANIZATION,
            "targets": set()
        },
        {
            "title": "API Rate Limits",
            "message": "New API rate limits will be enforced starting next Monday.",
            "severity": Severity.INFO,
            "visibility": VisibilityType.TEAM,
            "targets": {"engineering", "product"}
        }
    ]
    
    # Create alerts with different creation times to simulate real usage
    base_time = datetime.now()
    created_alerts = []
    
    for i, alert_data in enumerate(sample_alerts):
        # Stagger creation times
        created_time = base_time - timedelta(hours=i*3)
        
        alert = alert_service.create_alert(
            title=alert_data["title"],
            message=alert_data["message"],
            severity=alert_data["severity"],
            created_by="admin1",
            visibility_type=alert_data["visibility"],
            target_ids=alert_data["targets"],
            delivery_type=DeliveryType.IN_APP,
            start_time=created_time
        )
        created_alerts.append(alert)
    
    print(f"✅ Created {len(created_alerts)} sample alerts")
    
    # Simulate some user interactions
    print("🔄 Simulating user interactions...")
    
    # User1 marks some alerts as read
    notification_service.mark_as_read("user1", created_alerts[0].alert_id)  # Critical alert
    notification_service.mark_as_read("user1", created_alerts[1].alert_id)  # Engineering alert
    
    # User2 snoozes an alert
    notification_service.snooze_alert("user2", created_alerts[2].alert_id)  # Design alert
    
    # User3 interacts with multiple alerts
    notification_service.mark_as_read("user3", created_alerts[0].alert_id)  # Critical alert
    notification_service.snooze_alert("user3", created_alerts[1].alert_id)  # Engineering alert
    
    # User4 marks marketing alert as read
    notification_service.mark_as_read("user4", created_alerts[3].alert_id)  # Marketing alert
    
    # User5 interacts with management alerts
    notification_service.mark_as_read("user5", created_alerts[5].alert_id)  # Budget meeting
    
    print("✅ Sample user interactions completed")
    
    # Archive one alert to show the feature
    alert_service.archive_alert(created_alerts[6].alert_id)  # Archive security training
    
    print("📊 Sample Data Summary:")
    print(f"   Users: {len(users)}")
    print(f"   Teams: {len(teams)}") 
    print(f"   Alerts: {len(created_alerts)}")
    print(f"   Archived Alerts: 1")
    print("🌱 Sample data seeding completed!")

def create_minimal_test_data(alert_service):
    """
    Create minimal test data for quick testing
    """
    print("🌱 Creating minimal test data...")
    
    # Minimal users
    admin = User("admin1", "Test Admin", "admin@test.com", UserRole.ADMIN)
    user = User("user1", "Test User", "user@test.com")
    
    alert_service.add_user(admin)
    alert_service.add_user(user)
    
    # One team
    alert_service.add_team("test-team", {"user1"})
    
    # One alert
    alert_service.create_alert(
        title="Test Alert",
        message="This is a test alert",
        severity=Severity.INFO,
        created_by="admin1",
        visibility_type=VisibilityType.ORGANIZATION,
        target_ids=set()
    )
    
    print("✅ Minimal test data created")

def get_sample_metrics():
    """
    Return sample metrics for testing analytics
    """
    return {
        "user_engagement": {
            "active_users": 45,
            "daily_logins": 38,
            "avg_session_minutes": 12.5
        },
        "alert_stats": {
            "alerts_created_today": 3,
            "alerts_created_week": 15,
            "avg_response_time_minutes": 45.2
        },
        "system_health": {
            "uptime_percentage": 99.8,
            "avg_response_time_ms": 125,
            "error_rate": 0.02
        }
    }