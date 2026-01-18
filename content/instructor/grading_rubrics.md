# Grading Rubrics

## Overview

This document provides comprehensive grading rubrics for all assessments in the "Building Agentic AI Applications with LLMs" course. Use these rubrics to ensure consistent, fair, and transparent grading across all students.

## Table of Contents

1. [Module Quiz Rubrics](#module-quiz-rubrics)
2. [Lab Completion Rubrics](#lab-completion-rubrics)
3. [Mid-Course Project Rubric](#mid-course-project-rubric)
4. [Final Project Rubric](#final-project-rubric)
5. [Grading Guidelines](#grading-guidelines)

---

## Module Quiz Rubrics

### General Quiz Grading Criteria

**Scoring**:
- Each quiz contains 5-10 questions
- Each question worth equal points
- Passing score: 70%
- Time limit: 15-20 minutes (varies by module)

**Question Types**:
- **Multiple Choice**: One correct answer (full credit or no credit)
- **Multiple Select**: Multiple correct answers (partial credit possible)
- **Scenario-Based**: Application of concepts (full credit or no credit)

**Partial Credit Policy**:
- Multiple choice: No partial credit
- Multiple select: Proportional credit (e.g., 2/3 correct = 67% of points)
- Scenario-based: No partial credit

**Retake Policy**:
- Students may retake quizzes once if score < 70%
- Highest score counts
- Different questions on retake
- 24-hour waiting period between attempts

### Module-Specific Quiz Rubrics

#### Module 1: Fundamentals (10 questions, 10 points each)

**Topics Covered**:
- LLM capabilities and limitations (20%)
- Agent abstraction principles (20%)
- Architecture types and selection (30%)
- Error handling best practices (20%)
- NVIDIA platform basics (10%)

**Passing Score**: 70/100 points

**Common Deductions**:
- Confusing reactive vs deliberative architectures
- Not understanding LLM limitations
- Missing error handling importance

#### Modules 2-12: Similar Structure

Each module quiz follows the same general structure:
- 5-10 questions based on module content
- Topics weighted by importance
- 70% passing threshold
- Aligned with exam blueprint topics

---

## Lab Completion Rubrics

### General Lab Grading Criteria

**Total Points**: 100 per lab

**Category Breakdown**:
- Functionality (40 points)
- Code Quality (30 points)
- Error Handling (15 points)
- Documentation (10 points)
- Testing (5 points)

**Submission Requirements**:
- All code files
- README with setup instructions
- Test results or screenshots
- Reflection on challenges and learnings (optional)

**Late Submission Policy**:
- On time: Full credit
- 1-3 days late: -10%
- 4-7 days late: -25%
- >7 days late: -50%
- After solutions released: No credit

### Detailed Lab Rubric Template

#### Functionality (40 points)

**Excellent (36-40 points)**:
- All requirements fully implemented
- Code runs without errors
- Handles edge cases appropriately
- Produces correct outputs consistently
- Demonstrates understanding of concepts

**Good (32-35 points)**:
- Most requirements implemented
- Minor bugs or issues
- Basic edge case handling
- Generally correct outputs
- Shows solid understanding

**Satisfactory (28-31 points)**:
- Core requirements met
- Some functionality missing or buggy
- Limited edge case handling
- Outputs mostly correct
- Demonstrates basic understanding

**Needs Improvement (0-27 points)**:
- Significant functionality missing
- Major bugs or errors
- No edge case handling
- Incorrect or inconsistent outputs
- Limited understanding demonstrated

#### Code Quality (30 points)

**Excellent (27-30 points)**:
- Clean, readable, well-organized code
- Follows Python conventions (PEP 8)
- Meaningful variable and function names
- Appropriate use of functions and classes
- DRY principle applied
- No code smells

**Good (24-26 points)**:
- Generally clean and readable
- Mostly follows conventions
- Good naming with minor issues
- Reasonable organization
- Some repetition
- Minor code smells

**Satisfactory (21-23 points)**:
- Readable but could be cleaner
- Some convention violations
- Naming could be improved
- Organization could be better
- Noticeable repetition
- Some code smells

**Needs Improvement (0-20 points)**:
- Difficult to read or understand
- Poor or no conventions followed
- Confusing names
- Poor organization
- Significant repetition
- Major code smells

#### Error Handling (15 points)

**Excellent (14-15 points)**:
- Comprehensive error handling
- Appropriate exception types
- Informative error messages
- Graceful degradation
- Retry logic where appropriate
- Logging for debugging

**Good (12-13 points)**:
- Good error handling coverage
- Mostly appropriate exceptions
- Clear error messages
- Basic graceful degradation
- Some retry logic
- Basic logging

**Satisfactory (10-11 points)**:
- Basic error handling
- Generic exceptions
- Minimal error messages
- Limited graceful degradation
- No retry logic
- Minimal logging

**Needs Improvement (0-9 points)**:
- Little or no error handling
- Unhandled exceptions
- No error messages
- Crashes on errors
- No retry logic
- No logging

#### Documentation (10 points)

**Excellent (9-10 points)**:
- Comprehensive README
- Clear setup instructions
- Usage examples provided
- Code comments where needed
- Docstrings for functions/classes
- Explains design decisions

**Good (8 points)**:
- Good README
- Clear setup instructions
- Basic usage examples
- Some code comments
- Most docstrings present
- Some design explanation

**Satisfactory (7 points)**:
- Basic README
- Minimal setup instructions
- Limited examples
- Few code comments
- Some docstrings missing
- Little design explanation

**Needs Improvement (0-6 points)**:
- Minimal or no README
- Unclear setup instructions
- No examples
- No code comments
- No docstrings
- No design explanation

#### Testing (5 points)

**Excellent (5 points)**:
- Comprehensive testing
- Edge cases covered
- Test results documented
- All tests pass

**Good (4 points)**:
- Good test coverage
- Some edge cases
- Results documented
- Most tests pass

**Satisfactory (3 points)**:
- Basic testing
- Few edge cases
- Minimal documentation
- Some tests pass

**Needs Improvement (0-2 points)**:
- Little or no testing
- No edge cases
- No documentation
- Tests fail or missing

### Lab-Specific Rubrics

#### Lab 1: Minimal Agent (100 points)

**Functionality (40 points)**:
- API connection works (10 pts)
- Basic chat functionality (10 pts)
- Error handling implemented (10 pts)
- Context management (10 pts)

**Code Quality (30 points)**:
- Clean agent class design (15 pts)
- Good code organization (15 pts)

**Error Handling (15 points)**:
- Retry logic with exponential backoff (10 pts)
- Appropriate error messages (5 pts)

**Documentation (10 points)**:
- Setup instructions (5 pts)
- Usage examples (5 pts)

**Testing (5 points)**:
- Tested with various inputs (5 pts)

#### Lab 2: Structured Output (100 points)

**Functionality (40 points)**:
- Task Analyzer works (15 pts)
- Meeting Scheduler works (15 pts)
- Research Assistant works (10 pts)

**Code Quality (30 points)**:
- Schema design (10 pts)
- Code organization (10 pts)
- Prompt quality (10 pts)

**Error Handling (15 points)**:
- Validation with retry (10 pts)
- Error feedback to LLM (5 pts)

**Documentation (10 points)**:
- Schema documentation (5 pts)
- Usage examples (5 pts)

**Testing (5 points)**:
- Schema validation tests (5 pts)

#### Lab 3: RAG Pipeline (100 points)

**Functionality (40 points)**:
- Document ingestion (10 pts)
- Chunking strategy (10 pts)
- Vector database integration (10 pts)
- RAG query pipeline (10 pts)

**Code Quality (30 points)**:
- Pipeline architecture (15 pts)
- Code organization (15 pts)

**Error Handling (15 points)**:
- Database connection errors (5 pts)
- Embedding errors (5 pts)
- Query errors (5 pts)

**Documentation (10 points)**:
- Setup instructions (5 pts)
- Configuration options (5 pts)

**Testing (5 points)**:
- Retrieval quality tests (5 pts)

#### Labs 4-12: Similar Structure

Each lab follows similar rubric structure with specific criteria based on lab objectives.



---

## Mid-Course Project Rubric

### Project Overview

**Objective**: Build a multi-agent system that demonstrates understanding of Modules 1-6

**Requirements**:
- Multiple specialized agents (minimum 3)
- Agent-to-agent communication
- Integration with external data sources (RAG or APIs)
- Structured outputs
- Error handling and logging
- Deployment-ready code

**Total Points**: 200

**Submission Requirements**:
- Source code (all files)
- README with setup and usage instructions
- Architecture diagram
- Demo video or live demonstration (5-10 minutes)
- Reflection document (1-2 pages)

**Timeline**: 2 weeks from assignment to submission

### Detailed Rubric

#### 1. System Architecture and Design (40 points)

**Excellent (36-40 points)**:
- Well-designed multi-agent architecture
- Clear separation of concerns
- Appropriate agent specialization
- Scalable and maintainable design
- Comprehensive architecture diagram
- Design decisions well-justified

**Good (32-35 points)**:
- Good architecture with minor issues
- Mostly clear separation
- Reasonable specialization
- Generally scalable design
- Good architecture diagram
- Design decisions explained

**Satisfactory (28-31 points)**:
- Basic architecture
- Some coupling between agents
- Basic specialization
- Limited scalability
- Basic diagram
- Some design explanation

**Needs Improvement (0-27 points)**:
- Poor architecture
- Tight coupling
- Unclear specialization
- Not scalable
- Missing or poor diagram
- No design explanation

#### 2. Functionality (60 points)

**Agent Implementation (30 points)**:
- All required agents implemented (10 pts)
- Agents perform specialized tasks correctly (10 pts)
- Agent coordination works smoothly (10 pts)

**Integration (20 points)**:
- External data sources integrated (10 pts)
- Structured outputs implemented (10 pts)

**User Interface (10 points)**:
- Clear interface for interaction (5 pts)
- Good user experience (5 pts)

#### 3. Code Quality (40 points)

**Code Organization (15 points)**:
- Clean project structure
- Logical file organization
- Appropriate use of modules/packages

**Code Readability (15 points)**:
- Clear, readable code
- Meaningful names
- Follows conventions

**Best Practices (10 points)**:
- DRY principle
- SOLID principles
- No code smells

#### 4. Error Handling and Robustness (20 points)

**Error Handling (10 points)**:
- Comprehensive error handling
- Appropriate exception types
- Informative error messages

**Robustness (10 points)**:
- Handles edge cases
- Graceful degradation
- Retry logic where appropriate

#### 5. Documentation (20 points)

**README (10 points)**:
- Clear setup instructions
- Usage examples
- Configuration options
- Troubleshooting guide

**Code Documentation (5 points)**:
- Docstrings for functions/classes
- Comments where needed

**Architecture Documentation (5 points)**:
- Architecture diagram
- Design decisions explained
- Component interactions described

#### 6. Testing (10 points)

**Test Coverage (5 points)**:
- Unit tests for components
- Integration tests for workflows

**Test Quality (5 points)**:
- Tests are meaningful
- Edge cases covered
- All tests pass

#### 7. Demonstration (10 points)

**Demo Quality (5 points)**:
- Clear demonstration of functionality
- Shows key features
- Professional presentation

**Demo Content (5 points)**:
- Explains architecture
- Shows agent interactions
- Discusses challenges and solutions

### Grading Guidelines

**Total Score Interpretation**:
- 180-200 points (90-100%): Excellent - Exceeds expectations
- 160-179 points (80-89%): Good - Meets all requirements well
- 140-159 points (70-79%): Satisfactory - Meets basic requirements
- <140 points (<70%): Needs Improvement - Does not meet requirements

**Bonus Points** (up to 10 points):
- Exceptional creativity or innovation
- Advanced features beyond requirements
- Outstanding code quality
- Exceptional documentation

---

## Final Project Rubric

### Project Overview

**Objective**: Build a production-ready agentic AI application demonstrating all course competencies

**Requirements**:
- Scalable multi-tenant agent API
- Multiple retrieval operations (RAG, APIs, databases)
- Research gathering and synthesis capabilities
- Structured result return
- Complete deployment (containerized, orchestrated)
- Monitoring and logging
- Safety guardrails
- Human-in-the-loop capabilities
- Comprehensive documentation

**Total Points**: 300

**Submission Requirements**:
- Complete source code
- Deployment configuration (Docker, Kubernetes)
- Comprehensive documentation
- Demo video or live presentation (15-20 minutes)
- Technical report (5-10 pages)
- Reflection on learning journey

**Timeline**: 3-4 weeks from assignment to submission

### Detailed Rubric

#### 1. System Architecture (50 points)

**Architecture Design (25 points)**:
- Excellent (23-25): Sophisticated, scalable, well-designed architecture
- Good (20-22): Solid architecture with minor issues
- Satisfactory (17-19): Basic architecture meeting requirements
- Needs Improvement (0-16): Poor or incomplete architecture

**Multi-Tenancy (15 points)**:
- Excellent (14-15): Robust multi-tenant design with isolation
- Good (12-13): Good multi-tenancy with minor issues
- Satisfactory (10-11): Basic multi-tenancy
- Needs Improvement (0-9): Poor or missing multi-tenancy

**Scalability (10 points)**:
- Excellent (9-10): Highly scalable design
- Good (8): Scalable with minor limitations
- Satisfactory (7): Basic scalability
- Needs Improvement (0-6): Not scalable

#### 2. Core Functionality (80 points)

**Agent Capabilities (30 points)**:
- Research gathering (10 pts)
- Information synthesis (10 pts)
- Structured output generation (10 pts)

**Retrieval Operations (25 points)**:
- RAG pipeline implementation (10 pts)
- API integrations (8 pts)
- Database queries (7 pts)

**API Design (15 points)**:
- RESTful API design (8 pts)
- API documentation (7 pts)

**User Interface (10 points)**:
- Functional UI (5 pts)
- Good UX (5 pts)

#### 3. Production Readiness (60 points)

**Deployment (20 points)**:
- Containerization (Docker) (10 pts)
- Orchestration (Kubernetes) (10 pts)

**Monitoring and Logging (15 points)**:
- Comprehensive logging (8 pts)
- Monitoring and alerting (7 pts)

**Safety and Ethics (15 points)**:
- Guardrails implementation (8 pts)
- Bias detection/mitigation (7 pts)

**Human-in-the-Loop (10 points)**:
- Feedback mechanism (5 pts)
- Intervention capabilities (5 pts)

#### 4. Code Quality (40 points)

**Code Organization (15 points)**:
- Excellent (14-15): Exemplary organization
- Good (12-13): Well-organized
- Satisfactory (10-11): Adequately organized
- Needs Improvement (0-9): Poorly organized

**Code Readability (15 points)**:
- Excellent (14-15): Highly readable
- Good (12-13): Readable
- Satisfactory (10-11): Adequately readable
- Needs Improvement (0-9): Hard to read

**Best Practices (10 points)**:
- Excellent (9-10): Exemplary practices
- Good (8): Good practices
- Satisfactory (7): Basic practices
- Needs Improvement (0-6): Poor practices

#### 5. Error Handling and Robustness (25 points)

**Error Handling (15 points)**:
- Comprehensive error handling (15 pts)
- Good error handling (12-14 pts)
- Basic error handling (10-11 pts)
- Poor error handling (0-9 pts)

**Robustness (10 points)**:
- Highly robust (9-10 pts)
- Robust (8 pts)
- Adequately robust (7 pts)
- Not robust (0-6 pts)

#### 6. Documentation (25 points)

**Technical Documentation (10 points)**:
- Architecture documentation (3 pts)
- API documentation (3 pts)
- Deployment documentation (4 pts)

**User Documentation (8 points)**:
- Setup guide (4 pts)
- User guide (4 pts)

**Technical Report (7 points)**:
- Problem statement (2 pts)
- Solution approach (2 pts)
- Results and evaluation (2 pts)
- Reflection (1 pt)

#### 7. Testing (15 points)

**Test Coverage (8 points)**:
- Unit tests (3 pts)
- Integration tests (3 pts)
- End-to-end tests (2 pts)

**Test Quality (7 points)**:
- Tests are meaningful (3 pts)
- Edge cases covered (2 pts)
- All tests pass (2 pts)

#### 8. Presentation and Demo (15 points)

**Presentation Quality (8 points)**:
- Clear and professional (3 pts)
- Well-structured (3 pts)
- Engaging (2 pts)

**Demo Content (7 points)**:
- Shows all key features (3 pts)
- Explains architecture (2 pts)
- Discusses challenges (2 pts)

### Grading Guidelines

**Total Score Interpretation**:
- 270-300 points (90-100%): Excellent - Production-ready, exceeds expectations
- 240-269 points (80-89%): Good - Solid implementation, meets all requirements
- 210-239 points (70-79%): Satisfactory - Meets basic requirements
- <210 points (<70%): Needs Improvement - Significant gaps

**Bonus Points** (up to 20 points):
- Exceptional innovation (up to 10 pts)
- Advanced features (up to 5 pts)
- Outstanding quality (up to 5 pts)

---

## Grading Guidelines

### General Principles

**Consistency**:
- Use rubrics consistently across all students
- Apply same standards to all submissions
- Document any deviations from rubric

**Fairness**:
- Grade based on requirements, not personal preferences
- Provide constructive feedback
- Allow for different approaches to same problem
- Consider context (e.g., technical difficulties)

**Transparency**:
- Share rubrics with students before assignments
- Explain grading decisions
- Provide detailed feedback
- Be available for grade discussions

### Feedback Best Practices

**Timely**:
- Return graded work within one week
- Provide feedback while material is fresh
- Allow time for improvement on future work

**Specific**:
- Point to exact issues in code or documentation
- Explain why something is incorrect or suboptimal
- Provide examples of correct approaches
- Reference course materials

**Actionable**:
- Suggest specific improvements
- Provide resources for learning
- Offer opportunities for revision (when appropriate)
- Set clear expectations for future work

**Balanced**:
- Highlight strengths and successes
- Frame criticism constructively
- Encourage growth mindset
- Maintain high standards with appropriate support

### Grade Disputes

**Process**:
1. Student reviews rubric and grading
2. Student submits written dispute with specific concerns
3. Instructor reviews submission and rubric
4. Instructor meets with student to discuss
5. Instructor makes final decision
6. Decision is documented

**Valid Reasons for Dispute**:
- Grading error (miscalculation, missed component)
- Rubric not applied consistently
- Misunderstanding of requirements
- Technical issues affected submission

**Invalid Reasons**:
- Disagreement with rubric criteria
- Desire for higher grade without justification
- Comparison to other students' grades
- Personal circumstances (address separately)

### Grade Adjustments

**When to Adjust**:
- Clear grading error
- Rubric not applied correctly
- New information comes to light
- Technical issues verified

**When Not to Adjust**:
- Student simply wants higher grade
- Student disagrees with rubric
- Student had personal issues (handle through other channels)
- Adjustment would be unfair to other students

### Record Keeping

**Required Documentation**:
- All graded submissions
- Rubric scores for each student
- Feedback provided
- Any grade adjustments and reasons
- Communication with students about grades

**Retention Period**:
- Keep records for at least one year after course completion
- Longer if required by institution
- Secure storage of student work and grades

---

## Conclusion

These rubrics provide a framework for consistent, fair, and transparent grading. Remember:

- Rubrics are guides, not rigid rules
- Professional judgment is still required
- Focus on learning, not just grades
- Provide feedback that helps students improve
- Be consistent but also compassionate

The goal is to assess student learning accurately while supporting their growth and development as agentic AI practitioners.

**Document Version**: 1.0  
**Last Updated**: January 2026  
**For**: Building Agentic AI Applications with LLMs

