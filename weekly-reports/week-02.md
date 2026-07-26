# Week 02 Report

## Date

20 July - 26 July

## Main Focus

- Python fundamentals
- Virtual environment
- Functions
- Data structures
- File handling
- JSON persistence
- Basic CLI development
- Git workflow practice

## What I Completed

- [x] Created and practiced using a Python virtual environment
- [x] Reviewed variables and basic data types
- [x] Practiced conditionals and loops
- [x] Practiced functions, parameters, arguments, and return values
- [x] Compared `print()` and `return`
- [x] Practiced lists, dictionaries, tuples, and sets
- [x] Modeled OpsDesk ticket data
- [x] Read and wrote text files
- [x] Serialized Python data to JSON
- [x] Loaded JSON data back into Python
- [x] Handled missing and invalid files
- [x] Built a basic OpsDesk Ticket CLI
- [x] Added input validation and JSON persistence
- [x] Added basic isolated persistence checks
- [x] Updated project notes and README files

## What I Learned

- Variables store values with different data types.
- `None`, `0`, and an empty string represent different states.
- Condition order affects backend business rules.
- `for` loops process collections, while `while` loops continue based on a condition.
- Functions reduce duplication and separate responsibilities.
- Parameters are defined inputs, while arguments are actual values.
- `print()` displays a value, while `return` sends a value to the calling code.
- Lists, dictionaries, tuples, and sets solve different data-modeling problems.
- Dictionaries and lists can model JSON-like backend records.
- The `with` statement safely manages file resources.
- JSON serialization provides simple local persistence.
- Valid JSON does not automatically mean valid application data.
- Specific exceptions are safer than a bare `except`.
- Main guards prevent a CLI from starting when its module is imported.
- Function parameters improve flexibility and testability.
- Temporary directories protect real data during persistence checks.

## Code I Wrote

### Python Fundamentals Practice

- Variables and data types
- Conditionals
- `for` and `while` loops
- Counters and membership checks

### Function Practice

- Function definitions and calls
- Parameters and arguments
- Return values
- SLA calculation
- Basic behavior checks

### Data Structure Practice

- Lists
- Dictionaries
- Tuples
- Sets
- Lists of dictionaries
- OpsDesk ticket modeling

### File Handling Practice

- Text file reading and writing
- Append mode
- JSON serialization and deserialization
- `FileNotFoundError`
- Basic file checks

### OpsDesk Ticket CLI

- Interactive menu
- Ticket listing
- Ticket creation
- Title validation
- Priority validation and normalization
- JSON persistence
- Missing and invalid JSON handling
- Import-safe main guard
- Temporary-directory persistence checks

## Problems I Faced

- I had difficulty remembering some Python syntax.
- I initially treated `snake_case` as a function name instead of a naming style.
- I confused showing a value with returning a value.
- I reused variable names in ways that could overwrite earlier values.
- I created small indentation, whitespace, and newline problems.
- I passed `ensure_ascii` to `json.load()` even though it belongs to JSON writing.
- I compared a function object instead of the value returned by the function.
- I saw that valid JSON can still have the wrong application structure.
- I learned that normalization and validation can belong to different functions.

## How I Solved Them

- I used similar examples before completing the real exercises.
- I tested multiple condition branches manually.
- I used meaningful function and variable names.
- I reviewed staged changes before committing.
- I used `git diff --check` to find whitespace problems.
- I read traceback messages to identify unsupported function arguments.
- I separated function calls from function references.
- I added explicit validation and controlled error handling.
- I used temporary directories to avoid modifying real test data.

## GitHub Outputs

- Commits created during 20-26 July: 10
- Total commits labeled `week-02`: 13
- Pull requests: 0
- Basic `assert` checks: 22
- CLI test functions: 2
- Main Week 02 projects:
  - `projects/week-02-python-fundamentals/`
  - `projects/week-02-ticket-cli/`

## Interview Questions I Can Answer

- What is the difference between a parameter and an argument?
- What is the difference between `print()` and `return`?
- What is the difference between a list and a tuple?
- When should a set be used?
- What does `None` represent?
- Why should files be opened with `with`?
- What is the difference between `"w"` and `"a"` modes?
- What are serialization and deserialization?
- What is the difference between `FileNotFoundError` and `JSONDecodeError`?
- Why should internal file paths not be exposed to users?
- Why is `if __name__ == "__main__":` useful?
- Why should file paths be passed as function parameters?
- What does a persistence round-trip test verify?

## Next Week Goals

- Practice list comprehensions
- Add type hints to Python functions
- Practice raising and handling exceptions
- Review modules and imports
- Start using `pytest`
- Learn basic dependency management
- Introduce Ruff for linting
- Practice Git branches and pull requests
- Use `curl` for HTTP requests
- Review remaining HTTP fundamentals
- Prepare for Week 04 OOP and clean-code work
