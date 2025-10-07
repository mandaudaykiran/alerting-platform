#!/usr/bin/env python3
"""
Simple fix for GitHub Actions without Unicode characters
"""
import os
import subprocess

def cleanup_workflows():
    """Remove all existing workflow files"""
    workflow_dir = ".github/workflows"
    
    if os.path.exists(workflow_dir):
        print("Removing existing workflow files...")
        for file in os.listdir(workflow_dir):
            if file.endswith('.yml') or file.endswith('.yaml'):
                os.remove(os.path.join(workflow_dir, file))
                print(f"Removed: {file}")
    
    # Create directory if it doesn't exist
    os.makedirs(workflow_dir, exist_ok=True)

def create_simple_workflow():
    """Create a simple, working workflow without Unicode"""
    workflow_content = """name: Python Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10"]

    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Display Python version
      run: python --version
    
    - name: Run tests with unittest
      run: |
        python -m unittest discover tests -v
    
    - name: Verify demo runs
      run: |
        python demo.py
    
    - name: Verify imports work
      run: |
        python -c "from src.services.alert_service import AlertService; print('Import test passed')"
"""
    
    with open(".github/workflows/test.yml", "w", encoding="utf-8") as f:
        f.write(workflow_content)
    print("Created simple workflow")

def push_fixes():
    """Push all fixes to GitHub"""
    try:
        # Add all changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit
        subprocess.run(["git", "commit", "-m", "fix: Simple GitHub Actions workflow"], check=True)
        
        # Push
        result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Fixes pushed to GitHub!")
            print("GitHub Actions should now work correctly")
            print("Check: https://github.com/mandaudaykiran/alerting-platform/actions")
        else:
            print(f"Push failed: {result.stderr}")
            
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("GITHUB ACTIONS FIX")
    print("=" * 50)
    
    # Step 1: Clean up
    cleanup_workflows()
    
    # Step 2: Create simple workflow
    create_simple_workflow()
    
    # Step 3: Push fixes
    push_fixes()
    
    print("All fixes applied!")

if __name__ == "__main__":
    main()