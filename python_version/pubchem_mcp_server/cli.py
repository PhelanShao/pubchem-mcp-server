#!/usr/bin/env python3
"""
PubChem MCP Command Line Interface

Provides a command line interface for retrieving PubChem compound data.
"""

import argparse
import sys

from .pubchem_api import get_pubchem_data


def main():
    """Main function"""
    # Create argument parser
    parser = argparse.ArgumentParser(description='Retrieve PubChem compound data')
    parser.add_argument('query', help='Compound name or PubChem CID')
    parser.add_argument('--format', '-f', choices=['JSON', 'CSV', 'XYZ'], default='JSON',
                        help='Output format, options: JSON, CSV, or XYZ, default: JSON')
    parser.add_argument('--include-3d', '-3d', action='store_true',
                        help='Whether to include 3D structure information (only valid when format is XYZ)')
    
    # Parse command line arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    # Check if XYZ format requires include_3d parameter
    if args.format.upper() == 'XYZ' and not args.include_3d:
        print("Error: When using XYZ format, the --include-3d parameter must be set to true")
        sys.exit(1)
    
    try:
        # Get PubChem data
        result = get_pubchem_data(args.query, args.format, args.include_3d)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
