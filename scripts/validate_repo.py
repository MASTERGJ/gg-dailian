#!/usr/bin/env python3
"""Repository Validation Script — validates skill packages follow conventions."""
import os
import sys
import yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIRS = [BASE]

def check_skill(path):
    skill_md = os.path.join(path, "SKILL.md")
    if not os.path.exists(skill_md):
        print(f"FAIL: no SKILL.md in {path}")
        return False
    
    with open(skill_md) as f:
        content = f.read()
    
    if not content.startswith("---"):
        print(f"FAIL: no YAML frontmatter in {skill_md}")
        return False
    
    try:
        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1])
        if "name" not in frontmatter:
            print(f"FAIL: frontmatter missing 'name'")
            return False
    except Exception as e:
        print(f"FAIL: frontmatter parse error: {e}")
        return False
    
    for d in ["references", "templates", "examples", "evals"]:
        if not os.path.isdir(os.path.join(path, d)):
            print(f"WARN: missing {d}/")
    
    print(f"OK: {os.path.basename(path)}")
    return True

def main():
    errors = 0
    for skill in SKILL_DIRS:
        if not check_skill(skill):
            errors += 1
    
    if errors == 0:
        print("\nOK: repository")
    else:
        print(f"\nFAIL: {errors} skill(s)")
        sys.exit(1)

if __name__ == "__main__":
    main()
