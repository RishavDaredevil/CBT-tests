# CBT Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform fragmented exam directories into a unified, statically built CBT platform using a Jinja template and standardized JSON.

**Architecture:** We will create a two-step build process: a migration step to convert existing exam data (CUET, DSE, ISI, IIT JAM, JNU) into a standardized schema (`standardized_{exam}.json`), followed by a static generation step (`build.py`) that injects these standard JSONs into a Vanilla JS Jinja template (`cbt_template.html`) and creates an `index.html` dashboard.

**Tech Stack:** Python 3 (json, jinja2, pathlib), HTML/CSS/Vanilla JS (Frontend Template).

---

### Task 1: Create the Universal JSON Schema Migrator Template

**Files:**
- Create: `utils/migrate_base.py`
- Test: `tests/test_migration.py`

- [ ] **Step 1: Write the failing test**

```python
import json
import pytest
from utils.migrate_base import validate_standard_schema

def test_validate_standard_schema_fails_on_invalid():
    invalid_data = {"exam_title": "Test"}
    with pytest.raises(ValueError):
        validate_standard_schema(invalid_data)

def test_validate_standard_schema_passes():
    valid_data = {
        "exam_title": "Test Exam",
        "duration": 120,
        "questions": [
            {
                "question_text": "Sample Q?",
                "options": ["A", "B", "C", "D"],
                "correct_option": "A",
                "positive_marks": 4,
                "negative_marks": 1
            }
        ]
    }
    assert validate_standard_schema(valid_data) is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_migration.py -v`
Expected: FAIL with ModuleNotFoundError or ImportError

- [ ] **Step 3: Write minimal implementation**

```python
import json

def validate_standard_schema(data):
    required_keys = ["exam_title", "duration", "questions"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key: {key}")
    
    if not isinstance(data["questions"], list):
        raise ValueError("questions must be a list")
        
    for q in data["questions"]:
        for q_key in ["options", "correct_option", "positive_marks", "negative_marks"]:
            if q_key not in q:
                raise ValueError(f"Question missing key: {q_key}")
    return True
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_migration.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add utils/migrate_base.py tests/test_migration.py
git commit -m "feat: add schema validation utility"
```

### Task 2: Write JNU Data Migrator

**Files:**
- Create: `utils/migrate_jnu.py`
- Modify: None
- Test: `tests/test_migrate_jnu.py`

- [ ] **Step 1: Write the failing test**

```python
import os
import json
from utils.migrate_jnu import migrate_jnu

def test_migrate_jnu(tmp_path):
    # Setup dummy JNU input
    input_file = tmp_path / "JNU_Answer_key.json"
    input_file.write_text(json.dumps({
        "1": "A", "2": "B"
    }))
    
    output_file = tmp_path / "standardized_JNU.json"
    migrate_jnu(str(input_file), str(output_file), "JNU Entrance", 180)
    
    assert output_file.exists()
    data = json.loads(output_file.read_text())
    assert data["exam_title"] == "JNU Entrance"
    assert data["duration"] == 180
    assert len(data["questions"]) == 2
    assert data["questions"][0]["question_text"] == ""
    assert data["questions"][0]["correct_option"] == "A"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_migrate_jnu.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
import json
from .migrate_base import validate_standard_schema

def migrate_jnu(input_path, output_path, exam_title="JNU Exam", duration=180):
    with open(input_path, 'r') as f:
        raw_data = json.load(f)
        
    questions = []
    # Assuming JNU keys are question numbers and values are correct options
    for q_num, correct_opt in raw_data.items():
        questions.append({
            "question_text": "",
            "options": ["A", "B", "C", "D"],
            "correct_option": correct_opt,
            "positive_marks": 4,  # default assumptions
            "negative_marks": 1
        })
        
    standard_data = {
        "exam_title": exam_title,
        "duration": duration,
        "questions": questions
    }
    
    validate_standard_schema(standard_data)
    
    with open(output_path, 'w') as f:
        json.dump(standard_data, f, indent=4)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_migrate_jnu.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add utils/migrate_jnu.py tests/test_migrate_jnu.py
git commit -m "feat: add JNU data migrator"
```

### Task 3: Develop the Static CLI Builder

**Files:**
- Create: `build.py`
- Modify: None
- Test: `tests/test_builder.py`

- [ ] **Step 1: Write the failing test**

```python
import os
import json
from pathlib import Path
from build import build_site

def test_build_site(tmp_path):
    # Create mock template
    template_path = tmp_path / "cbt_template.html"
    template_path.write_text("Title: {{ exam_title }}, Data: {{ exam_json_data | safe }}")
    
    # Create mock standard JSON
    json_path = tmp_path / "standardized_Test.json"
    json_path.write_text(json.dumps({
        "exam_title": "Test",
        "duration": 120,
        "questions": []
    }))
    
    dist_dir = tmp_path / "dist"
    
    build_site(str(tmp_path), str(dist_dir), str(template_path))
    
    # Check output
    assert dist_dir.exists()
    assert (dist_dir / "Test.html").exists()
    assert (dist_dir / "index.html").exists()
    
    html_content = (dist_dir / "Test.html").read_text()
    assert "Title: Test" in html_content
    
    index_content = (dist_dir / "index.html").read_text()
    assert "href=\"Test.html\"" in index_content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_builder.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
import os
import json
import glob
from pathlib import Path
from jinja2 import Template

def build_site(data_dir, dist_dir, template_path):
    Path(dist_dir).mkdir(parents=True, exist_ok=True)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = Template(f.read())
        
    json_files = glob.glob(os.path.join(data_dir, "standardized_*.json"))
    
    exam_links = []
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        exam_title = data.get("exam_title", "Unknown Exam")
        filename = f"{exam_title.replace(' ', '_')}.html"
        
        # Render HTML
        rendered_html = template.render(
            exam_title=exam_title,
            exam_json_data=json.dumps(data)
        )
        
        with open(os.path.join(dist_dir, filename), 'w', encoding='utf-8') as f:
            f.write(rendered_html)
            
        exam_links.append((exam_title, filename))
        
    # Generate index.html
    index_html = "<html><head><title>Dashboard</title></head><body><h1>Exams</h1><ul>\n"
    for title, link in exam_links:
        index_html += f"<li><a href=\"{link}\">{title}</a></li>\n"
    index_html += "</ul></body></html>"
    
    with open(os.path.join(dist_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(index_html)

if __name__ == "__main__":
    build_site(".", "dist", "cbt_template.html")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pip install jinja2 pytest && pytest tests/test_builder.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add build.py tests/test_builder.py
git commit -m "feat: add static site builder using jinja2"
```