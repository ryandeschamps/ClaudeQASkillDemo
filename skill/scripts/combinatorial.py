import csv
import sys
import itertools

def generate_pairwise_tests(input_file, output_file):
    """
    Generates a pairwise test plan from a CSV file of parameters and variants.

    This is a simplified implementation for demonstration. For complex scenarios,
    a dedicated library like 'allpairspy' would be more robust.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            # Read parameters and their possible values (variants)
            params = {header: [] for header in headers}
            # Read all rows into a list to get columns easily
            rows = list(reader)
            if not rows:
                print("Input CSV file is empty after the header.")
                return

            for i, header in enumerate(headers):
                # Get unique values for each parameter column
                unique_values = sorted(list(set(row[i] for row in rows if len(row) > i)))
                params[header] = unique_values

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    except Exception as e:
        print(f"Error reading or parsing CSV: {e}")
        return

    # Get the list of parameter value lists
    param_lists = list(params.values())
    full_product = list(itertools.product(*param_lists)) # All possible combinations
    
    # Simple pairwise selection logic
    # 1. Start with the first test case
    # 2. For subsequent cases, pick one that covers the most new pairs
    
    if not full_product:
        print("No combinations to generate.")
        return

    uncovered_pairs = set()
    for i in range(len(headers)):
        for j in range(i + 1, len(headers)):
            # Get all pairs of values between two parameter lists
            p1_values = params[headers[i]]
            p2_values = params[headers[j]]
            for v1 in p1_values:
                for v2 in p2_values:
                    uncovered_pairs.add(((headers[i], v1), (headers[j], v2)))

    pairwise_plan = []
    
    while uncovered_pairs:
        best_candidate = None
        best_candidate_covered_count = -1

        for candidate in full_product:
            pairs_in_candidate = set()
            # Generate all pairs present in this candidate test case
            for i in range(len(headers)):
                for j in range(i + 1, len(headers)):
                    pair = ((headers[i], candidate[i]), (headers[j], candidate[j]))
                    if pair in uncovered_pairs:
                        pairs_in_candidate.add(pair)
            
            # If this candidate covers more new pairs, it's our new best
            if len(pairs_in_candidate) > best_candidate_covered_count:
                best_candidate = candidate
                best_candidate_covered_count = len(pairs_in_candidate)
        
        # Add the best candidate to our plan and remove its pairs from the uncovered set
        if best_candidate:
            pairwise_plan.append(best_candidate)
            pairs_to_remove = set()
            for i in range(len(headers)):
                for j in range(i + 1, len(headers)):
                     pairs_to_remove.add(((headers[i], best_candidate[i]), (headers[j], best_candidate[j])))
            uncovered_pairs -= pairs_to_remove
            # Remove from full product to avoid re-evaluating
            full_product.remove(best_candidate)
        else:
            # No more pairs can be covered
            break
            
    # Write the output to a markdown file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Combinatorial Test Execution Plan (Pairwise)\n\n")
        f.write(f"Generated a reduced set of **{len(pairwise_plan)}** test cases to cover all parameter pairs.\n\n")
        # Write table header
        f.write(f"| Test Case | {' | '.join(headers)} |\n")
        f.write(f"|-----------|{'|'.join(['---'] * len(headers))}|\n")
        # Write table rows
        for i, test_case in enumerate(pairwise_plan, 1):
            f.write(f"| {i}         | {' | '.join(test_case)} |\n")
    
    print(f"Successfully generated combinatorial plan at '{output_file}'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python combinatorial.py <input_variants_csv_path>")
        sys.exit(1)
    
    input_csv = sys.argv[1]
    output_md = "deliverables/07_combinatorial_plan.md"
    generate_pairwise_tests(input_csv, output_md)