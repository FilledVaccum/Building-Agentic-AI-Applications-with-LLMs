"""Course data model with exam blueprint alignment functionality."""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from .module import Module
from .exam_blueprint import ExamBlueprint


@dataclass
class Course:
    """
    Represents the complete course with all modules.
    
    Provides functionality to map module content to exam blueprint topics
    and validate alignment with certification requirements.
    """
    
    modules: List[Module]
    blueprint: ExamBlueprint = field(default_factory=ExamBlueprint)
    
    def get_total_duration(self) -> float:
        """Calculate total instructional hours across all modules."""
        return sum(module.duration_hours for module in self.modules)
    
    def get_module_by_id(self, module_id: int) -> Module:
        """
        Get a module by its ID.
        
        Args:
            module_id: The module identifier
            
        Returns:
            The module with the given ID
            
        Raises:
            ValueError: If module not found
        """
        for module in self.modules:
            if module.module_id == module_id:
                return module
        raise ValueError(f"Module {module_id} not found")
    
    def map_modules_to_blueprint(self) -> Dict[str, List[int]]:
        """
        Map exam topics to the modules that cover them.
        
        Returns:
            Dictionary mapping topic names to lists of module IDs
        """
        topic_to_modules: Dict[str, List[int]] = {
            topic: [] for topic in self.blueprint.get_topics()
        }
        
        for module in self.modules:
            for topic in module.exam_topics.keys():
                if topic in topic_to_modules:
                    topic_to_modules[topic].append(module.module_id)
        
        return topic_to_modules
    
    def calculate_topic_time_allocation(self) -> Dict[str, float]:
        """
        Calculate total time allocated to each exam topic across all modules.
        
        Returns:
            Dictionary mapping topic names to total hours allocated
        """
        topic_hours: Dict[str, float] = {
            topic: 0.0 for topic in self.blueprint.get_topics()
        }
        
        for module in self.modules:
            for topic, percentage in module.exam_topics.items():
                if topic in topic_hours:
                    # Calculate hours for this topic in this module
                    # percentage is the portion of this module dedicated to this topic
                    hours = module.duration_hours * (percentage / 100.0)
                    topic_hours[topic] += hours
        
        return topic_hours
    
    def calculate_topic_percentages(self) -> Dict[str, float]:
        """
        Calculate the percentage of total course time allocated to each topic.
        
        Returns:
            Dictionary mapping topic names to percentage of total course time
        """
        topic_hours = self.calculate_topic_time_allocation()
        total_hours = self.get_total_duration()
        
        if total_hours == 0:
            return {topic: 0.0 for topic in self.blueprint.get_topics()}
        
        return {
            topic: (hours / total_hours) * 100.0
            for topic, hours in topic_hours.items()
        }
    
    def validate_proportional_weighting(self, tolerance: float = 2.0) -> Tuple[bool, Dict[str, float]]:
        """
        Validate that topic time allocation matches blueprint percentages within tolerance.
        
        Args:
            tolerance: Maximum allowed deviation in percentage points (default ±2%)
            
        Returns:
            Tuple of (is_valid, deviations_dict)
            - is_valid: True if all topics are within tolerance
            - deviations_dict: Mapping of topic to deviation from blueprint percentage
        """
        actual_percentages = self.calculate_topic_percentages()
        blueprint_percentages = self.blueprint.get_all_topic_percentages()
        
        deviations: Dict[str, float] = {}
        is_valid = True
        
        for topic in self.blueprint.get_topics():
            actual = actual_percentages.get(topic, 0.0)
            expected = blueprint_percentages[topic]
            deviation = actual - expected
            deviations[topic] = deviation
            
            if abs(deviation) > tolerance:
                is_valid = False
        
        return is_valid, deviations
    
    def get_coverage_report(self) -> Dict[str, any]:
        """
        Generate a comprehensive coverage report for exam blueprint alignment.
        
        Returns:
            Dictionary containing:
            - total_hours: Total course duration
            - topic_hours: Hours per topic
            - topic_percentages: Actual percentages per topic
            - blueprint_percentages: Expected percentages per topic
            - deviations: Deviation from blueprint per topic
            - modules_per_topic: Module IDs covering each topic
            - is_aligned: Whether course meets alignment requirements
        """
        topic_hours = self.calculate_topic_time_allocation()
        topic_percentages = self.calculate_topic_percentages()
        blueprint_percentages = self.blueprint.get_all_topic_percentages()
        is_aligned, deviations = self.validate_proportional_weighting()
        modules_per_topic = self.map_modules_to_blueprint()
        
        return {
            "total_hours": self.get_total_duration(),
            "topic_hours": topic_hours,
            "topic_percentages": topic_percentages,
            "blueprint_percentages": blueprint_percentages,
            "deviations": deviations,
            "modules_per_topic": modules_per_topic,
            "is_aligned": is_aligned,
        }
    
    def validate_blueprint_coverage(self) -> Tuple[bool, List[str]]:
        """
        Validate that all exam topics are covered by at least one module.
        
        Returns:
            Tuple of (is_complete, missing_topics)
            - is_complete: True if all topics are covered
            - missing_topics: List of topics not covered by any module
        """
        covered_topics = set()
        
        for module in self.modules:
            covered_topics.update(module.exam_topics.keys())
        
        blueprint_topics = set(self.blueprint.get_topics())
        missing_topics = list(blueprint_topics - covered_topics)
        
        return len(missing_topics) == 0, missing_topics
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "modules": [module.to_dict() for module in self.modules],
            "blueprint": self.blueprint.to_dict(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Course":
        """Create from dictionary."""
        modules = [Module.from_dict(m) for m in data["modules"]]
        blueprint = ExamBlueprint.from_dict(data.get("blueprint", {}))
        return cls(modules=modules, blueprint=blueprint)
