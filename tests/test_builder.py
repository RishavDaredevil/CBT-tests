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
        "exam_name": "JNU",
        "exam_year": 2020,
        "exam_title": "Test",
        "duration": 120,
        "questions": []
    }))
    
    # Create second mock standard JSON for sorting
    json_path2 = tmp_path / "standardized_Test2.json"
    json_path2.write_text(json.dumps({
        "exam_name": "JNU",
        "exam_year": 2021,
        "exam_title": "Test",
        "duration": 120,
        "questions": []
    }))
    
    # Create mock dashboard template
    dash_path = tmp_path / "dashboard_template.html"
    dash_path.write_text("Catalog: {{ catalog_json | safe }}")
    
    dist_dir = tmp_path / "dist"
    
    build_site(str(tmp_path), str(dist_dir), str(template_path), str(dash_path))
    
    # Check output
    assert dist_dir.exists()
    assert (dist_dir / "Test_2020.html").exists()
    assert (dist_dir / "Test_2021.html").exists()
    assert (dist_dir / "index.html").exists()
    
    html_content = (dist_dir / "Test_2020.html").read_text()
    assert "Title: Test" in html_content
    
    index_content = (dist_dir / "index.html").read_text()
    assert '"JNU"' in index_content
    assert '"year": 2020' in index_content
    assert '"year": 2021' in index_content
    
    # Verify sorting
    catalog_data = json.loads(index_content.replace("Catalog: ", ""))
    assert catalog_data["JNU"][0]["year"] == 2021
    assert catalog_data["JNU"][1]["year"] == 2020
