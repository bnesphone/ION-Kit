# ION Kit Tests

Automated test suite for validating ION Kit functionality.

## Running Tests

### Run All Tests
```bash
python tests/run_tests.py
```

### Run Specific Test File
```bash
python -m unittest tests.test_cli
```

### Run Specific Test Class
```bash
python -m unittest tests.test_cli.TestCLICommands
```

### Run Specific Test Method
```bash
python -m unittest tests.test_cli.TestCLICommands.test_check_command
```

## Test Categories

### 1. CLI Tests (`test_cli.py`)
- ✅ Command execution
- ✅ Help output
- ✅ System check
- ✅ Version script

### 2. Tool Validation Tests
- ✅ Required tools exist
- ✅ Tool paths are correct
- ✅ Dependencies installed

### 3. Version Consistency Tests
- ✅ version.py exists and works
- ✅ Version values are valid
- ✅ Component counts are reasonable

## Adding New Tests

1. Create a new test file: `test_<feature>.py`
2. Import unittest and necessary modules
3. Create test classes inheriting from `unittest.TestCase`
4. Write test methods starting with `test_`
5. Run tests to verify

### Example Test Structure
```python
import unittest

class TestFeature(unittest.TestCase):
    def setUp(self):
        # Setup before each test
        pass
    
    def test_something(self):
        # Your test code
        self.assertTrue(condition)
```

## Continuous Integration

Add to CI/CD pipeline:
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: python tests/run_tests.py
```

## Test Coverage

Future enhancements:
- [ ] Integration tests for workflows
- [ ] Agent behavior tests
- [ ] Tool execution tests
- [ ] Error handling tests
- [ ] Performance tests
