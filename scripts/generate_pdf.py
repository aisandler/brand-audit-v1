#!/usr/bin/env python3
"""Generate PDF from HTML proposal using WeasyPrint."""
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: generate_pdf.py <input.html> <output.pdf>")
        sys.exit(1)

    try:
        from weasyprint import HTML
    except ImportError:
        print("Error: WeasyPrint is not installed.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    HTML(filename=input_path).write_pdf(output_path)
    print(f"PDF generated: {output_path}")

if __name__ == "__main__":
    main()
