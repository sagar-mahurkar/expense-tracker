# Testing Strategy

## 1. Testing Approach

The project uses automated API-level testing with pytest.

Testing is focused on:

- Core MVP functionality
- Authentication and authorization
- API validation
- User data isolation
- Critical CRUD and filtering flows

A dedicated PostgreSQL database is used for tests.

## 2. Test Environment

Test database:

```text
expense_tracker_test
```

A separate `TestConfig` is used for testing.

Key decisions:

- `TESTING = True`
- Database initialization is skipped during tests.
- The test database schema is recreated for each test.
- A dedicated JWT secret is used for tests.
- `TestConfig` inherits from the main `Config`.

The repository root remains the VS Code workspace.

Mypy is configured at the repository root:

```toml
[tool.mypy]
mypy_path = ["backend"]
```

## 3. Test Organization

Tests are organized by API area:

```text
backend/tests/
├── conftest.py
├── test_smoke.py
├── test_auth.py
├── test_categories.py
├── test_transactions.py
└── test_summary.py
```

`conftest.py` contains reusable fixtures for the application, client, authentication, categories, and transactions.

## 4. Test Coverage

### Authentication

Tests cover:

- User registration
- User login
- Invalid login
- Protected endpoint authentication

### Categories

Tests cover:

- Create
- List
- Get
- Delete

### Transactions

Tests cover:

- Create
- Get
- Update
- Delete
- Listing
- Type filtering
- Search
- Date filtering
- Pagination
- User isolation

### Summary

Tests cover:

- Overall summary
- Monthly summary
- Empty month
- Invalid month
- Missing parameters

## 5. Test Isolation

Each test starts with a clean database schema.

Reusable fixtures create the required test data for individual tests.

User isolation is explicitly tested to ensure one user cannot access another user's transactions.

## 6. Test Results

Phase 9 completed with:

```text
24 passed
```

The complete test suite was executed successfully.

Final code quality check:

```bash
git diff --check
```

passed without errors.

## 7. Testing Scope

Testing remains MVP-focused.

No additional testing frameworks or unnecessary infrastructure were introduced.

Frontend and end-to-end testing will be added after the frontend and integration phases.
