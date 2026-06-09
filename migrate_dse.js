const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'All_CBT_tests', 'DSE-CBT', 'DSE_Practice.html');
let content = fs.readFileSync(filePath, 'utf-8');

const startMarker = 'const examsDB = {';
let startIndex = content.indexOf(startMarker);
if (startIndex === -1) {
    console.error("Could not find examsDB");
    process.exit(1);
}

// Extract everything from examsDB to the end, then we will use string manipulation to find the end of the object.
// The DSE html is large.
// The end of examsDB should be right before `const LandingPage = ...` or similar.
const nextConstMarker = 'const LandingPage =';
let endIndex = content.indexOf(nextConstMarker, startIndex);

if (endIndex === -1) {
    console.error("Could not find end of examsDB");
    process.exit(1);
}

// Find the last closing brace before LandingPage
let block = content.substring(startIndex + startMarker.length - 1, endIndex);
let lastBrace = block.lastIndexOf('}');
let jsCode = block.substring(0, lastBrace + 1);

let examsDB;
try {
    examsDB = eval('(' + jsCode + ')');
} catch(e) {
    console.error('Error evaluating JSON for DSE', e);
    process.exit(1);
}

Object.keys(examsDB).forEach(yearKey => {
    const paper = examsDB[yearKey];
    const year = parseInt(paper.year || yearKey);
    
    const standardizedQs = paper.questions.map((q, index) => {
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
            positive_marks: q.marks || 4,
            negative_marks: q.negative || 1
        };
    });
    
    const duration = paper.defaultDuration ? Math.round(paper.defaultDuration / 60) : 120;
    
    const standardizedData = {
        exam_name: "DSE",
        exam_year: year,
        exam_title: `DSE ${year}`,
        duration: duration,
        questions: standardizedQs
    };
    
    const outputPath = path.join(__dirname, `standardized_DSE_${year}.json`);
    fs.writeFileSync(outputPath, JSON.stringify(standardizedData, null, 4));
    console.log(`Migrated DSE ${year}`);
});
