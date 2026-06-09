from pathlib import Path
from .migrate_base import validate_standard_schema
import json

def migrate_jnu(input_path: str | Path, output_path: str | Path, exam_name: str = "JNU Economics", exam_year: int = 2020, exam_title: str = "JNU Exam", duration: int = 180, positive_marks: int = 4, negative_marks: int = 1) -> None:
    with open(input_path, 'r') as f:
        raw_data = json.load(f)
    questions = []
    valid_items = [(k, v) for k, v in raw_data.items() if str(k).isdigit()]
    for q_num, correct_opt in sorted(valid_items, key=lambda x: int(x[0])):
        questions.append({
            "question_number": int(q_num),
            "question_text": "",
            "options": ["A", "B", "C", "D"],
            "correct_option": correct_opt,
            "positive_marks": positive_marks,
            "negative_marks": negative_marks
        })
    standard_data = {
        "exam_name": exam_name,
        "exam_year": exam_year,
        "exam_title": exam_title,
        "duration": duration,
        "questions": questions
    }
    validate_standard_schema(standard_data)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(standard_data, f, indent=4)
