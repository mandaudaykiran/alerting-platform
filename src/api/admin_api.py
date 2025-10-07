from typing import List, Optional, Set
from datetime import datetime

from models.alert import Alert, Severity, VisibilityType, DeliveryType
from services.alert_service import AlertService

class AdminAPI:
    """API for admin operations"""
    
    def __init__(self, alert_service: AlertService):
        self.alert_service = alert_service
    
    def create_alert(
        self,
        title: str,
        message: str,
        severity: Severity,
        created_by: str,
        visibility_type: VisibilityType,
        target_ids: Set[str],
        delivery_type: DeliveryType = DeliveryType.IN_APP,
        reminder_frequency: int = 120,
        start_time: Optional[datetime] = None,
        expiry_time: Optional[datetime] = None
    ) -> Alert:
        """Create a new alert"""
        
        print(f"🛠️  Admin creating alert: {title}")
        print(f"   Severity: {severity.value}")
        print(f"   Visibility: {visibility_type.value}")
        print(f"   Targets: {target_ids or 'All users'}")
        
        alert = self.alert_service.create_alert(
            title=title,
            message=message,
            severity=severity,
            created_by=created_by,
            visibility_type=visibility_type,
            target_ids=target_ids,
            delivery_type=delivery_type,
            reminder_frequency=reminder_frequency,
            start_time=start_time,
            expiry_time=expiry_time
        )
        
        print(f"✅ Alert created successfully: {alert.alert_id}")
        return alert
    
    def get_alert(self, alert_id: str) -> Optional[Alert]:
        """Get a specific alert by ID"""
        alert = self.alert_service.get_alert(alert_id)
        if alert:
            print(f"📋 Retrieved alert: {alert.title}")
        else:
            print(f"❌ Alert not found: {alert_id}")
        return alert
    
    def update_alert(self, alert_id: str, **kwargs) -> Optional[Alert]:
        """Update an existing alert"""
        print(f"🛠️  Updating alert: {alert_id}")
        print(f"   Changes: {kwargs}")
        
        alert = self.alert_service.update_alert(alert_id, **kwargs)
        if alert:
            print(f"✅ Alert updated successfully: {alert.title}")
        else:
            print(f"❌ Failed to update alert: {alert_id}")
        
        return alert
    
    def archive_alert(self, alert_id: str) -> bool:
        """Archive an alert"""
        print(f"🗃️  Archiving alert: {alert_id}")
        
        success = self.alert_service.archive_alert(alert_id)
        if success:
            print(f"✅ Alert archived successfully")
        else:
            print(f"❌ Failed to archive alert: {alert_id}")
        
        return success
    
    def list_alerts(
        self,
        severity: Optional[Severity] = None,
        status: Optional[str] = None
    ) -> List[Alert]:
        """List alerts with optional filtering"""
        
        filters = []
        if severity:
            filters.append(f"severity={severity.value}")
        if status:
            filters.append(f"status={status}")
        
        filter_str = " with filters: " + ", ".join(filters) if filters else ""
        print(f"📋 Listing alerts{filter_str}")
        
        alerts = self.alert_service.list_all_alerts(severity=severity, status=status)
        print(f"✅ Found {len(alerts)} alerts")
        
        return alerts
    
    def get_alert_metrics(self) -> dict:
        """Get system-wide alert metrics"""
        print("📊 Generating alert metrics...")
        
        alerts = self.alert_service.list_all_alerts()
        
        active_alerts = [a for a in alerts if a.is_active and not a.is_expired()]
        expired_alerts = [a for a in alerts if a.is_expired()]
        archived_alerts = [a for a in alerts if not a.is_active]
        
        severity_breakdown = {
            'info': len([a for a in alerts if a.severity == Severity.INFO]),
            'warning': len([a for a in alerts if a.severity == Severity.WARNING]),
            'critical': len([a for a in alerts if a.severity == Severity.CRITICAL]),
        }
        
        metrics = {
            'total_alerts': len(alerts),
            'active_alerts': len(active_alerts),
            'expired_alerts': len(expired_alerts),
            'archived_alerts': len(archived_alerts),
            'severity_breakdown': severity_breakdown,
            'visibility_breakdown': self._get_visibility_breakdown(alerts)
        }
        
        print("✅ Metrics generated successfully")
        return metrics
    
    def _get_visibility_breakdown(self, alerts: List[Alert]) -> dict:
        """Get breakdown of alerts by visibility type"""
        breakdown = {
            'organization': 0,
            'team': 0,
            'user': 0
        }
        
        for alert in alerts:
            visibility_type = alert.visibility.type.value
            if visibility_type in breakdown:
                breakdown[visibility_type] += 1
        
        return breakdown
    
    def get_system_stats(self) -> dict:
        """Get comprehensive system statistics"""
        print("📈 Generating system statistics...")
        
        alert_metrics = self.get_alert_metrics()
        service_stats = self.alert_service.get_stats()
        
        stats = {
            **alert_metrics,
            **service_stats,
            'system_health': {
                'alerts_created_today': self._get_today_alerts_count(),
                'active_users': len(self.alert_service.get_all_users()),
                'teams_configured': len(self.alert_service.get_all_teams())
            }
        }
        
        print("✅ System statistics generated")
        return stats
    
    def _get_today_alerts_count(self) -> int:
        """Get count of alerts created today"""
        alerts = self.alert_service.list_all_alerts()
        today = datetime.now().date()
        
        today_alerts = [
            alert for alert in alerts 
            if alert.created_at.date() == today
        ]
        
        return len(today_alerts)