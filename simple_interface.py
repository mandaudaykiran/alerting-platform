#!/usr/bin/env python3
"""
Alerting Platform - Simple Command Line Interface
"""
import sys
import os
import uuid
from datetime import datetime, timedelta

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from services.alert_service import AlertService
from services.notification_service import NotificationService
from api.admin_api import AdminAPI
from api.user_api import UserAPI
from api.analytics_api import AnalyticsAPI
from models.user import User, UserRole
from models.alert import Severity, VisibilityType, DeliveryType

class AlertingPlatformCLI:
    def __init__(self):
        self.alert_service = AlertService()
        self.notification_service = NotificationService(self.alert_service)
        self.admin_api = AdminAPI(self.alert_service)
        self.user_api = UserAPI(self.alert_service, self.notification_service)
        self.analytics_api = AnalyticsAPI(self.alert_service, self.notification_service)
        
        # Current logged in user
        self.current_user = None
        self.setup_sample_data()
    
    def setup_sample_data(self):
        """Setup some sample data for demonstration"""
        print("🔄 Setting up sample data...")
        
        # Create sample users
        admin = User("admin", "System Administrator", "admin@company.com", UserRole.ADMIN)
        alice = User("alice", "Alice Developer", "alice@company.com")
        bob = User("bob", "Bob Manager", "bob@company.com")
        charlie = User("charlie", "Charlie Tester", "charlie@company.com")
        
        self.alert_service.add_user(admin)
        self.alert_service.add_user(alice)
        self.alert_service.add_user(bob)
        self.alert_service.add_user(charlie)
        
        # Create teams
        self.alert_service.add_team("engineering", {"alice", "charlie"})
        self.alert_service.add_team("management", {"bob"})
        
        print("✅ Sample data ready!")
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self, title):
        """Display a formatted header"""
        self.clear_screen()
        print("🚀 ALERTING PLATFORM")
        print("=" * 50)
        print(f"📋 {title}")
        print("-" * 50)
        if self.current_user:
            print(f"👤 User: {self.current_user.name} ({self.current_user.role.value})")
        print()
    
    def wait_for_enter(self):
        """Wait for user to press Enter"""
        input("\nPress Enter to continue...")
    
    def login(self):
        """User login interface"""
        self.display_header("USER LOGIN")
        
        print("Available Users:")
        print("1. admin (Administrator)")
        print("2. alice (Developer)")
        print("3. bob (Manager)") 
        print("4. charlie (Tester)")
        print("5. Exit")
        
        choice = input("\nSelect user (1-5): ").strip()
        
        user_map = {
            "1": "admin",
            "2": "alice", 
            "3": "bob",
            "4": "charlie"
        }
        
        if choice == "5":
            print("👋 Goodbye!")
            sys.exit(0)
        elif choice in user_map:
            user_id = user_map[choice]
            self.current_user = self.alert_service.get_user(user_id)
            print(f"✅ Logged in as {self.current_user.name}")
            self.wait_for_enter()
            return True
        else:
            print("❌ Invalid selection")
            self.wait_for_enter()
            return False
    
    def admin_dashboard(self):
        """Administrator dashboard"""
        while True:
            self.display_header("ADMIN DASHBOARD")
            
            print("1. 📢 Create New Alert")
            print("2. 📋 View All Alerts") 
            print("3. 👥 Manage Users & Teams")
            print("4. 📊 System Analytics")
            print("5. 🔄 Process Reminders")
            print("6. 👤 Switch User")
            print("7. 🚪 Exit")
            
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == "1":
                self.create_alert()
            elif choice == "2":
                self.view_all_alerts()
            elif choice == "3":
                self.manage_users_teams()
            elif choice == "4":
                self.system_analytics()
            elif choice == "5":
                self.process_reminders()
            elif choice == "6":
                return True  # Switch user
            elif choice == "7":
                print("👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid option")
                self.wait_for_enter()
    
    def user_dashboard(self):
        """Regular user dashboard"""
        while True:
            self.display_header("USER DASHBOARD")
            
            print("1. 📨 View My Alerts")
            print("2. ⏰ View Snoozed Alerts")
            print("3. 📊 My Dashboard")
            print("4. 👤 Switch User") 
            print("5. 🚪 Exit")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == "1":
                self.view_my_alerts()
            elif choice == "2":
                self.view_snoozed_alerts()
            elif choice == "3":
                self.my_dashboard()
            elif choice == "4":
                return True  # Switch user
            elif choice == "5":
                print("👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid option")
                self.wait_for_enter()
    
    def create_alert(self):
        """Create a new alert"""
        self.display_header("CREATE NEW ALERT")
        
        print("Alert Details:")
        title = input("Title: ").strip()
        message = input("Message: ").strip()
        
        print("\nSeverity Level:")
        print("1. ℹ️  INFO")
        print("2. ⚠️  WARNING") 
        print("3. 🚨 CRITICAL")
        severity_choice = input("Select severity (1-3): ").strip()
        
        severity_map = {
            "1": Severity.INFO,
            "2": Severity.WARNING,
            "3": Severity.CRITICAL
        }
        
        if severity_choice not in severity_map:
            print("❌ Invalid severity selection")
            self.wait_for_enter()
            return
        
        print("\nVisibility Type:")
        print("1. 🌐 Organization (All users)")
        print("2. 👥 Team (Specific teams)")
        print("3. 👤 User (Specific users)")
        visibility_choice = input("Select visibility (1-3): ").strip()
        
        visibility_map = {
            "1": VisibilityType.ORGANIZATION,
            "2": VisibilityType.TEAM,
            "3": VisibilityType.USER
        }
        
        if visibility_choice not in visibility_map:
            print("❌ Invalid visibility selection")
            self.wait_for_enter()
            return
        
        target_ids = set()
        if visibility_choice == "2":
            print("Available teams: engineering, management")
            teams = input("Enter team names (comma-separated): ").strip()
            target_ids = set(team.strip() for team in teams.split(",") if team.strip())
        elif visibility_choice == "3":
            print("Available users: alice, bob, charlie")
            users = input("Enter user IDs (comma-separated): ").strip()
            target_ids = set(user.strip() for user in users.split(",") if user.strip())
        
        # Create the alert
        try:
            alert = self.admin_api.create_alert(
                title=title,
                message=message,
                severity=severity_map[severity_choice],
                created_by=self.current_user.user_id,
                visibility_type=visibility_map[visibility_choice],
                target_ids=target_ids
            )
            print(f"\n✅ Alert created successfully!")
            print(f"   ID: {alert.alert_id}")
            print(f"   Title: {alert.title}")
        except Exception as e:
            print(f"❌ Error creating alert: {e}")
        
        self.wait_for_enter()
    
    def view_all_alerts(self):
        """View all alerts in the system"""
        self.display_header("ALL ALERTS")
        
        alerts = self.admin_api.list_alerts()
        
        if not alerts:
            print("No alerts found in the system.")
            self.wait_for_enter()
            return
        
        print(f"Found {len(alerts)} alerts:\n")
        
        for i, alert in enumerate(alerts, 1):
            status = "🟢 ACTIVE" if alert.is_active else "🔴 ARCHIVED"
            expiry = alert.expiry_time.strftime("%Y-%m-%d") if alert.expiry_time else "No expiry"
            
            print(f"{i}. {alert.title}")
            print(f"   📝 {alert.message[:50]}...")
            print(f"   🚨 {alert.severity.value.upper()} | 👁️ {alert.visibility.type.value} | {status}")
            print(f"   ⏰ Created: {alert.created_at.strftime('%Y-%m-%d %H:%M')} | Expires: {expiry}")
            print(f"   🆔 {alert.alert_id}")
            print()
        
        print("\nOptions:")
        print("1. Archive an alert")
        print("2. Back to dashboard")
        
        choice = input("\nSelect option (1-2): ").strip()
        
        if choice == "1":
            alert_num = input("Enter alert number to archive: ").strip()
            try:
                alert_index = int(alert_num) - 1
                if 0 <= alert_index < len(alerts):
                    alert_to_archive = alerts[alert_index]
                    success = self.admin_api.archive_alert(alert_to_archive.alert_id)
                    if success:
                        print("✅ Alert archived successfully!")
                    else:
                        print("❌ Failed to archive alert")
                else:
                    print("❌ Invalid alert number")
            except ValueError:
                print("❌ Please enter a valid number")
        
        self.wait_for_enter()
    
    def view_my_alerts(self):
        """View current user's alerts"""
        self.display_header("MY ALERTS")
        
        alerts = self.user_api.get_alerts(self.current_user.user_id)
        
        if not alerts:
            print("No alerts found for you.")
            self.wait_for_enter()
            return
        
        print(f"You have {len(alerts)} alerts:\n")
        
        for i, alert_data in enumerate(alerts, 1):
            alert = alert_data
            status_icon = "🔴" if alert_data['status'] == 'unread' else "🟢" if alert_data['status'] == 'read' else "⏰"
            snooze_status = " (SNOOZED)" if alert_data['is_snoozed'] else ""
            
            print(f"{i}. {status_icon} {alert['title']}{snooze_status}")
            print(f"   📝 {alert['message'][:50]}...")
            print(f"   🚨 {alert['severity'].upper()} | 👁️ {alert['visibility_type']}")
            print(f"   ⏰ {alert['created_at'].strftime('%Y-%m-%d %H:%M')}")
            print(f"   🆔 {alert['alert_id']}")
            print()
        
        print("\nOptions:")
        print("1. Mark alert as read")
        print("2. Snooze alert") 
        print("3. Mark alert as unread")
        print("4. Back to dashboard")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice in ["1", "2", "3"]:
            alert_num = input("Enter alert number: ").strip()
            try:
                alert_index = int(alert_num) - 1
                if 0 <= alert_index < len(alerts):
                    alert_id = alerts[alert_index]['alert_id']
                    
                    if choice == "1":
                        self.user_api.mark_alert_read(self.current_user.user_id, alert_id)
                        print("✅ Alert marked as read!")
                    elif choice == "2":
                        self.user_api.snooze_alert(self.current_user.user_id, alert_id)
                        print("✅ Alert snoozed until tomorrow!")
                    elif choice == "3":
                        self.user_api.mark_alert_unread(self.current_user.user_id, alert_id)
                        print("✅ Alert marked as unread!")
                else:
                    print("❌ Invalid alert number")
            except ValueError:
                print("❌ Please enter a valid number")
        
        self.wait_for_enter()
    
    def view_snoozed_alerts(self):
        """View snoozed alerts"""
        self.display_header("SNOOZED ALERTS")
        
        snoozed_alerts = self.user_api.get_snoozed_alerts(self.current_user.user_id)
        
        if not snoozed_alerts:
            print("You have no snoozed alerts.")
            self.wait_for_enter()
            return
        
        print(f"You have {len(snoozed_alerts)} snoozed alerts:\n")
        
        for i, alert_data in enumerate(snoozed_alerts, 1):
            alert = alert_data
            print(f"{i}. ⏰ {alert['title']}")
            print(f"   📝 {alert['message'][:50]}...")
            print(f"   🚨 {alert['severity'].upper()}")
            print(f"   🆔 {alert['alert_id']}")
            print()
        
        self.wait_for_enter()
    
    def my_dashboard(self):
        """User personal dashboard"""
        self.display_header("MY DASHBOARD")
        
        dashboard = self.user_api.get_user_dashboard(self.current_user.user_id)
        summary = dashboard['summary']
        
        print("📊 ALERT SUMMARY:")
        print(f"   📨 Total Alerts: {summary['total_alerts']}")
        print(f"   🔴 Unread Alerts: {summary['unread_alerts']}")
        print(f"   ⏰ Snoozed Alerts: {summary['snoozed_alerts']}")
        print(f"   🚨 Critical Alerts: {summary['critical_alerts']}")
        print(f"   ⚠️  Warning Alerts: {summary['warning_alerts']}")
        print(f"   ℹ️  Info Alerts: {summary['info_alerts']}")
        
        print(f"\n📋 RECENT ALERTS ({len(dashboard['recent_alerts'])}):")
        for alert in dashboard['recent_alerts'][:3]:  # Show last 3
            status_icon = "🔴" if alert['status'] == 'unread' else "🟢"
            print(f"   {status_icon} {alert['title']}")
        
        self.wait_for_enter()
    
    def manage_users_teams(self):
        """Manage users and teams"""
        self.display_header("MANAGE USERS & TEAMS")
        
        stats = self.alert_service.get_stats()
        
        print("📊 CURRENT SYSTEM:")
        print(f"   👥 Total Users: {stats['total_users']}")
        print(f"   🏢 Total Teams: {stats['total_teams']}")
        print(f"   📢 Total Alerts: {stats['total_alerts']}")
        
        print(f"\n👥 USERS:")
        users = self.alert_service.get_all_users()
        for user in users:
            role_icon = "👑" if user.is_admin() else "👤"
            teams = self.alert_service.get_user_teams(user.user_id)
            teams_str = ", ".join(teams) if teams else "No teams"
            print(f"   {role_icon} {user.name} ({user.user_id}) - Teams: {teams_str}")
        
        print(f"\n🏢 TEAMS:")
        teams = self.alert_service.get_all_teams()
        for team_id, members in teams.items():
            print(f"   👥 {team_id}: {len(members)} members")
        
        self.wait_for_enter()
    
    def system_analytics(self):
        """System analytics dashboard"""
        self.display_header("SYSTEM ANALYTICS")
        
        metrics = self.analytics_api.get_system_metrics()
        
        print("📈 SYSTEM METRICS:")
        print(f"   📊 Total Alerts: {metrics['alerts']['total']}")
        print(f"   🟢 Active Alerts: {metrics['alerts']['active']}")
        print(f"   🔴 Expired Alerts: {metrics['alerts']['expired']}")
        print(f"   📁 Archived Alerts: {metrics['alerts']['archived']}")
        
        print(f"\n🚨 SEVERITY BREAKDOWN:")
        for severity, count in metrics['alerts']['by_severity'].items():
            print(f"   {severity.upper()}: {count}")
        
        print(f"\n👁️ VISIBILITY BREAKDOWN:")
        for visibility, count in metrics['alerts']['by_visibility'].items():
            print(f"   {visibility}: {count}")
        
        print(f"\n👥 USER STATISTICS:")
        print(f"   Total Users: {metrics['users']['total']}")
        print(f"   Active Users: {metrics['users']['active']}")
        print(f"   Teams Configured: {metrics['users']['teams']}")
        
        self.wait_for_enter()
    
    def process_reminders(self):
        """Process pending reminders"""
        self.display_header("PROCESS REMINDERS")
        
        print("🔄 Processing reminders...")
        reminders_sent = self.notification_service.process_reminders()
        
        print(f"✅ Sent {reminders_sent} reminders to users")
        self.wait_for_enter()
    
    def run(self):
        """Main application loop"""
        print("🚀 Welcome to Alerting Platform!")
        print("Setting up...")
        
        while True:
            # Login loop
            while not self.current_user:
                if not self.login():
                    continue
            
            # Route to appropriate dashboard
            if self.current_user.is_admin():
                should_switch = self.admin_dashboard()
            else:
                should_switch = self.user_dashboard()
            
            if should_switch:
                self.current_user = None  # Return to login

def main():
    """Main entry point"""
    try:
        cli = AlertingPlatformCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please make sure all required files are in the correct location.")

if __name__ == "__main__":
    main()