import json

def validate_standard_schema(data: dict) -> bool:
    required_keys = ["exam_title", "duration", "questions"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key: {key}")
    
    if not isinstance(data["questions"], list):
        raise ValueError("questions must be a list")
        
    for i, q in enumerate(data["questions"]):
        if not isinstance(q, dict):
            raise ValueError(f"Question at index {i} is not a dictionary")
        for q_key in ["options", "correct_option", "positive_marks", "negative_marks"]:
            if q_key not in q:
                raise ValueError(f"Question at index {i} missing key: {q_key}")
    return True
