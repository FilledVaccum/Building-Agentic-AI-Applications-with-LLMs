# Troubleshooting Guide: NCP-AAI Course

## Overview

This guide provides solutions to common issues encountered during deployment, operation, and maintenance of the NCP-AAI course.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Lab Environment Issues](#lab-environment-issues)
3. [LMS Integration Issues](#lms-integration-issues)
4. [NVIDIA Platform Issues](#nvidia-platform-issues)
5. [Performance Issues](#performance-issues)
6. [Student Access Issues](#student-access-issues)
7. [Assessment Issues](#assessment-issues)

## Installation Issues

### Issue: Docker Build Fails

**Symptoms:**
- Docker build command exits with error
- Missing dependencies or packages

**Solutions:**

```bash
# Check Docker daemon status
sudo systemctl status docker

# Restart Docker daemon
sudo systemctl restart docker

# Clear Docker cache
docker system prune -a

# Rebuild with no cache
docker build --no-cache -t ncp-aai-lab:latest .

# Check Docker logs
docker logs <container-id>
```

### Issue: Terraform Provisioning Fails

**Symptoms:**
- Terraform apply fails
- Quota exceeded errors
- Authentication errors

**Solutions:**

```bash
# Verify cloud credentials
aws sts get-caller-identity  # For AWS
az account show  # For Azure

# Check quota limits
aws service-quotas list-service-quotas --service-code ec2

# Request quota increase
aws service-quotas request-service-quota-increase \
  --service-code ec2 \
  --quota-code L-417A185B \
  --desired-value 20

# Review Terraform state
terraform state list
terraform state show <resource>

# Destroy and recreate
terraform destroy -auto-approve
terraform apply -auto-approve
```

### Issue: Python Dependencies Installation Fails

**Symptoms:**
- pip install errors
- Version conflicts
- Missing system libraries

**Solutions:**

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# Install system dependencies (Ubuntu)
sudo apt-get update
sudo apt-get install -y python3-dev build-essential

# Use virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Clear pip cache
pip cache purge
```

## Lab Environment Issues

### Issue: Lab Instance Won't Start

**Symptoms:**
- Instance stuck in "pending" state
- Instance fails health checks
- Cannot connect to instance

**Solutions:**

```bash
# Check instance status
aws ec2 describe-instances --instance-ids i-xxxxx

# Check system logs
aws ec2 get-console-output --instance-id i-xxxxx

# Reboot instance
aws ec2 reboot-instances --instance-ids i-xxxxx

# Terminate and recreate
aws ec2 terminate-instances --instance-ids i-xxxxx
# Wait for termination, then provision new instance
```

### Issue: GPU Not Detected

**Symptoms:**
- nvidia-smi command fails
- CUDA not available in Python
- GPU-accelerated tasks fail

**Solutions:**

```bash
# Check NVIDIA driver installation
nvidia-smi

# Install NVIDIA drivers (if missing)
sudo apt-get update
sudo apt-get install -y nvidia-driver-525

# Verify CUDA installation
nvcc --version

# Check Docker GPU access
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi

# Restart NVIDIA services
sudo systemctl restart nvidia-persistenced
```

### Issue: Jupyter Not Accessible

**Symptoms:**
- Cannot access Jupyter at port 8888
- Connection timeout
- 502 Bad Gateway error

**Solutions:**

```bash
# Check if Jupyter is running
docker ps | grep ncp-aai-lab

# Check Jupyter logs
docker logs ncp-aai-lab

# Restart Jupyter container
docker restart ncp-aai-lab

# Check port binding
netstat -tulpn | grep 8888

# Check security group rules
aws ec2 describe-security-groups --group-ids sg-xxxxx

# Test local access
curl http://localhost:8888

# Check firewall
sudo ufw status
sudo ufw allow 8888/tcp
```

### Issue: Out of Disk Space

**Symptoms:**
- "No space left on device" errors
- Lab operations fail
- Cannot save files

**Solutions:**

```bash
# Check disk usage
df -h

# Find large files
du -sh /* | sort -h

# Clean Docker images
docker system prune -a

# Clean Jupyter checkpoints
find /workspace -name ".ipynb_checkpoints" -type d -exec rm -rf {} +

# Increase EBS volume size (AWS)
aws ec2 modify-volume --volume-id vol-xxxxx --size 1000

# Extend filesystem
sudo resize2fs /dev/xvda1
```

## LMS Integration Issues

### Issue: SCORM Package Upload Fails

**Symptoms:**
- Upload times out
- File size error
- Invalid package error

**Solutions:**

```bash
# Check file size
ls -lh deployment/packages/*.zip

# Increase PHP limits (Moodle)
sudo nano /etc/php/8.1/apache2/php.ini
# Set:
upload_max_filesize = 500M
post_max_size = 500M
max_execution_time = 300

# Restart web server
sudo systemctl restart apache2

# Validate SCORM package
unzip -t deployment/packages/ncp_aai_course_v1.zip

# Check manifest validity
xmllint --noout deployment/packages/temp/imsmanifest.xml
```

### Issue: Progress Not Tracking

**Symptoms:**
- Student progress not saved
- Completion status not updating
- Grades not recording

**Solutions:**

```bash
# Check SCORM API initialization
# In browser console:
console.log(window.API_1484_11);

# Verify LMS SCORM player settings
# Enable: Track completion, Track score, Track time

# Check browser cookies
# Ensure cookies are enabled
# Clear cookies and retry

# Check LMS logs
tail -f /var/log/moodle/error.log

# Test with different browser
# Try Chrome, Firefox, Safari
```

### Issue: xAPI Statements Not Recording

**Symptoms:**
- No data in LRS
- xAPI errors in console
- Authentication failures

**Solutions:**

```bash
# Verify LRS endpoint
curl -X GET https://your-lrs.example.com/xapi/about \
  -u username:password

# Check xAPI statement format
python -c "
import json
with open('deployment/packages/temp/xapi_statements.json') as f:
    statements = json.load(f)
    print(json.dumps(statements[0], indent=2))
"

# Test statement submission
curl -X POST https://your-lrs.example.com/xapi/statements \
  -H "Content-Type: application/json" \
  -H "X-Experience-API-Version: 1.0.3" \
  -u username:password \
  -d @test_statement.json

# Check CORS settings
# Ensure LRS allows requests from LMS domain
```

## NVIDIA Platform Issues

### Issue: API Authentication Fails

**Symptoms:**
- 401 Unauthorized errors
- Invalid API key errors
- Rate limit exceeded

**Solutions:**

```bash
# Verify API key
echo $NVIDIA_API_KEY

# Test API access
curl -X GET https://api.nvidia.com/nim/v1/models \
  -H "Authorization: Bearer $NVIDIA_API_KEY"

# Regenerate API key
# Visit https://developer.nvidia.com/
# Navigate to API Keys section
# Generate new key

# Check rate limits
curl -X GET https://api.nvidia.com/nim/v1/rate_limit \
  -H "Authorization: Bearer $NVIDIA_API_KEY"

# Implement exponential backoff
# See config/nvidia_config.json
```

### Issue: NIM Inference Slow

**Symptoms:**
- High latency
- Timeouts
- Slow response times

**Solutions:**

```bash
# Check network latency
ping api.nvidia.com

# Use regional endpoint
export NVIDIA_NIM_ENDPOINT=https://api-us-east.nvidia.com/nim/v1

# Increase timeout
export NVIDIA_NIM_TIMEOUT=60

# Enable request batching
# See lab code examples

# Monitor API performance
curl -X GET https://api.nvidia.com/nim/v1/status
```

### Issue: TensorRT-LLM Optimization Fails

**Symptoms:**
- Model conversion errors
- Out of memory errors
- Unsupported operations

**Solutions:**

```bash
# Check GPU memory
nvidia-smi

# Reduce batch size
export TENSORRT_LLM_MAX_BATCH_SIZE=4

# Use lower precision
export TENSORRT_LLM_PRECISION=int8

# Check TensorRT version
python -c "import tensorrt; print(tensorrt.__version__)"

# Review conversion logs
cat /workspace/tensorrt_conversion.log
```

## Performance Issues

### Issue: Slow Lab Performance

**Symptoms:**
- Slow Jupyter response
- Long execution times
- High CPU/GPU usage

**Solutions:**

```bash
# Check resource usage
htop
nvidia-smi

# Restart Jupyter kernel
# In Jupyter: Kernel → Restart

# Clear output cells
# In Jupyter: Cell → All Output → Clear

# Increase instance size
# Modify terraform.tfvars:
instance_type = "g5.2xlarge"

# Enable GPU acceleration
# Verify CUDA is being used in code

# Optimize code
# Use vectorized operations
# Batch API calls
```

### Issue: High Network Latency

**Symptoms:**
- Slow API responses
- Timeouts
- Connection drops

**Solutions:**

```bash
# Check network connectivity
ping api.nvidia.com
traceroute api.nvidia.com

# Use CDN for static content
# Configure CloudFront or similar

# Enable compression
# In NGINX:
gzip on;
gzip_types text/plain application/json;

# Optimize DNS
# Use Route53 or CloudFlare DNS

# Enable HTTP/2
# In NGINX:
listen 443 ssl http2;
```

## Student Access Issues

### Issue: Cannot Access Course

**Symptoms:**
- Login fails
- Course not visible
- Permission denied

**Solutions:**

```bash
# Verify student enrollment
# Check LMS user management

# Reset password
# Use LMS password reset function

# Check course visibility
# Ensure course is published

# Verify user role
# Ensure student role is assigned

# Clear browser cache
# Ctrl+Shift+Delete in most browsers
```

### Issue: Lab Credentials Not Working

**Symptoms:**
- SSH connection refused
- Jupyter login fails
- API key invalid

**Solutions:**

```bash
# Regenerate SSH key
ssh-keygen -t rsa -b 4096

# Update authorized_keys
cat ~/.ssh/id_rsa.pub | ssh ubuntu@<lab-ip> "cat >> ~/.ssh/authorized_keys"

# Reset Jupyter token
docker exec ncp-aai-lab jupyter notebook list

# Verify API keys
cat /workspace/.env

# Provision new lab instance
python deployment/provision_labs.py --action provision --count 1
```

## Assessment Issues

### Issue: Quiz Not Submitting

**Symptoms:**
- Submit button not working
- Timeout on submission
- Answers not saved

**Solutions:**

```bash
# Check browser console for errors
# F12 → Console tab

# Disable browser extensions
# Try in incognito/private mode

# Check LMS server load
top
# Look for high CPU/memory usage

# Increase PHP timeout
# In php.ini:
max_execution_time = 300

# Check database connections
# In MySQL:
SHOW PROCESSLIST;
```

### Issue: Incorrect Grading

**Symptoms:**
- Wrong scores calculated
- Grading logic errors
- Missing points

**Solutions:**

```python
# Verify grading logic
python -c "
from src.models.assessment import Assessment
# Test grading with known answers
"

# Check answer key
cat content/assessments/quiz_01_fundamentals.json | jq '.questions[0].correct_answer'

# Regrade submissions
# In LMS: Grades → Regrade

# Review grading rubric
cat content/instructor/grading_rubrics.md
```

## Emergency Procedures

### Complete System Failure

```bash
# 1. Check system status
python deployment/provision_labs.py --action status

# 2. Review logs
tail -f /var/log/syslog
docker logs ncp-aai-lab

# 3. Restore from backup
tar -xzf /backups/ncp-aai/content_latest.tar.gz

# 4. Recreate infrastructure
cd deployment/terraform
terraform destroy -auto-approve
terraform apply -auto-approve

# 5. Notify stakeholders
# Send status update email
```

### Data Recovery

```bash
# Restore from S3 backup
aws s3 sync s3://ncp-aai-backups/latest/ ./restore/

# Restore database
mysql -u root -p < restore/database_backup.sql

# Restore student data
# Import from LMS backup
```

## Getting Help

### Support Channels

- **Technical Support**: ncp-aai-support@nvidia.com
- **Emergency Hotline**: +1-800-NVIDIA-HELP
- **Community Forum**: https://forums.nvidia.com/ncp-aai
- **Documentation**: https://docs.nvidia.com/ncp-aai

### Diagnostic Information to Provide

When contacting support, include:

```bash
# System information
uname -a
docker --version
python --version

# Error logs
docker logs ncp-aai-lab > logs.txt

# Configuration
cat config/course_config.json

# Resource usage
nvidia-smi
df -h
free -h
```

---

**Document Version:** 1.0  
**Last Updated:** January 2026
