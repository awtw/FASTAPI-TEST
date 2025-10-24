# How to do version control on database schema with Alembic

1. Outside the container, run the following command to generate the Alembic environment:

```bash
alembic init test-alembic
```

Alembic will create a directory named `test-alembic` with the following structure, and a file `alembic.ini`:

```
test-alembic
├── README
├── env.py
├── script.py.mako
└── versions
```

2. Modify the `alembic.ini` file to point to the database URL (let it blank):

```
sqlalchemy.url = 
```

3. Modify the `env.py` file to point to the database URL:

```python
import os
from logging.config import fileConfig

from alembic import context

from src.database.database import get_database_url
from src.database.models import Base

DB_HOST = os.getenv("DB_HOST", "mysql")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "admin1234")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "template_db")

config = context.config
config.set_main_option("sqlalchemy.url", get_database_url(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME))
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
```

4. Inside the container, run the following command to create the first migration:

```bash
alembic revision --autogenerate -m "Initial migration"
```

Alembic will create a file inside the `versions` directory.

5. Inside the container, run the following command to apply the migration:

```bash
alembic upgrade head
```
