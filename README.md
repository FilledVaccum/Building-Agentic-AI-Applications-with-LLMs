# Building Agentic AI Applications with LLMs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

Comprehensive course material for **NVIDIA-Certified Professional: Agentic AI (NCP-AAI)** certification preparation.

## 📚 Overview

This repository contains a complete course system for building production-ready agentic AI applications using Large Language Models (LLMs). The course is specifically designed to prepare students for the NCP-AAI certification exam.

### Course Highlights

- **13 comprehensive modules** covering agent architecture, development, deployment, and governance
- **Hands-on labs** with NVIDIA NIM, NeMo, TensorRT-LLM, and Triton Inference Server
- **Practice exams** aligned with official exam blueprint
- **Production-ready code examples** following security best practices
- **20-24 hours** of instruction + 20-30 hours of self-study

## 🎯 Target Audience

- Software developers and engineers
- Solutions architects
- Machine learning engineers
- Data scientists
- AI strategists with 1-2 years of AI/ML experience

## 📁 Project Structure

```
.
├── src/                          # Source code
│   ├── models/                   # Data models (Module, Lab, Assessment, etc.)
│   ├── schemas/                  # JSON schemas for validation
│   ├── validation.py             # Schema validation utilities
│   └── content_validation.py     # Content quality checks
├── content/                      # Course content (153 files)
│   ├── modules/                  # 13 module content files
│   ├── labs/                     # Hands-on lab exercises
│   ├── assessments/              # Quizzes and practice exams
│   ├── supplementary/            # Cheat sheets, references, glossary
│   └── instructor/               # Teaching guides and solutions
├── deployment/                   # Deployment and infrastructure
│   ├── docker/                   # Container configurations
│   ├── provision_labs.py         # Lab environment provisioning
│   └── scorm_packager.py         # LMS integration
├── tests/                        # Comprehensive test suite
│   ├── test_properties.py        # Property-based tests
│   └── test_code_quality.py      # Code quality checks
├── .kiro/                        # Kiro CLI configuration
│   ├── steering/                 # Course development guide
│   └── specs/                    # Project specifications
├── Reference Materials/          # Exam blueprints and study guides
└── integrated_course.json        # Complete course data (685KB)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- NVIDIA API key ([get one here](https://build.nvidia.com))
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Building-Agentic-AI-Applications-with-LLMs.git
   cd Building-Agentic-AI-Applications-with-LLMs
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your NVIDIA API keys
   ```

4. **Verify installation**
   ```bash
   pytest tests/
   ```

## 🔐 Security

**Important**: This repository follows strict security practices:

- ✅ No hardcoded API keys or credentials
- ✅ All sensitive data uses environment variables
- ✅ Comprehensive `.gitignore` for secrets
- ✅ Security scanning in pre-push checks

See [SECURITY.md](SECURITY.md) for detailed security guidelines.

## 📖 Course Modules

| Module | Title | Duration | Exam Coverage |
|--------|-------|----------|---------------|
| 1 | Fundamentals of Agent Abstraction and LLMs | 1.5h | Agent Architecture, Development |
| 2 | Structured Output & Basic Fulfillment | 1.5h | Agent Development, Cognition |
| 3 | Retrieval Mechanisms & Environmental Tooling | 2h | Knowledge Integration |
| 4 | Multi-Agent Systems & Frameworks | 2h | Agent Architecture, Deployment |
| 5 | Cognition, Planning, and Memory Management | 1.5h | Cognition & Planning |
| 6 | NVIDIA Platform Deep Dive | 1.5h | NVIDIA Platform Implementation |
| 7 | Evaluation, Tuning, and Optimization | 1.5h | Evaluation & Tuning |
| 8 | Production Deployment and Scaling | 2h | Deployment & Scaling |
| 9 | Monitoring, Observability, and Maintenance | 1.5h | Run, Monitor & Maintain |
| 10 | Safety, Ethics, and Guardrails | 1.5h | Safety, Ethics & Compliance |
| 11 | Human-in-the-Loop Systems | 1h | Human-AI Interaction |
| 12 | Advanced Topics and Real-World Applications | 1.5h | All Topics (Integration) |
| 13 | Final Assessment and Exam Preparation | 2h | Comprehensive Review |

## 🧪 Testing

Run the comprehensive test suite:

```bash
# All tests
pytest tests/

# Property-based tests
pytest tests/test_properties.py -v

# Code quality checks
pytest tests/test_code_quality.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

## 🛠️ Development

### Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Pre-Push Checklist

Before pushing to GitHub, run:

```bash
./pre-push-check.sh
```

This script checks for:
- Hardcoded credentials
- Large files
- Security vulnerabilities
- Code quality issues
- Test failures

### Code Quality

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write docstrings for classes and methods
- Maintain >80% test coverage
- No hardcoded secrets

## 📦 Deployment

### Docker Deployment

```bash
cd deployment/docker
docker build -t ncp-aai-course .
docker run -p 8888:8888 -e NVIDIA_API_KEY=$NVIDIA_API_KEY ncp-aai-course
```

### LMS Integration

The course supports SCORM 1.2 packaging for LMS integration:

```bash
python deployment/scorm_packager.py
```

See [deployment/LMS_INTEGRATION.md](deployment/LMS_INTEGRATION.md) for details.

## 📊 Exam Preparation

### Practice Exams

- 3 full-length practice exams (60-70 questions each)
- Aligned with official exam blueprint
- Detailed explanations for all answers
- Performance analytics

### Study Resources

- [Glossary](content/supplementary/glossary.md) - Key terms and concepts
- [Cheat Sheets](content/supplementary/) - Quick reference guides
- [External References](content/supplementary/external_references.md) - Curated links
- [Study Plan Template](content/supplementary/study_plan_template.md)

## 🔧 Tools and Platforms

### NVIDIA Platforms
- **NVIDIA NIM** - Inference microservices
- **NVIDIA NeMo** - Agent toolkit and guardrails
- **TensorRT-LLM** - Inference optimization
- **Triton Inference Server** - Model serving

### Frameworks
- LangChain, LangGraph
- PyTorch
- Docker, Kubernetes

### Databases
- Vector databases (Milvus, Pinecone)
- Traditional databases for structured data

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

NVIDIA, NIM, NeMo, TensorRT, Triton, and DGX are trademarks of NVIDIA Corporation.

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/Building-Agentic-AI-Applications-with-LLMs/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/Building-Agentic-AI-Applications-with-LLMs/discussions)
- **Security**: See [SECURITY.md](SECURITY.md)

## 📈 Project Status

- ✅ All 13 modules completed
- ✅ 153 content files created
- ✅ Comprehensive test suite (95%+ coverage)
- ✅ Security audit passed
- ✅ Ready for production deployment

## 🙏 Acknowledgments

- NVIDIA for AI platform and tools
- Course development team
- Open source community

---

**Ready to build production-ready agentic AI applications?** Start with [Module 1](content/modules/MODULE_01_README.md)!
