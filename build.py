import os
import re
import json
from pathlib import Path
from jinja2 import Template

def build_site(data_dir: str | Path, dist_dir: str | Path, template_path: str | Path) -> None:
    Path(dist_dir).mkdir(parents=True, exist_ok=True)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = Template(f.read())
        
    json_files = Path(data_dir).rglob("standardized_*.json")
    
    exam_links = []
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        exam_title = data.get("exam_title", "Unknown Exam")
        slugified_title = re.sub(r'[^a-zA-Z0-9_\-]', '_', exam_title)
        filename = f"{slugified_title}.html"
        
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
