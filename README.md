# 🚀 Alerting & Notification Platform

[![Python Tests](https://github.com/yourusername/alerting-platform/actions/workflows/python-tests.yml/badge.svg)](https://github.com/yourusername/alerting-platform/actions)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A lightweight, extensible alerting and notification system built with clean Object-Oriented Programming principles and design patterns.

## ✨ Features

### 🛠️ Admin Features
- 📢 Create alerts with configurable visibility (Organization, Team, User)
- ⚠️ Set severity levels (Info, Warning, Critical)
- ⏰ Configure reminder frequencies
- 📊 View comprehensive analytics
- 👥 Manage users and teams

### 👤 User Features
- 📨 Receive relevant alerts based on visibility rules
- ⏰ Snooze alerts for 24 hours
- 📖 Mark alerts as read/unread
- 🎯 Personalized dashboard

### 🏗️ Architecture
- **Strategy Pattern** for notification delivery channels
- **Observer Pattern** for alert lifecycle management
- **State Pattern** for user notification preferences
- **Factory Pattern** for delivery channel creation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher

### Installation
```bash
# Clone the repository
git clone https://github.com/mandaudaykiran/alerting-platform.git
cd alerting-platform

# Run the demo
python demo.py

# Or use the interactive interface
python simple_interface.py