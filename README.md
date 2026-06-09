# Unified Economics CBT Platform

This platform transforms fragmented JSON exam data into a unified, static Computer-Based Test (CBT) interface. It uses a two-step process: standardizing exam data into a universal JSON schema, and building a static HTML site using Jinja2.

## Project Architecture
1. **Migration Utilities (`utils/`)**: Scripts to convert specific exam formats (like JNU answer keys) into the universal schema.
2. **Schema Validator (`utils/migrate_base.py`)**: Ensures all generated JSONs have `exam_title`, `duration`, and properly structured `questions`.
3. **Static CLI Builder (`build.py`)**: Finds all `standardized_*.json` files in the repository, injects them into `cbt_template.html`, and outputs a final website in the `dist/` folder.

## Setup

Ensure you have Python 3.12+ installed. This project uses `uv` for dependency management.

```bash
# Install dependencies (Jinja2 and Pytest)
uv sync
# OR manually: uv pip install jinja2 pytest
```

## How to Operate

### Step 1: Migrate Exam Data
First, you need to migrate raw exam data into the standardized format. We currently have a migrator for JNU answer keys.

You can run the migrator in a python shell or write a quick script:
```python
from utils.migrate_jnu import migrate_jnu

# migrate_jnu(input_path, output_path, exam_title, duration, positive_marks, negative_marks)
migrate_jnu("JNU_Answer_key.json", "standardized_JNU_2020.json", "JNU Economics 2020", 180)
```

### Step 2: Build the Static Site
Once you have `standardized_*.json` files in your repository, build the static site:

```bash
python build.py
```
This script will:
- Parse all `standardized_*.json` files.
- Render them into `cbt_template.html`.
- Save the standalone exam HTML files to the `dist/` directory.
- Generate a `dist/index.html` dashboard linking to all your exams.

### Step 3: View the Site
Open the generated dashboard in your browser:
```bash
# On Linux
xdg-open dist/index.html
# On macOS
open dist/index.html
# On Windows
start dist/index.html
```

## Development & Testing

We use Test-Driven Development (TDD) and `pytest` to ensure structural integrity.

```bash
# Run the test suite
uv run pytest tests/ -v
```
