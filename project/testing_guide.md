# Testing Guide for banger

## Quick Test During Development

### 1. Direct Module Testing

```ascii
# From project root with activated venv
python -m src.banner_ng "TEST"
```

### 2. Editable Install Testing

```ascii
# Install in development mode
pip install -e .

# Test the command
banger "HELLO"
```

## Comparing with Original Banner

### 1. Side-by-Side Comparison

```ascii
# Run original banner
banner "TEST" > original.txt

# Run our implementation
banger "TEST" > new.txt

# Compare outputs
diff original.txt new.txt
```

### 2. Visual Comparison Script

```ascii
#!/bin/bash
# save as compare_banners.sh

TEXT="$1"
echo "=== Original banner ==="
banner "$TEXT"
echo
echo "=== banger ==="
banger "$TEXT"
```

### 3. Automated Test Cases

```ascii
# Test all characters
for char in A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 0 1 2 3 4 5 6 7 8 9; do
    echo "Testing: $char"
    banner "$char" > "test_orig_$char.txt"
    banger "$char" > "test_new_$char.txt"
    diff -q "test_orig_$char.txt" "test_new_$char.txt" || echo "MISMATCH: $char"
done

# Test special characters
for char in '#' '!' '@' '$' '%' '&' '*' '(' ')' '-' '+' '=' '?' '/' '.' ','; do
    echo "Testing: $char"
    banner "$char" > "test_orig_special_$char.txt"
    banger "$char" > "test_new_special_$char.txt"
    diff -q "test_orig_special_$char.txt" "test_new_special_$char.txt" || echo "MISMATCH: $char"
done
```

## Testing Edge Cases

### 1. Terminal Width

```ascii
# Test with different terminal widths
COLUMNS=40 banger "HELLO WORLD"
COLUMNS=80 banger "HELLO WORLD"
COLUMNS=120 banger "HELLO WORLD"

# Test truncation
COLUMNS=20 banger "TRUNCATED"
```

### 2. Multiple Arguments

```ascii
# Each word should be a separate banner
banger "HELLO" "WORLD"
```

### 3. Special Cases

```ascii
# Empty string
banger ""

# Single character
banger "A"

# Numbers
banger "12345"

# Mixed case (should convert to uppercase)
banger "Hello"

# Whitespace handling
banger "HELLO WORLD"
banger "HELLO	WORLD"  # Tab
banger "HELLO
WORLD"  # Newline

# Unknown characters (should be ignored)
banger "HELLO€WORLD"

# -- separator
banger -- "--help"
```

## Unit Testing

### Run pytest

```ascii
# Run all tests
pytest

# Run with coverage
pytest --cov=banner_ng --cov-report=html

# Run in verbose mode
pytest -v
```

### Test Structure Example

```python
# tests/test_compatibility.py
import subprocess
import pytest


def test_exact_match_letter_a():
    """Test that letter A matches original banner exactly."""
    # Run original banner
    orig = subprocess.run(['banner', 'A'], capture_output=True, text=True)

    # Run our banner
    new = subprocess.run(['banner-ng', 'A'], capture_output=True, text=True)

    assert orig.stdout == new.stdout
```

## Integration Testing

### 1. Package Installation Test

```ascii
# Build the package
python -m build

# Create a fresh virtual environment
python -m venv test-install-env
source test-install-env/bin/activate

# Install from the wheel
pip install dist/banner_ng-*.whl

# Test it works
banger "INSTALLED"

# Clean up
deactivate
rm -rf test-install-env
```

### 2. pipx Installation Test

```ascii
# Install with pipx
pipx install dist/banner_ng-*.whl

# Test it works
banger "PIPX TEST"

# Uninstall
pipx uninstall banner-ng
```

## Performance Testing

### Simple Timing

```ascii
# Time the execution
time banger "PERFORMANCE"

# Multiple runs
for i in {1..100}; do
    time banger "TEST" > /dev/null
done 2>&1 | grep real | awk '{sum += $2} END {print "Average:", sum/NR}'
```

### Python Performance Test

```python
# perf_test.py
import time
from banner_ng.core import BannerGenerator

# Test import time
start = time.time()
import banner_ng

print(f"Import time: {(time.time() - start) * 1000:.2f}ms")

# Test render time
text = "PERFORMANCE"
start = time.time()
gen = BannerGenerator()
gen.add_text(text)
result = gen.render()
print(f"Render time for '{text}': {(time.time() - start) * 1000:.2f}ms")
```

## Debugging Tips

### 1. Character-by-Character Debug

```python
# debug_char.py
from banner_ng.fonts import CHARACTERS

# Check a specific character
char = 'A'
if char in CHARACTERS:
    for line in CHARACTERS[char]:
        print(repr(line))  # Shows exact spacing
```

### 2. Width Detection Debug

```ascii
# Check what width is detected
python -c "from banner_ng.terminal import get_terminal_width; print(f'Width: {get_terminal_width()}')"

# Test with different COLUMNS values
COLUMNS=50 python -c "from banner_ng.terminal import get_terminal_width; print(f'Width: {get_terminal_width()}')"
```

### 3. Verbose Mode (if implemented)

```ascii
# Add a --verbose flag for debugging
banger --verbose "DEBUG"
```

## Continuous Testing

### GitHub Actions will run on every push

- Multiple Python versions (3.8-3.12)
- Multiple OS (Linux, macOS, Windows)
- Linting and type checking
- Coverage reporting

### Local Multi-Version Testing

```ascii
# Using tox
tox  # Run all environments
tox -e py38  # Run Python 3.8 only
tox -e lint  # Run linting only
```

## Acceptance Testing Checklist

- [ ] All uppercase letters A-Z render correctly
- [ ] All numbers 0-9 render correctly
- [ ] All supported special characters render correctly
- [ ] Lowercase converts to uppercase
- [ ] Terminal width detection works
- [ ] COLUMNS env var is respected
- [ ] Truncation works at terminal boundary
- [ ] Multiple arguments create separate banners
- [ ] Unknown characters are silently ignored
- [ ] -- separator works
- [ ] Help text displays with -h/--help
- [ ] No runtime dependencies required
- [ ] Import time < 100ms
- [ ] Render time < 50ms for 10 chars
- [ ] Works on Linux, macOS, Windows
