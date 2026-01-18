"""Exam blueprint data model for NCP-AAI certification alignment."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ExamBlueprint:
    """
    Represents the NVIDIA-Certified Professional: Agentic AI (NCP-AAI) exam blueprint.
    
    Defines the 10 exam topic areas with their official percentage weights.
    Used to validate course content alignment with certification requirements.
    """
    
    # Official exam topic areas with percentage weights
    OFFICIAL_TOPICS: Dict[str, float] = field(default_factory=lambda: {
        "Agent Architecture and Design": 15.0,
        "Agent Development": 15.0,
        "Evaluation and Tuning": 13.0,
        "Deployment and Scaling": 13.0,
        "Cognition, Planning, and Memory": 10.0,
        "Knowledge Integration and Data Handling": 10.0,
        "NVIDIA Platform Implementation": 7.0,
        "Run, Monitor, and Maintain": 5.0,
        "Safety, Ethics, and Compliance": 5.0,
        "Human-AI Interaction and Oversight": 5.0,
    })
    
    def __post_init__(self):
        """Validate that topic percentages are reasonable (allow for rounding)."""
        total = sum(self.OFFICIAL_TOPICS.values())
        # Allow for some flexibility in case of rounding or intentional gaps
        if total < 95.0 or total > 105.0:
            raise ValueError(f"Topic percentages should be close to 100%, got {total}%")
    
    def get_topics(self) -> List[str]:
        """Get list of all exam topic areas."""
        return list(self.OFFICIAL_TOPICS.keys())
    
    def get_topic_percentage(self, topic: str) -> float:
        """
        Get the percentage weight for a specific topic.
        
        Args:
            topic: The exam topic area name
            
        Returns:
            The percentage weight (0-100)
            
        Raises:
            KeyError: If topic is not in the official blueprint
        """
        if topic not in self.OFFICIAL_TOPICS:
            raise KeyError(f"Topic '{topic}' not found in exam blueprint")
        return self.OFFICIAL_TOPICS[topic]
    
    def get_all_topic_percentages(self) -> Dict[str, float]:
        """Get all topics with their percentage weights."""
        return self.OFFICIAL_TOPICS.copy()
    
    def validate_topic(self, topic: str) -> bool:
        """
        Validate that a topic exists in the exam blueprint.
        
        Args:
            topic: The topic name to validate
            
        Returns:
            True if topic is valid, False otherwise
        """
        return topic in self.OFFICIAL_TOPICS
    
    def calculate_topic_weight(self, topic: str, total_hours: float) -> float:
        """
        Calculate the expected hours for a topic based on total course hours.
        
        Args:
            topic: The exam topic area
            total_hours: Total instructional hours in the course
            
        Returns:
            Expected hours for this topic
        """
        percentage = self.get_topic_percentage(topic)
        return (percentage / 100.0) * total_hours
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "topics": self.OFFICIAL_TOPICS.copy()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ExamBlueprint":
        """
        Create from dictionary.
        
        Note: This will use the official topics, ignoring any provided data.
        The blueprint is fixed by NVIDIA certification requirements.
        """
        return cls()
