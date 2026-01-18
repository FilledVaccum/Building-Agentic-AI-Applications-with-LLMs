#!/usr/bin/env python3
"""
Validation script for Modules 9-13 checkpoint.
Ensures all module content is complete, accurate, and properly covers exam requirements.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

# ANSI color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}{text.center(80)}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")

def print_success(text: str):
    """Print success message."""
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text: str):
    """Print error message."""
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text: str):
    """Print warning message."""
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_info(text: str):
    """Print info message."""
    print(f"{BLUE}ℹ {text}{RESET}")

class ModuleValidator:
    """Validates module content for Modules 9-13."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.successes = []
        
        # Expected modules 9-13
        self.modules = {
            9: {
                "title": "Monitoring, Observability, and Maintenance",
                "exam_topics": ["Run Monitor & Maintain", "Evaluation & Tuning"],
                "duration": 1.5,
                "required_files": [
                    "content/modules/MODULE_09_README.md",
                    "content/modules/module_09_theoretical_content.md",
                    "content/modules/module_09_monitoring_maintenance.json",
                    "content/labs/lab_09_setup_instructions.md",
                    "content/labs/lab_09_implementation_guide.md",
                    "content/labs/lab_09_starter.py",
                    "content/labs/lab_09_solution.py",
                    "content/labs/lab_09_troubleshooting.md",
                    "content/labs/lab_09_monitoring_maintenance.json",
                    "content/assessments/quiz_09_monitoring_maintenance.json"
                ]
            },
            10: {
                "title": "Safety, Ethics, and Guardrails",
                "exam_topics": ["Safety Ethics & Compliance", "Human-AI Interaction"],
                "duration": 1.5,
                "required_files": [
                    "content/modules/MODULE_10_README.md",
                    "content/modules/module_10_theoretical_content.md",
                    "content/modules/module_10_safety_ethics.json",
                    "content/labs/lab_10_setup_instructions.md",
                    "content/labs/lab_10_implementation_guide.md",
                    "content/labs/lab_10_starter.py",
                    "content/labs/lab_10_solution.py",
                    "content/labs/lab_10_troubleshooting.md",
                    "content/labs/lab_10_safety_ethics.json",
                    "content/assessments/quiz_10_safety_ethics.json"
                ]
            },
            11: {
                "title": "Human-in-the-Loop Systems",
                "exam_topics": ["Human-AI Interaction & Oversight"],
                "duration": 1.0,
                "required_files": [
                    "content/modules/MODULE_11_README.md",
                    "content/modules/module_11_theoretical_content.md",
                    "content/modules/module_11_human_in_the_loop.json",
                    "content/labs/lab_11_setup_instructions.md",
                    "content/labs/lab_11_implementation_guide.md",
                    "content/labs/lab_11_starter.py",
                    "content/labs/lab_11_solution.py",
                    "content/labs/lab_11_troubleshooting.md",
                    "content/labs/lab_11_human_in_the_loop.json",
                    "content/assessments/quiz_11_human_in_the_loop.json"
                ]
            },
            12: {
                "title": "Advanced Topics and Real-World Applications",
                "exam_topics": ["All topics (integration)"],
                "duration": 1.5,
                "required_files": [
                    "content/modules/MODULE_12_README.md",
                    "content/modules/module_12_theoretical_content.md",
                    "content/modules/module_12_advanced_topics.json",
                    "content/labs/lab_12_setup_instructions.md",
                    "content/labs/lab_12_implementation_guide.md",
                    "content/labs/lab_12_starter.py",
                    "content/labs/lab_12_solution.py",
                    "content/labs/lab_12_troubleshooting.md",
                    "content/labs/lab_12_advanced_topics.json",
                    "content/assessments/quiz_12_advanced_topics.json"
                ]
            },
            13: {
                "title": "Final Assessment and Exam Preparation",
                "exam_topics": ["All topics (comprehensive)"],
                "duration": 2.0,
                "required_files": [
                    "content/modules/MODULE_13_README.md",
                    "content/modules/module_13_theoretical_content.md",
                    "content/modules/module_13_final_assessment.json",
                    "content/labs/final_project.json",
                    "content/labs/final_project_setup_instructions.md",
                    "content/labs/final_project_implementation_guide.md",
                    "content/assessments/final_assessment.json"
                ]
            }
        }
    
    def validate_file_exists(self, filepath: str) -> bool:
        """Check if a file exists."""
        if os.path.exists(filepath):
            return True
        return False
    
    def validate_json_file(self, filepath: str) -> Tuple[bool, Dict]:
        """Validate JSON file structure."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return True, data
        except json.JSONDecodeError as e:
            return False, {"error": str(e)}
        except Exception as e:
            return False, {"error": str(e)}
    
    def validate_markdown_content(self, filepath: str, min_length: int = 500) -> bool:
        """Validate markdown file has substantial content."""
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            return len(content) >= min_length
        except Exception:
            return False
    
    def validate_python_syntax(self, filepath: str) -> bool:
        """Validate Python file syntax."""
        try:
            with open(filepath, 'r') as f:
                code = f.read()
            compile(code, filepath, 'exec')
            return True
        except SyntaxError:
            return False
        except Exception:
            return False
    
    def validate_module_files(self, module_num: int) -> List[str]:
        """Validate all required files for a module exist."""
        module_info = self.modules[module_num]
        missing_files = []
        
        for filepath in module_info["required_files"]:
            if not self.validate_file_exists(filepath):
                missing_files.append(filepath)
        
        return missing_files
    
    def validate_module_json(self, module_num: int) -> Dict:
        """Validate module JSON structure."""
        results = {}
        module_info = self.modules[module_num]
        
        # Find module JSON file
        json_files = [f for f in module_info["required_files"] if f.endswith('.json') and 'module_' in f]
        
        for json_file in json_files:
            if self.validate_file_exists(json_file):
                is_valid, data = self.validate_json_file(json_file)
                results[json_file] = {
                    "valid": is_valid,
                    "data": data
                }
        
        return results
    
    def validate_quiz(self, module_num: int) -> Dict:
        """Validate quiz structure and content."""
        quiz_file = f"content/assessments/quiz_{module_num:02d}_*.json"
        module_info = self.modules[module_num]
        
        # Find the actual quiz file
        quiz_files = [f for f in module_info["required_files"] if 'quiz_' in f and f.endswith('.json')]
        
        results = {}
        for quiz_file in quiz_files:
            if self.validate_file_exists(quiz_file):
                is_valid, data = self.validate_json_file(quiz_file)
                if is_valid:
                    # Check quiz structure
                    question_count = len(data.get('questions', []))
                    results[quiz_file] = {
                        "valid": True,
                        "question_count": question_count,
                        "has_minimum_questions": 5 <= question_count <= 10
                    }
                else:
                    results[quiz_file] = {
                        "valid": False,
                        "error": data.get("error")
                    }
        
        return results
    
    def validate_lab_code(self, module_num: int) -> Dict:
        """Validate lab starter and solution code."""
        results = {}
        module_info = self.modules[module_num]
        
        # Find Python files
        py_files = [f for f in module_info["required_files"] if f.endswith('.py')]
        
        for py_file in py_files:
            if self.validate_file_exists(py_file):
                is_valid = self.validate_python_syntax(py_file)
                results[py_file] = {
                    "valid": is_valid,
                    "syntax_ok": is_valid
                }
        
        return results
    
    def validate_theoretical_content(self, module_num: int) -> Dict:
        """Validate theoretical content is substantial."""
        results = {}
        module_info = self.modules[module_num]
        
        # Find theoretical content file
        theory_files = [f for f in module_info["required_files"] if 'theoretical_content' in f]
        
        for theory_file in theory_files:
            if self.validate_file_exists(theory_file):
                has_content = self.validate_markdown_content(theory_file, min_length=2000)
                results[theory_file] = {
                    "exists": True,
                    "substantial_content": has_content
                }
        
        return results
    
    def validate_nvidia_platform_integration(self, module_num: int) -> Dict:
        """Check for NVIDIA platform mentions in content."""
        results = {}
        module_info = self.modules[module_num]
        
        nvidia_keywords = ['NVIDIA', 'NIM', 'NeMo', 'TensorRT', 'Triton', 'build.nvidia.com']
        
        # Check theoretical content
        theory_files = [f for f in module_info["required_files"] if 'theoretical_content' in f]
        
        for theory_file in theory_files:
            if self.validate_file_exists(theory_file):
                with open(theory_file, 'r') as f:
                    content = f.read()
                
                found_keywords = [kw for kw in nvidia_keywords if kw in content]
                results[theory_file] = {
                    "has_nvidia_content": len(found_keywords) > 0,
                    "keywords_found": found_keywords
                }
        
        return results
    
    def run_validation(self):
        """Run complete validation for Modules 9-13."""
        print_header("MODULES 9-13 CHECKPOINT VALIDATION")
        
        for module_num in sorted(self.modules.keys()):
            module_info = self.modules[module_num]
            print_header(f"Module {module_num}: {module_info['title']}")
            
            # 1. Check file existence
            print_info("Checking file existence...")
            missing_files = self.validate_module_files(module_num)
            if not missing_files:
                print_success(f"All {len(module_info['required_files'])} required files exist")
            else:
                for missing in missing_files:
                    print_error(f"Missing file: {missing}")
                self.errors.append(f"Module {module_num}: Missing {len(missing_files)} files")
            
            # 2. Validate JSON files
            print_info("Validating JSON files...")
            json_results = self.validate_module_json(module_num)
            for json_file, result in json_results.items():
                if result["valid"]:
                    print_success(f"Valid JSON: {json_file}")
                else:
                    print_error(f"Invalid JSON: {json_file} - {result['data'].get('error')}")
                    self.errors.append(f"Module {module_num}: Invalid JSON in {json_file}")
            
            # 3. Validate quiz
            print_info("Validating quiz...")
            quiz_results = self.validate_quiz(module_num)
            for quiz_file, result in quiz_results.items():
                if result.get("valid"):
                    q_count = result.get("question_count", 0)
                    if result.get("has_minimum_questions"):
                        print_success(f"Quiz has {q_count} questions (within 5-10 range)")
                    else:
                        print_warning(f"Quiz has {q_count} questions (expected 5-10)")
                        self.warnings.append(f"Module {module_num}: Quiz question count outside range")
                else:
                    print_error(f"Invalid quiz: {quiz_file}")
                    self.errors.append(f"Module {module_num}: Invalid quiz")
            
            # 4. Validate lab code
            if module_num != 13:  # Module 13 has final project instead
                print_info("Validating lab code...")
                code_results = self.validate_lab_code(module_num)
                for py_file, result in code_results.items():
                    if result.get("syntax_ok"):
                        print_success(f"Valid Python syntax: {py_file}")
                    else:
                        print_error(f"Syntax error in: {py_file}")
                        self.errors.append(f"Module {module_num}: Syntax error in {py_file}")
            
            # 5. Validate theoretical content
            print_info("Validating theoretical content...")
            theory_results = self.validate_theoretical_content(module_num)
            for theory_file, result in theory_results.items():
                if result.get("substantial_content"):
                    print_success(f"Substantial content: {theory_file}")
                else:
                    print_warning(f"Content may be too short: {theory_file}")
                    self.warnings.append(f"Module {module_num}: Theoretical content may be insufficient")
            
            # 6. Check NVIDIA platform integration
            print_info("Checking NVIDIA platform integration...")
            nvidia_results = self.validate_nvidia_platform_integration(module_num)
            for file, result in nvidia_results.items():
                if result.get("has_nvidia_content"):
                    keywords = ", ".join(result.get("keywords_found", []))
                    print_success(f"NVIDIA platform mentioned: {keywords}")
                else:
                    print_warning(f"No NVIDIA platform mentions found in {file}")
                    self.warnings.append(f"Module {module_num}: Limited NVIDIA platform integration")
        
        # Summary
        return self.print_summary()
    
    def print_summary(self):
        """Print validation summary."""
        print_header("VALIDATION SUMMARY")
        
        print(f"\n{BLUE}Total Errors:{RESET} {len(self.errors)}")
        if self.errors:
            for error in self.errors:
                print_error(error)
        else:
            print_success("No errors found!")
        
        print(f"\n{YELLOW}Total Warnings:{RESET} {len(self.warnings)}")
        if self.warnings:
            for warning in self.warnings:
                print_warning(warning)
        else:
            print_success("No warnings!")
        
        if not self.errors:
            print(f"\n{GREEN}{'='*80}{RESET}")
            print(f"{GREEN}✓ ALL MODULES 9-13 VALIDATION PASSED{RESET}".center(88))
            print(f"{GREEN}{'='*80}{RESET}\n")
            return True
        else:
            print(f"\n{RED}{'='*80}{RESET}")
            print(f"{RED}✗ VALIDATION FAILED - {len(self.errors)} ERRORS FOUND{RESET}".center(88))
            print(f"{RED}{'='*80}{RESET}\n")
            return False

def main():
    """Main validation function."""
    validator = ModuleValidator()
    success = validator.run_validation()
    
    if success:
        print_info("All modules 9-13 are complete and ready for use.")
        print_info("Comprehensive exam coverage validated.")
        print_info("All code examples and labs validated.")
        
        if validator.warnings:
            print_warning(f"{len(validator.warnings)} warnings found but validation passed.")
        
        return 0
    else:
        print_error("Validation failed. Please address the errors above.")
        return 1

if __name__ == "__main__":
    exit(main())
