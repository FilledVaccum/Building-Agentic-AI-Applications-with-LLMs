#!/usr/bin/env python3
"""Generate practice exam questions for NCP-AAI course."""

import json

# Practice Exam 2 questions (continuing from PE2-003)
pe2_questions = [
    # Agent Architecture (7 more questions needed - total 10)
    {
        "question_id": "PE2-004",
        "question_text": "In a layered agent architecture, what is the typical flow of information?",
        "question_type": "multiple_choice",
        "options": [
            "Random flow between layers",
            "Bottom-up from sensors through reasoning to actions",
            "Only horizontal within layers",
            "No information flow between layers"
        ],
        "correct_answer": "Bottom-up from sensors through reasoning to actions",
        "explanation": "Layered architectures typically flow bottom-up: perception layer receives input, reasoning layer processes it, action layer executes responses. This separation of concerns enables modularity. Random flow creates chaos, horizontal-only prevents integration, and no flow defeats the purpose of layers. Structured flow enables clear responsibility.",
        "exam_topic": "Agent Architecture and Design",
        "difficulty": "medium"
    },
    {
        "question_id": "PE2-005",
        "question_text": "What is the purpose of implementing a 'belief-desire-intention' (BDI) model in agent architecture?",
        "question_type": "multiple_choice",
        "options": [
            "To make agents have human emotions",
            "To structure agent reasoning around beliefs (knowledge), desires (goals), and intentions (plans)",
            "To slow down agent processing",
            "To eliminate the need for planning"
        ],
        "correct_answer": "To structure agent reasoning around beliefs (knowledge), desires (goals), and intentions (plans)",
        "explanation": "BDI provides a structured framework for agent reasoning: beliefs represent knowledge about the world, desires represent goals, and intentions represent committed plans. This enables sophisticated goal-directed behavior. It's not about emotions, doesn't aim to slow processing, and actually enhances rather than eliminates planning.",
        "exam_topic": "Agent Architecture and Design",
        "difficulty": "hard"
    },
    {
        "question_id": "PE2-006",
        "question_text": "Which architectural pattern BEST supports agents that need to adapt their behavior based on environmental changes?",
        "question_type": "multiple_choice",
        "options": [
            "Purely reactive with no state",
            "Hybrid architecture with feedback loops and adaptive components",
            "Static rule-based system",
            "Hardcoded decision trees"
        ],
        "correct_answer": "Hybrid architecture with feedback loops and adaptive components",
        "explanation": "Hybrid architectures with feedback loops can monitor environmental changes and adapt behavior accordingly, combining reactive responses with deliberative adaptation. Pure reactive can't learn, static rules can't adapt, and hardcoded trees are inflexible. Adaptive hybrid architectures enable environmental responsiveness.",
        "exam_topic": "Agent Architecture and Design",
        "difficulty": "medium"
    },
    {
        "question_id": "PE2-007",
        "question_text": "In multi-agent systems, what is the purpose of implementing agent roles?",
        "question_type": "multiple_choice",
        "options": [
            "To make the system more complicated",
            "To define agent responsibilities, capabilities, and interaction patterns",
            "To prevent agents from communicating",
            "To ensure all agents are identical"
        ],
        "correct_answer": "To define agent responsibilities, capabilities, and interaction patterns",
        "explanation": "Roles define what each agent is responsible for, what it can do, and how it interacts with others. This enables specialization, clear interfaces, and coordinated behavior. Roles don't complicate unnecessarily (they organize), don't prevent communication (they structure it), and enable diversity rather than uniformity.",
        "exam_topic": "Agent Architecture and Design",
        "difficulty": "medium"
    },
    {
        "question_id": "PE2-008",
        "question_text": "What is the primary advantage of using subsumption architecture in robotics and agent systems?",
        "question_type": "multiple_choice",
        "options": [
            "It requires complex planning for every action",
            "Lower-level behaviors can be overridden by higher-level behaviors when needed",
            "All behaviors execute simultaneously without priority",
            "It eliminates the need for sensors"
        ],
        "correct_answer": "Lower-level behaviors can be overridden by higher-level behaviors when needed",
        "explanation": "Subsumption architecture layers behaviors hierarchically - higher levels can subsume (override) lower levels. This enables reactive responses (low level) while allowing goal-directed behavior (high level) when appropriate. It doesn't require complex planning (it's reactive), behaviors have priority (not simultaneous), and sensors are essential (not eliminated).",
        "exam_topic": "Agent Architecture and Design",
        "difficulty": "hard"
    },
    {
        "question_id": "PE2-009",
        "question_text": "When designing agent communication protocols, which property is MOST important for reliability?",
        "question_type": "multiple_choice",
        "options": [
            "Messages should be as large as possible",
            "Messages should have acknowledgments and timeout handling",
            "Messages should never include metadata",
            "Messages should be sent without any structure"
        ],
        "correct_answer": "Messages should have acknowledgments and timeout handling",
        "explanation": "Reliable communication requires acknowledgments (confirm receipt) and timeouts (detect failures). This enables retry logic and error handling. Large messages aren't inherently better (can cause issues), metadata is valuable for routing and processing, and structure enables parsing and validation. Acknowledgments and timeouts are fundamental to reliability.",
        "exam_topic": "Agent Architecture and Design",
        "difficulty": "medium"
    },
    {
        "question_id": "PE2-010",
        "question_text": "What is the purpose of implementing a 'world model' in deliberative agent architectures?",
        "question_type": "multiple_choice",
        "options": [
            "To create virtual reality simulations",
            "To maintain an internal representation of the environment for planning and reasoning",
            "To replace all external sensors",
            "To make the agent slower"
        ],
        "correct_answer": "To maintain an internal representation of the environment for planning and reasoning",
        "explanation": "A world model is an internal representation of the environment that enables planning, prediction, and reasoning about actions. It doesn't create VR (it's for the agent's use), complements rather than replaces sensors, and while it adds processing, it enables more sophisticated behavior. World models are essential for deliberative reasoning.",
        "exam_topic": "Agent Architecture and Design",
        "difficulty": "medium"
    },
]

print(json.dumps(pe2_questions, indent=2))
