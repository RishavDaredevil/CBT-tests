# CBT Platform UX and Analytics Enhancements Design

## 1. Purpose
Enhance the aspirant's experience by providing a categorized, interactive entry dashboard, allowing custom test durations, tracking the time spent on individual questions, and allowing users to export their detailed performance metrics as a CSV upon test completion.

## 2. Architecture & Schema
- **Universal Schema Extension**: The standard JSON schema will be expanded to require `exam_name` (e.g., "JNU Economics") and `exam_year` (e.g., 2020) at the root level, alongside the existing `exam_title`.
- **Dashboard Separation**: `build.py` will no longer inline the index HTML. It will process a new `dashboard_template.html` (Jinja2) to render the categorized catalog.

## 3. Dashboard UI
- A clean, Vanilla JS driven interface embedded in `dashboard_template.html`.
- **Components**:
  - `Exam Name` Dropdown: Populated with unique `exam_name` values parsed during the build.
  - `Exam Year` Dropdown: Populated dynamically based on the selected `Exam Name`.
  - `Custom Duration` Number Input: Pre-filled with the default duration of the selected exam, allowing user overrides.
  - `Start Test` Button: Constructs a URL string like `[slugified_filename].html?duration=[custom_mins]` and redirects the user.

## 4. Test Interface Updates
- **Duration Parsing**: `cbt_template.html` will parse the `window.location.search` for the `duration` parameter. If valid, it overrides the default JSON duration before the timer initializes.
- **Time Tracking**: 
  - A `timeSpentPerQuestion` dictionary mapping question indices to seconds.
  - The existing 1-second interval timer will add 1 second to `timeSpentPerQuestion[currentQuestionIndex]`.
  - State persists across question navigation.

## 5. CSV Export
- On test submission (`submitExam()` function in `cbt_template.html`), the system will:
  - Generate a CSV payload with columns: `Serial Number`, `Attempt Status` (Attempted/Unattempted), `Selected Option`, `Correct Option`, `Time Taken (seconds)`.
  - Convert the string to a Blob.
  - Create a temporary `<a>` element with the `download` attribute set to `exam_results.csv` and trigger a click event to download the file.

## 6. Migration & Build adjustments
- `utils/migrate_base.py`: Update the required keys check.
- `utils/migrate_jnu.py`: Update function signature and output payload.
- Re-run test and migration logic to ensure JSON data is compliant before building the new UI.
