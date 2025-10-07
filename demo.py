#!/usr/bin/env python3
"""
Alerting Platform - Demonstration Script (Fixed Version)
"""
import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from services.alert_service import AlertService
from services.notification_service import NotificationService
from api.admin_api import AdminAPI
from api.user_api import UserAPI
from api.analytics_api import AnalyticsAPI
from models.user import User, UserRole
from models.alert import Severity, VisibilityType, DeliveryType
from datetime import datetime, timedelta

def run_demo():
    """Run a comprehensive demonstration of the platform"""
    print("🚀 Alerting Platform - Comprehensive Demo")
    print("=" * 60)
    
    # Initialize services
    alert_service = AlertService()
    notification_service = NotificationService(alert_service)
    
    # Create APIs
    admin_api = AdminAPI(alert_service)
    user_api = UserAPI(alert_service, notification_service)
    analytics_api = AnalyticsAPI(alert_service, notification_service)
    
    print("✅ Services initialized")
    
    # Create users
    admin_user = User("admin1", "Alice Admin", "alice@company.com", UserRole.ADMIN)
    user1 = User("user1", "Bob Developer", "bob@company.com")
    user2 = User("user2", "Charlie Marketer", "charlie@company.com")
    user3 = User("user3", "Dana Tester", "dana@company.com")
    
    # Add users to service
    alert_service.add_user(admin_user)
    alert_service.add_user(user1)
    alert_service.add_user(user2)
    alert_service.add_user(user3)
    
    # Create teams
    alert_service.add_team("engineering", {"user1", "user3"})
    alert_service.add_team("marketing", {"user2"})
    alert_service.add_team("qa", {"user3"})
    
    print("👥 Users and teams created")
    print("   - Engineering: user1, user3")
    print("   - Marketing: user2") 
    print("   - QA: user3")
    
    # Create various alerts
    print("\n📢 Creating Alerts...")
    
    # Organization-wide critical alert
    critical_alert = admin_api.create_alert(
        title="🚨 SYSTEM OUTAGE",
        message="Production system is experiencing issues. All teams investigate.",
        severity=Severity.CRITICAL,
        created_by="admin1",
        visibility_type=VisibilityType.ORGANIZATION,
        target_ids=set(),
        delivery_type=DeliveryType.IN_APP
    )
    
    # Team-specific alert
    engineering_alert = admin_api.create_alert(
        title="New Deployment",
        message="Version 2.1 deployed to staging. Engineering team please verify.",
        severity=Severity.INFO,
        created_by="admin1",
        visibility_type=VisibilityType.TEAM,
        target_ids={"engineering"},
        delivery_type=DeliveryType.IN_APP
    )
    
    # User-specific alert with expiry
    user_alert = admin_api.create_alert(
        title="Performance Review",
        message="Your quarterly performance review is scheduled.",
        severity=Severity.INFO,
        created_by="admin1",
        visibility_type=VisibilityType.USER,
        target_ids={"user1"},
        delivery_type=DeliveryType.IN_APP,
        expiry_time=datetime.now() + timedelta(days=7)
    )
    
    # Warning alert for marketing
    marketing_alert = admin_api.create_alert(
        title="Campaign Deadline",
        message="Q4 marketing campaign deadline approaching.",
        severity=Severity.WARNING,
        created_by="admin1",
        visibility_type=VisibilityType.TEAM,
        target_ids={"marketing"},
        delivery_type=DeliveryType.IN_APP
    )
    
    print("✅ Alerts created with different visibilities and severities")
    
    # Test user alert visibility
    print("\n👤 Testing Alert Visibility:")
    user1_alerts = user_api.get_alerts("user1")
    user2_alerts = user_api.get_alerts("user2") 
    user3_alerts = user_api.get_alerts("user3")
    
    print(f"   User1 (Engineering) sees {len(user1_alerts)} alerts")
    print(f"   User2 (Marketing) sees {len(user2_alerts)} alerts")
    print(f"   User3 (Engineering + QA) sees {len(user3_alerts)} alerts")
    
    # Simulate user interactions - FIXED: Use alert_id directly
    print("\n🔄 Simulating User Interactions...")
    
    # User1 actions
    if user1_alerts:
        user_api.mark_alert_read("user1", user1_alerts[0]['alert_id'])
        print("   User1 marked critical alert as READ")
        
        if len(user1_alerts) > 1:
            user_api.snooze_alert("user1", user1_alerts[1]['alert_id'])
            print("   User1 snoozed engineering alert")
    
    # User2 actions
    if user2_alerts:
        user_api.snooze_alert("user2", user2_alerts[0]['alert_id'])
        print("   User2 snoozed marketing alert")
    
    # User3 actions
    if user3_alerts:
        for alert_data in user3_alerts[:2]:
            user_api.mark_alert_read("user3", alert_data['alert_id'])
        print("   User3 marked first 2 alerts as READ")
    
    # Test archiving an alert
    print("\n🗃️ Archive one alert")
    admin_api.archive_alert(engineering_alert.alert_id)
    print("   Engineering alert archived")
    
    # Get updated user alerts
    user1_alerts_after = user_api.get_alerts("user1")
    print(f"   User1 now sees {len(user1_alerts_after)} alerts (1 archived)")
    
    # Analytics and metrics
    print("\n📊 Analytics Dashboard:")
    metrics = analytics_api.get_system_metrics()
    
    print(f"   Total Alerts: {metrics['alerts']['total']}")
    print(f"   Active Alerts: {metrics['alerts']['active']}")
    print(f"   Expired Alerts: {metrics['alerts']['expired']}")
    print(f"   Severity Breakdown:")
    for severity, count in metrics['alerts']['by_severity'].items():
        print(f"     - {severity.upper()}: {count}")
    
    # User-specific analytics
    print(f"\n👤 User-specific Stats:")
    user1_snoozed = user_api.get_snoozed_alerts("user1")
    print(f"   User1 snoozed alerts: {len(user1_snoozed)}")
    
    # Alert details
    print(f"\n📋 Alert Details:")
    all_alerts = admin_api.list_alerts()
    for alert in all_alerts[:3]:  # Show first 3 alerts
        status = "ACTIVE" if alert.is_active else "ARCHIVED"
        expiry = alert.expiry_time.strftime("%Y-%m-%d") if alert.expiry_time else "No expiry"
        print(f"   - {alert.title} [{alert.severity.value}] - {status} (Expires: {expiry})")
    
    print("\n🎉 Demo completed successfully!")
    print("\n💡 Try modifying demo.py to test different scenarios!")

if __name__ == "__main__":
    run_demo()