import os
import re
import json
from pathlib import Path
from jinja2 import Template
from collections import defaultdict

def build_site(data_dir: str | Path, dist_dir: str | Path, template_path: str | Path, dashboard_path: str | Path = "dashboard_template.html") -> None:
    Path(dist_dir).mkdir(parents=True, exist_ok=True)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = Template(f.read())
    
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        dash_template = Template(f.read())
        
    json_files = Path(data_dir).rglob("standardized_*.json")
    catalog = defaultdict(list)
    
    for json_file in json_files:
        if "dist" in json_file.parts:
            continue
            
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        exam_title = data.get("exam_title", "Unknown Exam")
        exam_name = data.get("exam_name", "Unknown")
        exam_year = data.get("exam_year", 0)
        duration = data.get("duration", 180)
        
        slugified_title = re.sub(r'[^a-zA-Z0-9_\-]', '_', exam_title)
        filename = f"{slugified_title}.html"
        
        rendered_html = template.render(
            exam_title=exam_title,
            exam_json_data=json.dumps(data)
        )
        with open(os.path.join(dist_dir, filename), 'w', encoding='utf-8') as f:
            f.write(rendered_html)
            
        catalog[exam_name].append({
            "year": exam_year,
            "duration": duration,
            "link": filename
        })
        
    for name in catalog:
        catalog[name].sort(key=lambda x: x["year"], reverse=True)
        
    dash_html = dash_template.render(catalog_json=json.dumps(catalog))
    with open(os.path.join(dist_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(dash_html)

if __name__ == "__main__":
    build_site(".", "dist", "cbt_template.html", "dashboard_template.html")
