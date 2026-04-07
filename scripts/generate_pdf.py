#!/usr/bin/env python3
"""Generate PDF from HTML proposal using WeasyPrint."""
import os
import sys
import platform


def ensure_library_path():
    """Ensure Homebrew libraries are discoverable on macOS."""
    if platform.system() != "Darwin":
        return

    brew_lib = "/opt/homebrew/lib"
    if not os.path.isdir(brew_lib):
        brew_lib = "/usr/local/lib"
    if not os.path.isdir(brew_lib):
        return

    current = os.environ.get("DYLD_LIBRARY_PATH", "")
    if brew_lib not in current:
        os.environ["DYLD_LIBRARY_PATH"] = f"{brew_lib}:{current}" if current else brew_lib


def main():
    if len(sys.argv) != 3:
        print("Usage: generate_pdf.py <input.html> <output.pdf>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.isfile(input_path):
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    ensure_library_path()

    try:
        from weasyprint import HTML
    except ImportError:
        print("Error: WeasyPrint is not installed.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    except OSError as e:
        print(f"Error: WeasyPrint system dependencies missing: {e}")
        print("On macOS, run: brew install gobject-introspection pango cairo glib")
        sys.exit(1)

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    try:
        HTML(filename=input_path).write_pdf(output_path)
    except Exception as e:
        print(f"Error generating PDF: {e}")
        sys.exit(1)

    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    main()
