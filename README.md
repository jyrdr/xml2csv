# xml2csv

A simple Python CLI tool that converts XML to CSV. No external dependencies — uses only Python 3 stdlib.

## Usage

```bash
python3 xml2csv/xml2csv.py <input.xml> <output.csv> --row TAG [--columns TAG ...] [-r]
```

### Arguments

| Argument | Required | Description |
|---|---|---|
| `input` | yes | Path to input XML file |
| `output` | yes | Path to output CSV file |
| `--row TAG` | yes | XML tag name whose elements become CSV rows |
| `--columns TAG [TAG ...]` | no | Child tag names to include as columns (default: all) |
| `-r` / `--recursive` | no | Recurse into all descendant elements instead of only direct children |

### How columns are determined

For each element matching `--row`:

1. **XML attributes** on the row element are always included as columns (e.g. `<book isbn="123">` → column `isbn`)
2. **Direct child elements** become columns — the tag name is the column name and the text content is the value
3. With `-r`, **all descendants** are included instead of just direct children
4. With `--columns`, only the listed child/descendant tag names are included (row-level attributes are always kept)

Column order follows first appearance across all row elements. Missing values are left empty.

## Examples

Given this XML:

```xml
<library>
  <book isbn="978-0-13-468599-1" year="2019">
    <title>The Pragmatic Programmer</title>
    <author>David Thomas</author>
    <genre>Programming</genre>
  </book>
  <book isbn="978-0-201-63361-0" year="1999">
    <title>Design Patterns</title>
    <author>Gang of Four</author>
  </book>
</library>
```

```bash
# All children as columns
python3 xml2csv/xml2csv.py library.xml books.csv --row book

# Only title and author columns
python3 xml2csv/xml2csv.py library.xml books.csv --row book --columns title author
```
