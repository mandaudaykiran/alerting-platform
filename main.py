#!/usr/bin/env python3
"""
Alerting Platform - Main Entry Point
"""
import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from services.alert_service import AlertService
from services.notification_service import NotificationService
from api.admin_api import AdminAPI
from api.user_api import UserAPI
from models.user import User, UserRole
from models.alert import Severity, VisibilityType
from data.seed_data import seed_sample_data

def main():
    """Main application entry point"""
    print("🚀 Alerting Platform Starting...")
    print("=" * 50)
    
    # Initialize services
    alert_service = AlertService()
    notification_service = NotificationService(alert_service)
    
    # Create APIs
    admin_api = AdminAPI(alert_service)
    user_api = UserAPI(alert_service, notification_service)
    
    # Seed sample data
    seed_sample_data(alert_service, notification_service)
    
    print("\n✅ System initialized successfully!")
    print("\nAvailable Commands:")
    print("1. Run 'python demo.py' for a full demo")
    print("2. Run tests with 'python -m unittest discover tests'")
    print("3. Check individual modules in src/ directory")

if __name__ == "__main__":
    main()