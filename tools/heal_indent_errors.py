import os
import re


def clean_bad_lines(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    fixed_lines = []
    for line in lines:
        # Fix lines like: i    return call_gpt('...')
        if re.match(r"^\s*[ie]\s+return call_gpt\(", line):
            fixed_lines.append(
                "    return call_gpt('NOVARIS fallback: what should I do?')\n"
            )
        # Fix lines like: e    return ...
        elif re.match(r"^\s*e\s+return ", line):
            indent = " " * (len(line) - len(line.lstrip()))
            fixed_lines.append(
                f"{indent}return call_gpt('Exception occurred. Suggest a solution.')\n"
            )
        else:
            fixed_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(fixed_lines)


def find_and_fix_all():
    print("🩺 Healing malformed 'call_gpt()' indent lines...")
    healed_files = 0
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                if re.search(r"^\s*[ie]\s+return call_gpt", content, re.MULTILINE):
                    clean_bad_lines(path)
                    healed_files += 1
                    print(f"✅ Healed: {path}")
    print(f"🎉 Healing complete. Total files healed: {healed_files}")


if __name__ == "__main__":
    find_and_fix_all()
