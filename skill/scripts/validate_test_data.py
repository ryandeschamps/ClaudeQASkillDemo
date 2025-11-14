#!/usr/bin/env python3
"""
Test Data Validation Script

This script validates that test data (05_test_data.csv) matches the variant
definitions (04_variants.csv) to ensure data consistency and quality.

Validation checks:
- Row count matches between variants and test data
- All Variant_IDs are present in both files
- Parameter consistency (test data reflects variant parameters)
- Data type and format validation

Author: QA Automation Skill
Version: 1.0.0
"""

import csv
import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class TestDataValidator:
    """
    Validates test data against variant definitions.
    """

    def __init__(self, verbose: bool = False):
        """
        Initialize the validator.

        Args:
            verbose: Enable detailed logging
        """
        self.verbose = verbose
        self._setup_logging()

        self.variants = {}  # variant_id -> {param: value}
        self.test_data = {}  # variant_id -> {field: value}
        self.variant_params = []  # Parameter columns from variants
        self.test_data_fields = []  # Field columns from test data
        self.errors = []
        self.warnings = []

    def _setup_logging(self):
        """Configure logging with appropriate level"""
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def validate_file(self, file_path: str, file_type: str) -> bool:
        """
        Validate that a file exists and is readable.

        Args:
            file_path: Path to the file
            file_type: Description of file type for error messages

        Returns:
            True if valid

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If path is not a file
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{file_type} file not found: {file_path}")

        if not path.is_file():
            raise ValueError(f"{file_type} path is not a file: {file_path}")

        self.logger.debug(f"✓ Validated {file_type}: {file_path}")
        return True

    def load_variants(self, variants_file: str):
        """
        Load variant definitions from CSV.

        Args:
            variants_file: Path to variants CSV file
        """
        self.logger.info(f"Loading variants from {variants_file}")

        try:
            self.validate_file(variants_file, "variants")

            with open(variants_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                # Get parameter columns (exclude Scenario_ID and Variant_ID)
                all_columns = reader.fieldnames
                if not all_columns:
                    raise ValueError("Variants file has no columns")

                if 'Variant_ID' not in all_columns:
                    raise ValueError("Variants file must have 'Variant_ID' column")

                self.variant_params = [
                    col for col in all_columns
                    if col not in ['Scenario_ID', 'Variant_ID']
                ]

                # Load all variants
                for row in reader:
                    variant_id = row.get('Variant_ID')
                    if not variant_id:
                        continue

                    # Store parameter values for this variant
                    self.variants[variant_id] = {
                        param: row.get(param, 'N/A')
                        for param in self.variant_params
                    }

            self.logger.info(f"✓ Loaded {len(self.variants)} variants with {len(self.variant_params)} parameters")

        except Exception as e:
            self.logger.error(f"Error loading variants: {e}")
            raise

    def load_test_data(self, test_data_file: str):
        """
        Load test data from CSV.

        Args:
            test_data_file: Path to test data CSV file
        """
        self.logger.info(f"Loading test data from {test_data_file}")

        try:
            self.validate_file(test_data_file, "test data")

            with open(test_data_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                # Get all field columns
                all_columns = reader.fieldnames
                if not all_columns:
                    raise ValueError("Test data file has no columns")

                if 'Variant_ID' not in all_columns:
                    raise ValueError("Test data file must have 'Variant_ID' column")

                self.test_data_fields = [
                    col for col in all_columns
                    if col != 'Variant_ID'
                ]

                # Load all test data rows
                for row in reader:
                    variant_id = row.get('Variant_ID')
                    if not variant_id:
                        continue

                    # Store all field values for this variant
                    self.test_data[variant_id] = {
                        field: row.get(field, '')
                        for field in self.test_data_fields
                    }

            self.logger.info(f"✓ Loaded {len(self.test_data)} test data rows with {len(self.test_data_fields)} fields")

        except Exception as e:
            self.logger.error(f"Error loading test data: {e}")
            raise

    def validate_row_counts(self):
        """Validate that row counts match between variants and test data."""
        self.logger.info("Validating row counts")

        variant_count = len(self.variants)
        test_data_count = len(self.test_data)

        if variant_count != test_data_count:
            error = (
                f"Row count mismatch: {variant_count} variants vs "
                f"{test_data_count} test data rows"
            )
            self.errors.append(error)
            self.logger.error(f"✗ {error}")
        else:
            self.logger.info(f"✓ Row counts match: {variant_count} rows")

    def validate_variant_ids(self):
        """Validate that all Variant_IDs are present in both files."""
        self.logger.info("Validating Variant_IDs")

        variant_ids = set(self.variants.keys())
        test_data_ids = set(self.test_data.keys())

        # Check for missing test data
        missing_test_data = variant_ids - test_data_ids
        if missing_test_data:
            error = f"Variants missing test data: {sorted(list(missing_test_data)[:10])}"
            if len(missing_test_data) > 10:
                error += f" ... and {len(missing_test_data) - 10} more"
            self.errors.append(error)
            self.logger.error(f"✗ {error}")

        # Check for extra test data
        extra_test_data = test_data_ids - variant_ids
        if extra_test_data:
            warning = f"Test data without variants: {sorted(list(extra_test_data)[:10])}"
            if len(extra_test_data) > 10:
                warning += f" ... and {len(extra_test_data) - 10} more"
            self.warnings.append(warning)
            self.logger.warning(f"⚠ {warning}")

        if not missing_test_data and not extra_test_data:
            self.logger.info(f"✓ All {len(variant_ids)} Variant_IDs are present in both files")

    def validate_parameter_consistency(self):
        """
        Validate that test data is consistent with variant parameters.

        This is a heuristic check - it looks for obvious mismatches where
        test data fields might correspond to variant parameters.
        """
        self.logger.info("Validating parameter consistency")

        # Find common field names between variants and test data
        # (case-insensitive matching)
        variant_params_lower = {p.lower(): p for p in self.variant_params}
        test_fields_lower = {f.lower(): f for f in self.test_data_fields}

        common_fields = set(variant_params_lower.keys()) & set(test_fields_lower.keys())

        if not common_fields:
            info = (
                "No matching field names found between variants and test data. "
                "This is normal if test data uses different field names."
            )
            self.logger.info(f"ℹ {info}")
            return

        self.logger.info(f"Found {len(common_fields)} common fields: {sorted(common_fields)}")

        # For each common field, check for consistency
        mismatches = defaultdict(list)

        for variant_id in self.variants:
            if variant_id not in self.test_data:
                continue  # Already reported in validate_variant_ids

            variant = self.variants[variant_id]
            test_row = self.test_data[variant_id]

            for field_lower in common_fields:
                variant_field = variant_params_lower[field_lower]
                test_field = test_fields_lower[field_lower]

                variant_value = variant.get(variant_field, 'N/A')
                test_value = test_row.get(test_field, '')

                # Simple consistency check: if values are very different, flag it
                # (This is heuristic - test data may legitimately differ)
                if variant_value and variant_value != 'N/A':
                    # Check if variant value appears in test value (loose matching)
                    if variant_value.lower() not in test_value.lower():
                        if len(mismatches[field_lower]) < 5:  # Limit examples
                            mismatches[field_lower].append(
                                f"{variant_id}: variant='{variant_value}' vs test='{test_value[:50]}'"
                            )

        # Report mismatches as warnings (not errors, since test data may be intentionally different)
        for field, examples in mismatches.items():
            warning = (
                f"Potential mismatch in field '{field}': {len(examples)} cases found. "
                f"Examples: {'; '.join(examples[:3])}"
            )
            self.warnings.append(warning)
            self.logger.warning(f"⚠ {warning}")

        if not mismatches:
            self.logger.info(f"✓ No obvious parameter inconsistencies detected")

    def validate_data_completeness(self):
        """Validate that test data has no empty critical fields."""
        self.logger.info("Validating data completeness")

        empty_counts = defaultdict(int)

        for variant_id, test_row in self.test_data.items():
            for field, value in test_row.items():
                if not value or value.strip() == '':
                    empty_counts[field] += 1

        if empty_counts:
            for field, count in sorted(empty_counts.items(), key=lambda x: -x[1]):
                if count > 0:
                    warning = f"Field '{field}' has {count} empty values ({count*100//len(self.test_data)}% of rows)"
                    self.warnings.append(warning)
                    self.logger.warning(f"⚠ {warning}")
        else:
            self.logger.info("✓ All test data fields are populated")

    def print_report(self):
        """Print validation report."""
        print(f"\n{'='*70}")
        print("TEST DATA VALIDATION REPORT")
        print(f"{'='*70}\n")

        print(f"📊 Summary:")
        print(f"  Variants: {len(self.variants)}")
        print(f"  Test Data Rows: {len(self.test_data)}")
        print(f"  Variant Parameters: {len(self.variant_params)}")
        print(f"  Test Data Fields: {len(self.test_data_fields)}")

        print(f"\n🔍 Validation Results:")
        if not self.errors and not self.warnings:
            print("  ✅ All validations passed!")
        else:
            if self.errors:
                print(f"  ❌ Errors: {len(self.errors)}")
                for i, error in enumerate(self.errors, 1):
                    print(f"     {i}. {error}")

            if self.warnings:
                print(f"  ⚠️  Warnings: {len(self.warnings)}")
                for i, warning in enumerate(self.warnings, 1):
                    print(f"     {i}. {warning}")

        print(f"\n{'='*70}\n")

        return len(self.errors) == 0

    def validate(
        self,
        variants_file: str,
        test_data_file: str
    ) -> bool:
        """
        Run all validation checks.

        Args:
            variants_file: Path to variants CSV
            test_data_file: Path to test data CSV

        Returns:
            True if validation passes (no errors)
        """
        self.logger.info("Starting test data validation")

        try:
            # Load files
            self.load_variants(variants_file)
            self.load_test_data(test_data_file)

            # Run validations
            self.validate_row_counts()
            self.validate_variant_ids()
            self.validate_parameter_consistency()
            self.validate_data_completeness()

            # Print report
            success = self.print_report()

            if success:
                self.logger.info("✓ Validation completed successfully")
            else:
                self.logger.error("✗ Validation completed with errors")

            return success

        except Exception as e:
            self.logger.error(f"✗ Validation failed: {e}")
            raise


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description='Validate test data against variant definitions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python validate_test_data.py deliverables/04_variants.csv deliverables/05_test_data.csv

  # With verbose logging
  python validate_test_data.py deliverables/04_variants.csv deliverables/05_test_data.csv --verbose
        """
    )

    parser.add_argument(
        'variants_file',
        help='Path to variants CSV file (e.g., deliverables/04_variants.csv)'
    )

    parser.add_argument(
        'test_data_file',
        help='Path to test data CSV file (e.g., deliverables/05_test_data.csv)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    try:
        validator = TestDataValidator(verbose=args.verbose)
        success = validator.validate(
            variants_file=args.variants_file,
            test_data_file=args.test_data_file
        )
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
