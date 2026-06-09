def validate_standard_schema(data: dict) -> bool:
    if not isinstance(data, dict):
        raise ValueError("Root data must be a dictionary")
    required_keys = ["exam_name", "exam_year", "exam_title", "duration", "questions"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key: {key}")
    if not isinstance(data["questions"], list):
        raise ValueError("questions must be a list")
    for i, q in enumerate(data["questions"]):
        if not isinstance(q, dict):
            raise ValueError(f"Question at index {i} must be a dict")
        for q_key in ["question_number", "question_text", "options", "correct_option", "positive_marks", "negative_marks"]:
            if q_key not in q:
                raise ValueError(f"Question at index {i} missing key: {q_key}")
    return True
