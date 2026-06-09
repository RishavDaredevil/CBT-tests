import json
import pytest
from utils.migrate_base import validate_standard_schema

def test_validate_standard_schema_fails_on_missing_root_key():
    invalid_data = {"exam_title": "Test"}
    with pytest.raises(ValueError, match="Missing required key: duration"):
        validate_standard_schema(invalid_data)

def test_validate_standard_schema_fails_on_non_list_questions():
    invalid_data = {"exam_title": "Test", "duration": 120, "questions": "not a list"}
    with pytest.raises(ValueError, match="questions must be a list"):
        validate_standard_schema(invalid_data)

def test_validate_standard_schema_fails_on_non_dict_question():
    invalid_data = {"exam_title": "Test", "duration": 120, "questions": ["not a dict"]}
    with pytest.raises(ValueError, match="Question at index 0 is not a dictionary"):
        validate_standard_schema(invalid_data)

def test_validate_standard_schema_fails_on_missing_question_key():
    invalid_data = {
        "exam_title": "Test",
        "duration": 120,
        "questions": [{"options": ["A", "B", "C", "D"]}]
    }
    with pytest.raises(ValueError, match="Question at index 0 missing key: correct_option"):
        validate_standard_schema(invalid_data)

def test_validate_standard_schema_passes():
    valid_data = {
        "exam_title": "Test Exam",
        "duration": 120,
        "questions": [
            {
                "question_text": "Sample Q?",
                "options": ["A", "B", "C", "D"],
                "correct_option": "A",
                "positive_marks": 4,
                "negative_marks": 1
            }
        ]
    }
    assert validate_standard_schema(valid_data) is True
