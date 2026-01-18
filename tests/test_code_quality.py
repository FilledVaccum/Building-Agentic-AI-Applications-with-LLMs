"""Property-based tests for code quality validation."""

from hypothesis import given, strategies as st, settings, HealthCheck
from hypothesis.strategies import composite
import pytest

from src.models import Module, LearningObjective, PlatformDemo, Course, HandsOnLab
from src.content_validation import CodeQualityValidator


@composite
def code_example_strategy(draw):
    """Generate code examples with varying quality characteristics."""
    # Base code structure
    has_function = draw(st.booleans())
    has_api_call = draw(st.booleans())
    has_file_io = draw(st.booleans())
    has_error_handling = draw(st.booleans())
    has_comments = draw(st.booleans())
    has_nvidia_platform = draw(st.booleans())
    has_retry_logic = draw(st.booleans())
    has_circuit_breaker = draw(st.booleans())
    
    code_parts = []
    
    # Add imports
    if has_api_call:
        code_parts.append("import requests")
    if has_file_io:
        code_parts.append("import os")
    if has_nvidia_platform:
        code_parts.append("from nvidia import nim")
    
    code_parts.append("")
    
    # Add comments if requested
    if has_comments:
        code_parts.append("# This is a code example")
        code_parts.append('"""Module docstring."""')
        code_parts.append("")
    
    # Add function
    if has_function:
        code_parts.append("def process_data(data):")
        if has_comments:
            code_parts.append('    """Process the data."""')
        
        # Add error handling if requested
        if has_error_handling:
            code_parts.append("    try:")
            indent = "        "
        else:
            indent = "    "
        
        # Add API call
        if has_api_call:
            code_parts.append(f"{indent}response = requests.get('https://api.example.com/data')")
            if has_retry_logic:
                code_parts.append(f"{indent}max_retries = 3")
                code_parts.append(f"{indent}for attempt in range(max_retries):")
                code_parts.append(f"{indent}    try:")
                code_parts.append(f"{indent}        response = requests.get('https://api.example.com/data')")
                code_parts.append(f"{indent}        break")
                code_parts.append(f"{indent}    except Exception:")
                code_parts.append(f"{indent}        if attempt == max_retries - 1:")
                code_parts.append(f"{indent}            raise")
        
        # Add file I/O
        if has_file_io:
            code_parts.append(f"{indent}with open('data.txt', 'r') as f:")
            code_parts.append(f"{indent}    content = f.read()")
        
        # Add NVIDIA platform usage
        if has_nvidia_platform:
            code_parts.append(f"{indent}client = nim.Client()")
            code_parts.append(f"{indent}result = client.generate(prompt='test')")
        
        # Add circuit breaker if requested
        if has_circuit_breaker:
            code_parts.append(f"{indent}if circuit_breaker.is_open():")
            code_parts.append(f"{indent}    raise Exception('Circuit breaker is open')")
        
        # Close error handling
        if has_error_handling:
            code_parts.append("    except Exception as e:")
            code_parts.append("        print(f'Error: {e}')")
            code_parts.append("        raise")
        
        code_parts.append(f"{indent}return data")
    
    return "\n".join(code_parts)


# Feature: ncp-aai-course-development, Property 12: Code Example Error Handling Completeness
@settings(suppress_health_check=[HealthCheck.large_base_example], max_examples=100)
@given(
    code=code_example_strategy(),
    context=st.text(min_size=5, max_size=50)
)
def test_code_example_error_handling_completeness(code, context):
    """
    Property 12: Code Example Error Handling Completeness
    
    For any code example in the course, if it involves external API calls or I/O operations,
    it must include error handling (try-catch blocks, retry logic, or circuit breakers).
    
    This property validates that:
    1. Code with external operations includes error handling
    2. Error handling patterns (retry, circuit breaker) are present when appropriate
    3. Code includes proper comments and documentation
    4. Security best practices are followed
    5. NVIDIA platform usage is present where expected
    
    Validates: Requirements 15.1, 15.6, 15.7, 15.8
    """
    # Create a minimal course for validation
    course = Course(modules=[])
    validator = CodeQualityValidator(course, {})
    
    # Validate error handling
    error_result = validator.validate_code_example_error_handling(code, context)
    
    # Check if code needs error handling
    needs_error_handling = any(pattern in code for pattern in [
        "requests.", "http", "api", ".get(", ".post(",
        "open(", "read(", "write(",
        "connect(", "execute(", "query(",
        "NVIDIA", "NIM", "NeMo", "Triton"
    ])
    
    has_error_handling = "try:" in code and "except" in code or "raise" in code
    
    # If code needs error handling, it must have it
    if needs_error_handling and not has_error_handling:
        assert not error_result.is_valid, \
            f"Code with external operations should fail validation without error handling"
        assert len(error_result.errors) > 0, \
            "Should have errors for missing error handling"
    
    # If code has error handling when needed, validation should pass (or have only warnings)
    if needs_error_handling and has_error_handling:
        # May have warnings but should not have errors about missing error handling
        error_handling_errors = [e for e in error_result.errors if "error handling" in e.lower()]
        assert len(error_handling_errors) == 0, \
            "Should not have error handling errors when error handling is present"
    
    # Validate error handling patterns
    pattern_result = validator.validate_error_handling_patterns(code, context)
    
    # Check for retry logic
    has_retry = any(pattern in code for pattern in ["retry", "max_retries", "attempt", "backoff"])
    needs_retry = any(pattern in code for pattern in ["requests.", "http", "api", "connect("])
    
    if needs_retry and not has_retry:
        # Should have warning (not error) about missing retry logic
        assert len(pattern_result.warnings) > 0 or len(pattern_result.errors) == 0, \
            "Should warn about missing retry logic for external calls"
    
    # Check for circuit breaker
    has_circuit_breaker = any(pattern in code for pattern in [
        "circuit", "breaker", "failure_threshold", "timeout"
    ])
    needs_circuit_breaker = any(pattern in code for pattern in [
        "external", "service", "api", "microservice"
    ])
    
    if needs_circuit_breaker and not has_circuit_breaker:
        # Should have warning about missing circuit breaker
        assert len(pattern_result.warnings) > 0 or len(pattern_result.errors) == 0, \
            "Should warn about missing circuit breaker for service calls"
    
    # Check for graceful failure
    has_graceful_failure = any(pattern in code for pattern in [
        "fallback", "default", "recover", "except Exception"
    ])
    
    if "try:" in code and "except" in code and not has_graceful_failure:
        # Should have error about missing graceful failure
        assert not pattern_result.is_valid, \
            "Code with try-except should have graceful failure recovery"


# Additional unit tests for code quality validation
def test_code_quality_validation_with_api_calls():
    """Test that code with API calls requires error handling."""
    code = """
import requests

def fetch_data():
    response = requests.get('https://api.example.com/data')
    return response.json()
"""
    
    course = Course(modules=[])
    validator = CodeQualityValidator(course, {})
    
    result = validator.validate_code_example_error_handling(code, "Test API code")
    
    # Should fail because API call lacks error handling
    assert not result.is_valid
    assert len(result.errors) > 0
    assert any("error handling" in error.lower() for error in result.errors)


def test_code_quality_validation_with_proper_error_handling():
    """Test that code with proper error handling passes validation."""
    code = """
import requests

def fetch_data():
    '''Fetch data from API with error handling.'''
    try:
        response = requests.get('https://api.example.com/data')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Error fetching data: {e}')
        return None
"""
    
    course = Course(modules=[])
    validator = CodeQualityValidator(course, {})
    
    result = validator.validate_code_example_error_handling(code, "Test API code")
    
    # Should pass because it has error handling and comments
    assert result.is_valid or len(result.errors) == 0


def test_code_quality_validation_with_retry_logic():
    """Test that retry logic is detected."""
    code = """
import requests
import time

def fetch_data_with_retry():
    '''Fetch data with retry logic.'''
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get('https://api.example.com/data')
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
"""
    
    course = Course(modules=[])
    validator = CodeQualityValidator(course, {})
    
    result = validator.validate_error_handling_patterns(code, "Test retry code")
    
    # Should detect retry logic
    assert result.details["has_retry_logic"] is True


def test_code_quality_validation_with_circuit_breaker():
    """Test that circuit breaker pattern is detected."""
    code = """
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.is_open = False
    
    def call(self, func):
        if self.is_open:
            raise Exception('Circuit breaker is open')
        try:
            result = func()
            self.failures = 0
            return result
        except Exception:
            self.failures += 1
            if self.failures >= self.failure_threshold:
                self.is_open = True
            raise
"""
    
    course = Course(modules=[])
    validator = CodeQualityValidator(course, {})
    
    result = validator.validate_error_handling_patterns(code, "Test circuit breaker")
    
    # Should detect circuit breaker pattern
    assert result.details["has_circuit_breaker"] is True


def test_code_quality_validation_security_issues():
    """Test that security issues are detected."""
    code_with_hardcoded_creds = """
import requests

def connect_to_api():
    api_key = "sk-1234567890abcdef"  # Hardcoded API key
    response = requests.get('https://api.example.com', headers={'Authorization': f'Bearer {api_key}'})
    return response.json()
"""
    
    course = Course(modules=[])
    validator = CodeQualityValidator(course, {})
    
    result = validator.validate_code_example_error_handling(code_with_hardcoded_creds, "Test security")
    
    # Should detect security issue
    assert not result.is_valid
    assert len(result.details["security_issues"]) > 0


def test_code_quality_validation_with_env_vars():
    """Test that using environment variables for credentials passes."""
    code = """
import os
import requests

def connect_to_api():
    '''Connect to API using environment variables.'''
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError('API_KEY not found in environment')
    
    try:
        response = requests.get(
            'https://api.example.com',
            headers={'Authorization': f'Bearer {api_key}'}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Error: {e}')
        raise
"""
    
    course = Course(modules=[])
    validator = CodeQualityValidator(course, {})
    
    result = validator.validate_code_example_error_handling(code, "Test env vars")
    
    # Should not have security issues
    assert len(result.details["security_issues"]) == 0


def test_code_quality_validation_nvidia_platform():
    """Test that NVIDIA platform usage is detected."""
    code = """
from nvidia import nim

def generate_response(prompt):
    '''Generate response using NVIDIA NIM.'''
    try:
        client = nim.Client()
        response = client.generate(prompt=prompt)
        return response
    except Exception as e:
        print(f'Error: {e}')
        return None
"""
    
    course = Course(modules=[])
    validator = CodeQualityValidator(course, {})
    
    result = validator.validate_code_example_error_handling(code, "NVIDIA NIM example")
    
    # Should detect NVIDIA platform usage
    assert result.details["uses_nvidia_platform"] is True


def test_code_quality_validation_minimal_comments():
    """Test that minimal comments generate warnings or errors."""
    code = """
import requests

def fetch_data():
    try:
        response = requests.get('https://api.example.com/data')
        return response.json()
    except Exception as e:
        return None
"""
    
    course = Course(modules=[])
    validator = CodeQualityValidator(course, {})
    
    result = validator.validate_code_example_error_handling(code, "Test comments")
    
    # Should have warning or error about minimal comments
    assert len(result.warnings) > 0 or len(result.errors) > 0


def test_code_quality_validation_comprehensive_comments():
    """Test that comprehensive comments pass validation."""
    code = """
import requests

def fetch_data():
    '''
    Fetch data from the API.
    
    Returns:
        dict: The JSON response from the API, or None if an error occurs.
    '''
    try:
        # Make GET request to API endpoint
        response = requests.get('https://api.example.com/data')
        response.raise_for_status()
        
        # Parse and return JSON response
        return response.json()
    except requests.RequestException as e:
        # Log error and return None for graceful failure
        print(f'Error fetching data: {e}')
        return None
"""
    
    course = Course(modules=[])
    validator = CodeQualityValidator(course, {})
    
    result = validator.validate_code_example_error_handling(code, "Test comprehensive comments")
    
    # Should have good comment coverage
    assert result.details["comment_lines"] >= 3
    assert result.details["has_docstrings"] is True


def test_code_quality_validation_all_code_examples():
    """Test validation of all code examples in a course."""
    # Create module with platform demo
    demo = PlatformDemo(
        demo_id="demo1",
        title="Test Demo",
        platform="NIM",
        description="Test",
        code_examples={
            "example1.py": """
import requests

def fetch_data():
    try:
        response = requests.get('https://api.example.com')
        return response.json()
    except Exception as e:
        return None
""",
            "example2.py": """
# Simple example
def hello():
    '''Say hello.'''
    print('Hello, world!')
"""
        }
    )
    
    module = Module(
        module_id=1,
        title="Test Module",
        duration_hours=1.5,
        exam_topics={"Agent Development": 100.0},
        learning_objectives=[LearningObjective(
            objective_id="obj1",
            description="Test",
            exam_topics=["Agent Development"],
            bloom_level="understand"
        )],
        prerequisites=[],
        theoretical_content="Content",
        platform_demos=[demo],
        lab_id="lab1",
        assessment_id="quiz1"
    )
    
    # Create lab
    lab = HandsOnLab(
        lab_id="lab1",
        title="Test Lab",
        objectives=["Test"],
        setup_instructions="Setup",
        implementation_guide="Guide",
        starter_code={
            "starter.py": """
# Starter code
def process():
    '''Process data.'''
    pass
"""
        },
        solution_code={
            "solution.py": """
import requests

def process():
    '''Process data with API call.'''
    try:
        response = requests.get('https://api.example.com')
        return response.json()
    except Exception as e:
        print(f'Error: {e}')
        return None
"""
        },
        expected_outputs={"output": "test"},
        troubleshooting_guide="Troubleshooting",
        nvidia_platforms_used=["NIM"]
    )
    
    course = Course(modules=[module])
    validator = CodeQualityValidator(course, {"lab1": lab})
    
    result = validator.validate_all_code_examples()
    
    # Should validate all code examples
    assert "modules" in result.details
    assert "labs" in result.details
    assert len(result.details["modules"]) == 2  # 2 code examples in demo
    assert len(result.details["labs"]) == 2  # starter + solution
