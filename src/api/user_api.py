from typing import List, Dict, Any
from services.alert_service import AlertService
from services.notification_service import NotificationService

class UserAPI:
    """API for user operations"""
    
    def __init__(self, alert_service: AlertService, notification_service: NotificationService):
        self.alert_service = alert_service
        self.notification_service = notification_service
    
    def get_alerts(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all alerts for a user with their preferences"""
        print(f"👤 User {user_id} fetching alerts...")
        
        alerts_with_prefs = self.notification_service.get_user_alerts_with_preferences(user_id)
        
        # Format the response - FIXED: Use the correct structure
        formatted_alerts = []
        for alert_data in alerts_with_prefs:
            alert = alert_data['alert']
            preference = alert_data['preference']
            
            formatted_alert = {
                'alert': alert,  # Keep the alert object for internal use
                'preference': preference,  # Keep preference object
                'alert_id': alert.alert_id,
                'title': alert.title,
                'message': alert.message,
                'severity': alert.severity.value,
                'created_at': alert.created_at,
                'status': alert_data['status'],
                'is_snoozed': alert_data['is_snoozed'],
                'is_active': alert.is_active,
                'is_expired': alert.is_expired(),
                'visibility_type': alert.visibility.type.value
            }
            formatted_alerts.append(formatted_alert)
        
        print(f"✅ User {user_id} has {len(formatted_alerts)} alerts")
        return formatted_alerts
    
    def mark_alert_read(self, user_id: str, alert_id: str):
        """Mark an alert as read for a user"""
        print(f"📖 User {user_id} marking alert {alert_id} as READ")
        
        # Verify the alert exists and is visible to user
        user_alerts = self.alert_service.get_alerts_for_user(user_id)
        alert_ids = [alert.alert_id for alert in user_alerts]
        
        if alert_id not in alert_ids:
            print(f"❌ Alert {alert_id} not found or not visible to user {user_id}")
            return False
        
        self.notification_service.mark_as_read(user_id, alert_id)
        return True
    
    def mark_alert_unread(self, user_id: str, alert_id: str):
        """Mark an alert as unread for a user"""
        print(f"📖 User {user_id} marking alert {alert_id} as UNREAD")
        
        # Verify the alert exists and is visible to user
        user_alerts = self.alert_service.get_alerts_for_user(user_id)
        alert_ids = [alert.alert_id for alert in user_alerts]
        
        if alert_id not in alert_ids:
            print(f"❌ Alert {alert_id} not found or not visible to user {user_id}")
            return False
        
        self.notification_service.mark_as_unread(user_id, alert_id)
        return True
    
    def snooze_alert(self, user_id: str, alert_id: str):
        """Snooze an alert for a user until tomorrow"""
        print(f"⏰ User {user_id} snoozing alert {alert_id}")
        
        # Verify the alert exists and is visible to user
        user_alerts = self.alert_service.get_alerts_for_user(user_id)
        alert_ids = [alert.alert_id for alert in user_alerts]
        
        if alert_id not in alert_ids:
            print(f"❌ Alert {alert_id} not found or not visible to user {user_id}")
            return False
        
        self.notification_service.snooze_alert(user_id, alert_id)
        return True
    
    def get_snoozed_alerts(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all snoozed alerts for a user"""
        print(f"👤 User {user_id} fetching snoozed alerts...")
        
        all_alerts = self.get_alerts(user_id)
        snoozed_alerts = [alert for alert in all_alerts if alert['is_snoozed']]
        
        print(f"✅ User {user_id} has {len(snoozed_alerts)} snoozed alerts")
        return snoozed_alerts
    
    def get_alert_detail(self, user_id: str, alert_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific alert"""
        print(f"👤 User {user_id} fetching alert detail: {alert_id}")
        
        user_alerts = self.get_alerts(user_id)
        alert_detail = next((alert for alert in user_alerts if alert['alert_id'] == alert_id), None)
        
        if alert_detail:
            print(f"✅ Alert detail retrieved")
        else:
            print(f"❌ Alert {alert_id} not found for user {user_id}")
        
        return alert_detail
    
    def get_user_dashboard(self, user_id: str) -> Dict[str, Any]:
        """Get user dashboard data"""
        print(f"📊 Generating dashboard for user {user_id}")
        
        all_alerts = self.get_alerts(user_id)
        snoozed_alerts = self.get_snoozed_alerts(user_id)
        
        # Categorize alerts
        critical_alerts = [a for a in all_alerts if a['severity'] == 'critical' and not a['is_snoozed']]
        warning_alerts = [a for a in all_alerts if a['severity'] == 'warning' and not a['is_snoozed']]
        info_alerts = [a for a in all_alerts if a['severity'] == 'info' and not a['is_snoozed']]
        unread_alerts = [a for a in all_alerts if a['status'] == 'unread' and not a['is_snoozed']]
        
        dashboard = {
            'summary': {
                'total_alerts': len(all_alerts),
                'unread_alerts': len(unread_alerts),
                'snoozed_alerts': len(snoozed_alerts),
                'critical_alerts': len(critical_alerts),
                'warning_alerts': len(warning_alerts),
                'info_alerts': len(info_alerts)
            },
            'recent_alerts': all_alerts[:5],  # Last 5 alerts
            'critical_alerts': critical_alerts,
            'snoozed_alerts': snoozed_alerts
        }
        
        print(f"✅ Dashboard generated for user {user_id}")
        return dashboard