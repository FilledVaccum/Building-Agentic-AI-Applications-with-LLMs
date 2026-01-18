"""
Validation Script for Modules 5-8
Checks completeness and accuracy of all module content
"""

import os
import json
from pathlib import Path

def validate_module(module_num):
    """Validate a single module's content"""
    print(f"\n{'='*70}")
    print(f"VALIDATING MODULE {module_num}")
    print(f"{'='*70}")
    
    issues = []
    
    # Check README
    readme_path = f"content/modules/MODULE_{module_num:02d}_README.md"
    if not os.path.exists(readme_path):
        issues.append(f"Missing {readme_path}")
    else:
        print(f"✓ Found {readme_path}")
        with open(readme_path, 'r') as f:
            content = f.read()
            if len(content) < 1000:
                issues.append(f"{readme_path} seems too short ({len(content)} chars)")
    
    # Check theoretical content
    theory_path = f"content/modules/module_{module_num:02d}_theoretical_content.md"
    if not os.path.exists(theory_path):
        issues.append(f"Missing {theory_path}")
    else:
        print(f"✓ Found {theory_path}")
        with open(theory_path, 'r') as f:
            content = f.read()
            if len(content) < 5000:
                issues.append(f"{theory_path} seems too short ({len(content)} chars)")
    
    # Check module JSON
    json_files = list(Path("content/modules").glob(f"module_{module_num:02d}_*.json"))
    if not json_files:
        issues.append(f"Missing module_{module_num:02d}_*.json")
    else:
        for json_file in json_files:
            print(f"✓ Found {json_file}")
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    # Validate structure
                    required_fields = ['module_id', 'title', 'duration_hours', 'exam_topics', 'learning_objectives']
                    for field in required_fields:
                        if field not in data:
                            issues.append(f"{json_file} missing field: {field}")
            except json.JSONDecodeError as e:
                issues.append(f"{json_file} has invalid JSON: {e}")
    
    # Check quiz
    quiz_path = f"content/assessments/quiz_{module_num:02d}_*.json"
    quiz_files = list(Path("content/assessments").glob(f"quiz_{module_num:02d}_*.json"))
    if not quiz_files:
        issues.append(f"Missing quiz for module {module_num}")
    else:
        for quiz_file in quiz_files:
            print(f"✓ Found {quiz_file}")
            try:
                with open(quiz_file, 'r') as f:
                    data = json.load(f)
                    questions = data.get('questions', [])
                    if len(questions) < 5:
                        issues.append(f"{quiz_file} has only {len(questions)} questions (should be 5-10)")
                    elif len(questions) > 10:
                        issues.append(f"{quiz_file} has {len(questions)} questions (should be 5-10)")
                    else:
                        print(f"  ✓ Quiz has {len(questions)} questions")
            except json.JSONDecodeError as e:
                issues.append(f"{quiz_file} has invalid JSON: {e}")
    
    # Check lab files
    lab_files = [
        f"content/labs/lab_{module_num:02d}_*.json",
        f"content/labs/lab_{module_num:02d}_setup_instructions.md",
        f"content/labs/lab_{module_num:02d}_implementation_guide.md",
        f"content/labs/lab_{module_num:02d}_starter.py",
        f"content/labs/lab_{module_num:02d}_solution.py",
        f"content/labs/lab_{module_num:02d}_troubleshooting.md"
    ]
    
    for pattern in lab_files:
        matching_files = list(Path(".").glob(pattern))
        if not matching_files:
            issues.append(f"Missing lab file: {pattern}")
        else:
            for file in matching_files:
                print(f"✓ Found {file}")
                # Check file size
                size = os.path.getsize(file)
                if size < 500:
                    issues.append(f"{file} seems too small ({size} bytes)")
    
    return issues

def check_nvidia_platform_integration(module_num):
    """Check that NVIDIA platform is mentioned in module content"""
    print(f"\nChecking NVIDIA platform integration for Module {module_num}...")
    
    theory_path = f"content/modules/module_{module_num:02d}_theoretical_content.md"
    if os.path.exists(theory_path):
        with open(theory_path, 'r') as f:
            content = f.read().lower()
            nvidia_mentions = content.count('nvidia')
            nim_mentions = content.count('nim')
            
            if nvidia_mentions > 0:
                print(f"  ✓ NVIDIA mentioned {nvidia_mentions} times")
            else:
                print(f"  ⚠ NVIDIA not mentioned in theoretical content")
            
            if module_num == 6:  # Module 6 should have extensive NVIDIA content
                if nvidia_mentions < 20:
                    print(f"  ⚠ Module 6 should have more NVIDIA mentions (found {nvidia_mentions})")

def validate_code_examples(module_num):
    """Check that code examples are present and valid Python"""
    print(f"\nChecking code examples for Module {module_num}...")
    
    starter_path = f"content/labs/lab_{module_num:02d}_starter.py"
    solution_path = f"content/labs/lab_{module_num:02d}_solution.py"
    
    for path in [starter_path, solution_path]:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    code = f.read()
                    # Basic syntax check
                    compile(code, path, 'exec')
                    print(f"  ✓ {path} has valid Python syntax")
                    
                    # Check for TODOs in starter
                    if 'starter' in path:
                        todo_count = code.count('TODO')
                        if todo_count > 0:
                            print(f"  ✓ Starter has {todo_count} TODO items")
                        else:
                            print(f"  ⚠ Starter has no TODO items")
                    
                    # Check for imports
                    if 'import' not in code:
                        print(f"  ⚠ {path} has no imports")
                    
            except SyntaxError as e:
                print(f"  ✗ {path} has syntax error: {e}")

def main():
    print("="*70)
    print("MODULE 5-8 VALIDATION REPORT")
    print("="*70)
    
    all_issues = {}
    
    # Validate each module
    for module_num in [5, 6, 7, 8]:
        issues = validate_module(module_num)
        check_nvidia_platform_integration(module_num)
        validate_code_examples(module_num)
        
        if issues:
            all_issues[f"Module {module_num}"] = issues
    
    # Summary
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    
    if not all_issues:
        print("\n✓ ALL MODULES PASSED VALIDATION!")
        print("\nAll required files are present and properly formatted.")
    else:
        print("\n⚠ ISSUES FOUND:\n")
        for module, issues in all_issues.items():
            print(f"\n{module}:")
            for issue in issues:
                print(f"  - {issue}")
    
    # Check overall structure
    print("\n" + "="*70)
    print("OVERALL STRUCTURE CHECK")
    print("="*70)
    
    required_dirs = [
        "content/modules",
        "content/labs",
        "content/assessments"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            file_count = len(list(Path(dir_path).glob("*")))
            print(f"✓ {dir_path} exists with {file_count} files")
        else:
            print(f"✗ {dir_path} missing")
    
    print("\n" + "="*70)
    print("VALIDATION COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()
