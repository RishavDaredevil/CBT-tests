import json
import glob
from pathlib import Path
from utils.migrate_base import validate_standard_schema

def write_standard(name, year, title, duration, questions):
    out = {
        "exam_name": name, 
        "exam_year": year, 
        "exam_title": title, 
        "duration": duration, 
        "questions": questions
    }
    validate_standard_schema(out)
    with open(f"data/standardized/standardized_{name.replace(' ', '_')}_{year}.json", "w") as f:
        json.dump(out, f, indent=4)

def migrate_isi_pea():
    with open("All_CBT_tests/ISI/ISI PEA extracted questions.json") as f:
        isi_pea = json.load(f)
    with open("All_CBT_tests/ISI/Answer key.json") as f:
        isi_answers = json.load(f)
    for paper in isi_pea:
        year = paper["year"]
        qs = []
        for i, q in enumerate(paper["questions"]):
            ans = isi_answers.get(str(year), {}).get("answers", {}).get(str(i+1), "Unknown")
            options = [q["options"].get(k, "") for k in ["A", "B", "C", "D"]]
            qs.append({
                "question_number": i+1,
                "question_text": q["text"],
                "options": options,
                "correct_option": ans,
                "positive_marks": 4,
                "negative_marks": 1
            })
        write_standard("ISI PEA", year, f"ISI PEA {year}", 120, qs)

def migrate_cuet():
    with open("All_CBT_tests/CUET/Cuet_unified_questions_sorted.json") as f:
        cuet = json.load(f)
    for paper in cuet:
        year = paper["year"]
        qs = []
        for i, q in enumerate(paper["questions"]):
            opts = q.get("options", {})
            if isinstance(opts, dict):
                options = list(opts.values())
                options = options + [""] * max(0, 4 - len(options))
                options = options[:4]
            elif isinstance(opts, list):
                # pad with empty strings if < 4
                options = opts + [""] * max(0, 4 - len(opts))
                options = options[:4] # ensure exactly 4 or so, though schema might not restrict.
            else:
                options = ["A", "B", "C", "D"]
            qs.append({
                "question_number": i+1,
                "question_text": q.get("text", ""),
                "options": options,
                "correct_option": q.get("correct_option", "Unknown") or "Unknown",
                "positive_marks": 4,
                "negative_marks": 1
            })
        write_standard("CUET", year, f"CUET {year}", 120, qs)

if __name__ == "__main__":
    try:
        migrate_isi_pea()
        print("Migrated ISI PEA")
    except Exception as e:
        print("Failed ISI PEA", e)
        
    try:
        migrate_cuet()
        print("Migrated CUET")
    except Exception as e:
        print("Failed CUET", e)
