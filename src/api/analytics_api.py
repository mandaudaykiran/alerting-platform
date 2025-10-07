from typing import Dict, List, Any
from datetime import datetime, timedelta
from services.alert_service import AlertService
from services.notification_service import NotificationService

class AnalyticsAPI:
    """API for analytics and reporting"""
    
    def __init__(self, alert_service: AlertService, notification_service: NotificationService):
        self.alert_service = alert_service
        self.notification_service = notification_service
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get comprehensive system metrics"""
        print("📈 Generating comprehensive system metrics...")
        
        # Get basic metrics from services
        alert_stats = self.alert_service.get_stats()
        delivery_stats = self.notification_service.get_delivery_stats()
        
        # Calculate additional metrics
        all_alerts = self.alert_service.list_all_alerts()
        all_users = self.alert_service.get_all_users()
        
        # Alert metrics
        active_alerts = [a for a in all_alerts if a.is_active and not a.is_expired()]
        expired_alerts = [a for a in all_alerts if a.is_expired()]
        
        # User engagement metrics (simulated)
        user_engagement = self._calculate_user_engagement()
        
        # System health metrics
        system_health = {
            'uptime': '99.9%',  # Simulated
            'response_time': '~50ms',  # Simulated
            'error_rate': '0.1%',  # Simulated
            'active_sessions': len(all_users)  # Simulated
        }
        
        metrics = {
            'alerts': {
                'total': len(all_alerts),
                'active': len(active_alerts),
                'expired': len(expired_alerts),
                'archived': len([a for a in all_alerts if not a.is_active]),
                'by_severity': self._get_severity_breakdown(all_alerts),
                'by_visibility': self._get_visibility_breakdown(all_alerts),
                'creation_trend': self._get_creation_trend(all_alerts)
            },
            'users': {
                'total': len(all_users),
                'active': user_engagement['active_users'],
                'teams': len(self.alert_service.get_all_teams()),
                'engagement': user_engagement
            },
            'notifications': delivery_stats,
            'system': system_health,
            'timestamp': datetime.now().isoformat()
        }
        
        print("✅ Comprehensive metrics generated")
        return metrics
    
    def get_alert_analytics(self) -> Dict[str, Any]:
        """Get detailed analytics for alerts"""
        print("📊 Generating alert analytics...")
        
        all_alerts = self.alert_service.list_all_alerts()
        
        # Time-based analytics
        today = datetime.now().date()
        last_week = today - timedelta(days=7)
        last_month = today - timedelta(days=30)
        
        alerts_today = [a for a in all_alerts if a.created_at.date() == today]
        alerts_week = [a for a in all_alerts if a.created_at.date() >= last_week]
        alerts_month = [a for a in all_alerts if a.created_at.date() >= last_month]
        
        analytics = {
            'time_periods': {
                'today': len(alerts_today),
                'last_7_days': len(alerts_week),
                'last_30_days': len(alerts_month)
            },
            'severity_trends': {
                'today': self._get_severity_breakdown(alerts_today),
                'week': self._get_severity_breakdown(alerts_week),
                'month': self._get_severity_breakdown(alerts_month)
            },
            'top_alert_creators': self._get_top_creators(all_alerts),
            'most_active_teams': self._get_most_active_teams(all_alerts),
            'alert_lifespan': self._get_alert_lifespan_stats(all_alerts)
        }
        
        print("✅ Alert analytics generated")
        return analytics
    
    def get_user_analytics(self) -> Dict[str, Any]:
        """Get analytics for user behavior"""
        print("👤 Generating user analytics...")
        
        all_users = self.alert_service.get_all_users()
        user_engagement = self._calculate_user_engagement()
        
        analytics = {
            'user_counts': {
                'total': len(all_users),
                'admins': len([u for u in all_users if u.is_admin()]),
                'regular_users': len([u for u in all_users if not u.is_admin()])
            },
            'engagement': user_engagement,
            'team_distribution': self._get_team_distribution(),
            'user_activity': self._get_user_activity_stats()
        }
        
        print("✅ User analytics generated")
        return analytics
    
    def _calculate_user_engagement(self) -> Dict[str, Any]:
        """Calculate user engagement metrics (simulated)"""
        # In a real system, this would query user activity data
        return {
            'active_users': len(self.alert_service.get_all_users()),  # Simulated
            'avg_alerts_per_user': 3.2,  # Simulated
            'response_rate': '85%',  # Simulated
            'snooze_rate': '15%'  # Simulated
        }
    
    def _get_severity_breakdown(self, alerts: List) -> Dict[str, int]:
        """Get breakdown of alerts by severity"""
        from models.alert import Severity
        
        breakdown = {severity.value: 0 for severity in Severity}
        
        for alert in alerts:
            severity_value = alert.severity.value
            if severity_value in breakdown:
                breakdown[severity_value] += 1
        
        return breakdown
    
    def _get_visibility_breakdown(self, alerts: List) -> Dict[str, int]:
        """Get breakdown of alerts by visibility type"""
        from models.alert import VisibilityType
        
        breakdown = {vt.value: 0 for vt in VisibilityType}
        
        for alert in alerts:
            visibility_value = alert.visibility.type.value
            if visibility_value in breakdown:
                breakdown[visibility_value] += 1
        
        return breakdown
    
    def _get_creation_trend(self, alerts: List) -> List[Dict[str, Any]]:
        """Get alert creation trend (simulated)"""
        # In a real system, this would analyze creation dates
        return [
            {'date': '2024-01-01', 'count': 5},
            {'date': '2024-01-02', 'count': 8},
            {'date': '2024-01-03', 'count': 12},
            {'date': '2024-01-04', 'count': 7},
            {'date': '2024-01-05', 'count': 10}
        ]
    
    def _get_top_creators(self, alerts: List) -> List[Dict[str, Any]]:
        """Get top alert creators"""
        creator_counts = {}
        
        for alert in alerts:
            creator = alert.created_by
            creator_counts[creator] = creator_counts.get(creator, 0) + 1
        
        top_creators = [
            {'user_id': creator, 'alert_count': count}
            for creator, count in sorted(creator_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
        
        return top_creators
    
    def _get_most_active_teams(self, alerts: List) -> List[Dict[str, Any]]:
        """Get most active teams (simulated)"""
        # In a real system, this would analyze team activity
        return [
            {'team_id': 'engineering', 'alert_count': 15},
            {'team_id': 'marketing', 'alert_count': 8},
            {'team_id': 'qa', 'alert_count': 5}
        ]
    
    def _get_alert_lifespan_stats(self, alerts: List) -> Dict[str, Any]:
        """Get alert lifespan statistics (simulated)"""
        return {
            'average_lifespan_hours': 24.5,
            'shortest_lifespan_hours': 1,
            'longest_lifespan_hours': 168,
            'extended_alerts_count': 3
        }
    
    def _get_team_distribution(self) -> Dict[str, Any]:
        """Get team distribution statistics"""
        teams = self.alert_service.get_all_teams()
        all_users = self.alert_service.get_all_users()
        
        return {
            'total_teams': len(teams),
            'users_in_teams': sum(len(members) for members in teams.values()),
            'users_without_teams': len([u for u in all_users if not self.alert_service.get_user_teams(u.user_id)]),
            'largest_team': max([len(members) for members in teams.values()]) if teams else 0
        }
    
    def _get_user_activity_stats(self) -> Dict[str, Any]:
        """Get user activity statistics (simulated)"""
        return {
            'daily_active_users': 45,
            'weekly_active_users': 120,
            'monthly_active_users': 450,
            'avg_session_minutes': 8.5
        }
    
    def generate_report(self, report_type: str = "weekly") -> Dict[str, Any]:
        """Generate a comprehensive report"""
        print(f"📄 Generating {report_type} report...")
        
        report = {
            'report_type': report_type,
            'generated_at': datetime.now().isoformat(),
            'summary': self.get_system_metrics(),
            'alert_analytics': self.get_alert_analytics(),
            'user_analytics': self.get_user_analytics(),
            'recommendations': self._generate_recommendations()
        }
        
        print(f"✅ {report_type.capitalize()} report generated")
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate system recommendations (simulated)"""
        return [
            "Consider setting up more team-specific alerts for better targeting",
            "Critical alerts response time can be improved",
            "User engagement is high - consider adding more features",
            "Alert expiration policies are working effectively"
        ]