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
            
        # Basic keys for all questions
        for q_key in ["question_number", "question_text", "positive_marks", "negative_marks"]:
            if q_key not in q:
                raise ValueError(f"Question at index {i} missing key: {q_key}")
                
        q_type = q.get("question_type", "MCQ")
        
        if q_type == "MCQ":
            if "options" not in q or "correct_option" not in q:
                raise ValueError(f"MCQ at index {i} missing options or correct_option")
        elif q_type == "MSQ":
            if "options" not in q or "correct_options_msq" not in q:
                raise ValueError(f"MSQ at index {i} missing options or correct_options_msq")
        elif q_type == "NAT":
            if "correct_range_nat" not in q:
                raise ValueError(f"NAT at index {i} missing correct_range_nat")
        else:
            raise ValueError(f"Unknown question_type {q_type} at index {i}")

    return True
