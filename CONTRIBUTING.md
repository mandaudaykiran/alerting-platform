# Contributing to Alerting Platform

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature
4. Make your changes
5. Run tests: `python -m unittest discover tests`
6. Submit a pull request

## Code Style

- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings for public methods
- Include tests for new features

## Adding New Features

### New Delivery Channels
1. Create class in `src/services/delivery/`
2. Implement the `DeliveryChannel` interface
3. Register with `DeliveryFactory`
4. Add tests

### Extending Functionality
- New alert types? Extend the `Alert` model
- New user roles? Update `UserRole` enum
- Additional analytics? Extend `AnalyticsAPI`