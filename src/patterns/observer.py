from abc import ABC, abstractmethod
from typing import List

class AlertObserver(ABC):
    """Observer interface for alert lifecycle events"""
    
    @abstractmethod
    def on_alert_created(self, alert):
        """Called when a new alert is created"""
        pass
    
    @abstractmethod
    def on_alert_updated(self, alert):
        """Called when an alert is updated"""
        pass
    
    @abstractmethod
    def on_alert_archived(self, alert):
        """Called when an alert is archived"""
        pass

class AlertObservable:
    """Observable class for alert lifecycle events"""
    
    def __init__(self):
        self._observers: List[AlertObserver] = []
    
    def add_observer(self, observer: AlertObserver):
        """Add an observer to the list"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"✅ Added observer: {observer.__class__.__name__}")
    
    def remove_observer(self, observer: AlertObserver):
        """Remove an observer from the list"""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"✅ Removed observer: {observer.__class__.__name__}")
    
    def notify_alert_created(self, alert):
        """Notify all observers about alert creation"""
        print(f"🔔 Notifying {len(self._observers)} observers about alert creation: {alert.title}")
        for observer in self._observers:
            try:
                observer.on_alert_created(alert)
            except Exception as e:
                print(f"❌ Error notifying observer {observer.__class__.__name__}: {e}")
    
    def notify_alert_updated(self, alert):
        """Notify all observers about alert update"""
        print(f"🔔 Notifying {len(self._observers)} observers about alert update: {alert.title}")
        for observer in self._observers:
            try:
                observer.on_alert_updated(alert)
            except Exception as e:
                print(f"❌ Error notifying observer {observer.__class__.__name__}: {e}")
    
    def notify_alert_archived(self, alert):
        """Notify all observers about alert archiving"""
        print(f"🔔 Notifying {len(self._observers)} observers about alert archiving: {alert.title}")
        for observer in self._observers:
            try:
                observer.on_alert_archived(alert)
            except Exception as e:
                print(f"❌ Error notifying observer {observer.__class__.__name__}: {e}")
    
    def get_observer_count(self) -> int:
        """Get the number of registered observers"""
        return len(self._observers)