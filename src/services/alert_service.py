from typing import Dict, List, Optional, Set
from datetime import datetime
import uuid

from models.alert import Alert, AlertVisibility, VisibilityType, Severity, DeliveryType
from models.user import User
from patterns.observer import AlertObservable

class AlertService(AlertObservable):
    def __init__(self):
        super().__init__()
        self._alerts: Dict[str, Alert] = {}
        self._users: Dict[str, User] = {}
        self._teams: Dict[str, Set[str]] = {}  # team_id -> set of user_ids
    
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
        
        alert_id = str(uuid.uuid4())
        visibility = AlertVisibility(type=visibility_type, target_ids=target_ids)
        
        alert = Alert(
            alert_id=alert_id,
            title=title,
            message=message,
            severity=severity,
            created_by=created_by,
            visibility=visibility,
            delivery_type=delivery_type,
            reminder_frequency=reminder_frequency,
            start_time=start_time,
            expiry_time=expiry_time
        )
        
        self._alerts[alert_id] = alert
        self.notify_alert_created(alert)
        return alert
    
    def get_alert(self, alert_id: str) -> Optional[Alert]:
        return self._alerts.get(alert_id)
    
    def update_alert(self, alert_id: str, **kwargs) -> Optional[Alert]:
        alert = self._alerts.get(alert_id)
        if alert:
            alert.update(**kwargs)
            self.notify_alert_updated(alert)
            return alert
        return None
    
    def archive_alert(self, alert_id: str) -> bool:
        alert = self._alerts.get(alert_id)
        if alert:
            alert.archive()
            self.notify_alert_archived(alert)
            return True
        return False
    
    def get_alerts_for_user(self, user_id: str) -> List[Alert]:
        user = self._users.get(user_id)
        if not user:
            return []
        
        user_teams = self.get_user_teams(user_id)
        user_alerts = []
        
        for alert in self._alerts.values():
            if alert.is_visible_to_user(user, user_teams):
                user_alerts.append(alert)
        
        return user_alerts
    
    def list_all_alerts(
        self,
        severity: Optional[Severity] = None,
        status: Optional[str] = None
    ) -> List[Alert]:
        filtered_alerts = list(self._alerts.values())
        
        if severity:
            filtered_alerts = [a for a in filtered_alerts if a.severity == severity]
        
        if status == "active":
            filtered_alerts = [a for a in filtered_alerts if a.is_active and not a.is_expired()]
        elif status == "expired":
            filtered_alerts = [a for a in filtered_alerts if a.is_expired()]
        elif status == "archived":
            filtered_alerts = [a for a in filtered_alerts if not a.is_active]
        
        return filtered_alerts
    
    def add_user(self, user: User):
        self._users[user.user_id] = user
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
    
    def add_team(self, team_id: str, user_ids: Set[str]):
        self._teams[team_id] = user_ids
    
    def get_user_teams(self, user_id: str) -> Set[str]:
        teams = set()
        for team_id, members in self._teams.items():
            if user_id in members:
                teams.add(team_id)
        return teams
    
    def get_team_members(self, team_id: str) -> Set[str]:
        return self._teams.get(team_id, set())
    
    def get_all_users(self) -> List[User]:
        return list(self._users.values())
    
    def get_all_teams(self) -> Dict[str, Set[str]]:
        return self._teams.copy()
    
    def get_stats(self) -> Dict[str, int]:
        return {
            "total_alerts": len(self._alerts),
            "total_users": len(self._users),
            "total_teams": len(self._teams),
            "active_alerts": len([a for a in self._alerts.values() if a.is_active and not a.is_expired()])
        }