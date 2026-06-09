import json
from pathlib import Path
import sys
import os

# Ensure utils is in path if not run from root
sys.path.append(str(Path(__file__).parent.parent))

from utils.migrate_base import validate_standard_schema

def migrate_all_jnu():
    input_file = Path("All_CBT_tests/JNU good/JNU q paper ans key json/JNU_Answer_key.json")
    output_dir = Path("data/standardized")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(input_file, "r") as f:
        data = json.load(f)
        
    for year_str, year_data in data.items():
        year = int(year_str)
        answers = year_data.get("answers", {})
        
        questions = []
        # Sort keys numerically to ensure correct order
        valid_items = [(k, v) for k, v in answers.items() if str(k).isdigit()]
        for q_num, correct_opt in sorted(valid_items, key=lambda x: int(x[0])):
            questions.append({
                "question_number": int(q_num),
                "question_text": "", # Dummy text
                "question_type": "MCQ", # Standard JNU is MCQ
                "options": ["A", "B", "C", "D"], # Dummy options
                "correct_option": correct_opt,
                "positive_marks": 4, # Assuming standard 4 marks, could be different but 4 is safe default
                "negative_marks": 1
            })
            
        standard_data = {
            "exam_name": "JNU Economics",
            "exam_year": year,
            "exam_title": f"JNU Economics {year}",
            "duration": 180, # Assuming 3 hours standard
            "questions": questions
        }
        
        validate_standard_schema(standard_data)
        
        output_file = output_dir / f"standardized_JNU_{year}.json"
        with open(output_file, 'w') as f_out:
            json.dump(standard_data, f_out, indent=4)
            
        print(f"Migrated JNU {year} ({len(questions)} questions)")

if __name__ == "__main__":
    migrate_all_jnu()
