# Backend Testing - Quick Reference

## 🚀 Quick Start

```bash
# Chạy tất cả tests (64 tests)
./run_tests.sh

# Hoặc dùng Python script (cross-platform)
python run_tests.py

# Hoặc traditional Django
python manage.py test apps.projects apps.employees apps.packages apps.users
```

## 📦 Test Coverage

### ✅ Apps Tested

- **Projects** - 19 tests (10 service + 9 API)
- **Employees** - 8 tests (8 service)
- **Packages** - 24 tests (11 service + 13 API)
- **Users/Auth** - 13 tests (authentication)

**Total: 64 tests**

## 🎯 Run Specific Tests

```bash
# By app
./run_tests.sh projects      # 19 tests
./run_tests.sh employees     # 8 tests
./run_tests.sh packages      # 24 tests
./run_tests.sh users         # 13 tests

# With coverage report
./run_tests.sh coverage

# Fast tests only
./run_tests.sh fast

# Using pytest
./run_tests.sh pytest
```

## 📊 Coverage Goals

| Component | Target | Status |
|-----------|--------|--------|
| Services  | 90%+   | ✅ 92% |
| API       | 85%+   | ✅ 88% |
| Models    | 80%+   | ✅ 83% |

## 📁 Test Structure

```
backend/
├── apps/
│   ├── projects/tests/      # 19 tests (10 service + 9 API)
│   ├── employees/tests/     # 8 tests (service)
│   ├── packages/tests/      # 24 tests (11 service + 13 API)
│   └── users/tests/         # 13 tests (authentication)
├── pytest.ini               # Pytest config
├── run_tests.sh             # Test runner (Linux/Mac)
└── run_tests.py             # Test runner (Cross-platform)
```

## 🔍 Example Commands

```bash
# Traditional Django test
python manage.py test apps.projects.tests.test_services

# Pytest with verbose
pytest -v apps/projects/tests/

# Coverage with HTML report
coverage run --source='apps' manage.py test
coverage html
open htmlcov/index.html
```

## 📖 Full Documentation

See [TEST_GUIDE.md](../TEST_GUIDE.md) for comprehensive testing documentation.
