#!/bin/bash

# Test runner script cho Backend
# Usage:
#   ./run_tests.sh              - Chạy tất cả tests
#   ./run_tests.sh projects     - Chạy tests của projects app
#   ./run_tests.sh employees    - Chạy tests của employees app
#   ./run_tests.sh packages     - Chạy tests của packages app
#   ./run_tests.sh users        - Chạy tests của users app

set -e

echo "======================================"
echo "   Studio Management - Test Runner"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}Warning: Virtual environment not activated${NC}"
    echo "Attempting to activate venv..."
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    elif [ -f "../venv/bin/activate" ]; then
        source ../venv/bin/activate
    else
        echo -e "${RED}Error: Could not find virtual environment${NC}"
        exit 1
    fi
fi

# Default to all tests if no argument provided
TARGET="${1:-all}"

case "$TARGET" in
    all)
        echo -e "${GREEN}Running ALL tests...${NC}"
        python manage.py test
        ;;

    projects)
        echo -e "${GREEN}Running Projects app tests...${NC}"
        python manage.py test apps.projects.tests
        ;;

    employees)
        echo -e "${GREEN}Running Employees app tests...${NC}"
        python manage.py test apps.employees.tests
        ;;

    packages)
        echo -e "${GREEN}Running Packages app tests...${NC}"
        python manage.py test apps.packages.tests
        ;;

    users)
        echo -e "${GREEN}Running Users/Auth tests...${NC}"
        python manage.py test apps.users.tests
        ;;

    coverage)
        echo -e "${GREEN}Running tests with coverage...${NC}"
        if ! command -v coverage &> /dev/null; then
            echo "Installing coverage..."
            pip install coverage
        fi
        coverage run --source='apps' manage.py test
        coverage report
        coverage html
        echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
        ;;

    pytest)
        echo -e "${GREEN}Running tests with pytest...${NC}"
        if ! command -v pytest &> /dev/null; then
            echo "Installing pytest and pytest-django..."
            pip install pytest pytest-django
        fi
        pytest
        ;;

    fast)
        echo -e "${GREEN}Running fast tests (excluding slow tests)...${NC}"
        pytest -m "not slow"
        ;;

    *)
        echo -e "${RED}Unknown test target: $TARGET${NC}"
        echo ""
        echo "Available options:"
        echo "  all       - Run all tests (default)"
        echo "  projects  - Run projects app tests"
        echo "  employees - Run employees app tests"
        echo "  packages  - Run packages app tests"
        echo "  users     - Run users/auth tests"
        echo "  coverage  - Run tests with coverage report"
        echo "  pytest    - Run tests using pytest"
        echo "  fast      - Run fast tests only"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✓ Tests completed!${NC}"
