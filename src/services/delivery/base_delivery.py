from abc import ABC, abstractmethod
from models.alert import Alert
from models.user import User

class DeliveryChannel(ABC):
    @abstractmethod
    def send(self, user: User, alert: Alert) -> bool:
        """Send notification to user"""
        pass
    
    @abstractmethod
    def get_channel_type(self) -> str:
        """Get the type of delivery channel"""
        pass

class DeliveryResult:
    def __init__(self, success: bool, message: str = "", delivery_id: str = ""):
        self.success = success
        self.message = message
        self.delivery_id = delivery_id
    
    def __bool__(self):
        return self.success
    
    def __str__(self):
        status = "✅ SUCCESS" if self.success else "❌ FAILED"
        return f"Delivery {status}: {self.message}"