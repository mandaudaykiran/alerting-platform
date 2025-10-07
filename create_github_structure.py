#!/usr/bin/env python3
"""
Script to create the complete GitHub repository structure for Alerting Platform
"""
import os
import sys

def create_structure():
    """Create the complete file structure"""
    
    # Root directory files
    root_files = [
        'README.md', 'LICENSE', 'CONTRIBUTING.md', 'CHANGELOG.md',
        'pyproject.toml', 'requirements.txt', 'setup.py',
        'main.py', 'demo.py', 'simple_interface.py', 'test_scenarios.py',
        '.gitignore'
    ]
    
    # Directory structure
    directories = [
        '.github/workflows',
        'src/models',
        'src/services/delivery', 
        'src/patterns',
        'src/api',
        'src/utils',
        'tests',
        'docs',
        'config',
        'data'
    ]
    
    # Create directories
    print("📁 Creating directory structure...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ {directory}/")
    
    # Create __init__.py files
    init_files = [
        'src/__init__.py',
        'src/models/__init__.py',
        'src/services/__init__.py',
        'src/services/delivery/__init__.py',
        'src/patterns/__init__.py',
        'src/api/__init__.py',
        'src/utils/__init__.py',
        'tests/__init__.py'
    ]
    
    for init_file in init_files:
        with open(init_file, 'w') as f:
            f.write('"""Package initialization"""\n')
        print(f"  ✅ {init_file}")
    
    # Create empty files for the structure
    for root_file in root_files:
        open(root_file, 'a').close()
        print(f"  ✅ {root_file}")
    
    print("✅ GitHub structure created successfully!")
    print("\nNext steps:")
    print("1. Copy all your existing code files to their respective locations")
    print("2. Run: git init")
    print("3. Run: git add .")
    print("4. Run: git commit -m 'Initial commit'")
    print("5. Run: git remote add origin https://github.com/mandaudaykiran/alerting-platform.git")
    print("6. Run: git push -u origin main")

if __name__ == "__main__":
    create_structure()