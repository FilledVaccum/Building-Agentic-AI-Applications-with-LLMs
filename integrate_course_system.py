"""
Course System Integration Script

This script integrates all 13 modules into a complete course system,
linking assessments, labs, supplementary materials, and instructor resources.

Validates: Requirements 2.1
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from src.models import (
    Module, LearningObjective, PlatformDemo,
    Course, ExamBlueprint,
    Assessment, Question,
    HandsOnLab
)


class CourseSystemIntegrator:
    """Integrates all course components into a unified system."""
    
    def __init__(self, content_dir: Path = Path("content")):
        """Initialize integrator with content directory."""
        self.content_dir = content_dir
        self.modules_dir = content_dir / "modules"
        self.labs_dir = content_dir / "labs"
        self.assessments_dir = content_dir / "assessments"
        self.supplementary_dir = content_dir / "supplementary"
        self.instructor_dir = content_dir / "instructor"
        
        self.modules: List[Module] = []
        self.assessments: Dict[str, Assessment] = {}
        self.labs: Dict[str, HandsOnLab] = {}
        self.supplementary_materials: Dict[str, str] = {}
        self.instructor_resources: Dict[str, str] = {}
    
    def load_all_modules(self) -> List[Module]:
        """Load all 13 modules from JSON files."""
        print("Loading modules...")
        modules = []
        
        for module_id in range(1, 14):
            # Try different naming patterns
            possible_files = [
                self.modules_dir / f"module_{module_id:02d}_fundamentals.json",
                self.modules_dir / f"module_{module_id:02d}_structured_output.json",
                self.modules_dir / f"module_{module_id:02d}_retrieval.json",
                self.modules_dir / f"module_{module_id:02d}_multi_agent.json",
                self.modules_dir / f"module_{module_id:02d}_cognition_planning_memory.json",
                self.modules_dir / f"module_{module_id:02d}_nvidia_platform.json",
                self.modules_dir / f"module_{module_id:02d}_evaluation_tuning.json",
                self.modules_dir / f"module_{module_id:02d}_deployment_scaling.json",
                self.modules_dir / f"module_{module_id:02d}_monitoring_maintenance.json",
                self.modules_dir / f"module_{module_id:02d}_safety_ethics.json",
                self.modules_dir / f"module_{module_id:02d}_human_in_the_loop.json",
                self.modules_dir / f"module_{module_id:02d}_advanced_topics.json",
                self.modules_dir / f"module_{module_id:02d}_final_assessment.json",
            ]
            
            module_file = None
            for file_path in possible_files:
                if file_path.exists():
                    module_file = file_path
                    break
            
            if module_file:
                with open(module_file, 'r') as f:
                    data = json.load(f)
                    
                    # Add default values for fields not in JSON
                    if "theoretical_content" not in data:
                        # Load from separate markdown file if exists
                        md_file = self.modules_dir / f"module_{module_id:02d}_theoretical_content.md"
                        if md_file.exists():
                            with open(md_file, 'r') as mf:
                                data["theoretical_content"] = mf.read()
                        else:
                            data["theoretical_content"] = f"Theoretical content for Module {module_id}"
                    
                    if "platform_demos" not in data:
                        # Create default platform demo
                        data["platform_demos"] = [{
                            "demo_id": f"demo_{module_id:02d}",
                            "title": f"NVIDIA Platform Demo for Module {module_id}",
                            "platform": "NIM",
                            "description": f"Demonstration of NVIDIA platform tools for Module {module_id}",
                            "code_examples": {"demo.py": "# Demo code"}
                        }]
                    
                    if "additional_resources" not in data:
                        data["additional_resources"] = []
                    
                    # Remove fields not in Module dataclass
                    extra_fields = ["time_allocation", "nvidia_platforms_used"]
                    for field in extra_fields:
                        data.pop(field, None)
                    
                    module = Module.from_dict(data)
                    modules.append(module)
                    print(f"  ✓ Loaded Module {module_id}: {module.title}")
            else:
                print(f"  ✗ Module {module_id} not found")
        
        self.modules = sorted(modules, key=lambda m: m.module_id)
        return self.modules
    
    def load_all_assessments(self) -> Dict[str, Assessment]:
        """Load all assessments (quizzes and practice exams)."""
        print("\nLoading assessments...")
        assessments = {}
        
        # Load module quizzes
        for quiz_id in range(1, 13):
            quiz_files = [
                self.assessments_dir / f"quiz_{quiz_id:02d}_fundamentals.json",
                self.assessments_dir / f"quiz_{quiz_id:02d}_structured_output.json",
                self.assessments_dir / f"quiz_{quiz_id:02d}_retrieval.json",
                self.assessments_dir / f"quiz_{quiz_id:02d}_multi_agent.json",
                self.assessments_dir / f"quiz_{quiz_id:02d}_cognition_planning.json",
                self.assessments_dir / f"quiz_{quiz_id:02d}_nvidia_platform.json",
                self.assessments_dir / f"quiz_{quiz_id:02d}_evaluation_tuning.json",
                self.assessments_dir / f"quiz_{quiz_id:02d}_deployment_scaling.json",
                self.assessments_dir / f"quiz_{quiz_id:02d}_monitoring_maintenance.json",
                self.assessments_dir / f"quiz_{quiz_id:02d}_safety_ethics.json",
                self.assessments_dir / f"quiz_{quiz_id:02d}_human_in_the_loop.json",
                self.assessments_dir / f"quiz_{quiz_id:02d}_advanced_topics.json",
            ]
            
            for quiz_file in quiz_files:
                if quiz_file.exists():
                    with open(quiz_file, 'r') as f:
                        data = json.load(f)
                        
                        # Normalize field names
                        if "type" in data:
                            data["assessment_type"] = data.pop("type")
                        if "time_limit_minutes" in data:
                            data["time_limit"] = data.pop("time_limit_minutes")
                        
                        # Clean up questions
                        if "questions" in data:
                            for q in data["questions"]:
                                # Remove extra question fields
                                q.pop("scenario_based", None)
                                q.pop("tags", None)
                                q.pop("points", None)
                        
                        # Keep only required fields
                        required_fields = [
                            "assessment_id", "assessment_type", "questions",
                            "passing_score", "time_limit", "exam_topics_covered"
                        ]
                        filtered_data = {k: v for k, v in data.items() if k in required_fields}
                        
                        assessment = Assessment.from_dict(filtered_data)
                        assessments[assessment.assessment_id] = assessment
                        print(f"  ✓ Loaded {assessment.assessment_id}")
                    break
        
        # Load practice exams
        for exam_num in range(1, 4):
            exam_file = self.assessments_dir / f"practice_exam_{exam_num:02d}.json"
            if exam_file.exists():
                with open(exam_file, 'r') as f:
                    data = json.load(f)
                    
                    # Normalize field names
                    if "type" in data:
                        data["assessment_type"] = data.pop("type")
                    if "time_limit_minutes" in data:
                        data["time_limit"] = data.pop("time_limit_minutes")
                    
                    # Clean up questions
                    if "questions" in data:
                        for q in data["questions"]:
                            # Remove extra question fields
                            q.pop("scenario_based", None)
                            q.pop("tags", None)
                            q.pop("points", None)
                    
                    # Keep only required fields
                    required_fields = [
                        "assessment_id", "assessment_type", "questions",
                        "passing_score", "time_limit", "exam_topics_covered"
                    ]
                    filtered_data = {k: v for k, v in data.items() if k in required_fields}
                    
                    assessment = Assessment.from_dict(filtered_data)
                    assessments[assessment.assessment_id] = assessment
                    print(f"  ✓ Loaded {assessment.assessment_id}")
        
        # Load final assessment
        final_file = self.assessments_dir / "final_assessment.json"
        if final_file.exists():
            with open(final_file, 'r') as f:
                data = json.load(f)
                
                # Normalize field names
                if "type" in data:
                    data["assessment_type"] = data.pop("type")
                if "time_limit_minutes" in data:
                    data["time_limit"] = data.pop("time_limit_minutes")
                
                # Clean up questions
                if "questions" in data:
                    for q in data["questions"]:
                        # Remove extra question fields
                        q.pop("scenario_based", None)
                        q.pop("tags", None)
                        q.pop("points", None)
                
                # Keep only required fields
                required_fields = [
                    "assessment_id", "assessment_type", "questions",
                    "passing_score", "time_limit", "exam_topics_covered"
                ]
                filtered_data = {k: v for k, v in data.items() if k in required_fields}
                
                assessment = Assessment.from_dict(filtered_data)
                assessments[assessment.assessment_id] = assessment
                print(f"  ✓ Loaded {assessment.assessment_id}")
        
        self.assessments = assessments
        return assessments
    
    def load_all_labs(self) -> Dict[str, HandsOnLab]:
        """Load all hands-on labs."""
        print("\nLoading labs...")
        labs = {}
        
        for lab_id in range(1, 13):
            lab_files = [
                self.labs_dir / f"lab_{lab_id:02d}_minimal_agent.json",
                self.labs_dir / f"lab_{lab_id:02d}_structured_output.json",
                self.labs_dir / f"lab_{lab_id:02d}_rag_pipeline.json",
                self.labs_dir / f"lab_{lab_id:02d}_multi_agent.json",
                self.labs_dir / f"lab_{lab_id:02d}_cognition_planning.json",
                self.labs_dir / f"lab_{lab_id:02d}_nvidia_platform.json",
                self.labs_dir / f"lab_{lab_id:02d}_evaluation_tuning.json",
                self.labs_dir / f"lab_{lab_id:02d}_deployment_scaling.json",
                self.labs_dir / f"lab_{lab_id:02d}_monitoring_maintenance.json",
                self.labs_dir / f"lab_{lab_id:02d}_safety_ethics.json",
                self.labs_dir / f"lab_{lab_id:02d}_human_in_the_loop.json",
                self.labs_dir / f"lab_{lab_id:02d}_advanced_topics.json",
            ]
            
            for lab_file in lab_files:
                if lab_file.exists():
                    with open(lab_file, 'r') as f:
                        data = json.load(f)
                        
                        # Keep only required fields
                        required_fields = [
                            "lab_id", "title", "objectives", "setup_instructions",
                            "implementation_guide", "starter_code", "solution_code",
                            "expected_outputs", "troubleshooting_guide", "nvidia_platforms_used"
                        ]
                        filtered_data = {k: v for k, v in data.items() if k in required_fields}
                        
                        # Add defaults for missing required fields
                        if "objectives" not in filtered_data:
                            filtered_data["objectives"] = ["Complete lab exercise"]
                        if "setup_instructions" not in filtered_data:
                            filtered_data["setup_instructions"] = "Setup instructions not available"
                        if "implementation_guide" not in filtered_data:
                            filtered_data["implementation_guide"] = "Implementation guide not available"
                        if "starter_code" not in filtered_data:
                            filtered_data["starter_code"] = {}
                        if "solution_code" not in filtered_data:
                            filtered_data["solution_code"] = {}
                        if "expected_outputs" not in filtered_data:
                            filtered_data["expected_outputs"] = {}
                        if "troubleshooting_guide" not in filtered_data:
                            filtered_data["troubleshooting_guide"] = "Troubleshooting guide not available"
                        if "nvidia_platforms_used" not in filtered_data:
                            filtered_data["nvidia_platforms_used"] = ["NIM"]
                        
                        lab = HandsOnLab.from_dict(filtered_data)
                        labs[lab.lab_id] = lab
                        print(f"  ✓ Loaded {lab.lab_id}")
                    break
        
        # Load final project
        final_lab_file = self.labs_dir / "final_project.json"
        if final_lab_file.exists():
            with open(final_lab_file, 'r') as f:
                data = json.load(f)
                
                # Keep only required fields
                required_fields = [
                    "lab_id", "title", "objectives", "setup_instructions",
                    "implementation_guide", "starter_code", "solution_code",
                    "expected_outputs", "troubleshooting_guide", "nvidia_platforms_used"
                ]
                filtered_data = {k: v for k, v in data.items() if k in required_fields}
                
                # Add defaults for missing required fields
                if "objectives" not in filtered_data:
                    filtered_data["objectives"] = ["Complete final project"]
                if "setup_instructions" not in filtered_data:
                    filtered_data["setup_instructions"] = "Setup instructions not available"
                if "implementation_guide" not in filtered_data:
                    filtered_data["implementation_guide"] = "Implementation guide not available"
                if "starter_code" not in filtered_data:
                    filtered_data["starter_code"] = {}
                if "solution_code" not in filtered_data:
                    filtered_data["solution_code"] = {}
                if "expected_outputs" not in filtered_data:
                    filtered_data["expected_outputs"] = {}
                if "troubleshooting_guide" not in filtered_data:
                    filtered_data["troubleshooting_guide"] = "Troubleshooting guide not available"
                if "nvidia_platforms_used" not in filtered_data:
                    filtered_data["nvidia_platforms_used"] = ["NIM"]
                
                lab = HandsOnLab.from_dict(filtered_data)
                labs[lab.lab_id] = lab
                print(f"  ✓ Loaded {lab.lab_id}")
        
        self.labs = labs
        return labs
    
    def load_supplementary_materials(self) -> Dict[str, str]:
        """Load all supplementary materials."""
        print("\nLoading supplementary materials...")
        materials = {}
        
        supplementary_files = [
            "glossary.md",
            "nvidia_nim_quick_reference.md",
            "nvidia_nemo_quick_reference.md",
            "nvidia_tensorrt_llm_quick_reference.md",
            "nvidia_triton_quick_reference.md",
            "agent_patterns_cheat_sheet.md",
            "framework_comparison_cheat_sheet.md",
            "error_handling_cheat_sheet.md",
            "deployment_checklist.md",
            "study_plan_template.md",
            "external_references.md",
            "exam_day_checklist.md",
        ]
        
        for filename in supplementary_files:
            file_path = self.supplementary_dir / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    materials[filename] = f.read()
                    print(f"  ✓ Loaded {filename}")
            else:
                print(f"  ✗ {filename} not found")
        
        self.supplementary_materials = materials
        return materials
    
    def load_instructor_resources(self) -> Dict[str, str]:
        """Load all instructor resources."""
        print("\nLoading instructor resources...")
        resources = {}
        
        instructor_files = [
            "instructor_guide.md",
            "lab_solutions_guide.md",
            "faq.md",
            "grading_rubrics.md",
            "teaching_guidance.md",
            "README.md",
        ]
        
        for filename in instructor_files:
            file_path = self.instructor_dir / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    resources[filename] = f.read()
                    print(f"  ✓ Loaded {filename}")
            else:
                print(f"  ✗ {filename} not found")
        
        self.instructor_resources = resources
        return resources
    
    def link_modules_to_assessments(self) -> None:
        """Link each module to its assessment."""
        print("\nLinking modules to assessments...")
        
        for module in self.modules:
            if module.assessment_id in self.assessments:
                print(f"  ✓ Module {module.module_id} → {module.assessment_id}")
            else:
                print(f"  ✗ Module {module.module_id} assessment '{module.assessment_id}' not found")
    
    def link_modules_to_labs(self) -> None:
        """Link each module to its lab."""
        print("\nLinking modules to labs...")
        
        for module in self.modules:
            if module.lab_id in self.labs:
                print(f"  ✓ Module {module.module_id} → {module.lab_id}")
            else:
                print(f"  ✗ Module {module.module_id} lab '{module.lab_id}' not found")
    
    def create_integrated_course(self) -> Course:
        """Create integrated course with all components."""
        print("\nCreating integrated course...")
        
        blueprint = ExamBlueprint()
        course = Course(modules=self.modules, blueprint=blueprint)
        
        print(f"  ✓ Course created with {len(self.modules)} modules")
        print(f"  ✓ Total duration: {course.get_total_duration():.1f} hours")
        
        return course
    
    def validate_integration(self, course: Course) -> Dict[str, Any]:
        """Validate the integrated course system."""
        print("\nValidating integration...")
        
        validation_results = {
            "timestamp": datetime.now().isoformat(),
            "modules_count": len(course.modules),
            "assessments_count": len(self.assessments),
            "labs_count": len(self.labs),
            "supplementary_materials_count": len(self.supplementary_materials),
            "instructor_resources_count": len(self.instructor_resources),
            "issues": [],
            "warnings": [],
        }
        
        # Validate module count
        if len(course.modules) != 13:
            validation_results["issues"].append(
                f"Expected 13 modules, found {len(course.modules)}"
            )
        else:
            print("  ✓ All 13 modules present")
        
        # Validate module sequence
        expected_ids = list(range(1, 14))
        actual_ids = [m.module_id for m in course.modules]
        if actual_ids != expected_ids:
            validation_results["issues"].append(
                f"Module IDs not sequential: {actual_ids}"
            )
        else:
            print("  ✓ Module sequence correct")
        
        # Validate exam blueprint coverage
        is_complete, missing_topics = course.validate_blueprint_coverage()
        if not is_complete:
            validation_results["issues"].append(
                f"Missing exam topics: {missing_topics}"
            )
        else:
            print("  ✓ All exam topics covered")
        
        # Validate proportional weighting
        is_aligned, deviations = course.validate_proportional_weighting(tolerance=2.0)
        if not is_aligned:
            excessive_deviations = {
                topic: dev for topic, dev in deviations.items()
                if abs(dev) > 2.0
            }
            validation_results["warnings"].append(
                f"Topic weighting deviations exceed ±2%: {excessive_deviations}"
            )
        else:
            print("  ✓ Topic weighting aligned")
        
        # Validate module-assessment links
        missing_assessments = []
        for module in course.modules:
            if module.assessment_id not in self.assessments:
                missing_assessments.append(module.assessment_id)
        
        if missing_assessments:
            validation_results["issues"].append(
                f"Missing assessments: {missing_assessments}"
            )
        else:
            print("  ✓ All module assessments linked")
        
        # Validate module-lab links
        missing_labs = []
        for module in course.modules:
            if module.lab_id not in self.labs:
                missing_labs.append(module.lab_id)
        
        if missing_labs:
            validation_results["issues"].append(
                f"Missing labs: {missing_labs}"
            )
        else:
            print("  ✓ All module labs linked")
        
        # Validate practice exams
        practice_exams = [
            a for a in self.assessments.values()
            if a.assessment_type == "practice_exam"
        ]
        if len(practice_exams) < 2:
            validation_results["warnings"].append(
                f"Expected 2-3 practice exams, found {len(practice_exams)}"
            )
        else:
            print(f"  ✓ {len(practice_exams)} practice exams available")
        
        # Validate supplementary materials
        required_materials = [
            "glossary.md",
            "study_plan_template.md",
            "exam_day_checklist.md",
        ]
        missing_materials = [
            m for m in required_materials
            if m not in self.supplementary_materials
        ]
        if missing_materials:
            validation_results["warnings"].append(
                f"Missing supplementary materials: {missing_materials}"
            )
        else:
            print("  ✓ Required supplementary materials present")
        
        # Validate instructor resources
        required_resources = [
            "instructor_guide.md",
            "lab_solutions_guide.md",
            "grading_rubrics.md",
        ]
        missing_resources = [
            r for r in required_resources
            if r not in self.instructor_resources
        ]
        if missing_resources:
            validation_results["warnings"].append(
                f"Missing instructor resources: {missing_resources}"
            )
        else:
            print("  ✓ Required instructor resources present")
        
        return validation_results
    
    def export_integrated_course(self, course: Course, output_file: Path) -> None:
        """Export integrated course to JSON."""
        print(f"\nExporting integrated course to {output_file}...")
        
        course_data = {
            "course": course.to_dict(),
            "assessments": {
                aid: assessment.to_dict()
                for aid, assessment in self.assessments.items()
            },
            "labs": {
                lid: lab.to_dict()
                for lid, lab in self.labs.items()
            },
            "supplementary_materials": list(self.supplementary_materials.keys()),
            "instructor_resources": list(self.instructor_resources.keys()),
            "metadata": {
                "integration_date": datetime.now().isoformat(),
                "total_modules": len(course.modules),
                "total_duration_hours": course.get_total_duration(),
                "total_assessments": len(self.assessments),
                "total_labs": len(self.labs),
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(course_data, f, indent=2)
        
        print(f"  ✓ Course exported successfully")
    
    def generate_integration_report(
        self,
        course: Course,
        validation_results: Dict[str, Any],
        output_file: Path
    ) -> None:
        """Generate comprehensive integration report."""
        print(f"\nGenerating integration report to {output_file}...")
        
        report_lines = [
            "# Course System Integration Report",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            "",
            f"- **Total Modules:** {len(course.modules)}",
            f"- **Total Duration:** {course.get_total_duration():.1f} hours",
            f"- **Total Assessments:** {len(self.assessments)}",
            f"- **Total Labs:** {len(self.labs)}",
            f"- **Supplementary Materials:** {len(self.supplementary_materials)}",
            f"- **Instructor Resources:** {len(self.instructor_resources)}",
            "",
            "## Modules",
            "",
        ]
        
        for module in course.modules:
            report_lines.extend([
                f"### Module {module.module_id}: {module.title}",
                "",
                f"- **Duration:** {module.duration_hours} hours",
                f"- **Learning Objectives:** {len(module.learning_objectives)}",
                f"- **Platform Demos:** {len(module.platform_demos)}",
                f"- **Lab:** {module.lab_id}",
                f"- **Assessment:** {module.assessment_id}",
                f"- **Exam Topics:** {', '.join(module.exam_topics.keys())}",
                "",
            ])
        
        report_lines.extend([
            "## Exam Blueprint Alignment",
            "",
        ])
        
        coverage_report = course.get_coverage_report()
        for topic, percentage in coverage_report["topic_percentages"].items():
            expected = coverage_report["blueprint_percentages"][topic]
            deviation = coverage_report["deviations"][topic]
            status = "✓" if abs(deviation) <= 2.0 else "✗"
            report_lines.append(
                f"- {status} **{topic}:** {percentage:.1f}% "
                f"(expected {expected:.1f}%, deviation {deviation:+.1f}%)"
            )
        
        report_lines.extend([
            "",
            "## Validation Results",
            "",
        ])
        
        if validation_results["issues"]:
            report_lines.extend([
                "### Issues",
                "",
            ])
            for issue in validation_results["issues"]:
                report_lines.append(f"- ❌ {issue}")
            report_lines.append("")
        
        if validation_results["warnings"]:
            report_lines.extend([
                "### Warnings",
                "",
            ])
            for warning in validation_results["warnings"]:
                report_lines.append(f"- ⚠️  {warning}")
            report_lines.append("")
        
        if not validation_results["issues"] and not validation_results["warnings"]:
            report_lines.extend([
                "✅ **All validation checks passed!**",
                "",
            ])
        
        report_lines.extend([
            "## Assessments",
            "",
        ])
        
        for assessment_id, assessment in sorted(self.assessments.items()):
            report_lines.extend([
                f"### {assessment_id}",
                "",
                f"- **Type:** {assessment.assessment_type}",
                f"- **Questions:** {len(assessment.questions)}",
                f"- **Time Limit:** {assessment.time_limit} minutes",
                f"- **Passing Score:** {assessment.passing_score}%",
                "",
            ])
        
        report_lines.extend([
            "## Labs",
            "",
        ])
        
        for lab_id, lab in sorted(self.labs.items()):
            report_lines.extend([
                f"### {lab_id}",
                "",
                f"- **Title:** {lab.title}",
                f"- **Objectives:** {len(lab.objectives)}",
                f"- **NVIDIA Platforms:** {', '.join(lab.nvidia_platforms_used)}",
                "",
            ])
        
        with open(output_file, 'w') as f:
            f.write('\n'.join(report_lines))
        
        print(f"  ✓ Integration report generated")


def main():
    """Main integration workflow."""
    print("=" * 70)
    print("COURSE SYSTEM INTEGRATION")
    print("=" * 70)
    
    integrator = CourseSystemIntegrator()
    
    # Load all components
    integrator.load_all_modules()
    integrator.load_all_assessments()
    integrator.load_all_labs()
    integrator.load_supplementary_materials()
    integrator.load_instructor_resources()
    
    # Link components
    integrator.link_modules_to_assessments()
    integrator.link_modules_to_labs()
    
    # Create integrated course
    course = integrator.create_integrated_course()
    
    # Validate integration
    validation_results = integrator.validate_integration(course)
    
    # Export results
    integrator.export_integrated_course(
        course,
        Path("integrated_course.json")
    )
    
    integrator.generate_integration_report(
        course,
        validation_results,
        Path("INTEGRATION_REPORT.md")
    )
    
    print("\n" + "=" * 70)
    print("INTEGRATION COMPLETE")
    print("=" * 70)
    
    # Print summary
    if validation_results["issues"]:
        print(f"\n❌ {len(validation_results['issues'])} issues found")
        for issue in validation_results["issues"]:
            print(f"   - {issue}")
    
    if validation_results["warnings"]:
        print(f"\n⚠️  {len(validation_results['warnings'])} warnings")
        for warning in validation_results["warnings"]:
            print(f"   - {warning}")
    
    if not validation_results["issues"] and not validation_results["warnings"]:
        print("\n✅ All validation checks passed!")
    
    print(f"\nIntegrated course exported to: integrated_course.json")
    print(f"Integration report generated: INTEGRATION_REPORT.md")


if __name__ == "__main__":
    main()
