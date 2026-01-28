# Type Hints Guide

## Overview

The Antigravity Workspace uses comprehensive type hints throughout the codebase to improve code quality, enable better IDE support, and catch type-related bugs early through static analysis with mypy.

## Why Type Hints?

### Benefits

1. **Early Bug Detection**: Catch type errors before runtime
2. **Better IDE Support**: Enhanced autocomplete and inline documentation
3. **Self-Documenting Code**: Types serve as inline documentation
4. **Refactoring Safety**: Easier to refactor with confidence
5. **Team Collaboration**: Clear contracts between functions

### Example

```python
# Without type hints - unclear what types are expected
def process_data(data, config):
    return data.transform(config.get("mode"))

# With type hints - crystal clear
def process_data(data: Dict[str, Any], config: Dict[str, str]) -> List[str]:
    mode = config.get("mode", "default")
    return data.transform(mode)
```

## Type Hint Standards

### Basic Types

```python
from typing import List, Dict, Set, Tuple, Optional, Any, Union

# Primitives
name: str = "Antigravity"
count: int = 42
ratio: float = 3.14
is_active: bool = True

# Collections
names: List[str] = ["Alice", "Bob"]
scores: Dict[str, int] = {"Alice": 95, "Bob": 87}
unique_ids: Set[int] = {1, 2, 3}
coordinates: Tuple[float, float] = (10.5, 20.3)

# Optional values (can be None)
optional_name: Optional[str] = None
optional_count: Optional[int] = get_count()  # May return None

# Union types (multiple possible types)
id_value: Union[str, int] = "user_123"  # Can be str or int

# Any type (use sparingly)
dynamic_value: Any = get_dynamic_data()
```

### Function Signatures

```python
from typing import List, Optional, Dict, Any

# Basic function
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Function with optional parameter
def greet_optional(name: str, title: Optional[str] = None) -> str:
    if title:
        return f"Hello, {title} {name}!"
    return f"Hello, {name}!"

# Function with multiple return types
def parse_value(value: str) -> Union[int, float, str]:
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value

# Function with no return value
def log_message(message: str) -> None:
    print(f"[LOG] {message}")

# Function with complex types
def process_users(
    users: List[Dict[str, Any]],
    filters: Optional[Dict[str, str]] = None
) -> List[str]:
    """Process user data and return user IDs."""
    if filters:
        users = [u for u in users if matches_filters(u, filters)]
    return [user["id"] for user in users]
```

### Class Type Hints

```python
from typing import List, Optional, ClassVar
from pathlib import Path

class DataProcessor:
    """Process data with configurable settings."""
    
    # Class variable
    default_mode: ClassVar[str] = "standard"
    
    def __init__(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
        batch_size: int = 100
    ) -> None:
        """Initialize processor."""
        self.input_path = input_path
        self.output_path = output_path or Path("output")
        self.batch_size = batch_size
        self._cache: Dict[str, Any] = {}
    
    def process(self, data: List[Dict[str, Any]]) -> List[str]:
        """Process data and return results."""
        results: List[str] = []
        for item in data:
            result = self._process_item(item)
            results.append(result)
        return results
    
    def _process_item(self, item: Dict[str, Any]) -> str:
        """Process single item."""
        return str(item.get("value", ""))
```

### Generic Types

```python
from typing import TypeVar, Generic, List, Optional

# Define type variable
T = TypeVar('T')

class Stack(Generic[T]):
    """Generic stack data structure."""
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        """Add item to stack."""
        self._items.append(item)
    
    def pop(self) -> Optional[T]:
        """Remove and return top item."""
        if self._items:
            return self._items.pop()
        return None
    
    def peek(self) -> Optional[T]:
        """Return top item without removing."""
        if self._items:
            return self._items[-1]
        return None

# Usage
int_stack: Stack[int] = Stack()
int_stack.push(42)

str_stack: Stack[str] = Stack()
str_stack.push("hello")
```

### Callable Types

```python
from typing import Callable, List, Any

# Function that takes a callback
def process_with_callback(
    data: List[int],
    callback: Callable[[int], str]
) -> List[str]:
    """Process data using callback function."""
    return [callback(item) for item in data]

# Usage
def int_to_str(value: int) -> str:
    return f"Value: {value}"

results = process_with_callback([1, 2, 3], int_to_str)

# Complex callable
TransformFunc = Callable[[Dict[str, Any]], Optional[str]]

def apply_transform(
    items: List[Dict[str, Any]],
    transform: TransformFunc
) -> List[str]:
    """Apply transformation to items."""
    results: List[str] = []
    for item in items:
        result = transform(item)
        if result:
            results.append(result)
    return results
```

## Mypy Configuration

The project uses mypy for static type checking. Configuration is in `mypy.ini`:

```ini
[mypy]
python_version = 3.10
files = src

# Type checking strictness
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
no_implicit_optional = True
strict_optional = True

# Warnings
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True

# Error display
show_error_context = True
show_column_numbers = True
show_error_codes = True
pretty = True
color_output = True
```

## Running Type Checks

### Check Specific File

```bash
source venv/bin/activate
mypy src/exceptions.py --config-file mypy.ini
```

### Check Entire Project

```bash
source venv/bin/activate
mypy src --config-file mypy.ini
```

### Check with Verbose Output

```bash
mypy src --config-file mypy.ini --verbose
```

### Generate Type Coverage Report

```bash
mypy src --config-file mypy.ini --html-report mypy-report
```

## Common Patterns

### Exception Handling

```python
from typing import Optional, Type
from src.exceptions import AntigravityError, APIError

def safe_api_call(
    func: Callable[[], str],
    default: str = "",
    catch: Type[Exception] = APIError
) -> str:
    """Safely call API function with error handling."""
    try:
        return func()
    except catch as e:
        logger.error(f"API call failed: {e}")
        return default
```

### Configuration

```python
from typing import Dict, Any, Optional
from pathlib import Path

def load_config(
    config_path: Path,
    defaults: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Load configuration from file."""
    config: Dict[str, Any] = defaults or {}
    
    if config_path.exists():
        with open(config_path) as f:
            loaded = json.load(f)
            config.update(loaded)
    
    return config
```

### Data Processing

```python
from typing import List, Dict, Any, Optional, Callable

def filter_and_transform(
    items: List[Dict[str, Any]],
    filter_func: Optional[Callable[[Dict[str, Any]], bool]] = None,
    transform_func: Optional[Callable[[Dict[str, Any]], Any]] = None
) -> List[Any]:
    """Filter and transform list of items."""
    result: List[Any] = items
    
    if filter_func:
        result = [item for item in result if filter_func(item)]
    
    if transform_func:
        result = [transform_func(item) for item in result]
    
    return result
```

## Best Practices

### 1. Always Type Function Signatures

```python
# ✅ Good
def calculate_total(prices: List[float], tax_rate: float) -> float:
    subtotal = sum(prices)
    return subtotal * (1 + tax_rate)

# ❌ Avoid
def calculate_total(prices, tax_rate):
    subtotal = sum(prices)
    return subtotal * (1 + tax_rate)
```

### 2. Use Optional for Nullable Values

```python
# ✅ Good
def find_user(user_id: str) -> Optional[Dict[str, Any]]:
    user = database.get(user_id)
    return user if user else None

# ❌ Avoid - unclear if None is possible
def find_user(user_id: str) -> Dict[str, Any]:
    return database.get(user_id)
```

### 3. Be Specific with Collection Types

```python
# ✅ Good - specific types
def process_scores(scores: Dict[str, int]) -> List[int]:
    return sorted(scores.values())

# ❌ Avoid - too generic
def process_scores(scores: dict) -> list:
    return sorted(scores.values())
```

### 4. Use Type Aliases for Complex Types

```python
# ✅ Good - readable
from typing import Dict, List, Any

UserData = Dict[str, Any]
UserList = List[UserData]

def filter_users(users: UserList, active_only: bool) -> UserList:
    if active_only:
        return [u for u in users if u.get("active")]
    return users

# ❌ Avoid - hard to read
def filter_users(
    users: List[Dict[str, Any]],
    active_only: bool
) -> List[Dict[str, Any]]:
    ...
```

### 5. Document Complex Types

```python
from typing import TypedDict, List

class UserProfile(TypedDict):
    """User profile data structure."""
    id: str
    name: str
    email: str
    age: int
    active: bool

def create_user(profile: UserProfile) -> str:
    """Create user from profile data."""
    # Type checker knows exact structure
    return profile["id"]
```

## Handling Third-Party Libraries

### Libraries Without Type Stubs

```python
# In mypy.ini
[mypy-some_library.*]
ignore_missing_imports = True
```

### Installing Type Stubs

```bash
# Many popular libraries have type stubs
pip install types-requests
pip install types-redis
```

## Migration Strategy

### Gradual Typing

1. **Start with new code**: All new code should have type hints
2. **Add to modified code**: Add hints when modifying existing code
3. **Prioritize public APIs**: Type public functions first
4. **Use `# type: ignore` sparingly**: Only when absolutely necessary

### Example Migration

```python
# Before
def process_data(data, config):
    result = []
    for item in data:
        if item.get("active"):
            result.append(transform(item, config))
    return result

# After
from typing import List, Dict, Any

def process_data(
    data: List[Dict[str, Any]],
    config: Dict[str, str]
) -> List[Any]:
    result: List[Any] = []
    for item in data:
        if item.get("active"):
            result.append(transform(item, config))
    return result
```

## Troubleshooting

### Common Mypy Errors

#### Error: Function is missing a type annotation

```python
# Problem
def process(**kwargs):
    ...

# Solution
from typing import Any

def process(**kwargs: Any) -> None:
    ...
```

#### Error: Incompatible return value type

```python
# Problem
def get_count() -> int:
    return None  # Error!

# Solution
from typing import Optional

def get_count() -> Optional[int]:
    return None  # OK
```

#### Error: Argument has incompatible type

```python
# Problem
def add_numbers(a: int, b: int) -> int:
    return a + b

result = add_numbers("1", "2")  # Error!

# Solution
result = add_numbers(int("1"), int("2"))  # OK
```

## Reference

- **Type hints module:** All files in `src/`
- **Mypy configuration:** `mypy.ini`
- **Python typing docs:** https://docs.python.org/3/library/typing.html
- **Mypy documentation:** https://mypy.readthedocs.io/
