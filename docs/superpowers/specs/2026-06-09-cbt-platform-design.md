# CBT Platform Design

## 1. Purpose
Transform a fragmented set of examination directories into a homogeneous, single-UI static web platform for Economics Master's entrance exams. The platform will use a single Jinja template and standardized JSON data to build self-contained HTML files, connected via a central index dashboard.

## 2. Architecture
The architecture is based on a static site generation approach.
- **Universal Schema:** A standardized JSON format representing the exam data.
- **Vanilla JS Template:** `cbt_template.html` serves as the Jinja template that accepts the injected JSON.
- **Python CLI Builder:** Iterates over standardized JSON files, injects them into the template, and outputs static HTML files to a `dist/` directory.

## 3. Data Standardization
A two-step build process will be implemented.
- **Step 1 (Migration):** We will create dedicated python scripts to migrate the various existing JSON formats (CUET, DSE, ISI, IIT JAM, JNU) into a new `standardized_<exam>.json` format.
- **Universal Schema Structure:**
  - `exam_title`: String
  - `duration`: Integer (in minutes)
  - `questions`: Array of objects
    - `question_text`: String (Can be empty for JNU)
    - `options`: Array of strings
    - `correct_option`: String (representing the correct index or letter)
    - `positive_marks`: Number
    - `negative_marks`: Number

## 4. The JNU "OMR Mode"
The frontend template already includes logic for OMR mode. When a JNU JSON file is injected and its `question_text` fields are empty/missing, the UI will fall back to displaying only the options (A, B, C, D) alongside the question number, allowing aspirants to use a physical or PDF question paper.

## 5. Build Process & Dashboard
- The `main.py` CLI script will:
  1. Parse all `standardized_*.json` files.
  2. Use Jinja2 to render `cbt_template.html` with the data.
  3. Save the resulting files into `dist/`.
  4. Generate a static `dist/index.html` dashboard with links to each generated exam.