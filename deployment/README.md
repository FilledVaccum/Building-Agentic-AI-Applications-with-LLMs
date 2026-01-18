# NCP-AAI Course Deployment Package

## Overview

This directory contains all necessary files and documentation for deploying the "Building Agentic AI Applications with LLMs" course in your organization.

## Contents

### Documentation

- **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - Complete installation instructions
- **[CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md)** - Configuration options and customization
- **[TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md)** - Common issues and solutions
- **[MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md)** - Ongoing maintenance procedures
- **[LMS_INTEGRATION.md](LMS_INTEGRATION.md)** - LMS integration guide
- **[LAB_ENVIRONMENT_SETUP.md](LAB_ENVIRONMENT_SETUP.md)** - Lab environment setup guide

### Scripts and Tools

- **scorm_packager.py** - SCORM 2004 package generator
- **provision_labs.py** - Lab environment provisioning script
- **docker/** - Docker container configurations
- **terraform/** - Infrastructure as code (Terraform)
- **scripts/** - Maintenance and utility scripts
- **monitoring/** - Monitoring and alerting configurations

## Quick Start

### 1. Prerequisites

Ensure you have:
- Python 3.10+
- Docker 20.10+
- Terraform 1.0+
- Cloud provider account (AWS, Azure, or NVIDIA DGX Cloud)
- NVIDIA Developer Program membership

### 2. Installation

```bash
# Clone repository
git clone https://github.com/nvidia/ncp-aai-course.git
cd ncp-aai-course

# Install dependencies
pip install -r requirements.txt

# Configure NVIDIA API access
export NVIDIA_API_KEY="your-api-key"
export NVIDIA_NIM_ENDPOINT="https://api.nvidia.com/nim/v1"

# Build Docker container
cd deployment/docker
docker build -t ncp-aai-lab:latest .

# Generate SCORM package
cd ../..
python -c "
from deployment.scorm_packager import SCORMPackager
import json
with open('integrated_course.json', 'r') as f:
    course_data = json.load(f)
packager = SCORMPackager(course_data)
packager.create_package()
"

# Provision lab environments
python deployment/provision_labs.py --action provision --count 100
```

### 3. Upload to LMS

Upload the generated SCORM package to your LMS:
- Package location: `deployment/packages/ncp_aai_course_*.zip`
- See [LMS_INTEGRATION.md](LMS_INTEGRATION.md) for platform-specific instructions

## Deployment Options

### Option 1: Full Deployment

Complete deployment with all components:
- Course content (SCORM package)
- Lab environments (cloud GPU instances)
- Monitoring and alerting
- Backup and recovery

**Best for:** Production deployments with 50+ students

### Option 2: Content Only

Deploy course content without lab environments:
- Course content (SCORM package)
- Students use local development environments
- No cloud infrastructure required

**Best for:** Small pilot programs or self-study

### Option 3: Hybrid Deployment

Deploy content with shared lab environment:
- Course content (SCORM package)
- Single shared lab environment
- Students access via JupyterHub

**Best for:** Budget-conscious deployments with 10-30 students

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    LMS Platform                          │
│              (Moodle, Canvas, Blackboard)               │
└─────────────────────────────────────────────────────────┘
                          │
                          │ SCORM 2004
                          │
┌─────────────────────────────────────────────────────────┐
│                  Course Content                          │
│         (13 Modules, Assessments, Labs)                 │
└─────────────────────────────────────────────────────────┘
                          │
                          │
┌─────────────────────────────────────────────────────────┐
│              Lab Environment (Cloud)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ GPU Instance │  │ GPU Instance │  │ GPU Instance │ │
│  │  (Student 1) │  │  (Student 2) │  │  (Student N) │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          │
┌─────────────────────────────────────────────────────────┐
│              NVIDIA Platform Services                    │
│    (NIM, NeMo, TensorRT-LLM, Triton)                   │
└─────────────────────────────────────────────────────────┘
```

## Cost Estimation

Use the cost estimator to plan your budget:

```bash
python deployment/provision_labs.py \
  --action estimate \
  --count 100 \
  --hours 40 \
  --instance-type g5.xlarge
```

Example output:
```
Total estimated cost: $4,024.00
Cost per student: $40.24
```

## Support

### Documentation

- Installation: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- Configuration: [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md)
- Troubleshooting: [TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md)
- Maintenance: [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md)

### Technical Support

- Email: ncp-aai-support@nvidia.com
- Forum: https://forums.nvidia.com/ncp-aai
- Emergency: +1-800-NVIDIA-HELP

### Community

- GitHub: https://github.com/nvidia/ncp-aai-course
- Discord: https://discord.gg/nvidia-education
- Twitter: @NVIDIAEducation

## License

Copyright © 2026 NVIDIA Corporation. All rights reserved.

This course material is provided for educational purposes. See LICENSE file for details.

## Changelog

### Version 1.0 (January 2026)
- Initial release
- 13 modules covering all exam topics
- Full NVIDIA platform integration
- SCORM 2004 and xAPI support
- Automated lab provisioning
- Comprehensive documentation

## Roadmap

### Version 1.1 (Q2 2026)
- Additional practice exams
- Enhanced monitoring dashboards
- Multi-language support
- Mobile-optimized content

### Version 2.0 (Q4 2026)
- Advanced multi-agent labs
- Real-world case studies
- Industry certifications
- Enterprise features

## Contributing

We welcome contributions! Please see CONTRIBUTING.md for guidelines.

## Acknowledgments

- NVIDIA Education Team
- Course content developers
- Beta testers and early adopters
- Open source community

---

**Document Version:** 1.0  
**Last Updated:** January 2026  
**Maintained By:** NVIDIA Education Team
