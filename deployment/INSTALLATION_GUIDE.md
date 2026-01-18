# Installation Guide: NCP-AAI Course Deployment

## Overview

This guide provides step-by-step instructions for installing and deploying the "Building Agentic AI Applications with LLMs" course in your organization. The deployment includes course content, lab environments, assessment systems, and LMS integration.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Requirements](#system-requirements)
3. [Installation Steps](#installation-steps)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Post-Installation](#post-installation)

## Prerequisites

### Required Accounts and Access

- **NVIDIA Developer Program**: Free membership required
  - Sign up at: https://developer.nvidia.com/developer-program
  - Obtain API keys for NIM, NeMo, and other services

- **Cloud Provider Account**: One of the following
  - NVIDIA DGX Cloud (recommended)
  - AWS with GPU quota
  - Azure with GPU quota

- **LMS Platform**: SCORM 2004 compatible
  - Moodle 3.9+, Canvas, Blackboard, or D2L Brightspace

- **Container Registry**: For Docker images
  - Docker Hub (free tier available)
  - AWS ECR, Azure ACR, or private registry

### Required Software

Install the following on your deployment machine:

```bash
# Python 3.10+
python3 --version

# Docker 20.10+
docker --version

# Terraform 1.0+ (for infrastructure provisioning)
terraform --version

# kubectl (for Kubernetes management)
kubectl version --client

# Cloud provider CLI
aws --version  # or az --version for Azure
```

### Required Permissions

- Cloud provider admin access
- LMS administrator access
- Container registry push permissions
- DNS management (for custom domains)

## System Requirements

### Deployment Server

Minimum specifications for the deployment/management server:

- **CPU**: 4 cores
- **RAM**: 16 GB
- **Storage**: 100 GB SSD
- **Network**: 1 Gbps connection
- **OS**: Ubuntu 22.04 LTS or macOS 12+

### Lab Environment

Per-student requirements:

- **GPU**: 1x NVIDIA A100 (40GB) or equivalent
- **CPU**: 8 cores
- **RAM**: 32 GB
- **Storage**: 500 GB SSD
- **Network**: 10 Gbps connection

### LMS Server

- **CPU**: 8+ cores
- **RAM**: 32+ GB
- **Storage**: 500+ GB
- **Concurrent Users**: Support for 100+ students

## Installation Steps

### Step 1: Clone Repository

```bash
# Clone the course repository
git clone https://github.com/nvidia/ncp-aai-course.git
cd ncp-aai-course

# Verify contents
ls -la
```

### Step 2: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python -c "import src.models.course; print('Dependencies installed successfully')"
```

### Step 3: Configure NVIDIA Platform Access

```bash
# Set up NVIDIA API credentials
export NVIDIA_API_KEY="your-nvidia-api-key"
export NVIDIA_NIM_ENDPOINT="https://api.nvidia.com/nim/v1"
export NEMO_API_KEY="your-nemo-api-key"

# Save to environment file
cat > .env << EOF
NVIDIA_API_KEY=${NVIDIA_API_KEY}
NVIDIA_NIM_ENDPOINT=${NVIDIA_NIM_ENDPOINT}
NEMO_API_KEY=${NEMO_API_KEY}
EOF

# Test API access
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('NVIDIA API configured:', os.getenv('NVIDIA_API_KEY')[:10] + '...')
"
```

### Step 4: Build Docker Container

```bash
# Navigate to Docker directory
cd deployment/docker

# Build container image
docker build -t ncp-aai-lab:latest .

# Test container locally
docker run --rm --gpus all ncp-aai-lab:latest python -c "import torch; print('CUDA available:', torch.cuda.is_available())"

# Tag for registry
docker tag ncp-aai-lab:latest your-registry/ncp-aai-lab:latest

# Push to registry
docker push your-registry/ncp-aai-lab:latest
```

### Step 5: Generate SCORM Package

```bash
# Return to project root
cd ../..

# Generate integrated course data
python integrate_course_system.py

# Create SCORM package
python -c "
from deployment.scorm_packager import SCORMPackager
import json

# Load course data
with open('integrated_course.json', 'r') as f:
    course_data = json.load(f)

# Create packager
packager = SCORMPackager(course_data)

# Generate package
package_path = packager.create_package('ncp_aai_course_v1')
print(f'SCORM package created: {package_path}')
"
```

### Step 6: Provision Lab Environments

```bash
# Configure cloud provider credentials
# For AWS:
aws configure

# For Azure:
az login

# Estimate costs
python deployment/provision_labs.py \
  --action estimate \
  --count 100 \
  --hours 40 \
  --instance-type g5.xlarge

# Provision lab environments
python deployment/provision_labs.py \
  --action provision \
  --count 100 \
  --provider aws

# Verify provisioning
python deployment/provision_labs.py \
  --action status \
  --provider aws
```

### Step 7: Upload to LMS

#### For Moodle:

1. Log in to Moodle as administrator
2. Navigate to your course
3. Turn editing on
4. Add activity → SCORM package
5. Upload `deployment/packages/ncp_aai_course_v1.zip`
6. Configure settings:
   - Grading method: Highest attempt
   - Maximum grade: 100
   - Attempts allowed: Unlimited
7. Save and display

#### For Canvas:

1. Log in to Canvas as administrator
2. Go to Settings → Import Course Content
3. Select "SCORM Package" as content type
4. Upload `deployment/packages/ncp_aai_course_v1.zip`
5. Complete import process
6. Configure grading and completion settings

#### For Blackboard:

1. Log in to Blackboard as administrator
2. Navigate to Content area
3. Build Content → SCORM Package
4. Browse and upload `deployment/packages/ncp_aai_course_v1.zip`
5. Submit and configure settings

### Step 8: Configure LMS Integration

```bash
# Generate LMS integration documentation
cp deployment/LMS_INTEGRATION.md /path/to/lms/documentation/

# Configure xAPI endpoint (if supported)
# In LMS settings:
# - LRS Endpoint: https://your-lrs-endpoint.com/xapi/
# - Auth Type: Basic Auth
# - Enable statement tracking
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# NVIDIA Platform
NVIDIA_API_KEY=your-nvidia-api-key
NVIDIA_NIM_ENDPOINT=https://api.nvidia.com/nim/v1
NEMO_API_KEY=your-nemo-api-key
NEMO_ENDPOINT=https://api.nvidia.com/nemo/v1

# Cloud Provider (AWS example)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key

# Lab Environment
LAB_INSTANCE_TYPE=g5.xlarge
LAB_STUDENT_COUNT=100
LAB_DOCKER_IMAGE=your-registry/ncp-aai-lab:latest

# LMS Integration
LMS_TYPE=moodle
LMS_URL=https://your-lms.example.com
LMS_API_KEY=your-lms-api-key

# xAPI/LRS
LRS_ENDPOINT=https://your-lrs.example.com/xapi/
LRS_USERNAME=your-lrs-username
LRS_PASSWORD=your-lrs-password

# Monitoring
PROMETHEUS_ENDPOINT=http://localhost:9090
GRAFANA_ENDPOINT=http://localhost:3000
```

### Course Configuration

Edit `config/course_config.json`:

```json
{
  "course_title": "Building Agentic AI Applications with LLMs",
  "course_code": "NCP-AAI-001",
  "duration_weeks": 8,
  "student_capacity": 100,
  "certification_threshold": 0.80,
  "module_passing_score": 0.70,
  "practice_exam_count": 3,
  "lab_environment": {
    "provider": "aws",
    "instance_type": "g5.xlarge",
    "auto_teardown": true,
    "teardown_delay_hours": 24
  },
  "nvidia_platforms": {
    "nim_enabled": true,
    "nemo_enabled": true,
    "tensorrt_enabled": true,
    "triton_enabled": true
  }
}
```

### Security Configuration

```bash
# Generate SSL certificates for lab environments
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout deployment/certs/lab.key \
  -out deployment/certs/lab.crt

# Set up firewall rules
# Allow only necessary ports: 22 (SSH), 8888 (Jupyter), 443 (HTTPS)

# Configure API key rotation
# Set up automated rotation every 90 days
```

## Verification

### Verify Course Content

```bash
# Validate all course content
python src/content_validation.py

# Check module completeness
python validate_modules_1_4.py
python validate_modules_5_8.py
python validate_modules_9_13.py

# Verify assessment system
python demo_assessment_system.py
```

### Verify Lab Environment

```bash
# Check lab instance health
python deployment/scripts/health_check.py

# Test GPU access
ssh ubuntu@<lab-instance-ip> nvidia-smi

# Test Jupyter access
curl http://<lab-instance-ip>:8888

# Test NVIDIA API access
ssh ubuntu@<lab-instance-ip> "python -c 'import os; print(os.getenv(\"NVIDIA_API_KEY\"))'"
```

### Verify LMS Integration

1. Log in to LMS as a test student
2. Access the NCP-AAI course
3. Complete Module 1 quiz
4. Verify progress tracking
5. Check grade book integration
6. Test lab environment link

### Run Integration Tests

```bash
# Run all property-based tests
pytest tests/test_properties.py -v

# Run code quality tests
pytest tests/test_code_quality.py -v

# Generate test report
pytest --html=test_report.html --self-contained-html
```

## Post-Installation

### Student Onboarding

1. **Create Student Accounts**:
   ```bash
   # Bulk import students to LMS
   # Prepare CSV file with student data
   # Import via LMS admin interface
   ```

2. **Send Welcome Email**:
   - Course access instructions
   - Lab environment credentials
   - NVIDIA platform setup guide
   - Support contact information

3. **Schedule Orientation Session**:
   - Course overview
   - Platform walkthrough
   - Lab environment demo
   - Q&A session

### Instructor Setup

1. **Provide Instructor Materials**:
   ```bash
   # Copy instructor materials
   cp -r content/instructor /path/to/instructor/resources/
   ```

2. **Configure Grading Access**:
   - Grant instructor role in LMS
   - Provide access to solution code
   - Set up grading rubrics

3. **Schedule Training**:
   - Platform training
   - Grading procedures
   - Student support protocols

### Monitoring Setup

```bash
# Set up Prometheus monitoring
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/deployment/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Set up Grafana dashboards
docker run -d \
  --name grafana \
  -p 3000:3000 \
  grafana/grafana

# Import course dashboards
# Access Grafana at http://localhost:3000
# Import dashboards from deployment/monitoring/dashboards/
```

### Backup Configuration

```bash
# Set up automated backups
# Create backup script
cat > deployment/scripts/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/ncp-aai"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup course content
tar -czf ${BACKUP_DIR}/content_${DATE}.tar.gz content/

# Backup student data
# Export from LMS

# Backup lab configurations
tar -czf ${BACKUP_DIR}/deployment_${DATE}.tar.gz deployment/

echo "Backup completed: ${DATE}"
EOF

chmod +x deployment/scripts/backup.sh

# Schedule daily backups
crontab -e
# Add: 0 2 * * * /path/to/deployment/scripts/backup.sh
```

### Update Procedures

```bash
# Create update script
cat > deployment/scripts/update.sh << 'EOF'
#!/bin/bash
echo "Updating NCP-AAI Course..."

# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Rebuild Docker images
cd deployment/docker
docker build -t ncp-aai-lab:latest .
docker push your-registry/ncp-aai-lab:latest

# Update SCORM package
cd ../..
python -c "
from deployment.scorm_packager import SCORMPackager
import json
with open('integrated_course.json', 'r') as f:
    course_data = json.load(f)
packager = SCORMPackager(course_data)
packager.create_package('ncp_aai_course_updated')
"

echo "Update completed. Please re-upload SCORM package to LMS."
EOF

chmod +x deployment/scripts/update.sh
```

## Troubleshooting

### Common Installation Issues

**Issue: Docker build fails**
```bash
# Solution: Check Docker daemon is running
sudo systemctl status docker

# Solution: Increase Docker memory limit
# Edit /etc/docker/daemon.json
{
  "default-runtime": "nvidia",
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
}
```

**Issue: Terraform provisioning fails**
```bash
# Solution: Verify cloud credentials
aws sts get-caller-identity

# Solution: Check quota limits
aws service-quotas list-service-quotas --service-code ec2

# Solution: Review Terraform logs
terraform plan -out=tfplan
terraform show tfplan
```

**Issue: SCORM package upload fails**
```bash
# Solution: Check file size limits in LMS
# Increase PHP upload limits if using Moodle:
# Edit php.ini:
upload_max_filesize = 500M
post_max_size = 500M

# Restart web server
sudo systemctl restart apache2
```

### Getting Help

- **Documentation**: See `deployment/` directory for detailed guides
- **Technical Support**: ncp-aai-support@nvidia.com
- **Community Forum**: https://forums.nvidia.com/ncp-aai
- **Emergency Hotline**: +1-800-NVIDIA-HELP

## Next Steps

After successful installation:

1. Review [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md) for advanced settings
2. Read [TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md) for common issues
3. Consult [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) for ongoing operations
4. Check [LMS_INTEGRATION.md](LMS_INTEGRATION.md) for LMS-specific configuration

## Appendix

### Installation Checklist

- [ ] Prerequisites verified
- [ ] Software dependencies installed
- [ ] NVIDIA API access configured
- [ ] Docker container built and pushed
- [ ] SCORM package generated
- [ ] Lab environments provisioned
- [ ] LMS upload completed
- [ ] Integration tests passed
- [ ] Student accounts created
- [ ] Instructor training scheduled
- [ ] Monitoring configured
- [ ] Backup procedures established

### Support Resources

- Installation Guide: This document
- Configuration Guide: `deployment/CONFIGURATION_GUIDE.md`
- Troubleshooting Guide: `deployment/TROUBLESHOOTING_GUIDE.md`
- Maintenance Guide: `deployment/MAINTENANCE_GUIDE.md`
- LMS Integration: `deployment/LMS_INTEGRATION.md`
- Lab Environment Setup: `deployment/LAB_ENVIRONMENT_SETUP.md`

---

**Document Version:** 1.0  
**Last Updated:** January 2026  
**Maintained By:** NVIDIA Education Team
