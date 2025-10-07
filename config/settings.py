"""
Application configuration settings
"""

import os
from typing import Dict, Any

class Settings:
    """Application settings configuration"""
    
    def __init__(self):
        # Application settings
        self.APP_NAME = "Alerting Platform"
        self.APP_VERSION = "1.0.0"
        self.DEBUG = True
        
        # Alert settings
        self.DEFAULT_REMINDER_FREQUENCY = 120  # minutes
        self.MAX_REMINDER_FREQUENCY = 1440     # 24 hours in minutes
        self.MIN_REMINDER_FREQUENCY = 5        # 5 minutes
        self.SNOOZE_DURATION_HOURS = 24
        
        # Notification settings
        self.MAX_RETRY_ATTEMPTS = 3
        self.RETRY_DELAY_SECONDS = 30
        self.BATCH_PROCESSING_SIZE = 100
        
        # User settings
        self.MAX_ALERTS_PER_USER = 1000
        self.MAX_TEAMS_PER_USER = 10
        self.USER_SESSION_TIMEOUT = 3600  # 1 hour in seconds
        
        # System settings
        self.LOG_LEVEL = "INFO"
        self.ENABLE_ANALYTICS = True
        self.DATA_RETENTION_DAYS = 365
        
        # Delivery settings
        self.ENABLED_DELIVERY_CHANNELS = ["in_app"]
        self.DEFAULT_DELIVERY_CHANNEL = "in_app"
        
        # Security settings
        self.ENABLE_AUTHENTICATION = False  # For MVP
        self.API_RATE_LIMIT = 1000  # requests per hour
        
        # Database settings (for future use)
        self.DATABASE_URL = "sqlite:///alerts.db"
        self.ENABLE_PERSISTENCE = False  # For MVP using in-memory storage
        
        # Load environment variables
        self._load_environment_variables()
    
    def _load_environment_variables(self):
        """Load settings from environment variables"""
        # Alert settings
        reminder_freq = os.getenv('DEFAULT_REMINDER_FREQUENCY')
        if reminder_freq:
            self.DEFAULT_REMINDER_FREQUENCY = int(reminder_freq)
        
        debug_mode = os.getenv('DEBUG')
        if debug_mode:
            self.DEBUG = debug_mode.lower() == 'true'
        
        log_level = os.getenv('LOG_LEVEL')
        if log_level:
            self.LOG_LEVEL = log_level.upper()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary"""
        return {
            'app_name': self.APP_NAME,
            'app_version': self.APP_VERSION,
            'debug': self.DEBUG,
            'default_reminder_frequency': self.DEFAULT_REMINDER_FREQUENCY,
            'snooze_duration_hours': self.SNOOZE_DURATION_HOURS,
            'max_alerts_per_user': self.MAX_ALERTS_PER_USER,
            'log_level': self.LOG_LEVEL,
            'enabled_delivery_channels': self.ENABLED_DELIVERY_CHANNELS,
            'enable_analytics': self.ENABLE_ANALYTICS
        }
    
    def validate(self) -> bool:
        """Validate settings configuration"""
        try:
            assert self.DEFAULT_REMINDER_FREQUENCY >= self.MIN_REMINDER_FREQUENCY, \
                f"Reminder frequency must be at least {self.MIN_REMINDER_FREQUENCY} minutes"
            
            assert self.DEFAULT_REMINDER_FREQUENCY <= self.MAX_REMINDER_FREQUENCY, \
                f"Reminder frequency cannot exceed {self.MAX_REMINDER_FREQUENCY} minutes"
            
            assert self.SNOOZE_DURATION_HOURS > 0, "Snooze duration must be positive"
            
            assert self.MAX_ALERTS_PER_USER > 0, "Max alerts per user must be positive"
            
            assert self.LOG_LEVEL in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], \
                "Invalid log level"
            
            return True
            
        except AssertionError as e:
            print(f"❌ Configuration validation failed: {e}")
            return False
    
    def __str__(self):
        return f"Settings(APP_NAME={self.APP_NAME}, DEBUG={self.DEBUG})"

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get the global settings instance"""
    return settings

def print_settings():
    """Print current settings (for debugging)"""
    print("🔧 Current Settings:")
    print("=" * 50)
    for key, value in settings.to_dict().items():
        print(f"  {key}: {value}")
    print("=" * 50)
    
    # Validate settings
    if settings.validate():
        print("✅ Settings validation: PASSED")
    else:
        print("❌ Settings validation: FAILED")