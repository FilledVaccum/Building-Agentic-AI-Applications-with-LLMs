# Contributing to NCP-AAI Course Development

Thank you for your interest in contributing to the Building Agentic AI Applications with LLMs course!

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs or suggest enhancements
- Check existing issues before creating a new one
- Provide detailed information including:
  - Steps to reproduce
  - Expected vs actual behavior
  - Environment details (OS, Python version, etc.)
  - Relevant logs or error messages

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow the code style guidelines
   - Add tests for new functionality
   - Update documentation as needed
4. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```
5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request**

## Code Style Guidelines

### Python Code

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Write docstrings for all classes and functions
- Maximum line length: 100 characters
- Use meaningful variable and function names

Example:
```python
def create_agent(api_key: str, model: str = "llama-3.1-8b") -> Agent:
    """
    Create and initialize an agent instance.
    
    Args:
        api_key: NVIDIA API key for authentication
        model: Model identifier to use (default: llama-3.1-8b)
        
    Returns:
        Initialized Agent instance
        
    Raises:
        ValueError: If api_key is invalid
    """
    pass
```

### Documentation

- Use Markdown for all documentation
- Include code examples where appropriate
- Keep language clear and concise
- Update README.md if adding new features

### Testing

- Write unit tests for all new functionality
- Use pytest for testing
- Aim for >80% code coverage
- Include property-based tests using Hypothesis where applicable

Run tests:
```bash
pytest tests/
```

## Content Contributions

### Module Content

When contributing module content:

1. Follow the course structure defined in the steering document
2. Align with exam blueprint topics and weights
3. Include hands-on labs with starter and solution code
4. Provide clear learning objectives
5. Add assessment questions

### Lab Exercises

Lab contributions should include:

- `lab_XX_setup_instructions.md` - Environment setup
- `lab_XX_implementation_guide.md` - Step-by-step guide
- `lab_XX_starter.py` - Starter code with TODOs
- `lab_XX_solution.py` - Complete solution
- `lab_XX_troubleshooting.md` - Common issues and fixes
- `lab_XX_*.json` - Lab metadata

### Assessment Questions

When adding quiz or exam questions:

- Align with specific exam blueprint topics
- Include detailed explanations for correct answers
- Provide distractors that test common misconceptions
- Follow the assessment schema format

## Security Guidelines

**Critical**: Never commit sensitive information

- No API keys, passwords, or credentials
- Use environment variables for configuration
- Review changes before committing
- Use `.env.example` for configuration templates

## Review Process

1. All contributions require review by maintainers
2. Automated tests must pass
3. Code must follow style guidelines
4. Documentation must be updated
5. Security scan must pass

## Questions?

- Open a GitHub Discussion for general questions
- Tag maintainers in issues for specific questions
- Check existing documentation and FAQs first

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow professional standards

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping improve this course! 🚀
