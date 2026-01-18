"""Assessment and question data models."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Union, Optional


@dataclass
class Question:
    """Represents an assessment question."""
    
    question_id: str
    question_text: str
    question_type: str  # "multiple_choice", "multiple_select", "scenario"
    options: List[str]
    correct_answer: Union[str, List[str]]
    explanation: str
    exam_topic: str
    difficulty: str  # "easy", "medium", "hard"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "question_id": self.question_id,
            "question_text": self.question_text,
            "question_type": self.question_type,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
            "exam_topic": self.exam_topic,
            "difficulty": self.difficulty,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Question":
        """Create from dictionary."""
        return cls(**data)
    
    def validate(self) -> bool:
        """Validate question structure."""
        valid_types = {"multiple_choice", "multiple_select", "scenario"}
        if self.question_type not in valid_types:
            raise ValueError(f"Invalid question_type: {self.question_type}")
        
        valid_difficulties = {"easy", "medium", "hard"}
        if self.difficulty not in valid_difficulties:
            raise ValueError(f"Invalid difficulty: {self.difficulty}")
        
        if not self.options:
            raise ValueError("Question must have options")
        
        return True


@dataclass
class PerformanceAnalytics:
    """Performance analytics for an assessment."""
    
    overall_score: float
    topic_breakdown: Dict[str, float]  # topic -> score percentage
    weak_areas: List[str]  # topics with < 70%
    strong_areas: List[str]  # topics with >= 90%
    difficulty_breakdown: Dict[str, float]  # difficulty -> score percentage
    question_type_breakdown: Dict[str, float]  # question_type -> score percentage
    recommendations: List[str]
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "overall_score": self.overall_score,
            "topic_breakdown": self.topic_breakdown,
            "weak_areas": self.weak_areas,
            "strong_areas": self.strong_areas,
            "difficulty_breakdown": self.difficulty_breakdown,
            "question_type_breakdown": self.question_type_breakdown,
            "recommendations": self.recommendations,
        }


@dataclass
class GradingResult:
    """Result of grading an assessment."""
    
    student_id: str
    assessment_id: str
    score: float  # percentage
    correct_count: int
    total_count: int
    time_taken: int  # minutes
    topic_breakdown: Dict[str, float]  # topic -> score percentage
    weak_areas: List[str]
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "student_id": self.student_id,
            "assessment_id": self.assessment_id,
            "score": self.score,
            "correct_count": self.correct_count,
            "total_count": self.total_count,
            "time_taken": self.time_taken,
            "topic_breakdown": self.topic_breakdown,
            "weak_areas": self.weak_areas,
        }
    
    def get_performance_analytics(self, questions: List[Question], answers: Dict[str, Any]) -> PerformanceAnalytics:
        """Generate comprehensive performance analytics."""
        # Identify strong areas (>= 90%)
        strong_areas = [topic for topic, score in self.topic_breakdown.items() if score >= 90.0]
        
        # Calculate difficulty breakdown
        difficulty_scores: Dict[str, List[float]] = {}
        for question in questions:
            student_answer = answers.get(question.question_id)
            is_correct = student_answer == question.correct_answer
            
            if question.difficulty not in difficulty_scores:
                difficulty_scores[question.difficulty] = []
            difficulty_scores[question.difficulty].append(1.0 if is_correct else 0.0)
        
        difficulty_breakdown = {
            difficulty: (sum(scores) / len(scores)) * 100
            for difficulty, scores in difficulty_scores.items()
        }
        
        # Calculate question type breakdown
        type_scores: Dict[str, List[float]] = {}
        for question in questions:
            student_answer = answers.get(question.question_id)
            is_correct = student_answer == question.correct_answer
            
            if question.question_type not in type_scores:
                type_scores[question.question_type] = []
            type_scores[question.question_type].append(1.0 if is_correct else 0.0)
        
        question_type_breakdown = {
            qtype: (sum(scores) / len(scores)) * 100
            for qtype, scores in type_scores.items()
        }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            self.score,
            self.weak_areas,
            difficulty_breakdown,
            question_type_breakdown
        )
        
        return PerformanceAnalytics(
            overall_score=self.score,
            topic_breakdown=self.topic_breakdown,
            weak_areas=self.weak_areas,
            strong_areas=strong_areas,
            difficulty_breakdown=difficulty_breakdown,
            question_type_breakdown=question_type_breakdown,
            recommendations=recommendations
        )
    
    def _generate_recommendations(
        self,
        overall_score: float,
        weak_areas: List[str],
        difficulty_breakdown: Dict[str, float],
        question_type_breakdown: Dict[str, float]
    ) -> List[str]:
        """Generate personalized recommendations based on performance."""
        recommendations = []
        
        # Overall score recommendations
        if overall_score < 70:
            recommendations.append("Review all course materials and focus on fundamental concepts.")
        elif overall_score < 80:
            recommendations.append("You're close to certification readiness. Focus on weak areas to improve your score.")
        elif overall_score >= 80:
            recommendations.append("Great job! You're ready for certification. Consider taking the exam soon.")
        
        # Topic-specific recommendations
        if weak_areas:
            recommendations.append(f"Focus on these weak areas: {', '.join(weak_areas)}")
            recommendations.append("Review module content and complete additional practice exercises for weak topics.")
        
        # Difficulty-specific recommendations
        if "hard" in difficulty_breakdown and difficulty_breakdown["hard"] < 60:
            recommendations.append("Practice more challenging questions to improve performance on difficult topics.")
        
        if "easy" in difficulty_breakdown and difficulty_breakdown["easy"] < 80:
            recommendations.append("Review fundamental concepts - you should be scoring higher on easy questions.")
        
        # Question type recommendations
        if "scenario" in question_type_breakdown and question_type_breakdown["scenario"] < 70:
            recommendations.append("Practice scenario-based questions to improve real-world application skills.")
        
        if "multiple_select" in question_type_breakdown and question_type_breakdown["multiple_select"] < 70:
            recommendations.append("Pay careful attention to multiple-select questions - read all options thoroughly.")
        
        return recommendations


@dataclass
class Assessment:
    """Represents an assessment (quiz, exam, or project)."""
    
    assessment_id: str
    assessment_type: str  # "module_quiz", "mid_course_project", "final_project", "practice_exam"
    questions: List[Question]
    passing_score: float  # percentage
    time_limit: int  # minutes
    exam_topics_covered: Dict[str, float]  # topic -> percentage
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "assessment_id": self.assessment_id,
            "assessment_type": self.assessment_type,
            "questions": [q.to_dict() for q in self.questions],
            "passing_score": self.passing_score,
            "time_limit": self.time_limit,
            "exam_topics_covered": self.exam_topics_covered,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Assessment":
        """Create from dictionary."""
        data = data.copy()
        data["questions"] = [Question.from_dict(q) for q in data["questions"]]
        return cls(**data)
    
    def validate(self) -> bool:
        """Validate assessment structure."""
        valid_types = {"module_quiz", "mid_course_project", "final_project", "practice_exam"}
        if self.assessment_type not in valid_types:
            raise ValueError(f"Invalid assessment_type: {self.assessment_type}")
        
        # Validate question count based on type
        if self.assessment_type == "module_quiz":
            if not (5 <= len(self.questions) <= 10):
                raise ValueError(f"Module quiz must have 5-10 questions, got {len(self.questions)}")
        elif self.assessment_type == "practice_exam":
            if not (60 <= len(self.questions) <= 70):
                raise ValueError(f"Practice exam must have 60-70 questions, got {len(self.questions)}")
        
        # Validate all questions
        for question in self.questions:
            question.validate()
        
        return True
    
    def grade_submission(self, answers: Dict[str, Any]) -> GradingResult:
        """Grade a student's submission."""
        correct_count = 0
        topic_scores: Dict[str, List[float]] = {}
        
        for question in self.questions:
            student_answer = answers.get(question.question_id)
            is_correct = student_answer == question.correct_answer
            
            if is_correct:
                correct_count += 1
            
            # Track by topic
            topic = question.exam_topic
            if topic not in topic_scores:
                topic_scores[topic] = []
            topic_scores[topic].append(1.0 if is_correct else 0.0)
        
        # Calculate topic breakdown
        topic_breakdown = {
            topic: sum(scores) / len(scores) * 100
            for topic, scores in topic_scores.items()
        }
        
        # Identify weak areas (< 70%)
        weak_areas = [topic for topic, score in topic_breakdown.items() if score < 70.0]
        
        score = (correct_count / len(self.questions)) * 100
        
        return GradingResult(
            student_id="",  # To be filled by caller
            assessment_id=self.assessment_id,
            score=score,
            correct_count=correct_count,
            total_count=len(self.questions),
            time_taken=0,  # To be filled by caller
            topic_breakdown=topic_breakdown,
            weak_areas=weak_areas,
        )
    
    def get_performance_analytics(self, answers: Dict[str, Any]) -> PerformanceAnalytics:
        """Generate comprehensive performance analytics for a submission."""
        result = self.grade_submission(answers)
        return result.get_performance_analytics(self.questions, answers)
