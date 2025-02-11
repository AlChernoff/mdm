# Using Alembic for Database Migrations

This guide explains everything you need to know to use Alembic for managing database schema migrations in your project. Alembic is a lightweight and powerful tool for version control of your database schema.

---

## 1. What is Alembic?

**Alembic** is a database migration tool for Python. It is typically used with SQLAlchemy but can work with any database supported by SQLAlchemy, such as PostgreSQL, MySQL, SQLite, and others.

With Alembic, you can:
- Track changes to your database schema over time.
- Apply incremental updates (migrations) to your database.
- Roll back changes if necessary.

---

## 2. Installation

### Using `poetry`:

```bash
poetry install
```

Ensure that **SQLAlchemy** is also installed, as it is required by Alembic.

---

## 3. Alembic Setup

To set up Alembic in your project, perform the following steps:

### Initialize Alembic

Run the following command in your terminal to initialize Alembic:

```bash
alembic init migrations
```

This command creates a folder named `migrations` (or any directory you specify) with the following structure:
```
migrations/
|-- versions/           # Contains versioned migration scripts
|-- env.py              # Main migration configuration file
|-- README.md           # This file
|-- script.py.mako      # Template for new migrations
|-- alembic.ini         # Configuration file for Alembic``` 
```
> **Note**: If the `migrations` folder was already created, you can skip this step. Instead, configure the existing folder as detailed below.

---

## 4. Configure Alembic

1. Open the `alembic.ini` file (found at the project root).
2. Update the `sqlalchemy.url` with your database connection string. For example:

```ini
sqlalchemy.url = postgresql+psycopg2://user:password@localhost:5432/mydatabase
```

Supported databases include PostgreSQL, MySQL, SQLite, Oracle, and more! Modify the URL accordingly.

3. Edit the **`env.py`** file in the `migrations` folder:
    - Inside `env.py`, locate the `target_metadata` variable.
    - Set it to your SQLAlchemy `Base` metadata object to automatically generate migrations from your models:

```python
from my_project.models import Base  # Replace with the path to your models
target_metadata = Base.metadata
```

---

## 5. Creating Migrations

### Create a New Migration Script

To create a new manual migration script, run:

```bash
alembic revision -m "description of the change"
```

- This creates a new file in the `migrations/versions/` directory.
- The file name will include a revision ID and the message you provided, e.g., `migrations/versions/123abcdef_add_users_table.py`.

> **Tip**: The migration script is generated using the `script.py.mako` template.

---

### Auto-generating Migrations (For Declarative Models)

If you're working with SQLAlchemy models, Alembic can auto-generate migrations based on your `Base` metadata:

1. Define or update your database models in your Python code.
2. Run the following command to generate a migration script:

```bash
alembic revision --autogenerate -m "description of the change"
```

- Alembic will inspect your database schema and models, then generate the necessary migration code.

3. Verify the generated script in the `migrations/versions/` folder and make any necessary edits.

---

### Example: Creating a Table

Here’s an example of a migration script that creates a `users` table:

```python
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '1234567890ab'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), nullable=False, unique=True)
    )

def downgrade():
    op.drop_table('users')
```

---

## 6. Applying Migrations to the Database

Migrations must be applied to the database to reflect schema changes. Use one of these commands:

### Upgrade to the Latest Version:
```bash
alembic upgrade head
```

### Upgrade to a Specific Version:
```bash
alembic upgrade <revision-id>
```

### Roll Back (Downgrade) to a Previous Version:
```bash
alembic downgrade -1
```

- The `-1` argument rolls back one migration.
- You can also specify a *revision ID* to downgrade to a specific point in time.

---

## 7. Viewing and Managing Revisions

### Check Current Database Revision:
```bash
alembic current
```

### List All Revisions:
```bash
alembic history
```

### Show Information About a Revision:
```bash
alembic show <revision-id>
```

---

## 8. Common Issues

### No Changes Detected with `--autogenerate`
- Ensure `target_metadata` is correctly configured in the `env.py` file.
- Check that your SQLAlchemy models' `Base.metadata` is in sync with the database.
- Check that models are imported in __init__.py file of relevant model folder  and also in env file.

### Import Errors or Missing Models
- Alembic relies on the Python environment. Ensure the correct paths and dependencies are available when running Alembic (e.g., activate your virtual environment).

---

## 9. Integrating Alembic in Your Code

You can also run Alembic migrations programmatically in Python using its API. Here’s an example:

```python
from alembic.config import Config
from alembic import command

# Create Alembic configuration object
alembic_cfg = Config("alembic.ini")

# Upgrade database to the latest version
command.upgrade(alembic_cfg, "head")
```

---

## 10. Tips for Productivity

1. Always test auto-generated migrations. Double-check the `upgrade()` and `downgrade()` methods in generated scripts.
2. Use meaningful messages when creating revisions (e.g., `add_users_table` instead of `changes`).
3. Use version control (e.g., Git) to track migration files under the `migrations/versions/` directory.
4. For collaborative projects, ensure teammates apply the same migrations when working on the same database.

---

## 11. Learn More

For more details, refer to the [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/).

---