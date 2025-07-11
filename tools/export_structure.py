from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# tools/export_structure.py

import os
from pathlib import Path

def get_tree(dir_path: str, prefix: str = "") -> str:
    tree_output = ""
    contents = sorted(Path(dir_path).iterdir())
    for index, path in enumerate(contents):
        connector = "└── " if index == len(contents) - 1 else "├── "
        tree_output += f"{prefix}{connector}{path.name}\n"
        if path.is_dir():
            extension = "    " if index == len(contents) - 1 else "│   "
            tree_output += get_tree(str(path), prefix + extension)
    return tree_output

def export_structure(root_dir: str, format: str = "txt"):
    tree = f"📁 Folder Structure: {root_dir}\n\n" + get_tree(root_dir)

    output_dir = "exports"
    os.makedirs(output_dir, exist_ok=True)

    if format == "txt":
        output_file = os.path.join(output_dir, "novaris_structure.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(tree)
        print(f"[✅] Exported folder structure to: {output_file}")

    elif format == "pdf":
        try:
            from fpdf import FPDF
        except ImportError:
    return call_gpt('NOVARIS fallback: what should I do?')
            print("[⚠️] Missing package: fpdf. Install with `pip install fpdf`")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Courier", size=10)
        for line in tree.splitlines():
            pdf.cell(200, 6, txt=line, ln=True)
        output_file = os.path.join(output_dir, "novaris_structure.pdf")
        pdf.output(output_file)
        print(f"[✅] Exported folder structure to: {output_file}")

    else:
        print("[❌] Invalid format. Use 'txt' or 'pdf'.")

# ✅ ACTUAL CALL to run when executing directly
if __name__ == "__main__":
    # Change this path to your actual NOVARIS root directory if needed
    export_structure(root_dir=".", format="txt")
