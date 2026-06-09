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
