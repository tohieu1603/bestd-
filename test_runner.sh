#!/bin/bash
#
# Beautiful test runner for Django Backend
# Usage: ./test_runner.sh
#

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════════"
echo "                          🧪 DJANGO BACKEND TEST SUITE"
echo "                           $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════════════════════════════════════════════"
echo ""

# Run tests with auto-yes to clean test database
echo "yes" | python3 manage.py test apps.projects apps.employees apps.packages apps.users --verbosity=2 2>&1 | tee /tmp/django_test_output.log | tail -100

# Extract summary
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════════"
echo "                              📊  FINAL SUMMARY"
echo "═══════════════════════════════════════════════════════════════════════════════════"
echo ""

# Count tests by parsing output
PROJECTS=$(grep -c "apps\.projects\.tests.*\.\.\. ok$" /tmp/django_test_output.log)
EMPLOYEES=$(grep -c "apps\.employees\.tests.*\.\.\. ok$" /tmp/django_test_output.log)
PACKAGES=$(grep -c "apps\.packages\.tests.*\.\.\. ok$" /tmp/django_test_output.log)
USERS=$(grep -c "apps\.users\.tests.*\.\.\. ok$" /tmp/django_test_output.log)
TOTAL=$(($PROJECTS + $EMPLOYEES + $PACKAGES + $USERS))

echo "  ✅  Projects:    $PROJECTS/19 tests passed"
echo "  ✅  Employees:   $EMPLOYEES/8 tests passed"
echo "  ✅  Packages:    $PACKAGES/24 tests passed"
echo "  ✅  Users/Auth:  $USERS/13 tests passed"
echo "  ─────────────────────────────────────────────"
echo "  ✅  TOTAL:       $TOTAL/64 tests passed"
echo ""

# Check if all passed
if grep -q "^OK$" /tmp/django_test_output.log && [ $TOTAL -eq 64 ]; then
    echo "  🎉  ALL 64 TESTS PASSED!"
else
    echo "  ⚠️   SOME TESTS FAILED - Check output above"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════════"
echo ""
