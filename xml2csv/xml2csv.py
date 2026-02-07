#!/usr/bin/env python3
"""Convert XML to CSV.

Usage: python3 xml2csv.py <input.xml> <output.csv> --row TAG [--columns TAG ...] [-r]

Each element matching --row becomes a CSV row. The element's XML attributes
are always included as columns. Child elements become additional columns
(tag name → column name, text content → value). Use --columns to limit
which child tags are included, and -r to recurse into all descendants.
"""

import argparse
import csv
import xml.etree.ElementTree as ET


def main():
    parser = argparse.ArgumentParser(description="Convert XML to CSV")
    parser.add_argument("input", help="Path to input XML file")
    parser.add_argument("output", help="Path to output CSV file")
    parser.add_argument("--row", required=True, help="XML tag name whose elements become CSV rows")
    parser.add_argument("--columns", nargs="+", help="Child tag names to include as columns (default: all)")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recurse into all descendants instead of only direct children")
    args = parser.parse_args()

    tree = ET.parse(args.input)
    root = tree.getroot()

    column_filter = set(args.columns) if args.columns else None

    rows = []
    fieldnames = []
    seen_fields = set()

    for element in root.iter(args.row):
        row = {}

        # Row element's XML attributes (always included)
        for key, value in element.attrib.items():
            row[key] = value
            if key not in seen_fields:
                seen_fields.add(key)
                fieldnames.append(key)

        # Child/descendant elements
        children = element.iter() if args.recursive else element
        for child in children:
            if child is element:
                continue
            if column_filter and child.tag not in column_filter:
                continue
            row[child.tag] = child.text or ""
            if child.tag not in seen_fields:
                seen_fields.add(child.tag)
                fieldnames.append(child.tag)

        rows.append(row)

    if not rows:
        print(f"No <{args.row}> elements found.")
        return

    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval="")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
