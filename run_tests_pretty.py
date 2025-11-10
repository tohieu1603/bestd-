#!/usr/bin/env python3
"""
Beautiful test runner for Django backend tests.
"""
import subprocess
import sys
import re
from datetime import datetime


def print_header():
    """Print test suite header."""
    print("\n" + "═" * 80)
    print("                        🧪 BACKEND TEST SUITE")
    print("                    " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("═" * 80 + "\n")


def print_section(title):
    """Print section header."""
    print(f"\n{'─' * 80}")
    print(f"  {title}")
    print('─' * 80)


def parse_test_output(output):
    """Parse Django test output and extract test results."""
    lines = output.split('\n')
    tests = []

    for line in lines:
        if line.startswith('test_') and ' ... ' in line:
            # Extract test name and result
            parts = line.split(' ... ')
            if len(parts) >= 2:
                test_name = parts[0].split('(')[0].strip()
                result = parts[1].strip().lower()

                if 'ok' in result:
                    tests.append(('✅', test_name, 'PASS'))
                elif 'fail' in result:
                    tests.append(('❌', test_name, 'FAIL'))
                elif 'error' in result:
                    tests.append(('⚠️ ', test_name, 'ERROR'))

    return tests


def run_app_tests(app_name, app_path, expected_count):
    """Run tests for a single app and return results."""
    print_section(f"📦 Testing {app_name} ({expected_count} tests expected)")

    result = subprocess.run(
        ['python3', 'manage.py', 'test', app_path, '--verbosity=2'],
        capture_output=True,
        text=True
    )

    output = result.stdout + result.stderr
    tests = parse_test_output(output)

    # Print test results
    for emoji, test_name, status in tests:
        print(f"  {emoji} {test_name}")

    # Extract summary
    for line in output.split('\n'):
        if 'Ran' in line and 'test' in line:
            match = re.search(r'Ran (\d+) tests? in ([\d.]+)s', line)
            if match:
                count = match.group(1)
                time = match.group(2)
                print(f"\n  ⏱️  Ran {count} tests in {time}s")

        if line.strip() == 'OK':
            print(f"  ✅ Status: ALL PASSED")
        elif 'FAILED' in line:
            print(f"  ❌ Status: SOME TESTS FAILED")

    return tests, result.returncode == 0


def main():
    """Main test runner."""
    print_header()

    # Apps to test
    apps_config = [
        ('Projects', 'apps.projects', 19),
        ('Employees', 'apps.employees', 8),
        ('Packages', 'apps.packages', 24),
        ('Users/Auth', 'apps.users', 13),
    ]

    all_results = {}
    all_passed = True
    total_tests = 0

    # Run tests for each app
    for app_name, app_path, expected_count in apps_config:
        tests, passed = run_app_tests(app_name, app_path, expected_count)
        all_results[app_name] = {
            'tests': tests,
            'passed': passed,
            'count': len(tests)
        }
        total_tests += len(tests)
        if not passed:
            all_passed = False

    # Final summary
    print("\n" + "═" * 80)
    print("                           📊 FINAL SUMMARY")
    print("═" * 80 + "\n")

    for app_name, results in all_results.items():
        passed = sum(1 for _, _, status in results['tests'] if status == 'PASS')
        total = results['count']
        emoji = '✅' if passed == total else '❌'
        print(f"  {emoji} {app_name:12s}: {passed:2d}/{total:2d} tests passed")

    print(f"  {'─' * 40}")
    total_passed = sum(
        sum(1 for _, _, status in r['tests'] if status == 'PASS')
        for r in all_results.values()
    )
    print(f"  {'TOTAL':14s}: {total_passed:2d}/{total_tests:2d} tests passed")

    if all_passed and total_tests > 0:
        print(f"\n  🎉 RESULT: ALL {total_tests} TESTS PASSED ✅")
    else:
        failed = total_tests - total_passed
        print(f"\n  ⚠️  RESULT: {failed} TEST(S) FAILED ❌")

    print("\n" + "═" * 80 + "\n")

    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
