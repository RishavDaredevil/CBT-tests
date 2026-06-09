# Project Directive: Unified Economics CBT Platform

## 1. Project Context & Current State
The project is an open-source, Computer-Based Test (CBT) platform for Economics Master's entrance exams (CUET, DSE, IIT JAM, ISI, JNU). 

Currently, the repository (`CBT tests`) contains separate, disjointed environments for each exam. Each directory contains its own isolated HTML files and extracted JSON question banks or answer keys. 

## 2. Core Objective
Transform this fragmented setup into a **homogeneous, single-UI web platform** composed of fully static, self-contained HTML files. Aspirants should land on a unified dashboard, select their target exam, and take the test in a standardized CBT interface. **Under no circumstances should the end-user be required to upload or load JSON files manually.**

## 3. The Architecture Strategy (Static Pre-Compilation)
We will use the existing `./DSE-CBT/DSE_Practice.html` as the architectural baseline to create a Jinja2 template.

A Python-based CLI tool will act as the builder:
1. It will read the standardized JSON data for a specific exam.
2. It will inject (bake) that JSON data directly into the Jinja template (e.g., assigning it to a `const examData = {{ injected_json }};` variable inside the `<script>` tag).
3. It will output a final, standalone `.html` file for each exam year.
4. All final HTML files will be linked together via a static central dashboard (`index.html`).

## 4. The JNU Exception: "OMR Mode"
The CLI must understand a strict structural exception for the JNU examinations. 
* **Constraint:** We do not have the extracted question text for JNU, only the answer keys (e.g., `JNU_Answer_key.json`).
* **Implementation:** When the CLI is building a JNU test, it must trigger a fallback UI state ("OMR Mode"). The interface should not attempt to render question text or images. Instead, it must simply display the question number and the clickable options (A, B, C, D) so the user can record their responses while reading the questions from an external physical or PDF paper. The timer, review status palette, and scoring logic must still function normally based on the answer key.

## 5. Key Milestones for the AI Assistant
When assisting with code generation or debugging, follow these phases:

* **Phase 1: Template Abstraction & Data Baking**
    * Convert `DSE_Practice.html` into a dynamic Jinja template.
    * Ensure the JavaScript is written to accept a fully injected JSON object at build time, with zero client-side file-fetching logic.

* **Phase 2: Handling the JNU UI Variant**
    * Modify the CSS/JS in the template to allow for a graceful "OMR layout" when the injected JSON lacks `question_text` fields. 
    * Ensure the status palette and submission logic don't break when text is missing.

* **Phase 3: Data Standardization**
    * Design a universal JSON schema.
    * Write Python utility scripts to map/migrate the existing JSON files (CUET, ISI, IIT JAM) into this universal schema so the CLI can uniformly inject them into the template.

* **Phase 4: Dashboard & Routing Assembly**
    * Construct the central `index.html` entry point.
    * Build the final Python build script that iterates through the repository, pairs the correct JSON with the template, generates the static HTMLs into a `/dist` folder, and updates the dashboard links.