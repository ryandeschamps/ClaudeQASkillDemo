import csv
import sys
import re
import os

def build_rtm(requirements_files, scenarios_file, output_file):
    """
    Builds a Requirements Traceability Matrix (RTM) by mapping requirement IDs
    to test scenario IDs.
    """
    req_pattern = re.compile(r'\b(REQ[-_]?\d+)\b', re.IGNORECASE)
    scenario_pattern = re.compile(r'\b(TS[-_]?\d+)\b', re.IGNORECASE)

    # Dictionary to store {req_id: [scenario_id_1, scenario_id_2]}
    req_to_scenarios = {}

    # 1. Read all requirement IDs from the requirements files
    all_req_ids = set()
    for req_file in requirements_files:
        try:
            with open(req_file, 'r', encoding='utf-8') as f:
                content = f.read()
                found_ids = req_pattern.findall(content)
                all_req_ids.update([req_id.upper() for req_id in found_ids])
        except FileNotFoundError:
            print(f"Warning: Requirement file '{req_file}' not found. Skipping.")
            continue
        except Exception as e:
            print(f"Warning: Could not read file '{req_file}'. Error: {e}")

    # Initialize the mapping with all found requirement IDs
    for req_id in all_req_ids:
        req_to_scenarios[req_id] = []

    # 2. Read scenarios file and map scenarios to requirements
    # A scenario is assumed to trace to a requirement if the req ID is mentioned
    # in the scenario's description block.
    try:
        with open(scenarios_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Split the content by scenario ID to process each one individually
            scenarios = scenario_pattern.split(content)
            # The pattern returns the delimiter, so we process in chunks
            for i in range(1, len(scenarios), 2):
                scenario_id = scenarios[i].upper()
                scenario_text = scenarios[i+1]
                # Find all requirement IDs mentioned in this scenario's text
                mentioned_reqs = req_pattern.findall(scenario_text)
                for req_id in mentioned_reqs:
                    req_id = req_id.upper()
                    if req_id in req_to_scenarios:
                        req_to_scenarios[req_id].append(scenario_id)
    except FileNotFoundError:
        print(f"Error: Scenarios file '{scenarios_file}' not found.")
        return
    except Exception as e:
        print(f"Error processing scenarios file: {e}")
        return

    # 3. Write the RTM to a CSV file
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Requirement_ID", "Test_Scenario_ID(s)"])
            
            if not req_to_scenarios:
                 writer.writerow(["No requirements found", "N/A"])

            for req_id in sorted(req_to_scenarios.keys()):
                linked_scenarios = ", ".join(sorted(list(set(req_to_scenarios[req_id]))))
                if not linked_scenarios:
                    linked_scenarios = "NOT COVERED"
                writer.writerow([req_id, linked_scenarios])
        
        print(f"Successfully built RTM at '{output_file}'")

    except Exception as e:
        print(f"Error writing RTM to CSV: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python rtm_builder.py <scenarios_file> <req_file_1> [<req_file_2> ...]")
        sys.exit(1)
        
    scenarios_path = sys.argv[1]
    req_paths = sys.argv[2:]
    output_csv = "deliverables/09_rtm.csv"
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    
    build_rtm(req_paths, scenarios_path, output_csv)