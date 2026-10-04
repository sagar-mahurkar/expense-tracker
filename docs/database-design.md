# Database Design

## 1. Entities

### User

Represents a registered application user.

### Category

Represents a user-defined income or expense category.

### Transaction

Represents an individual income or expense transaction.

---

## 2. Relationships

| Relationship | Cardinality |
| --- | --- |
| User → Category | 1:N |
| User → Transaction | 1:N |
| Category → Transaction | 1:N |

---

## 3. Naming Convention

- Database: `snake_case`
- Python / Flask: `snake_case`
- Node.js / TypeScript: `camelCase`
- JavaScript / Vue: `camelCase`

---

## 4. Database

PostgreSQL

---

## 5. Tables

### 5.1 users

| Column | Data Type | Constraints |
| --- | --- | --- |
| `id` | `UUID` | Primary Key |
| `name` | `VARCHAR(100)` | NOT NULL |
| `email` | `VARCHAR(255)` | NOT NULL, UNIQUE |
| `password_hash` | `VARCHAR(255)` | NOT NULL |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL |

---

### 5.2 categories

| Column | Data Type | Constraints |
| --- | --- | --- |
| `id` | `UUID` | Primary Key |
| `user_id` | `UUID` | NOT NULL, FK → `users.id` |
| `name` | `VARCHAR(100)` | NOT NULL |
| `type` | `VARCHAR(10)` | NOT NULL, `income` / `expense` |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL |

#### Constraints for `categories`

```text
UNIQUE (user_id, name, type)
UNIQUE (id, user_id)
CHECK (type IN ('income', 'expense'))
```

The `(id, user_id)` constraint supports the composite foreign key from `transactions`.

---

### 5.3 transactions

| Column | Data Type | Constraints |
| --- | --- | --- |
| `id` | `UUID` | Primary Key |
| `user_id` | `UUID` | NOT NULL, FK → `users.id` |
| `category_id` | `UUID` | NOT NULL |
| `type` | `VARCHAR(10)` | NOT NULL, `income` / `expense` |
| `amount` | `NUMERIC(12,2)` | NOT NULL, > 0 |
| `description` | `VARCHAR(500)` | NULL |
| `transaction_date` | `DATE` | NOT NULL |
| `created_at` | `TIMESTAMPTZ` | NOT NULL |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL |

#### Foreign Keys

```text
FOREIGN KEY (user_id)
REFERENCES users(id)

FOREIGN KEY (category_id, user_id)
REFERENCES categories(id, user_id)
```

This guarantees that a transaction can only use a category belonging to the same user.

#### Constraints for `transactions`

```text
CHECK (type IN ('income', 'expense'))
CHECK (amount > 0)
```

---

## 6. Referential Integrity

### User → Category

A category belongs to exactly one user.

```text
categories.user_id → users.id
```

### User → Transaction

A transaction belongs to exactly one user.

```text
transactions.user_id → users.id
```

### Category → Transaction

A transaction belongs to exactly one category.

The composite foreign key ensures the category belongs to the same user:

```text
transactions(category_id, user_id)
        ↓
categories(id, user_id)
```

---

## 7. Data Type Decisions

### UUID

UUIDs are used as primary keys to provide globally unique identifiers without exposing sequential database IDs.

### NUMERIC(12,2)

Used for monetary amounts instead of floating-point types to avoid precision problems.

### DATE

`transaction_date` represents the business date of the transaction and does not require a timestamp.

### TIMESTAMPTZ

`created_at` and `updated_at` use timezone-aware timestamps.

---

## 8. Referential Actions

| Relationship | ON DELETE |
| --- | --- |
| User → Category | CASCADE |
| User → Transaction | CASCADE |
| Category → Transaction | RESTRICT |

## 9. Indexes

Indexes are created based on the application's query patterns rather than indexing every column.

### 9.1 users

No additional index is required.

The `UNIQUE` constraint on `email` automatically creates a unique index.

### 9.2 categories

No additional index is required.

The unique constraint:

```sql
UNIQUE (user_id, name, type)
```

creates an index that also supports queries filtering by `user_id`.

### 9.3 transactions

Create an index for the most common transaction listing and date-filtering queries:

```sql
CREATE INDEX idx_transactions_user_date
ON transactions(user_id, transaction_date);
```

This supports queries such as:

```sql
WHERE user_id = ?
ORDER BY transaction_date DESC
```

### Indexing Principle

For the MVP, indexes will be kept minimal and based on actual query requirements. Additional indexes may be introduced if future query patterns justify them.

## 10. Referential Update Actions

Primary keys are UUIDs and are treated as immutable identifiers. Therefore, referenced primary keys should not be updated during normal application operation.

| Relationship | ON UPDATE |
| --- | --- |
| User → Category | RESTRICT |
| User → Transaction | RESTRICT |
| Category → Transaction | RESTRICT |

Using `RESTRICT` prevents modification of a referenced primary key when dependent records exist.

## 11. Default Values

### UUID Defaults

Primary keys use database-generated UUIDs:

```sql
DEFAULT gen_random_uuid()
```

This means the application does not need to generate IDs before inserting records.

### Timestamp Defaults

`created_at` is automatically set when a record is created:

```sql
DEFAULT CURRENT_TIMESTAMP
```

`updated_at` is also initialized to the current timestamp:

```sql
DEFAULT CURRENT_TIMESTAMP
```

The application is responsible for updating `updated_at` when a record is modified.

### Summary

| Column | Default |
| --- | --- |
| `id` | `gen_random_uuid()` |
| `created_at` | `CURRENT_TIMESTAMP` |
| `updated_at` | `CURRENT_TIMESTAMP` |
