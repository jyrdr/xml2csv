#!/usr/bin/env python3
"""Convert CVAT annotations.xml to CSV for viewing in LibreOffice Calc.

Usage: python3 retouch_annotations_xml2csv.py <input.xml> <output.csv>
"""

import argparse
import csv
import xml.etree.ElementTree as ET


def main():
    parser = argparse.ArgumentParser(description="Convert CVAT annotations XML to CSV")
    parser.add_argument("input", help="Path to annotations.xml")
    parser.add_argument("output", help="Path to output .csv file")
    args = parser.parse_args()

    tree = ET.parse(args.input)
    root = tree.getroot()

    rows = []
    for image in root.iter("image"):
        row = {
            "id": image.get("id", ""),
            "name": image.get("name", ""),
            "width": image.get("width", ""),
            "height": image.get("height", ""),
            "tag_label": "",
            "tag_source": "",
            "retouch_quality": "",
            "hallucination_severity": "",
        }
        tag = image.find("tag")
        if tag is not None:
            row["tag_label"] = tag.get("label", "")
            row["tag_source"] = tag.get("source", "")
            for attr in tag.findall("attribute"):
                name = attr.get("name", "")
                if name in row:
                    row[name] = attr.text or ""
        rows.append(row)

    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
