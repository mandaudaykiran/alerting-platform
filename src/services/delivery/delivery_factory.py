from services.delivery.base_delivery import DeliveryChannel
from services.delivery.inapp_delivery import InAppDeliveryChannel
from models.alert import DeliveryType

class DeliveryFactory:
    _channels = {}
    
    @classmethod
    def register_channel(cls, delivery_type: DeliveryType, channel_class):
        """Register a new delivery channel"""
        cls._channels[delivery_type] = channel_class
        print(f"✅ Registered delivery channel: {delivery_type.value} -> {channel_class.__name__}")
    
    @classmethod
    def create_channel(cls, delivery_type: DeliveryType, **kwargs) -> DeliveryChannel:
        """Create a delivery channel instance"""
        if delivery_type not in cls._channels:
            raise ValueError(f"❌ Unsupported delivery type: {delivery_type}")
        
        channel_class = cls._channels[delivery_type]
        return channel_class(**kwargs)
    
    @classmethod
    def get_supported_channels(cls):
        """Get list of supported delivery channels"""
        return list(cls._channels.keys())
    
    @classmethod
    def is_channel_supported(cls, delivery_type: DeliveryType) -> bool:
        """Check if a delivery channel is supported"""
        return delivery_type in cls._channels

# Initialize with default channels
DeliveryFactory.register_channel(DeliveryType.IN_APP, InAppDeliveryChannel)