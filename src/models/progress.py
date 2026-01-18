"""Student progress tracking data model."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class StudentProgress:
    """Tracks a student's progress through the course."""
    
    student_id: str
    completed_modules: List[int] = field(default_factory=list)
    quiz_scores: Dict[str, float] = field(default_factory=dict)  # quiz_id -> score
    lab_completions: Dict[str, bool] = field(default_factory=dict)  # lab_id -> completed
    practice_exam_scores: List[float] = field(default_factory=list)
    mid_course_project_score: Optional[float] = None
    final_project_score: Optional[float] = None
    readiness_score: float = 0.0
    weak_topics: List[str] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "student_id": self.student_id,
            "completed_modules": self.completed_modules,
            "quiz_scores": self.quiz_scores,
            "lab_completions": self.lab_completions,
            "practice_exam_scores": self.practice_exam_scores,
            "mid_course_project_score": self.mid_course_project_score,
            "final_project_score": self.final_project_score,
            "readiness_score": self.readiness_score,
            "weak_topics": self.weak_topics,
            "last_updated": self.last_updated.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "StudentProgress":
        """Create from dictionary."""
        data = data.copy()
        if "last_updated" in data and isinstance(data["last_updated"], str):
            data["last_updated"] = datetime.fromisoformat(data["last_updated"])
        return cls(**data)
    
    def record_module_completion(self, module_id: int) -> bool:
        """Record completion of a module."""
        if module_id not in self.completed_modules:
            self.completed_modules.append(module_id)
            self.completed_modules.sort()
            self.last_updated = datetime.now()
            return True
        return False
    
    def record_quiz_score(self, quiz_id: str, score: float) -> bool:
        """Record a quiz score."""
        self.quiz_scores[quiz_id] = score
        self.last_updated = datetime.now()
        return True
    
    def record_lab_completion(self, lab_id: str) -> bool:
        """Record lab completion."""
        self.lab_completions[lab_id] = True
        self.last_updated = datetime.now()
        return True
    
    def record_practice_exam(self, score: float, weak_topics: Optional[List[str]] = None) -> bool:
        """
        Record a practice exam score and update weak topics.
        
        Args:
            score: The exam score (percentage)
            weak_topics: Optional list of weak topic areas from the exam
        """
        self.practice_exam_scores.append(score)
        
        # Update weak topics if provided
        if weak_topics:
            # Merge with existing weak topics (keep unique)
            all_weak_topics = set(self.weak_topics + weak_topics)
            self.weak_topics = list(all_weak_topics)
        
        self.last_updated = datetime.now()
        self._calculate_readiness()
        return True
    
    def _calculate_readiness(self) -> None:
        """Calculate certification readiness score."""
        if not self.practice_exam_scores:
            self.readiness_score = 0.0
            return
        
        # Average of practice exam scores
        avg_practice_score = sum(self.practice_exam_scores) / len(self.practice_exam_scores)
        
        # Factor in module completion
        completion_factor = len(self.completed_modules) / 13.0  # 13 total modules
        
        # Weighted readiness score
        self.readiness_score = (avg_practice_score * 0.7) + (completion_factor * 100 * 0.3)
    
    def is_certification_ready(self) -> bool:
        """Check if student is ready for certification (80%+ on practice exams)."""
        if not self.practice_exam_scores:
            return False
        
        avg_score = sum(self.practice_exam_scores) / len(self.practice_exam_scores)
        return avg_score >= 80.0
    
    def get_certification_readiness_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive certification readiness report.
        
        Returns:
            Dictionary containing:
            - is_ready: bool indicating if student meets 80% threshold
            - average_practice_score: float average of practice exam scores
            - readiness_score: float weighted readiness score
            - completed_modules: int number of completed modules
            - completion_percentage: float percentage of course completed
            - recommendations: list of personalized recommendations
        """
        if not self.practice_exam_scores:
            return {
                "is_ready": False,
                "average_practice_score": 0.0,
                "readiness_score": self.readiness_score,
                "completed_modules": len(self.completed_modules),
                "completion_percentage": self.get_completion_percentage(),
                "recommendations": [
                    "Complete at least one practice exam to assess your readiness.",
                    "Finish all course modules before attempting practice exams.",
                ]
            }
        
        avg_practice_score = sum(self.practice_exam_scores) / len(self.practice_exam_scores)
        is_ready = avg_practice_score >= 80.0
        
        recommendations = self._generate_readiness_recommendations(
            avg_practice_score,
            len(self.completed_modules),
            self.weak_topics
        )
        
        return {
            "is_ready": is_ready,
            "average_practice_score": avg_practice_score,
            "readiness_score": self.readiness_score,
            "completed_modules": len(self.completed_modules),
            "completion_percentage": self.get_completion_percentage(),
            "weak_topics": self.weak_topics,
            "recommendations": recommendations
        }
    
    def _generate_readiness_recommendations(
        self,
        avg_practice_score: float,
        completed_modules: int,
        weak_topics: List[str]
    ) -> List[str]:
        """Generate personalized recommendations for certification readiness."""
        recommendations = []
        
        # Check if ready
        if avg_practice_score >= 80.0:
            recommendations.append("Congratulations! You meet the 80% threshold for certification readiness.")
            recommendations.append("Schedule your certification exam when you feel confident.")
            
            if weak_topics:
                recommendations.append(f"Consider reviewing these topics before the exam: {', '.join(weak_topics)}")
        else:
            # Calculate gap to 80%
            gap = 80.0 - avg_practice_score
            recommendations.append(f"You need to improve your score by {gap:.1f}% to reach certification readiness.")
            
            if weak_topics:
                recommendations.append(f"Focus on improving these weak areas: {', '.join(weak_topics)}")
            
            recommendations.append("Take additional practice exams to identify knowledge gaps.")
            recommendations.append("Review module content for topics where you scored below 70%.")
        
        # Module completion recommendations
        if completed_modules < 13:
            remaining = 13 - completed_modules
            recommendations.append(f"Complete the remaining {remaining} module(s) to ensure comprehensive coverage.")
        
        # Practice exam recommendations
        num_practice_exams = len(self.practice_exam_scores)
        if num_practice_exams < 2:
            recommendations.append("Take at least 2-3 practice exams to ensure consistent performance.")
        
        # Score trend analysis
        if num_practice_exams >= 2:
            recent_score = self.practice_exam_scores[-1]
            previous_score = self.practice_exam_scores[-2]
            
            if recent_score > previous_score:
                recommendations.append("Your scores are improving! Keep up the good work.")
            elif recent_score < previous_score:
                recommendations.append("Your recent score decreased. Review the topics you struggled with.")
        
        return recommendations
    
    def get_completion_percentage(self) -> float:
        """Get overall course completion percentage."""
        return (len(self.completed_modules) / 13.0) * 100
    
    def get_progress_analytics(self) -> Dict[str, Any]:
        """
        Generate comprehensive progress analytics.
        
        Returns:
            Dictionary containing:
            - module_completion_percentage: float percentage of modules completed
            - completed_modules_count: int number of modules completed
            - total_modules: int total number of modules (13)
            - quiz_completion_percentage: float percentage of quizzes completed
            - quiz_scores_summary: dict with min, max, avg quiz scores
            - lab_completion_percentage: float percentage of labs completed
            - practice_exam_count: int number of practice exams taken
            - practice_exam_scores_summary: dict with min, max, avg practice exam scores
            - weak_topics: list of weak topic areas
            - strong_topics: list of strong topic areas (quiz scores >= 90%)
            - overall_progress_score: float weighted progress score (0-100)
            - recommendations: list of personalized recommendations
        """
        # Module completion
        module_completion_pct = self.get_completion_percentage()
        completed_modules_count = len(self.completed_modules)
        
        # Quiz completion and scores
        quiz_count = len(self.quiz_scores)
        quiz_completion_pct = (quiz_count / 13.0) * 100  # 13 modules with quizzes
        
        quiz_scores_summary = {}
        if self.quiz_scores:
            scores = list(self.quiz_scores.values())
            quiz_scores_summary = {
                "min": min(scores),
                "max": max(scores),
                "average": sum(scores) / len(scores),
                "count": len(scores)
            }
        
        # Identify strong topics from quiz scores
        strong_topics = []
        for quiz_id, score in self.quiz_scores.items():
            if score >= 90.0:
                # Extract topic from quiz_id if possible
                # This is a simplified version - real implementation might parse quiz_id
                strong_topics.append(quiz_id)
        
        # Lab completion
        lab_count = len([completed for completed in self.lab_completions.values() if completed])
        lab_completion_pct = (lab_count / 13.0) * 100  # 13 modules with labs
        
        # Practice exam scores
        practice_exam_count = len(self.practice_exam_scores)
        practice_exam_scores_summary = {}
        if self.practice_exam_scores:
            practice_exam_scores_summary = {
                "min": min(self.practice_exam_scores),
                "max": max(self.practice_exam_scores),
                "average": sum(self.practice_exam_scores) / len(self.practice_exam_scores),
                "count": len(self.practice_exam_scores)
            }
        
        # Calculate overall progress score (weighted)
        # 40% module completion, 30% quiz performance, 20% lab completion, 10% practice exams
        overall_progress_score = (
            (module_completion_pct * 0.4) +
            (quiz_scores_summary.get("average", 0) * 0.3) +
            (lab_completion_pct * 0.2) +
            (practice_exam_scores_summary.get("average", 0) * 0.1)
        )
        
        # Generate recommendations
        recommendations = self._generate_progress_recommendations(
            module_completion_pct,
            quiz_completion_pct,
            lab_completion_pct,
            practice_exam_count,
            quiz_scores_summary.get("average", 0),
            practice_exam_scores_summary.get("average", 0)
        )
        
        return {
            "module_completion_percentage": module_completion_pct,
            "completed_modules_count": completed_modules_count,
            "total_modules": 13,
            "quiz_completion_percentage": quiz_completion_pct,
            "quiz_scores_summary": quiz_scores_summary,
            "lab_completion_percentage": lab_completion_pct,
            "practice_exam_count": practice_exam_count,
            "practice_exam_scores_summary": practice_exam_scores_summary,
            "weak_topics": self.weak_topics,
            "strong_topics": strong_topics,
            "overall_progress_score": overall_progress_score,
            "recommendations": recommendations,
            "last_updated": self.last_updated.isoformat()
        }
    
    def _generate_progress_recommendations(
        self,
        module_completion_pct: float,
        quiz_completion_pct: float,
        lab_completion_pct: float,
        practice_exam_count: int,
        avg_quiz_score: float,
        avg_practice_score: float
    ) -> List[str]:
        """Generate personalized recommendations based on progress."""
        recommendations = []
        
        # Module completion recommendations
        if module_completion_pct < 50:
            recommendations.append("Focus on completing more modules to build foundational knowledge.")
        elif module_completion_pct < 100:
            remaining = 13 - len(self.completed_modules)
            recommendations.append(f"You're making good progress! Complete the remaining {remaining} module(s).")
        else:
            recommendations.append("Excellent! You've completed all course modules.")
        
        # Quiz performance recommendations
        if quiz_completion_pct < 100:
            recommendations.append("Complete all module quizzes to assess your understanding of each topic.")
        
        if avg_quiz_score > 0:
            if avg_quiz_score < 70:
                recommendations.append("Your quiz scores are below passing threshold. Review module content and retake quizzes.")
            elif avg_quiz_score < 80:
                recommendations.append("Good quiz performance! Focus on weak areas to improve further.")
            elif avg_quiz_score >= 90:
                recommendations.append("Outstanding quiz performance! You have strong grasp of the material.")
        
        # Lab completion recommendations
        if lab_completion_pct < 100:
            recommendations.append("Complete all hands-on labs to gain practical experience with NVIDIA platforms.")
        else:
            recommendations.append("Great job completing all hands-on labs!")
        
        # Practice exam recommendations
        if practice_exam_count == 0:
            recommendations.append("Take your first practice exam to assess certification readiness.")
        elif practice_exam_count < 2:
            recommendations.append("Take additional practice exams to ensure consistent performance.")
        elif practice_exam_count >= 3:
            if avg_practice_score >= 80:
                recommendations.append("You're certification ready! Consider scheduling your exam.")
            else:
                recommendations.append("Continue practicing and reviewing weak areas before attempting certification.")
        
        # Weak topics recommendations
        if self.weak_topics:
            recommendations.append(f"Review these weak areas: {', '.join(self.weak_topics[:3])}")
        
        return recommendations
