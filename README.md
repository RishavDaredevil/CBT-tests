# Unified Economics CBT Platform

Welcome to the Unified Economics Computer-Based Test (CBT) Platform! This repository hosts a project designed to help economics aspirants practice Previous Year Questions (PYQs) using an interactive, simulated CBT interface. It tracks your attempt statistics and time spent on each question to provide comprehensive insights into your performance.

## Quick Links

- 🎯 **Take a Test:** [https://econ-entrance-cbt-tests.pages.dev/](https://econ-entrance-cbt-tests.pages.dev/)
- 📖 **Doubts & Explanations:** [http://econ-entrance-doubts-and-explanations.pages.dev/](http://econ-entrance-doubts-and-explanations.pages.dev/) *(Contains personal doubts encountered while solving these papers and their explanations. It is highly recommended to refer to this after giving a test).*

## How to Use This Platform

1. **Download the Question Paper**: Due to limitations in displaying complex mathematical equations and formatting across different papers, the interface itself does not display the full question text in all cases. You should use the interface **alongside another device** (or split screen) displaying the actual question paper. You can download the respective PDFs from the `All_test_papers_pdf` folder in this repository.
2. **Attempt the Exam**: Open the [CBT Interface](https://econ-entrance-cbt-tests.pages.dev/), select your exam and year, and use the platform to mark your answers and manage your time just like the real CBT exam.
3. **Download Your Report**: After submitting your exam, click the button on the final dialog box to download a detailed CSV report containing your selected options, correct answers, status, and time taken per question.
4. **Calculate Your Result**: Open the compiled Excel tracker sheets provided in the `Compiled Excel for Calculating results` directory, and paste your attempts from the CSV to evaluate your final score.

---

## Project Architecture & How it Works

The platform functions by transforming fragmented exam data and answer keys into a unified, static website. It relies on a two-step process:

1. **Migration Utilities (`scripts/` & `utils/`)**: Raw exam answer keys and parameters are processed via Python and Node.js migrator scripts. These scripts standardize everything into a universal JSON schema stored in `data/standardized/`.
2. **Static Builder (`build.py`)**: A static site generator script reads the `standardized_*.json` files along with HTML templates (`templates/cbt_template.html` and `templates/dashboard_template.html`) using Jinja2. It then outputs the finalized static frontend into the `dist/` directory.

The frontend itself is built purely with Vanilla JavaScript, HTML, and CSS, ensuring the CBT interface works entirely client-side without needing a backend server for test execution.

---

## Local Development

Ensure you have Python 3.12+ installed. The project uses `uv` for dependency management.

### Setup and Build

```bash
# Install dependencies (Jinja2 and Pytest)
uv sync

# Step 1: Run migrators (if you added new raw data)
node scripts/migrate_iit_jam.js
node scripts/migrate_dse.js
python scripts/migrate_all.py

# Step 2: Build the static site
python build.py
```

### Running the Local Server

When in the root directory, you can start a local development server to test the generated site:

```bash
python3 -m http.server 8000 -d dist
```

Then visit `http://localhost:8000` in your web browser.

### Testing

The project uses Test-Driven Development (TDD) via `pytest` to ensure the structure and logic are correct.

```bash
uv run pytest tests/ -v
```
