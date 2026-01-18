"""Module data model and related classes."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json


@dataclass
class LearningObjective:
    """Represents a measurable learning outcome."""
    
    objective_id: str
    description: str
    exam_topics: List[str]
    bloom_level: str  # "remember", "understand", "apply", "analyze", "evaluate", "create"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "objective_id": self.objective_id,
            "description": self.description,
            "exam_topics": self.exam_topics,
            "bloom_level": self.bloom_level,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "LearningObjective":
        """Create from dictionary."""
        return cls(**data)
    
    def validate(self) -> bool:
        """Validate the learning objective."""
        valid_bloom_levels = {"remember", "understand", "apply", "analyze", "evaluate", "create"}
        if self.bloom_level not in valid_bloom_levels:
            raise ValueError(f"Invalid bloom_level: {self.bloom_level}")
        if not self.exam_topics:
            raise ValueError("Learning objective must map to at least one exam topic")
        return True


@dataclass
class PlatformDemo:
    """Represents an NVIDIA platform demonstration."""
    
    demo_id: str
    title: str
    platform: str  # "NIM", "NeMo", "TensorRT-LLM", "Triton", "build.nvidia.com"
    description: str
    code_examples: Dict[str, str]  # filename -> code
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "demo_id": self.demo_id,
            "title": self.title,
            "platform": self.platform,
            "description": self.description,
            "code_examples": self.code_examples,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PlatformDemo":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class Module:
    """Represents a course module with all components."""
    
    module_id: int
    title: str
    duration_hours: float
    exam_topics: Dict[str, float]  # topic -> percentage
    learning_objectives: List[LearningObjective]
    prerequisites: List[str]
    theoretical_content: str
    platform_demos: List[PlatformDemo]
    lab_id: Optional[str] = None
    assessment_id: Optional[str] = None
    additional_resources: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "module_id": self.module_id,
            "title": self.title,
            "duration_hours": self.duration_hours,
            "exam_topics": self.exam_topics,
            "learning_objectives": [obj.to_dict() for obj in self.learning_objectives],
            "prerequisites": self.prerequisites,
            "theoretical_content": self.theoretical_content,
            "platform_demos": [demo.to_dict() for demo in self.platform_demos],
            "lab_id": self.lab_id,
            "assessment_id": self.assessment_id,
            "additional_resources": self.additional_resources,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Module":
        """Create from dictionary."""
        data = data.copy()
        data["learning_objectives"] = [
            LearningObjective.from_dict(obj) for obj in data["learning_objectives"]
        ]
        data["platform_demos"] = [
            PlatformDemo.from_dict(demo) for demo in data["platform_demos"]
        ]
        return cls(**data)
    
    def validate(self) -> bool:
        """Validate module structure consistency."""
        # Validate required components exist
        if not self.learning_objectives:
            raise ValueError(f"Module {self.module_id} missing learning objectives")
        
        if not self.theoretical_content:
            raise ValueError(f"Module {self.module_id} missing theoretical content")
        
        if not self.platform_demos:
            raise ValueError(f"Module {self.module_id} missing NVIDIA platform integration")
        
        if not self.lab_id:
            raise ValueError(f"Module {self.module_id} missing hands-on lab")
        
        if not self.assessment_id:
            raise ValueError(f"Module {self.module_id} missing assessment")
        
        # Validate learning objectives
        for obj in self.learning_objectives:
            obj.validate()
        
        # Validate exam topics
        if not self.exam_topics:
            raise ValueError(f"Module {self.module_id} must map to exam topics")
        
        return True
    
    def get_exam_topic_mapping(self) -> Dict[str, float]:
        """Get exam topic mapping."""
        return self.exam_topics.copy()
