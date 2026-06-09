const fs = require('fs');
const path = require('path');

const jamDir = path.join(__dirname, 'All_CBT_tests', 'IIT_JAM', 'IIT JAM papers');
const files = fs.readdirSync(jamDir).filter(f => f.endsWith('.html'));

files.forEach(file => {
    const yearMatch = file.match(/(\d{4})/);
    if (!yearMatch) return;
    const year = parseInt(yearMatch[1]);
    
    const filePath = path.join(jamDir, file);
    let content = fs.readFileSync(filePath, 'utf-8');
    
    // Extract questionsData
    const startMarker = 'const questionsData = [';
    let startIndex = content.indexOf(startMarker);
    if (startIndex === -1) return;
    
    // We need to find the matching closing bracket '];'
    // A simple regex might not work due to nested brackets, but let's try finding the end of the array assignment.
    // The structure usually is:
    // const questionsData = [ ... ];
    // We can extract everything between startIndex and the first "];" at the same indentation, but let's use a simpler approach.
    // Let's just find the substring and evaluate it.
    
    // We can replace window, React, etc if needed, but since it's just an array definition, we can use eval.
    let arrayContent = content.substring(startIndex + startMarker.length - 1);
    let endIndex = arrayContent.indexOf('];\n');
    if (endIndex === -1) {
        endIndex = arrayContent.indexOf('];\r');
    }
    if (endIndex === -1) {
        endIndex = arrayContent.indexOf('];');
    }
    
    let jsCode = arrayContent.substring(0, endIndex + 1);
    
    let questionsData;
    try {
        // Evaluate the array
        questionsData = eval('(' + jsCode + ')');
    } catch (e) {
        console.error('Error evaluating JSON for', file, e);
        return;
    }
    
    // Map to standardized schema
    const standardizedQs = questionsData.map((q, index) => {
        let options = q.options;
        if (!options || !Array.isArray(options)) {
            options = ["Option A", "Option B", "Option C", "Option D"];
        }
        
        let correctOption = q.correct || "Unknown";
        
        return {
            question_number: index + 1,
            question_text: q.text || "",
            options: options,
            correct_option: correctOption,
            positive_marks: q.marks || 1,
            negative_marks: q.negative || 0
        };
    });
    
    const standardizedData = {
        exam_name: "IIT JAM",
        exam_year: year,
        exam_title: `IIT JAM ${year}`,
        duration: 180, // Default to 180 mins
        questions: standardizedQs
    };
    
    const outputPath = path.join(__dirname, `standardized_IIT_JAM_${year}.json`);
    fs.writeFileSync(outputPath, JSON.stringify(standardizedData, null, 4));
    console.log(`Migrated IIT JAM ${year}`);
});
