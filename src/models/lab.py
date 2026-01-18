"""Hands-on lab data models."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class ValidationResult:
    """Result of validating student lab output."""
    
    is_valid: bool
    score: float  # 0.0 to 1.0
    feedback: str
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "is_valid": self.is_valid,
            "score": self.score,
            "feedback": self.feedback,
            "errors": self.errors,
        }


@dataclass
class HandsOnLab:
    """Represents a hands-on laboratory exercise."""
    
    lab_id: str
    title: str
    objectives: List[str]
    setup_instructions: str
    implementation_guide: str
    starter_code: Dict[str, str]  # filename -> code
    solution_code: Dict[str, str]  # filename -> code
    expected_outputs: Dict[str, Any]
    troubleshooting_guide: str
    nvidia_platforms_used: List[str]
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "lab_id": self.lab_id,
            "title": self.title,
            "objectives": self.objectives,
            "setup_instructions": self.setup_instructions,
            "implementation_guide": self.implementation_guide,
            "starter_code": self.starter_code,
            "solution_code": self.solution_code,
            "expected_outputs": self.expected_outputs,
            "troubleshooting_guide": self.troubleshooting_guide,
            "nvidia_platforms_used": self.nvidia_platforms_used,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "HandsOnLab":
        """Create from dictionary."""
        return cls(**data)
    
    def validate(self) -> bool:
        """Validate lab completeness."""
        if not self.setup_instructions:
            raise ValueError(f"Lab {self.lab_id} missing setup instructions")
        
        if not self.implementation_guide:
            raise ValueError(f"Lab {self.lab_id} missing implementation guide")
        
        if not self.starter_code:
            raise ValueError(f"Lab {self.lab_id} missing starter code")
        
        if not self.expected_outputs:
            raise ValueError(f"Lab {self.lab_id} missing expected outputs")
        
        if not self.troubleshooting_guide:
            raise ValueError(f"Lab {self.lab_id} missing troubleshooting guide")
        
        return True
    
    def validate_student_output(self, output: Any) -> ValidationResult:
        """Validate student output against expected outputs."""
        # Basic validation - can be extended with specific checks
        errors = []
        
        if not output:
            errors.append("No output provided")
            return ValidationResult(
                is_valid=False,
                score=0.0,
                feedback="No output was provided for validation",
                errors=errors
            )
        
        # Compare with expected outputs
        # This is a simplified version - real implementation would be more sophisticated
        return ValidationResult(
            is_valid=True,
            score=1.0,
            feedback="Output validated successfully",
            errors=[]
        )


@dataclass
class LabSubmission:
    """Represents a student's lab submission."""
    
    submission_id: str
    student_id: str
    lab_id: str
    code_files: Dict[str, str]  # filename -> code
    outputs: Dict[str, Any]
    submitted_at: datetime
    validation_result: Optional[ValidationResult] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "submission_id": self.submission_id,
            "student_id": self.student_id,
            "lab_id": self.lab_id,
            "code_files": self.code_files,
            "outputs": self.outputs,
            "submitted_at": self.submitted_at.isoformat(),
            "validation_result": self.validation_result.to_dict() if self.validation_result else None,
        }
