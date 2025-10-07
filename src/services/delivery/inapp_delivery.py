from services.delivery.base_delivery import DeliveryChannel, DeliveryResult
from models.alert import Alert
from models.user import User
import uuid

class InAppDeliveryChannel(DeliveryChannel):
    def __init__(self, delivery_logger=None):
        self.delivery_logger = delivery_logger
    
    def send(self, user: User, alert: Alert) -> bool:
        try:
            # Simulate in-app delivery
            delivery_id = str(uuid.uuid4())
            
            print(f"📱 IN-APP NOTIFICATION [{delivery_id}]")
            print(f"   To: {user.name} ({user.email})")
            print(f"   Title: {alert.title}")
            print(f"   Message: {alert.message}")
            print(f"   Severity: {alert.severity.value.upper()}")
            print(f"   Type: {alert.delivery_type.value}")
            print("   " + "-" * 40)
            
            # Log delivery if logger is available
            if self.delivery_logger:
                self.delivery_logger.log_delivery({
                    'delivery_id': delivery_id,
                    'user_id': user.user_id,
                    'alert_id': alert.alert_id,
                    'channel': self.get_channel_type(),
                    'timestamp': 'now'
                })
            
            return True
        except Exception as e:
            print(f"❌ Failed to deliver in-app notification: {e}")
            return False
    
    def get_channel_type(self) -> str:
        return "in_app"