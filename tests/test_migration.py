import json
import pytest
from utils.migrate_base import validate_standard_schema

def test_validate_standard_schema_fails_on_invalid():
    invalid_data = {"exam_title": "Test"}
    with pytest.raises(ValueError):
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
