"""Content validation system for course materials."""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import json

from src.models.course import Course
from src.models.module import Module
from src.models.lab import HandsOnLab
from src.models.exam_blueprint import ExamBlueprint


@dataclass
class ValidationResult:
    """Result of a validation check."""
    
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    details: Dict[str, any]
    
    def __str__(self) -> str:
        """String representation of validation result."""
        status = "PASS" if self.is_valid else "FAIL"
        result = f"Validation: {status}\n"
        
        if self.errors:
            result += f"\nErrors ({len(self.errors)}):\n"
            for error in self.errors:
                result += f"  - {error}\n"
        
        if self.warnings:
            result += f"\nWarnings ({len(self.warnings)}):\n"
            for warning in self.warnings:
                result += f"  - {warning}\n"
        
        return result


class ExamBlueprintValidator:
    """Validates course alignment with exam blueprint."""
    
    def __init__(self, course: Course):
        """Initialize validator with course."""
        self.course = course
        self.blueprint = course.blueprint
    
    def validate_all_topics_covered(self) -> ValidationResult:
        """
        Validate that all 10 exam topics are covered.
        
        Requirements: 1.1
        """
        errors = []
        warnings = []
        details = {}
        
        # Get all topics from blueprint
        blueprint_topics = set(self.blueprint.get_topics())
        details["required_topics"] = list(blueprint_topics)
        
        # Get all topics covered by modules
        covered_topics = set()
        for module in self.course.modules:
            covered_topics.update(module.exam_topics.keys())
        
        details["covered_topics"] = list(covered_topics)
        
        # Check for missing topics
        missing_topics = blueprint_topics - covered_topics
        if missing_topics:
            for topic in sorted(missing_topics):
                errors.append(f"Exam topic not covered: '{topic}'")
        
        details["missing_topics"] = list(missing_topics)
        details["coverage_percentage"] = (len(covered_topics) / len(blueprint_topics)) * 100
        
        is_valid = len(missing_topics) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            details=details
        )
    
    def validate_proportional_time_allocation(self, tolerance: float = 2.0) -> ValidationResult:
        """
        Validate that time allocation matches blueprint percentages within tolerance.
        
        Requirements: 1.2
        
        Args:
            tolerance: Maximum allowed deviation in percentage points (default ±2%)
        """
        errors = []
        warnings = []
        details = {}
        
        # Calculate actual topic percentages
        actual_percentages = self.course.calculate_topic_percentages()
        blueprint_percentages = self.blueprint.get_all_topic_percentages()
        
        # Validate proportional weighting
        is_aligned, deviations = self.course.validate_proportional_weighting(tolerance)
        
        details["actual_percentages"] = actual_percentages
        details["blueprint_percentages"] = blueprint_percentages
        details["deviations"] = deviations
        details["tolerance"] = tolerance
        details["total_hours"] = self.course.get_total_duration()
        
        # Check each topic
        for topic in self.blueprint.get_topics():
            actual = actual_percentages.get(topic, 0.0)
            expected = blueprint_percentages[topic]
            deviation = deviations[topic]
            
            if abs(deviation) > tolerance:
                errors.append(
                    f"Topic '{topic}': allocation {actual:.1f}% deviates from "
                    f"blueprint {expected:.1f}% by {deviation:+.1f}% (tolerance: ±{tolerance}%)"
                )
            elif abs(deviation) > tolerance * 0.5:
                # Warning if deviation is more than half the tolerance
                warnings.append(
                    f"Topic '{topic}': allocation {actual:.1f}% is close to "
                    f"tolerance limit (deviation: {deviation:+.1f}%, tolerance: ±{tolerance}%)"
                )
        
        return ValidationResult(
            is_valid=is_aligned,
            errors=errors,
            warnings=warnings,
            details=details
        )
    
    def validate_learning_objective_mappings(self) -> ValidationResult:
        """
        Validate that all learning objectives map to exam topics.
        
        Requirements: 1.13
        """
        errors = []
        warnings = []
        details = {}
        
        blueprint_topics = set(self.blueprint.get_topics())
        unmapped_objectives = []
        invalid_topic_references = []
        
        for module in self.course.modules:
            for obj in module.learning_objectives:
                # Check if objective has exam topics
                if not obj.exam_topics:
                    unmapped_objectives.append({
                        "module_id": module.module_id,
                        "objective_id": obj.objective_id,
                        "description": obj.description
                    })
                    errors.append(
                        f"Module {module.module_id}, Objective '{obj.objective_id}': "
                        f"No exam topics mapped"
                    )
                
                # Check if referenced topics are valid
                for topic in obj.exam_topics:
                    if topic not in blueprint_topics:
                        invalid_topic_references.append({
                            "module_id": module.module_id,
                            "objective_id": obj.objective_id,
                            "invalid_topic": topic
                        })
                        errors.append(
                            f"Module {module.module_id}, Objective '{obj.objective_id}': "
                            f"References invalid exam topic '{topic}'"
                        )
        
        details["unmapped_objectives"] = unmapped_objectives
        details["invalid_topic_references"] = invalid_topic_references
        details["total_objectives"] = sum(len(m.learning_objectives) for m in self.course.modules)
        
        is_valid = len(unmapped_objectives) == 0 and len(invalid_topic_references) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            details=details
        )
    
    def validate_all(self) -> ValidationResult:
        """Run all exam blueprint alignment validations."""
        all_errors = []
        all_warnings = []
        all_details = {}
        
        # Validate topic coverage
        coverage_result = self.validate_all_topics_covered()
        all_errors.extend(coverage_result.errors)
        all_warnings.extend(coverage_result.warnings)
        all_details["topic_coverage"] = coverage_result.details
        
        # Validate time allocation
        allocation_result = self.validate_proportional_time_allocation()
        all_errors.extend(allocation_result.errors)
        all_warnings.extend(allocation_result.warnings)
        all_details["time_allocation"] = allocation_result.details
        
        # Validate learning objective mappings
        mapping_result = self.validate_learning_objective_mappings()
        all_errors.extend(mapping_result.errors)
        all_warnings.extend(mapping_result.warnings)
        all_details["learning_objective_mappings"] = mapping_result.details
        
        is_valid = (
            coverage_result.is_valid and
            allocation_result.is_valid and
            mapping_result.is_valid
        )
        
        return ValidationResult(
            is_valid=is_valid,
            errors=all_errors,
            warnings=all_warnings,
            details=all_details
        )


class ModuleCompletenessValidator:
    """Validates that modules have all required components."""
    
    def __init__(self, course: Course):
        """Initialize validator with course."""
        self.course = course
    
    def validate_module_components(self, module: Module) -> ValidationResult:
        """
        Validate that a module has all required components.
        
        Requirements: 2.7
        """
        errors = []
        warnings = []
        details = {
            "module_id": module.module_id,
            "module_title": module.title
        }
        
        # Check learning objectives
        if not module.learning_objectives:
            errors.append(f"Module {module.module_id}: Missing learning objectives")
        else:
            details["learning_objectives_count"] = len(module.learning_objectives)
            if len(module.learning_objectives) < 3:
                warnings.append(
                    f"Module {module.module_id}: Only {len(module.learning_objectives)} "
                    f"learning objectives (recommended: 4-6)"
                )
        
        # Check theoretical content
        if not module.theoretical_content or not module.theoretical_content.strip():
            errors.append(f"Module {module.module_id}: Missing theoretical content")
        else:
            content_length = len(module.theoretical_content)
            details["theoretical_content_length"] = content_length
            if content_length < 100:
                warnings.append(
                    f"Module {module.module_id}: Theoretical content is very short "
                    f"({content_length} characters)"
                )
        
        # Check NVIDIA platform integration
        if not module.platform_demos:
            errors.append(f"Module {module.module_id}: Missing NVIDIA platform integration")
        else:
            details["platform_demos_count"] = len(module.platform_demos)
            details["platforms_used"] = [demo.platform for demo in module.platform_demos]
        
        # Check hands-on lab
        if not module.lab_id:
            errors.append(f"Module {module.module_id}: Missing hands-on lab")
        else:
            details["lab_id"] = module.lab_id
        
        # Check assessment
        if not module.assessment_id:
            errors.append(f"Module {module.module_id}: Missing assessment")
        else:
            details["assessment_id"] = module.assessment_id
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            details=details
        )
    
    def validate_time_allocation_percentages(self, module: Module) -> ValidationResult:
        """
        Validate that module time allocation follows the 20/30/40/10 pattern.
        
        Requirements: 2.8, 2.9, 2.10, 2.11
        
        Note: This validates the conceptual requirement. Actual time tracking
        would require more detailed module structure.
        """
        errors = []
        warnings = []
        details = {
            "module_id": module.module_id,
            "duration_hours": module.duration_hours
        }
        
        # Expected allocation pattern
        expected_pattern = {
            "concept_introduction": 20.0,
            "demonstration": 30.0,
            "hands_on_practice": 40.0,
            "assessment": 10.0
        }
        
        details["expected_pattern"] = expected_pattern
        
        # For now, we validate that the module has the components
        # that would support this allocation
        has_theoretical = bool(module.theoretical_content)
        has_demos = bool(module.platform_demos)
        has_lab = bool(module.lab_id)
        has_assessment = bool(module.assessment_id)
        
        details["has_components"] = {
            "theoretical_content": has_theoretical,
            "platform_demos": has_demos,
            "hands_on_lab": has_lab,
            "assessment": has_assessment
        }
        
        if not (has_theoretical and has_demos and has_lab and has_assessment):
            errors.append(
                f"Module {module.module_id}: Cannot support 20/30/40/10 time allocation "
                f"without all required components"
            )
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            details=details
        )
    
    def validate_nvidia_platform_integration(self, module: Module) -> ValidationResult:
        """
        Validate that module includes NVIDIA platform integration.
        
        Requirements: 3.1
        """
        errors = []
        warnings = []
        details = {
            "module_id": module.module_id
        }
        
        if not module.platform_demos:
            errors.append(
                f"Module {module.module_id}: No NVIDIA platform integration found"
            )
        else:
            platforms_used = [demo.platform for demo in module.platform_demos]
            details["platforms_used"] = platforms_used
            details["demo_count"] = len(module.platform_demos)
            
            # Check for valid NVIDIA platforms
            valid_platforms = {"NIM", "NeMo", "TensorRT-LLM", "Triton", "build.nvidia.com"}
            invalid_platforms = [p for p in platforms_used if p not in valid_platforms]
            
            if invalid_platforms:
                warnings.append(
                    f"Module {module.module_id}: Uses non-standard platforms: "
                    f"{', '.join(invalid_platforms)}"
                )
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            details=details
        )
    
    def validate_all_modules(self) -> ValidationResult:
        """Validate all modules in the course."""
        all_errors = []
        all_warnings = []
        all_details = {"modules": []}
        
        for module in self.course.modules:
            # Validate components
            components_result = self.validate_module_components(module)
            all_errors.extend(components_result.errors)
            all_warnings.extend(components_result.warnings)
            
            # Validate time allocation
            time_result = self.validate_time_allocation_percentages(module)
            all_errors.extend(time_result.errors)
            all_warnings.extend(time_result.warnings)
            
            # Validate NVIDIA platform integration
            platform_result = self.validate_nvidia_platform_integration(module)
            all_errors.extend(platform_result.errors)
            all_warnings.extend(platform_result.warnings)
            
            # Collect details
            module_details = {
                "module_id": module.module_id,
                "components": components_result.details,
                "time_allocation": time_result.details,
                "platform_integration": platform_result.details,
                "is_valid": (
                    components_result.is_valid and
                    time_result.is_valid and
                    platform_result.is_valid
                )
            }
            all_details["modules"].append(module_details)
        
        is_valid = len(all_errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=all_errors,
            warnings=all_warnings,
            details=all_details
        )


class LabRequirementsValidator:
    """Validates that labs meet all requirements."""
    
    def __init__(self, labs: Dict[str, HandsOnLab]):
        """
        Initialize validator with labs.
        
        Args:
            labs: Dictionary mapping lab_id to HandsOnLab instances
        """
        self.labs = labs
    
    def validate_lab_completeness(self, lab: HandsOnLab) -> ValidationResult:
        """
        Validate that a lab has all required components.
        
        Requirements: 4.2, 4.3, 4.4, 4.5
        """
        errors = []
        warnings = []
        details = {
            "lab_id": lab.lab_id,
            "lab_title": lab.title
        }
        
        # Check setup instructions (Requirement 4.2)
        if not lab.setup_instructions or not lab.setup_instructions.strip():
            errors.append(f"Lab {lab.lab_id}: Missing setup instructions")
        else:
            details["has_setup_instructions"] = True
            details["setup_instructions_length"] = len(lab.setup_instructions)
        
        # Check implementation guide (Requirement 4.3)
        if not lab.implementation_guide or not lab.implementation_guide.strip():
            errors.append(f"Lab {lab.lab_id}: Missing implementation guide")
        else:
            details["has_implementation_guide"] = True
            details["implementation_guide_length"] = len(lab.implementation_guide)
        
        # Check starter code (Requirement 4.4)
        if not lab.starter_code:
            errors.append(f"Lab {lab.lab_id}: Missing starter code")
        else:
            details["has_starter_code"] = True
            details["starter_code_files"] = list(lab.starter_code.keys())
        
        # Check expected outputs (Requirement 4.4)
        if not lab.expected_outputs:
            errors.append(f"Lab {lab.lab_id}: Missing expected outputs")
        else:
            details["has_expected_outputs"] = True
        
        # Check troubleshooting guide (Requirement 4.5)
        if not lab.troubleshooting_guide or not lab.troubleshooting_guide.strip():
            errors.append(f"Lab {lab.lab_id}: Missing troubleshooting guide")
        else:
            details["has_troubleshooting_guide"] = True
            details["troubleshooting_guide_length"] = len(lab.troubleshooting_guide)
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            details=details
        )
    
    def validate_nvidia_platform_usage(self, lab: HandsOnLab) -> ValidationResult:
        """
        Validate that lab uses NVIDIA platforms.
        
        Requirements: 4.1
        """
        errors = []
        warnings = []
        details = {
            "lab_id": lab.lab_id
        }
        
        if not lab.nvidia_platforms_used:
            errors.append(f"Lab {lab.lab_id}: No NVIDIA platforms specified")
        else:
            details["nvidia_platforms_used"] = lab.nvidia_platforms_used
            details["platform_count"] = len(lab.nvidia_platforms_used)
            
            # Check for valid NVIDIA platforms
            valid_platforms = {"NIM", "NeMo", "TensorRT-LLM", "Triton", "build.nvidia.com"}
            invalid_platforms = [p for p in lab.nvidia_platforms_used if p not in valid_platforms]
            
            if invalid_platforms:
                warnings.append(
                    f"Lab {lab.lab_id}: Uses non-standard platforms: "
                    f"{', '.join(invalid_platforms)}"
                )
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            details=details
        )
    
    def validate_all_labs(self) -> ValidationResult:
        """Validate all labs."""
        all_errors = []
        all_warnings = []
        all_details = {"labs": []}
        
        for lab_id, lab in self.labs.items():
            # Validate completeness
            completeness_result = self.validate_lab_completeness(lab)
            all_errors.extend(completeness_result.errors)
            all_warnings.extend(completeness_result.warnings)
            
            # Validate NVIDIA platform usage
            platform_result = self.validate_nvidia_platform_usage(lab)
            all_errors.extend(platform_result.errors)
            all_warnings.extend(platform_result.warnings)
            
            # Collect details
            lab_details = {
                "lab_id": lab_id,
                "completeness": completeness_result.details,
                "platform_usage": platform_result.details,
                "is_valid": (
                    completeness_result.is_valid and
                    platform_result.is_valid
                )
            }
            all_details["labs"].append(lab_details)
        
        is_valid = len(all_errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=all_errors,
            warnings=all_warnings,
            details=all_details
        )


class CodeQualityValidator:
    """Validates code examples for quality standards."""
    
    def __init__(self, course: Course, labs: Optional[Dict[str, HandsOnLab]] = None):
        """
        Initialize code quality validator.
        
        Args:
            course: Course instance to validate
            labs: Optional dictionary of labs (lab_id -> HandsOnLab)
        """
        self.course = course
        self.labs = labs or {}
    
    def validate_code_example_error_handling(self, code: str, context: str = "") -> ValidationResult:
        """
        Validate that code examples include proper error handling.
        
        Requirements: 15.1, 15.6, 15.7, 15.8
        
        Args:
            code: Code string to validate
            context: Context description (e.g., "Module 1 demo", "Lab 3 solution")
        """
        errors = []
        warnings = []
        details = {"context": context, "code_length": len(code)}
        
        # Check for error handling patterns
        has_try_except = "try:" in code and "except" in code
        has_error_handling = has_try_except or "raise" in code
        
        details["has_try_except"] = has_try_except
        details["has_error_handling"] = has_error_handling
        
        # Check for external operations that need error handling
        needs_error_handling = False
        external_operations = []
        
        # API calls
        if any(pattern in code for pattern in ["requests.", "http", "api", ".get(", ".post("]):
            needs_error_handling = True
            external_operations.append("API calls")
        
        # File I/O
        if any(pattern in code for pattern in ["open(", "read(", "write(", "with open"]):
            needs_error_handling = True
            external_operations.append("File I/O")
        
        # Database operations
        if any(pattern in code for pattern in ["connect(", "execute(", "query(", "cursor"]):
            needs_error_handling = True
            external_operations.append("Database operations")
        
        # Network operations
        if any(pattern in code for pattern in ["socket", "urllib", "httpx"]):
            needs_error_handling = True
            external_operations.append("Network operations")
        
        # NVIDIA API calls
        if any(pattern in code for pattern in ["NVIDIA", "NIM", "NeMo", "Triton"]):
            needs_error_handling = True
            external_operations.append("NVIDIA platform calls")
        
        details["needs_error_handling"] = needs_error_handling
        details["external_operations"] = external_operations
        
        # Validate error handling is present when needed
        if needs_error_handling and not has_error_handling:
            errors.append(
                f"{context}: Code contains {', '.join(external_operations)} "
                f"but lacks error handling (try-except blocks or raise statements)"
            )
        
        # Check for comprehensive comments
        comment_lines = [line for line in code.split('\n') if line.strip().startswith('#')]
        docstring_count = code.count('"""') + code.count("'''")
        
        details["comment_lines"] = len(comment_lines)
        details["has_docstrings"] = docstring_count >= 2
        
        if len(comment_lines) == 0 and docstring_count == 0:
            errors.append(f"{context}: Code lacks comments and documentation")
        elif len(comment_lines) < 3 and docstring_count < 2:
            warnings.append(f"{context}: Code has minimal comments/documentation")
        
        # Check for security best practices
        security_issues = []
        
        # Hardcoded credentials - check for patterns with or without spaces
        credential_patterns = ["password", "api_key", "secret", "token"]
        for pattern in credential_patterns:
            # Check for assignment patterns like: api_key = "..." or api_key="..."
            if f"{pattern} =" in code.lower() or f"{pattern}=" in code.lower():
                # Check if it's using environment variables
                if "os.getenv" not in code and "os.environ" not in code:
                    security_issues.append("Potential hardcoded credentials")
                    break  # Only report once
        
        # SQL injection risk
        if "execute(" in code and "%" in code and "format" in code:
            security_issues.append("Potential SQL injection risk (string formatting in queries)")
        
        # Unsafe eval/exec
        if "eval(" in code or "exec(" in code:
            security_issues.append("Use of eval() or exec() is unsafe")
        
        details["security_issues"] = security_issues
        
        if security_issues:
            for issue in security_issues:
                errors.append(f"{context}: Security issue - {issue}")
        
        # Check for NVIDIA platform usage
        nvidia_platforms = ["NIM", "NeMo", "TensorRT", "Triton", "build.nvidia.com"]
        uses_nvidia = any(platform in code for platform in nvidia_platforms)
        details["uses_nvidia_platform"] = uses_nvidia
        
        if not uses_nvidia and "nvidia" in context.lower():
            warnings.append(f"{context}: Expected NVIDIA platform usage but none found")
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            details=details
        )
    
    def validate_error_handling_patterns(self, code: str, context: str = "") -> ValidationResult:
        """
        Validate specific error handling patterns.
        
        Requirements: 15.6, 15.7, 15.8
        
        Args:
            code: Code string to validate
            context: Context description
        """
        errors = []
        warnings = []
        details = {"context": context}
        
        # Check for retry logic
        has_retry = any(pattern in code for pattern in ["retry", "max_retries", "attempt", "backoff"])
        details["has_retry_logic"] = has_retry
        
        # Check for circuit breaker pattern
        has_circuit_breaker = any(pattern in code for pattern in [
            "circuit", "breaker", "failure_threshold", "timeout"
        ])
        details["has_circuit_breaker"] = has_circuit_breaker
        
        # Check for graceful failure recovery
        has_graceful_failure = any(pattern in code for pattern in [
            "fallback", "default", "recover", "except Exception"
        ])
        details["has_graceful_failure"] = has_graceful_failure
        
        # Determine if patterns are needed based on code content
        needs_retry = any(pattern in code for pattern in [
            "requests.", "http", "api", "connect(", "provision"
        ])
        
        needs_circuit_breaker = any(pattern in code for pattern in [
            "external", "service", "api", "microservice"
        ])
        
        needs_graceful_failure = "try:" in code and "except" in code
        
        details["needs_retry"] = needs_retry
        details["needs_circuit_breaker"] = needs_circuit_breaker
        details["needs_graceful_failure"] = needs_graceful_failure
        
        # Validate patterns are present when needed
        if needs_retry and not has_retry:
            warnings.append(
                f"{context}: Code makes external calls but lacks retry logic"
            )
        
        if needs_circuit_breaker and not has_circuit_breaker:
            warnings.append(
                f"{context}: Code calls external services but lacks circuit breaker pattern"
            )
        
        if needs_graceful_failure and not has_graceful_failure:
            errors.append(
                f"{context}: Code has try-except blocks but lacks graceful failure recovery"
            )
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            details=details
        )
    
    def validate_all_code_examples(self) -> ValidationResult:
        """Validate all code examples in the course."""
        all_errors = []
        all_warnings = []
        all_details = {"modules": [], "labs": []}
        
        # Validate module platform demos
        for module in self.course.modules:
            for demo in module.platform_demos:
                for filename, code in demo.code_examples.items():
                    context = f"Module {module.module_id} - {demo.title} - {filename}"
                    
                    # Validate error handling
                    error_result = self.validate_code_example_error_handling(code, context)
                    all_errors.extend(error_result.errors)
                    all_warnings.extend(error_result.warnings)
                    
                    # Validate error handling patterns
                    pattern_result = self.validate_error_handling_patterns(code, context)
                    all_errors.extend(pattern_result.errors)
                    all_warnings.extend(pattern_result.warnings)
                    
                    all_details["modules"].append({
                        "module_id": module.module_id,
                        "demo_title": demo.title,
                        "filename": filename,
                        "error_handling": error_result.details,
                        "patterns": pattern_result.details,
                        "is_valid": error_result.is_valid and pattern_result.is_valid
                    })
        
        # Validate lab code
        for lab_id, lab in self.labs.items():
            # Validate starter code
            for filename, code in lab.starter_code.items():
                context = f"Lab {lab_id} - Starter - {filename}"
                
                error_result = self.validate_code_example_error_handling(code, context)
                all_errors.extend(error_result.errors)
                all_warnings.extend(error_result.warnings)
                
                pattern_result = self.validate_error_handling_patterns(code, context)
                all_errors.extend(pattern_result.errors)
                all_warnings.extend(pattern_result.warnings)
                
                all_details["labs"].append({
                    "lab_id": lab_id,
                    "code_type": "starter",
                    "filename": filename,
                    "error_handling": error_result.details,
                    "patterns": pattern_result.details,
                    "is_valid": error_result.is_valid and pattern_result.is_valid
                })
            
            # Validate solution code
            for filename, code in lab.solution_code.items():
                context = f"Lab {lab_id} - Solution - {filename}"
                
                error_result = self.validate_code_example_error_handling(code, context)
                all_errors.extend(error_result.errors)
                all_warnings.extend(error_result.warnings)
                
                pattern_result = self.validate_error_handling_patterns(code, context)
                all_errors.extend(pattern_result.errors)
                all_warnings.extend(pattern_result.warnings)
                
                all_details["labs"].append({
                    "lab_id": lab_id,
                    "code_type": "solution",
                    "filename": filename,
                    "error_handling": error_result.details,
                    "patterns": pattern_result.details,
                    "is_valid": error_result.is_valid and pattern_result.is_valid
                })
        
        is_valid = len(all_errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=all_errors,
            warnings=all_warnings,
            details=all_details
        )


class ContentValidator:
    """Main content validation orchestrator."""
    
    def __init__(self, course: Course, labs: Optional[Dict[str, HandsOnLab]] = None):
        """
        Initialize content validator.
        
        Args:
            course: Course instance to validate
            labs: Optional dictionary of labs (lab_id -> HandsOnLab)
        """
        self.course = course
        self.labs = labs or {}
        
        self.blueprint_validator = ExamBlueprintValidator(course)
        self.module_validator = ModuleCompletenessValidator(course)
        self.lab_validator = LabRequirementsValidator(self.labs)
        self.code_quality_validator = CodeQualityValidator(course, labs)
    
    def validate_all(self) -> ValidationResult:
        """Run all content validations."""
        all_errors = []
        all_warnings = []
        all_details = {}
        
        # Validate exam blueprint alignment
        blueprint_result = self.blueprint_validator.validate_all()
        all_errors.extend(blueprint_result.errors)
        all_warnings.extend(blueprint_result.warnings)
        all_details["exam_blueprint_alignment"] = blueprint_result.details
        
        # Validate module completeness
        module_result = self.module_validator.validate_all_modules()
        all_errors.extend(module_result.errors)
        all_warnings.extend(module_result.warnings)
        all_details["module_completeness"] = module_result.details
        
        # Validate lab requirements
        if self.labs:
            lab_result = self.lab_validator.validate_all_labs()
            all_errors.extend(lab_result.errors)
            all_warnings.extend(lab_result.warnings)
            all_details["lab_requirements"] = lab_result.details
        
        # Validate code quality
        code_quality_result = self.code_quality_validator.validate_all_code_examples()
        all_errors.extend(code_quality_result.errors)
        all_warnings.extend(code_quality_result.warnings)
        all_details["code_quality"] = code_quality_result.details
        
        is_valid = len(all_errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=all_errors,
            warnings=all_warnings,
            details=all_details
        )
    
    def generate_report(self) -> str:
        """Generate a comprehensive validation report."""
        result = self.validate_all()
        
        report = "=" * 80 + "\n"
        report += "COURSE CONTENT VALIDATION REPORT\n"
        report += "=" * 80 + "\n\n"
        
        report += f"Overall Status: {'PASS' if result.is_valid else 'FAIL'}\n"
        report += f"Total Errors: {len(result.errors)}\n"
        report += f"Total Warnings: {len(result.warnings)}\n"
        report += "\n"
        
        if result.errors:
            report += "-" * 80 + "\n"
            report += "ERRORS\n"
            report += "-" * 80 + "\n"
            for i, error in enumerate(result.errors, 1):
                report += f"{i}. {error}\n"
            report += "\n"
        
        if result.warnings:
            report += "-" * 80 + "\n"
            report += "WARNINGS\n"
            report += "-" * 80 + "\n"
            for i, warning in enumerate(result.warnings, 1):
                report += f"{i}. {warning}\n"
            report += "\n"
        
        # Add summary details
        report += "-" * 80 + "\n"
        report += "SUMMARY\n"
        report += "-" * 80 + "\n"
        
        if "exam_blueprint_alignment" in result.details:
            bp_details = result.details["exam_blueprint_alignment"]
            if "topic_coverage" in bp_details:
                coverage = bp_details["topic_coverage"]
                report += f"Topic Coverage: {coverage.get('coverage_percentage', 0):.1f}%\n"
            
            if "time_allocation" in bp_details:
                allocation = bp_details["time_allocation"]
                report += f"Total Course Hours: {allocation.get('total_hours', 0):.1f}\n"
        
        if "module_completeness" in result.details:
            mod_details = result.details["module_completeness"]
            if "modules" in mod_details:
                total_modules = len(mod_details["modules"])
                valid_modules = sum(1 for m in mod_details["modules"] if m.get("is_valid", False))
                report += f"Valid Modules: {valid_modules}/{total_modules}\n"
        
        if "lab_requirements" in result.details:
            lab_details = result.details["lab_requirements"]
            if "labs" in lab_details:
                total_labs = len(lab_details["labs"])
                valid_labs = sum(1 for l in lab_details["labs"] if l.get("is_valid", False))
                report += f"Valid Labs: {valid_labs}/{total_labs}\n"
        
        if "code_quality" in result.details:
            code_details = result.details["code_quality"]
            if "modules" in code_details:
                total_module_examples = len(code_details["modules"])
                valid_module_examples = sum(1 for m in code_details["modules"] if m.get("is_valid", False))
                report += f"Valid Module Code Examples: {valid_module_examples}/{total_module_examples}\n"
            if "labs" in code_details:
                total_lab_examples = len(code_details["labs"])
                valid_lab_examples = sum(1 for l in code_details["labs"] if l.get("is_valid", False))
                report += f"Valid Lab Code Examples: {valid_lab_examples}/{total_lab_examples}\n"
        
        report += "\n" + "=" * 80 + "\n"
        
        return report
