# Unified Economics CBT Platform

This platform transforms fragmented JSON exam data into a unified, static Computer-Based Test (CBT) interface. It uses a two-step process: standardizing exam data into a universal JSON schema, and building an interactive static HTML site using Jinja2 and Vanilla JS.

## Project Features
1. **Interactive Categorized Dashboard**: Easily select tests grouped by Exam Name and Year. 
2. **Customizable Durations**: Before starting a test, students can override the default time limits directly from the dashboard.
3. **Advanced Time Tracking**: Records the exact number of seconds spent on each individual question during the attempt.
4. **CSV Analytics Export**: Generates an exhaustive CSV report on test completion detailing selected options, correct answers, and time spent on a per-question basis.

## Project Architecture
1. **Migration Utilities (`scripts/` & `utils/`)**: Scripts to convert specific exam formats (like JNU answer keys) into the universal schema.
2. **Schema Validator (`utils/migrate_base.py`)**: Ensures all generated JSONs have `exam_name`, `exam_year`, `exam_title`, `duration`, and properly structured `questions`.
3. **Static CLI Builder (`build.py`)**: Finds all `standardized_*.json` files in `data/standardized/`, processes the `templates/cbt_template.html` and `templates/dashboard_template.html`, and outputs a final website in the `dist/` folder.

## Setup

Ensure you have Python 3.12+ installed. This project uses `uv` for dependency management.

```bash
# Install dependencies (Jinja2 and Pytest)
uv sync
# OR manually: uv pip install jinja2 pytest
```

## How to Operate

### Step 1: Migrate Exam Data
First, you need to migrate raw exam data into the standardized format inside `data/standardized/`. We currently have migrators for JNU, CUET, DSE, and IIT JAM.

You can run the migrators via the shell:
```bash
node scripts/migrate_iit_jam.js
node scripts/migrate_dse.js
python scripts/migrate_all.py
```

### Step 2: Build the Static Site
Once you have `standardized_*.json` files in your `data/standardized/` directory, build the static site:

```bash
python build.py
```
This script will:
- Parse all `standardized_*.json` files.
- Render them into `cbt_template.html`.
- Save the standalone exam HTML files to the `dist/` directory.
- Generate an interactive categorized `dist/index.html` dashboard using `dashboard_template.html`.

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
