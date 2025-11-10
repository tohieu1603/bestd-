#!/usr/bin/env python
"""
Python test runner script - Cross-platform alternative to run_tests.sh
Usage: python run_tests.py [target]
"""
import sys
import os
import subprocess
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

    @classmethod
    def disable(cls):
        """Disable colors for Windows or non-TTY environments."""
        cls.RED = ''
        cls.GREEN = ''
        cls.YELLOW = ''
        cls.BLUE = ''
        cls.NC = ''


# Disable colors on Windows if not supported
if os.name == 'nt' and not os.environ.get('ANSICON'):
    Colors.disable()


def print_header():
    """Print test runner header."""
    print("=" * 50)
    print("   Studio Management - Test Runner")
    print("=" * 50)
    print()


def print_success(message):
    """Print success message."""
    print(f"{Colors.GREEN}{message}{Colors.NC}")


def print_error(message):
    """Print error message."""
    print(f"{Colors.RED}{message}{Colors.NC}")


def print_warning(message):
    """Print warning message."""
    print(f"{Colors.YELLOW}{message}{Colors.NC}")


def print_info(message):
    """Print info message."""
    print(f"{Colors.BLUE}{message}{Colors.NC}")


def run_command(command):
    """Run a command and return success status."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            cwd=Path(__file__).parent
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed with exit code {e.returncode}")
        return False


def run_all_tests():
    """Run all tests using Django test runner."""
    print_info("Running ALL tests...")
    return run_command("python manage.py test")


def run_app_tests(app_name):
    """Run tests for a specific app."""
    print_info(f"Running {app_name.capitalize()} app tests...")
    return run_command(f"python manage.py test apps.{app_name}.tests")


def run_coverage():
    """Run tests with coverage."""
    print_info("Running tests with coverage...")

    # Check if coverage is installed
    try:
        import coverage
    except ImportError:
        print_warning("Coverage not installed. Installing...")
        if not run_command("pip install coverage"):
            print_error("Failed to install coverage")
            return False

    success = run_command("coverage run --source='apps' manage.py test")
    if success:
        run_command("coverage report")
        run_command("coverage html")
        print_success("\nCoverage report generated in htmlcov/index.html")
    return success


def run_pytest():
    """Run tests using pytest."""
    print_info("Running tests with pytest...")

    # Check if pytest is installed
    try:
        import pytest
    except ImportError:
        print_warning("Pytest not installed. Installing...")
        if not run_command("pip install pytest pytest-django"):
            print_error("Failed to install pytest")
            return False

    return run_command("pytest")


def run_fast_tests():
    """Run fast tests only (excluding slow tests)."""
    print_info("Running fast tests (excluding slow tests)...")
    return run_command('pytest -m "not slow"')


def show_help():
    """Show help message."""
    print("Available options:")
    print("  all       - Run all tests (default)")
    print("  projects  - Run projects app tests")
    print("  employees - Run employees app tests")
    print("  packages  - Run packages app tests")
    print("  users     - Run users/auth tests")
    print("  coverage  - Run tests with coverage report")
    print("  pytest    - Run tests using pytest")
    print("  fast      - Run fast tests only")
    print("  help      - Show this help message")


def main():
    """Main entry point."""
    print_header()

    # Get target from command line or default to 'all'
    target = sys.argv[1] if len(sys.argv) > 1 else 'all'

    # Route to appropriate test runner
    success = False

    if target == 'all':
        success = run_all_tests()

    elif target in ['projects', 'employees', 'packages', 'users']:
        success = run_app_tests(target)

    elif target == 'coverage':
        success = run_coverage()

    elif target == 'pytest':
        success = run_pytest()

    elif target == 'fast':
        success = run_fast_tests()

    elif target in ['help', '-h', '--help']:
        show_help()
        sys.exit(0)

    else:
        print_error(f"Unknown test target: {target}")
        print()
        show_help()
        sys.exit(1)

    # Print result
    print()
    if success:
        print_success("✓ Tests completed!")
        sys.exit(0)
    else:
        print_error("✗ Tests failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()
