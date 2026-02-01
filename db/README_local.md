Setup
-----

1. Create a virtual environment inside the project (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the script:

```bash
python3 CRUD.py
```

Notes
-----
- The script imports `mysql.connector`. The correct package is `mysql-connector-python` (not `mysql`).
- If you see "externally-managed-environment" when running `pip`, use a venv or `pip install --user ...`.
- If you already created a venv named `myenv` in the project root, activate it from the project root with `source myenv/bin/activate`. If you `cd myenv` first, activate with `source bin/activate`.
