#!/usr/bin/env python3
"""
Test runner script for SHALLION project
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print("Output:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Failed!")
        print(f"Error: {e}")
        if e.stdout:
            print("Stdout:")
            print(e.stdout)
        if e.stderr:
            print("Stderr:")
            print(e.stderr)
        return False


def run_unit_tests():
    """Run unit tests"""
    return run_command(
        "python -m pytest . -v -m 'unit' --tb=short",
        "Unit Tests"
    )


def run_integration_tests():
    """Run integration tests"""
    return run_command(
        "python -m pytest . -v -m 'integration' --tb=short",
        "Integration Tests"
    )


def run_all_tests():
    """Run all tests"""
    return run_command(
        "python -m pytest . -v --tb=short",
        "All Tests"
    )


def run_tests_with_coverage():
    """Run tests with coverage report"""
    return run_command(
        "python -m pytest . -v --cov=apps --cov-report=html --cov-report=term-missing",
        "Tests with Coverage"
    )


def run_fast_tests():
    """Run fast tests only"""
    return run_command(
        "python -m pytest . -v -m 'fast' --tb=short",
        "Fast Tests"
    )


def run_slow_tests():
    """Run slow tests only"""
    return run_command(
        "python -m pytest . -v -m 'slow' --tb=short",
        "Slow Tests"
    )


def run_frontend_tests():
    """Run frontend tests"""
    return run_command(
        "python -m pytest test_frontend.py -v --tb=short",
        "Frontend Tests"
    )


def run_backend_tests():
    """Run backend tests"""
    return run_command(
        "python -m pytest test_products.py test_orders.py test_users.py -v --tb=short",
        "Backend Tests"
    )


def check_test_environment():
    """Check if test environment is properly set up"""
    print("\n🔍 Checking test environment...")
    
    # Check if we're in the tests directory
    if not Path("conftest.py").exists():
        print("❌ Error: conftest.py not found. Please run from tests directory.")
        return False
    
    # Check if we can access the project root
    project_root = Path("..")
    if not (project_root / "manage.py").exists():
        print("❌ Error: manage.py not found in parent directory.")
        return False
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment might not be activated.")
    
    # Check if required packages are installed
    try:
        import pytest
        import django
        print("✅ Required packages are installed.")
    except ImportError as e:
        print(f"❌ Error: Missing required package - {e}")
        return False
    
    return True


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="SHALLION Test Runner")
    parser.add_argument(
        "--type",
        choices=["unit", "integration", "all", "coverage", "fast", "slow", "frontend", "backend"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--check-env",
        action="store_true",
        help="Check test environment only"
    )
    
    args = parser.parse_args()
    
    print("🚀 SHALLION Test Runner")
    print("=" * 50)
    
    # Check environment first
    if not check_test_environment():
        sys.exit(1)
    
    if args.check_env:
        print("✅ Environment check completed.")
        return
    
    # Run tests based on type
    success = False
    
    if args.type == "unit":
        success = run_unit_tests()
    elif args.type == "integration":
        success = run_integration_tests()
    elif args.type == "coverage":
        success = run_tests_with_coverage()
    elif args.type == "fast":
        success = run_fast_tests()
    elif args.type == "slow":
        success = run_slow_tests()
    elif args.type == "frontend":
        success = run_frontend_tests()
    elif args.type == "backend":
        success = run_backend_tests()
    else:  # all
        success = run_all_tests()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("💥 Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 