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
