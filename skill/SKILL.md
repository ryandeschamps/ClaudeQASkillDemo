name: generate-qa-artifacts-from-requirements
description: >
Generate QA deliverables (scenarios, variants, data, scripts, plan, RTM) from
requirement/specification documents. Use when you have requirements, specs,
user stories or acceptance criteria and need to automate QA artifact generation.
Generate QA Artifacts from Requirements
This skill automates the creation of a full suite of Quality Assurance artifacts based on provided requirements documents.
Instructions
Follow this workflow precisely. Create a deliverables/ directory to store all outputs.
CRITICAL PRINCIPLE: This skill prioritizes EXHAUSTIVE generation first, OPTIMIZATION second. Generate ALL content completely before any reduction happens via combinatorial analysis.

Acknowledge and Prepare:

Confirm you have understood the request.
Ask the user to upload all their requirements and specification documents.
Ask the user if they want to use a custom output directory or use the default `deliverables/` directory.

Once they are provided, handle the output directory:
- **Set OUTPUT_DIR variable**: If user specified a custom directory, use it (e.g., `custom_output/`). Otherwise, use `deliverables/`
- **If OUTPUT_DIR does NOT exist**: Create OUTPUT_DIR and OUTPUT_DIR/06_test_scripts/
- **If OUTPUT_DIR EXISTS**:
  - Ask user: "Output directory 'OUTPUT_DIR' already exists. Options: (1) Overwrite, (2) Use timestamped directory (e.g., OUTPUT_DIR_20251114_225805/), (3) Cancel"
  - Based on user choice:
    - Overwrite: Remove existing OUTPUT_DIR and create fresh directories
    - Timestamped: Create OUTPUT_DIR_YYYYMMDD_HHMMSS/ and update OUTPUT_DIR variable and all subsequent paths
    - Cancel: Stop and wait for user to manually handle the directory

Set expectations: Tell the user this process generates exhaustive content first, then optimizes.
Confirm the final output directory path being used (e.g., "All artifacts will be saved to: deliverables/")


Step 1: Assess Requirements:

Carefully read all the provided requirement documents.
Analyze them for gaps, ambiguities, contradictions, and unstated assumptions.
Synthesize your findings into a markdown file named OUTPUT_DIR/01_requirements_assessment.md.


Step 2: Extract and Number Requirements:

From the source requirement documents, extract and clearly articulate all functional and non-functional requirements.
Assign a unique ID to each requirement in the format: REQ-001, REQ-002, etc.
Group requirements by functional area (e.g., User Management, Data Processing, Security, Performance).

**REQUIRED FORMAT (for rtm_builder.py script consumption):**
```markdown
## [Functional Area Name]
- **REQ-001**: [Clear, concise requirement statement]
- **REQ-002**: [Clear, concise requirement statement]
```
OR
```markdown
| Requirement ID | Description | Priority |
|---------------|-------------|----------|
| REQ-001 | [Requirement statement] | High |
| REQ-002 | [Requirement statement] | Medium |
```

Include both explicit requirements (stated in the document) and implicit requirements (derived from context).
Save to OUTPUT_DIR/00_requirements.md (numbered 00 to appear first in directory listing).
Count and report: State the total number of requirements extracted (e.g., "Extracted 47 requirements").
This document will be used by Step 10 for Requirements Traceability Matrix generation.


Step 3: Extract Entities and Flows:

From the requirements, identify and list all key entities (e.g., user roles, system components, data objects) and the primary user/system flows.
Document these in OUTPUT_DIR/02_entities_and_flows.md.
Count and report: State the number of entities and flows identified.


Step 4: Derive Test Scenarios (EXHAUSTIVE):

Based on the entities and flows, generate an EXHAUSTIVE set of test scenarios.
DO NOT skip scenarios. Cover every requirement, every entity, every flow, every edge case.
Each scenario must follow the user story format: "As a [user role], I want to [perform an action], so that I can [achieve a benefit]."
Assign a unique ID (e.g., TS-001, TS-002) to each scenario.

**REQUIRED FORMAT (for rtm_builder.py script consumption):**
```markdown
### TS-001: [Scenario Title]
As a [user role], I want to [perform an action], so that I can [achieve a benefit].

**Priority**: Critical|High|Medium|Low
**Related Requirements**: REQ-001, REQ-005, REQ-012

[Additional scenario details...]

### TS-002: [Scenario Title]
...
```

**CRITICAL FORMAT REQUIREMENTS:**
- Scenario heading MUST use format: `### TS-XXX: Title`
- Priority field is OPTIONAL but recommended
- **Related Requirements** field is REQUIRED - list all requirement IDs this scenario tests
- Use exact format: `**Related Requirements**: REQ-001, REQ-002` (comma-separated, no line breaks)

Save these to OUTPUT_DIR/03_test_scenarios.md.
VERIFICATION CHECKPOINT: After generating, count the total scenarios and report: "Generated X test scenarios covering Y requirements."
Cross-check: Review OUTPUT_DIR/00_requirements.md to ensure every requirement has at least one scenario. If any are missing, add them now.


Step 5: Define Variants (EXHAUSTIVE):

For EACH AND EVERY scenario from Step 4, identify all parameters that can vary.
Parameters include: user types, input values, data states, system configurations, edge cases, boundary conditions.
Create the COMPLETE EXHAUSTIVE CARTESIAN PRODUCT of these parameters.
DO NOT limit variants. The goal is to capture EVERY possible combination. Optimization happens in Step 8.

**REQUIRED CSV FORMAT (for combinatorial.py script consumption):**

**Column structure:**
1. First column MUST be: `Scenario_ID` (links to TS-XXX from 03_test_scenarios.md)
2. Second column MUST be: `Variant_ID` (format: V001, V002, V003, etc.)
3. Remaining columns: Parameter names (e.g., User_Type, Browser, Input_Validity, Data_State, etc.)

**Example format:**
```csv
Scenario_ID,Variant_ID,User_Type,Input_Validity,Browser,Device,Network_Speed
TS-001,V001,Admin,Valid,Chrome,Desktop,High
TS-001,V002,Admin,Valid,Firefox,Desktop,High
TS-001,V003,Admin,Invalid,Chrome,Mobile,Low
TS-002,V004,Visitor,Valid,Safari,Tablet,Medium
```

**CRITICAL FORMAT REQUIREMENTS:**
- Use exact column names: `Scenario_ID` and `Variant_ID` (case-sensitive)
- Variant IDs MUST be unique across entire file
- Use "N/A" for parameters that don't apply to certain combinations (e.g., payment_method for visitors)
- NO empty cells - use "N/A" instead
- Parameter values should be consistent (e.g., don't mix "Admin" and "Administrator")

Expected scale: For a moderate application, expect 200-1000+ variants.
Output this as a CSV file to OUTPUT_DIR/04_variants.csv.
VERIFICATION CHECKPOINT: After generating, count total variants and report: "Generated X variants across Y scenarios (average Z variants per scenario)."
Spot check: Verify that common scenarios have multiple variants (e.g., TS-001 should have variants for all user types × all input conditions).
Note: Step 8 will use combinatorial analysis to reduce this to an optimal subset (~95% reduction).


Step 6: Create Test Data (EXHAUSTIVE):

For EACH AND EVERY variant in OUTPUT_DIR/04_variants.csv, generate corresponding realistic test data.
DO NOT skip variants. One variant = one data row.
Include the Variant_ID as the first column to maintain traceability.
Save this data in OUTPUT_DIR/05_test_data.csv.
VERIFICATION CHECKPOINT: After generating, verify row count matches OUTPUT_DIR/04_variants.csv and report: "Generated test data for X variants."
Quality check: Ensure data is realistic, valid, and matches the variant parameters.


Step 7: Generate Test Scripts (EXHAUSTIVE - BATCH APPROACH):

CRITICAL: You must generate a test script for EVERY SINGLE SCENARIO from OUTPUT_DIR/03_test_scenarios.md.
DO NOT skip any scenarios. Missing scripts break traceability.

**REQUIRED FORMAT (for rtm_builder.py script consumption):**
- File naming: MUST use format `TS-XXX.txt` where XXX matches scenario ID
- Content format: Use "Given / When / Then" format with clear "Expected Result"
- Save location: OUTPUT_DIR/06_test_scripts/

BATCH PROCESSING STRATEGY (for large scenario counts):

First: Count total scenarios to generate (e.g., "Need to generate 85 test scripts")
Batch 1 (scripts 1-20): Generate TS-001 through TS-020, save all files
Batch 2 (scripts 21-40): Generate TS-021 through TS-040, save all files
Batch 3 (scripts 41-60): Generate TS-041 through TS-060, save all files
Continue until ALL scenarios have scripts
After each batch: Report progress (e.g., "Completed 40/85 test scripts")

VERIFICATION CHECKPOINT:

After completion, perform BOTH quantity and quality checks:

**Quantity Check:**
- List the OUTPUT_DIR/06_test_scripts/ directory
- Count files and verify: "Generated X test scripts for X scenarios - 100% complete"
- If any are missing: Generate the missing scripts immediately before proceeding

**Quality Check (CRITICAL - prevents generic templates):**
- Randomly sample 10-15 scripts (at least 5% of total)
- For each sampled script, verify it has:
  ✓ NO generic placeholders like "scenario NN", "appropriate page", "user/admin", "required action"
  ✓ Specific GIVEN conditions (not "system is in ready state")
  ✓ Specific WHEN actions (not "performs required action")
  ✓ Specific THEN outcomes (not "displays expected result")
  ✓ Concrete test data values (actual names, emails, numbers)
  ✓ Measurable expected results (specific messages, states, redirects)
- If ANY sampled script fails quality check:
  - Identify the affected batch (scripts were generated in batches)
  - Regenerate that entire batch with explicit instruction: "Be specific, no placeholders, use concrete values"
  - Re-sample to verify quality
- Report: "Quality check passed for X/X sampled scripts"


Step 8: Produce Combinatorial Plan (OPTIMIZATION):

NOW is when optimization happens - you have exhaustive content, now reduce it intelligently.
Execute the scripts/combinatorial.py script using the command:

python3 skill/scripts/combinatorial.py OUTPUT_DIR/04_variants.csv --output OUTPUT_DIR/07_combinatorial_plan.md

**IMPORTANT:** Replace OUTPUT_DIR with the actual directory path being used (e.g., `deliverables/` or custom path).

- The script will automatically select an optimal subset of variants from `04_variants.csv` that achieves maximum pairwise coverage.
- This reduces the number of test executions while maintaining comprehensive parameter interaction coverage.
- The output will be saved to `OUTPUT_DIR/07_combinatorial_plan.md`.
- Review the generated plan for coverage statistics and selected variants.
- **Report:** "Combinatorial analysis reduced X variants to Y test cases (Z% reduction) with W% pairwise coverage."
- **Optional flags:**
  - `--mode generate` - Generate new variants instead of selecting from existing ones (not recommended for typical use)
  - `--verbose` - Enable detailed logging
  - `--output <path>` - Specify custom output path (REQUIRED when using custom OUTPUT_DIR)

9. Step 9: Draft Full Test Plan:
- Synthesize all previous outputs into a comprehensive test plan document.
- The plan should include:
- Executive summary with key statistics
- Scope and objectives
- Test approach (exhaustive generation + combinatorial optimization)
- Schedule and resource estimates
- Summary of all test scenarios and variants (both exhaustive and optimized)
- Traceability matrix summary
- Risk assessment
- Save the document as OUTPUT_DIR/08_test_plan.md.

10. Step 10: Build Requirements Traceability Matrix (RTM):

Execute the scripts/rtm_builder.py script using the command:

python3 skill/scripts/rtm_builder.py OUTPUT_DIR/03_test_scenarios.md OUTPUT_DIR/00_requirements.md --test-scripts OUTPUT_DIR/06_test_scripts --gap-report --output OUTPUT_DIR/09_rtm.csv

**IMPORTANT:** Replace OUTPUT_DIR with the actual directory path being used (e.g., `deliverables/` or custom path).

- The script will generate a comprehensive RTM with:
  - Requirement-to-scenario mappings
  - Coverage status and statistics
  - Test script availability tracking
  - Gap analysis (uncovered requirements, orphaned scenarios)
- The output will be saved to `OUTPUT_DIR/09_rtm.csv`.
- Gap report (if --gap-report flag used) will be saved to `OUTPUT_DIR/09_rtm_gap_report.md`.
- Review the summary statistics and address any coverage gaps.
- **Report:** "RTM shows X% requirement coverage with Y uncovered requirements and Z orphaned scenarios."
- **Optional flags:**
  - `--gap-report` - Generate detailed gap analysis report (recommended)
  - `--output <path>` - Specify custom output path (REQUIRED when using custom OUTPUT_DIR)
  - `--verbose` - Enable detailed logging

**Expected RTM Output Format:**
```csv
Requirement_ID,Requirement_Description,Priority,Test_Scenario_IDs,Test_Script_Available,Coverage_Status,Notes
REQ-001,Users shall be able to log in...,N/A,"TS-007, TS-009, TS-017",Yes,Covered,
REQ-002,Password reset functionality...,High,"TS-013, TS-014",Yes,Covered,
```

11. Completion and Summary:
- List all files in OUTPUT_DIR directory with file sizes
- Provide a comprehensive summary with key metrics:
- Total requirements extracted
- Total test scenarios generated
- Total variants created (exhaustive)
- Optimized test case count (from combinatorial analysis)
- Reduction percentage achieved
- Requirements coverage percentage
- Test scripts completion status
- Notify the user that all QA artifacts have been generated and are available in the OUTPUT_DIR directory.
- Confirm the final output directory path (e.g., "All artifacts saved to: deliverables/")
- Final verification: Confirm no gaps or missing artifacts.