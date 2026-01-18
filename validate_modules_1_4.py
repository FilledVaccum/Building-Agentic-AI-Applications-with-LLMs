#!/usr/bin/env python3
"""
Checkpoint Validation Script for Modules 1-4
Validates completeness, accuracy, and NVIDIA platform integration
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any

class ModuleValidator:
    """Validates module content and structure"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.successes = []
        
    def validate_module(self, module_num: int) -> Dict[str, Any]:
        """Validate a complete module"""
        print(f"\n{'='*60}")
        print(f"Validating Module {module_num}")
        print(f"{'='*60}")
        
        results = {
            'module_num': module_num,
            'checks': []
        }
        
        # Check module JSON
        results['checks'].append(self._check_module_json(module_num))
        
        # Check theoretical content
        results['checks'].append(self._check_theoretical_content(module_num))
        
        # Check lab files
        results['checks'].append(self._check_lab_files(module_num))
        
        # Check quiz
        results['checks'].append(self._check_quiz(module_num))
        
        # Check NVIDIA integration
        results['checks'].append(self._check_nvidia_integration(module_num))
        
        return results
    
    def _check_module_json(self, module_num: int) -> Dict[str, Any]:
        """Check module JSON file exists and is valid"""
        check_name = f"Module {module_num} JSON"
        
        # Map module numbers to file names
        file_map = {
            1: "module_01_fundamentals.json",
            2: "module_02_structured_output.json",
            3: "module_03_retrieval.json",
            4: "module_04_multi_agent.json"
        }
        
        file_path = f"content/modules/{file_map[module_num]}"
        
        if not os.path.exists(file_path):
            return {'check': check_name, 'status': 'FAIL', 'message': f'File not found: {file_path}'}
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Validate required fields
            required_fields = ['module_id', 'title', 'duration_hours', 'learning_objectives']
            missing = [f for f in required_fields if f not in data]
            
            if missing:
                return {'check': check_name, 'status': 'FAIL', 'message': f'Missing fields: {missing}'}
            
            # Check learning objectives
            if not data['learning_objectives'] or len(data['learning_objectives']) < 4:
                return {'check': check_name, 'status': 'WARN', 'message': 'Less than 4 learning objectives'}
            
            return {'check': check_name, 'status': 'PASS', 'message': f'Valid with {len(data["learning_objectives"])} objectives'}
            
        except json.JSONDecodeError as e:
            return {'check': check_name, 'status': 'FAIL', 'message': f'Invalid JSON: {e}'}
        except Exception as e:
            return {'check': check_name, 'status': 'FAIL', 'message': f'Error: {e}'}
    
    def _check_theoretical_content(self, module_num: int) -> Dict[str, Any]:
        """Check theoretical content file"""
        check_name = f"Module {module_num} Theoretical Content"
        
        file_path = f"content/modules/module_0{module_num}_theoretical_content.md"
        
        if not os.path.exists(file_path):
            return {'check': check_name, 'status': 'FAIL', 'message': f'File not found: {file_path}'}
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check minimum length
            if len(content) < 5000:
                return {'check': check_name, 'status': 'WARN', 'message': f'Content seems short ({len(content)} chars)'}
            
            # Check for key sections
            required_sections = ['##', 'Overview', 'Learning Objectives']
            missing_sections = [s for s in required_sections if s not in content]
            
            if missing_sections:
                return {'check': check_name, 'status': 'WARN', 'message': f'May be missing sections: {missing_sections}'}
            
            return {'check': check_name, 'status': 'PASS', 'message': f'{len(content)} characters, well-structured'}
            
        except Exception as e:
            return {'check': check_name, 'status': 'FAIL', 'message': f'Error: {e}'}
    
    def _check_lab_files(self, module_num: int) -> Dict[str, Any]:
        """Check lab files are complete"""
        check_name = f"Module {module_num} Lab Files"
        
        required_files = [
            f"content/labs/lab_0{module_num}_setup_instructions.md",
            f"content/labs/lab_0{module_num}_implementation_guide.md",
            f"content/labs/lab_0{module_num}_starter.py",
            f"content/labs/lab_0{module_num}_solution.py",
            f"content/labs/lab_0{module_num}_troubleshooting.md"
        ]
        
        missing = [f for f in required_files if not os.path.exists(f)]
        
        if missing:
            return {'check': check_name, 'status': 'FAIL', 'message': f'Missing files: {[os.path.basename(f) for f in missing]}'}
        
        # Check solution file has content
        solution_file = f"content/labs/lab_0{module_num}_solution.py"
        with open(solution_file, 'r') as f:
            solution_content = f.read()
        
        if len(solution_content) < 1000:
            return {'check': check_name, 'status': 'WARN', 'message': 'Solution file seems short'}
        
        return {'check': check_name, 'status': 'PASS', 'message': 'All lab files present'}
    
    def _check_quiz(self, module_num: int) -> Dict[str, Any]:
        """Check quiz file"""
        check_name = f"Module {module_num} Quiz"
        
        # Map module numbers to quiz file names
        file_map = {
            1: "quiz_01_fundamentals.json",
            2: "quiz_02_structured_output.json",
            3: "quiz_03_retrieval.json",
            4: "quiz_04_multi_agent.json"
        }
        
        file_path = f"content/assessments/{file_map[module_num]}"
        
        if not os.path.exists(file_path):
            return {'check': check_name, 'status': 'FAIL', 'message': f'File not found: {file_path}'}
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Check question count (should be 5-10)
            question_count = len(data.get('questions', []))
            
            if question_count < 5:
                return {'check': check_name, 'status': 'FAIL', 'message': f'Only {question_count} questions (need 5-10)'}
            elif question_count > 10:
                return {'check': check_name, 'status': 'WARN', 'message': f'{question_count} questions (recommended 5-10)'}
            
            # Check each question has required fields
            for i, q in enumerate(data['questions'], 1):
                required = ['question_id', 'question_text', 'options', 'correct_answer', 'explanation']
                missing = [f for f in required if f not in q]
                if missing:
                    return {'check': check_name, 'status': 'FAIL', 'message': f'Question {i} missing: {missing}'}
            
            return {'check': check_name, 'status': 'PASS', 'message': f'{question_count} well-formed questions'}
            
        except json.JSONDecodeError as e:
            return {'check': check_name, 'status': 'FAIL', 'message': f'Invalid JSON: {e}'}
        except Exception as e:
            return {'check': check_name, 'status': 'FAIL', 'message': f'Error: {e}'}
    
    def _check_nvidia_integration(self, module_num: int) -> Dict[str, Any]:
        """Check NVIDIA platform integration in lab solution"""
        check_name = f"Module {module_num} NVIDIA Integration"
        
        solution_file = f"content/labs/lab_0{module_num}_solution.py"
        
        if not os.path.exists(solution_file):
            return {'check': check_name, 'status': 'FAIL', 'message': 'Solution file not found'}
        
        try:
            with open(solution_file, 'r') as f:
                content = f.read()
            
            # Check for NVIDIA-related keywords
            nvidia_keywords = ['nvidia', 'NIM', 'NVIDIA_API_KEY', 'build.nvidia']
            found_keywords = [kw for kw in nvidia_keywords if kw.lower() in content.lower()]
            
            if not found_keywords:
                return {'check': check_name, 'status': 'FAIL', 'message': 'No NVIDIA platform references found'}
            
            # Check for API key handling
            if 'NVIDIA_API_KEY' not in content:
                return {'check': check_name, 'status': 'WARN', 'message': 'No API key handling found'}
            
            # Check for error handling
            if 'try:' not in content or 'except' not in content:
                return {'check': check_name, 'status': 'WARN', 'message': 'Limited error handling'}
            
            return {'check': check_name, 'status': 'PASS', 'message': f'NVIDIA integration present: {", ".join(found_keywords)}'}
            
        except Exception as e:
            return {'check': check_name, 'status': 'FAIL', 'message': f'Error: {e}'}
    
    def print_results(self, results: List[Dict[str, Any]]):
        """Print validation results"""
        print(f"\n{'='*60}")
        print("VALIDATION SUMMARY")
        print(f"{'='*60}\n")
        
        total_checks = 0
        passed = 0
        warned = 0
        failed = 0
        
        for module_result in results:
            module_num = module_result['module_num']
            print(f"Module {module_num}:")
            
            for check in module_result['checks']:
                total_checks += 1
                status = check['status']
                
                if status == 'PASS':
                    icon = '✅'
                    passed += 1
                elif status == 'WARN':
                    icon = '⚠️'
                    warned += 1
                else:
                    icon = '❌'
                    failed += 1
                
                print(f"  {icon} {check['check']}: {check['message']}")
            
            print()
        
        print(f"{'='*60}")
        print(f"Total Checks: {total_checks}")
        print(f"✅ Passed: {passed}")
        print(f"⚠️  Warnings: {warned}")
        print(f"❌ Failed: {failed}")
        print(f"{'='*60}\n")
        
        if failed > 0:
            print("❌ CHECKPOINT FAILED - Please address failures before proceeding")
            return False
        elif warned > 0:
            print("⚠️  CHECKPOINT PASSED WITH WARNINGS - Review warnings")
            return True
        else:
            print("✅ CHECKPOINT PASSED - All modules validated successfully!")
            return True


def main():
    """Main validation function"""
    print("="*60)
    print("MODULE 1-4 CHECKPOINT VALIDATION")
    print("="*60)
    
    validator = ModuleValidator()
    results = []
    
    # Validate each module
    for module_num in [1, 2, 3, 4]:
        results.append(validator.validate_module(module_num))
    
    # Print summary
    success = validator.print_results(results)
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
