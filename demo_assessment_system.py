#!/usr/bin/env python3
"""
Demonstration of the Assessment System

This script demonstrates the key features of the assessment system:
1. Question and Assessment classes with validation
2. Automated grading with topic breakdowns
3. Performance analytics generation
4. Certification readiness calculation
"""

from src.models.assessment import Assessment, Question, PerformanceAnalytics
from src.models.progress import StudentProgress


def demo_module_quiz():
    """Demonstrate module quiz grading and analytics."""
    print("=" * 70)
    print("DEMO 1: Module Quiz Grading and Analytics")
    print("=" * 70)
    
    # Create a sample module quiz
    questions = [
        Question(
            question_id="Q1",
            question_text="What is the primary purpose of agent abstraction?",
            question_type="multiple_choice",
            options=[
                "To make code more complex",
                "To decompose tasks into manageable components",
                "To increase latency",
                "To reduce functionality"
            ],
            correct_answer="To decompose tasks into manageable components",
            explanation="Agent abstraction helps break down complex tasks into simpler, manageable components.",
            exam_topic="Agent Architecture and Design",
            difficulty="easy"
        ),
        Question(
            question_id="Q2",
            question_text="Which NVIDIA platform is used for inference microservices?",
            question_type="multiple_choice",
            options=["NIM", "PyTorch", "TensorFlow", "Keras"],
            correct_answer="NIM",
            explanation="NVIDIA NIM (NVIDIA Inference Microservices) is designed for inference.",
            exam_topic="NVIDIA Platform Implementation",
            difficulty="medium"
        ),
        Question(
            question_id="Q3",
            question_text="What is the minimum passing score for module quizzes?",
            question_type="multiple_choice",
            options=["60%", "70%", "80%", "90%"],
            correct_answer="70%",
            explanation="Module quizzes require a 70% score to pass.",
            exam_topic="Evaluation and Tuning",
            difficulty="easy"
        ),
        Question(
            question_id="Q4",
            question_text="Which frameworks support multi-agent systems?",
            question_type="multiple_select",
            options=["LangGraph", "CrewAI", "AutoGen", "NumPy"],
            correct_answer=["LangGraph", "CrewAI", "AutoGen"],
            explanation="LangGraph, CrewAI, and AutoGen are multi-agent frameworks.",
            exam_topic="Agent Development",
            difficulty="hard"
        ),
        Question(
            question_id="Q5",
            question_text="What is RAG?",
            question_type="multiple_choice",
            options=[
                "Random Access Generation",
                "Retrieval-Augmented Generation",
                "Rapid Agent Gateway",
                "Resource Allocation Graph"
            ],
            correct_answer="Retrieval-Augmented Generation",
            explanation="RAG stands for Retrieval-Augmented Generation.",
            exam_topic="Knowledge Integration and Data Handling",
            difficulty="medium"
        ),
    ]
    
    quiz = Assessment(
        assessment_id="module_01_quiz",
        assessment_type="module_quiz",
        questions=questions,
        passing_score=70.0,
        time_limit=30,
        exam_topics_covered={
            "Agent Architecture and Design": 20.0,
            "NVIDIA Platform Implementation": 20.0,
            "Evaluation and Tuning": 20.0,
            "Agent Development": 20.0,
            "Knowledge Integration and Data Handling": 20.0,
        }
    )
    
    # Validate the quiz
    print(f"\nQuiz ID: {quiz.assessment_id}")
    print(f"Type: {quiz.assessment_type}")
    print(f"Questions: {len(quiz.questions)}")
    print(f"Passing Score: {quiz.passing_score}%")
    print(f"Time Limit: {quiz.time_limit} minutes")
    print(f"Valid: {quiz.validate()}")
    
    # Student submits answers (3 correct, 2 wrong)
    student_answers = {
        "Q1": "To decompose tasks into manageable components",  # Correct
        "Q2": "PyTorch",  # Wrong
        "Q3": "70%",  # Correct
        "Q4": ["LangGraph", "CrewAI"],  # Wrong (missing AutoGen)
        "Q5": "Retrieval-Augmented Generation",  # Correct
    }
    
    # Grade the submission
    result = quiz.grade_submission(student_answers)
    result.student_id = "student_123"
    result.time_taken = 25
    
    print(f"\n--- Grading Results ---")
    print(f"Student ID: {result.student_id}")
    print(f"Score: {result.score:.2f}%")
    print(f"Correct: {result.correct_count}/{result.total_count}")
    print(f"Time Taken: {result.time_taken} minutes")
    print(f"Passed: {'Yes' if result.score >= quiz.passing_score else 'No'}")
    
    print(f"\n--- Topic Breakdown ---")
    for topic, score in result.topic_breakdown.items():
        print(f"  {topic}: {score:.1f}%")
    
    if result.weak_areas:
        print(f"\n--- Weak Areas (< 70%) ---")
        for topic in result.weak_areas:
            print(f"  - {topic}")
    
    # Generate performance analytics
    analytics = quiz.get_performance_analytics(student_answers)
    
    print(f"\n--- Performance Analytics ---")
    print(f"Overall Score: {analytics.overall_score:.2f}%")
    
    print(f"\nDifficulty Breakdown:")
    for difficulty, score in analytics.difficulty_breakdown.items():
        print(f"  {difficulty}: {score:.1f}%")
    
    print(f"\nQuestion Type Breakdown:")
    for qtype, score in analytics.question_type_breakdown.items():
        print(f"  {qtype}: {score:.1f}%")
    
    if analytics.strong_areas:
        print(f"\nStrong Areas (>= 90%):")
        for topic in analytics.strong_areas:
            print(f"  - {topic}")
    
    print(f"\nRecommendations:")
    for i, rec in enumerate(analytics.recommendations, 1):
        print(f"  {i}. {rec}")


def demo_certification_readiness():
    """Demonstrate certification readiness calculation."""
    print("\n\n" + "=" * 70)
    print("DEMO 2: Certification Readiness Calculation")
    print("=" * 70)
    
    # Create student progress
    progress = StudentProgress(student_id="student_456")
    
    # Record module completions
    for module_id in range(1, 11):  # Completed 10 out of 13 modules
        progress.record_module_completion(module_id)
    
    print(f"\nStudent ID: {progress.student_id}")
    print(f"Completed Modules: {len(progress.completed_modules)}/13")
    print(f"Completion: {progress.get_completion_percentage():.1f}%")
    
    # Record practice exam scores
    print(f"\n--- Recording Practice Exam Scores ---")
    exam_scores = [75.0, 78.0, 82.0]
    weak_topics_per_exam = [
        ["Agent Development", "Deployment and Scaling"],
        ["Deployment and Scaling", "NVIDIA Platform Implementation"],
        ["NVIDIA Platform Implementation"],
    ]
    
    for i, (score, weak_topics) in enumerate(zip(exam_scores, weak_topics_per_exam), 1):
        progress.record_practice_exam(score, weak_topics)
        print(f"  Practice Exam {i}: {score}%")
    
    # Check certification readiness
    is_ready = progress.is_certification_ready()
    print(f"\n--- Certification Readiness ---")
    print(f"Ready for Certification: {'Yes' if is_ready else 'No'}")
    print(f"Readiness Score: {progress.readiness_score:.2f}")
    
    # Get detailed readiness report
    report = progress.get_certification_readiness_report()
    
    print(f"\n--- Detailed Readiness Report ---")
    print(f"Average Practice Score: {report['average_practice_score']:.2f}%")
    print(f"Threshold: 80%")
    print(f"Gap: {80.0 - report['average_practice_score']:.2f}%")
    
    if report['weak_topics']:
        print(f"\nWeak Topics:")
        for topic in report['weak_topics']:
            print(f"  - {topic}")
    
    print(f"\nRecommendations:")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    # Simulate improvement - student takes another practice exam
    print(f"\n--- After Additional Study ---")
    progress.record_practice_exam(85.0, [])
    
    report = progress.get_certification_readiness_report()
    print(f"New Average Score: {report['average_practice_score']:.2f}%")
    print(f"Ready for Certification: {'Yes' if report['is_ready'] else 'No'}")
    
    print(f"\nUpdated Recommendations:")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"  {i}. {rec}")


def demo_practice_exam_validation():
    """Demonstrate practice exam validation."""
    print("\n\n" + "=" * 70)
    print("DEMO 3: Practice Exam Validation")
    print("=" * 70)
    
    # Create a practice exam with 65 questions
    questions = []
    topics = [
        "Agent Architecture and Design",
        "Agent Development",
        "Evaluation and Tuning",
        "Deployment and Scaling",
        "Cognition, Planning, and Memory",
    ]
    
    for i in range(65):
        topic = topics[i % len(topics)]
        questions.append(
            Question(
                question_id=f"PE_Q{i+1}",
                question_text=f"Practice exam question {i+1}",
                question_type="multiple_choice",
                options=["A", "B", "C", "D"],
                correct_answer="B",
                explanation=f"Explanation for question {i+1}",
                exam_topic=topic,
                difficulty="medium"
            )
        )
    
    practice_exam = Assessment(
        assessment_id="practice_exam_01",
        assessment_type="practice_exam",
        questions=questions,
        passing_score=70.0,
        time_limit=120,
        exam_topics_covered={topic: 20.0 for topic in topics}
    )
    
    print(f"\nPractice Exam ID: {practice_exam.assessment_id}")
    print(f"Type: {practice_exam.assessment_type}")
    print(f"Questions: {len(practice_exam.questions)}")
    print(f"Time Limit: {practice_exam.time_limit} minutes")
    
    # Validate
    try:
        is_valid = practice_exam.validate()
        print(f"Valid: {is_valid}")
        print("✓ Question count is within 60-70 range")
        print("✓ Time limit is 120 minutes")
        print("✓ All questions are properly formatted")
    except ValueError as e:
        print(f"Validation Error: {e}")


if __name__ == "__main__":
    demo_module_quiz()
    demo_certification_readiness()
    demo_practice_exam_validation()
    
    print("\n\n" + "=" * 70)
    print("Assessment System Demo Complete!")
    print("=" * 70)
