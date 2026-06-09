import json
from utils.migrate_jnu import migrate_jnu

def test_migrate_jnu(tmp_path):
    input_file = tmp_path / "JNU_Answer_key.json"
    input_file.write_text(json.dumps({
        "2": "B", "10": "C", "1": "A", "version": "1.0", "metadata": {}
    }))
    
    output_file = tmp_path / "standardized_JNU.json"
    migrate_jnu(str(input_file), str(output_file), "JNU Exam", 2020, "JNU Entrance", 180, 3, 0)
    
    assert output_file.exists()
    data = json.loads(output_file.read_text())
    assert data["exam_name"] == "JNU Exam"
    assert data["exam_year"] == 2020
    assert data["exam_title"] == "JNU Entrance"
    assert data["duration"] == 180
    assert len(data["questions"]) == 3
    
    # Check that sorting works correctly (1, 2, 10)
    assert data["questions"][0]["question_number"] == 1
    assert data["questions"][0]["correct_option"] == "A"
    assert data["questions"][0]["positive_marks"] == 3
    assert data["questions"][0]["negative_marks"] == 0
    
    assert data["questions"][1]["question_number"] == 2
    assert data["questions"][1]["correct_option"] == "B"
    
    assert data["questions"][2]["question_number"] == 10
    assert data["questions"][2]["correct_option"] == "C"
