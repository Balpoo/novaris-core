import os
import re

EXCLUDED_DIRS = {"venv", "__pycache__", ".git", "logs", "backup"}

def clean_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Failed to read {filepath}: {e}")
        return

    fixed = False
    cleaned_lines = []
    pattern = re.compile(r"^\s*[iex]\s{2,}(.*)$")

    for line in lines:
        match = pattern.match(line)
        if match:
            leading_spaces = len(line) - len(line.lstrip())
            fixed_line = " " * leading_spaces + match.group(1).strip() + "\n"
            cleaned_lines.append(fixed_line)
            fixed = True
        else:
            cleaned_lines.append(line)

    if fixed:
        try:
            with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
                f.writelines(cleaned_lines)
            print(f"✅ Fixed: {filepath}")
        except Exception as e:
            print(f"❌ Failed to write {filepath}: {e}")

def walk_and_clean(base_dir):
    for dirpath, dirnames, filenames in os.walk(base_dir):
        # Modify dirnames in-place to skip excluded directories
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]

        for filename in filenames:
            if filename.endswith(".py"):
                clean_file(os.path.join(dirpath, filename))

if __name__ == "__main__":
    walk_and_clean(".")
