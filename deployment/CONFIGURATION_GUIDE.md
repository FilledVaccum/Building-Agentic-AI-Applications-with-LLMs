# Configuration Guide: NCP-AAI Course

## Overview

This guide provides detailed configuration options for customizing the NCP-AAI course deployment to meet your organization's specific needs.

## Course Configuration

### Basic Settings

Edit `config/course_config.json`:

```json
{
  "course_title": "Building Agentic AI Applications with LLMs",
  "course_code": "NCP-AAI-001",
  "course_version": "1.0",
  "duration_weeks": 8,
  "student_capacity": 100,
  "instructor_count": 5,
  "certification_threshold": 0.80,
  "module_passing_score": 0.70,
  "practice_exam_count": 3,
  "language": "en-US",
  "timezone": "America/New_York"
}
```

### Module Configuration

Customize module settings in `config/modules_config.json`:

```json
{
  "modules": [
    {
      "module_id": 1,
      "enabled": true,
      "duration_hours": 1.5,
      "quiz_attempts": 3,
      "quiz_time_limit_minutes": 30,
      "lab_time_limit_hours": 4,
      "prerequisites": []
    }
  ]
}
```

### Assessment Configuration

Configure assessment behavior in `config/assessment_config.json`:

```json
{
  "module_quizzes": {
    "attempts_allowed": 3,
    "time_limit_minutes": 30,
    "passing_score": 0.70,
    "show_correct_answers": true,
    "randomize_questions": true,
    "randomize_options": true
  },
  "practice_exams": {
    "attempts_allowed": -1,
    "time_limit_minutes": 120,
    "question_count": 65,
    "passing_score": 0.80,
    "show_correct_answers": true,
    "detailed_feedback": true
  },
  "final_project": {
    "submission_deadline_days": 14,
    "late_submission_penalty": 0.10,
    "peer_review_enabled": false,
    "instructor_review_required": true
  }
}
```

## Lab Environment Configuration

### Cloud Provider Settings

#### AWS Configuration

Edit `deployment/terraform/terraform.tfvars`:

```hcl
aws_region = "us-east-1"
instance_type = "g5.xlarge"
student_count = 100
vpc_cidr = "10.0.0.0/16"
subnet_cidr = "10.0.1.0/24"

# Auto-scaling configuration
min_instances = 0
max_instances = 120
desired_instances = 100

# Storage configuration
ebs_volume_size = 500
ebs_volume_type = "gp3"
ebs_iops = 3000

# Networking
enable_public_ip = true
ssh_allowed_cidrs = ["0.0.0.0/0"]
jupyter_allowed_cidrs = ["0.0.0.0/0"]

# Tags
tags = {
  Environment = "production"
  Course = "NCP-AAI"
  ManagedBy = "Terraform"
}
```

#### Azure Configuration

```hcl
azure_region = "eastus"
resource_group_name = "ncp-aai-labs"
vm_size = "Standard_NC24ads_A100_v4"
student_count = 100

# Networking
vnet_address_space = ["10.0.0.0/16"]
subnet_address_prefix = "10.0.1.0/24"

# Storage
os_disk_size_gb = 500
os_disk_type = "Premium_LRS"
```

### Docker Container Configuration

Customize `deployment/docker/Dockerfile`:

```dockerfile
# Change base image version
FROM nvidia/cuda:12.2.0-cudnn8-devel-ubuntu22.04

# Add custom Python packages
RUN pip3 install --no-cache-dir \
    your-custom-package==1.0.0

# Add custom datasets
COPY custom_datasets/ /workspace/datasets/

# Configure Jupyter extensions
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

### Resource Limits

Configure resource limits in `deployment/docker/docker-compose.yml`:

```yaml
version: '3.8'
services:
  lab:
    image: ncp-aai-lab:latest
    deploy:
      resources:
        limits:
          cpus: '8'
          memory: 32G
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## NVIDIA Platform Configuration

### API Access

Configure NVIDIA platform access in `.env`:

```bash
# NVIDIA NIM
NVIDIA_API_KEY=your-nvidia-api-key
NVIDIA_NIM_ENDPOINT=https://api.nvidia.com/nim/v1
NVIDIA_NIM_MODEL=llama-3-70b-instruct
NVIDIA_NIM_TIMEOUT=30

# NVIDIA NeMo
NEMO_API_KEY=your-nemo-api-key
NEMO_ENDPOINT=https://api.nvidia.com/nemo/v1
NEMO_GUARDRAILS_ENABLED=true

# TensorRT-LLM
TENSORRT_LLM_PATH=/usr/local/tensorrt_llm
TENSORRT_LLM_PRECISION=fp16
TENSORRT_LLM_MAX_BATCH_SIZE=8

# Triton Inference Server
TRITON_SERVER_URL=http://localhost:8000
TRITON_HTTP_PORT=8000
TRITON_GRPC_PORT=8001
TRITON_METRICS_PORT=8002
```

### Rate Limiting

Configure API rate limits in `config/nvidia_config.json`:

```json
{
  "rate_limits": {
    "nim": {
      "requests_per_minute": 60,
      "requests_per_hour": 1000,
      "concurrent_requests": 10
    },
    "nemo": {
      "requests_per_minute": 30,
      "requests_per_hour": 500,
      "concurrent_requests": 5
    }
  },
  "retry_policy": {
    "max_retries": 3,
    "backoff_factor": 2,
    "max_backoff_seconds": 60
  }
}
```

## LMS Integration Configuration

### SCORM Settings

Configure SCORM package generation in `config/scorm_config.json`:

```json
{
  "manifest": {
    "identifier": "NCP_AAI_COURSE",
    "version": "1.0",
    "schema": "ADL SCORM",
    "schemaversion": "2004 4th Edition"
  },
  "sequencing": {
    "enforce_prerequisites": true,
    "allow_skip": false,
    "completion_threshold": 0.70
  },
  "tracking": {
    "track_completion": true,
    "track_time": true,
    "track_score": true,
    "track_interactions": true
  }
}
```

### xAPI Configuration

Configure xAPI statements in `config/xapi_config.json`:

```json
{
  "lrs": {
    "endpoint": "https://your-lrs.example.com/xapi/",
    "username": "your-lrs-username",
    "password": "your-lrs-password",
    "version": "1.0.3"
  },
  "statements": {
    "module_completed": true,
    "assessment_attempted": true,
    "lab_completed": true,
    "certification_ready": true
  },
  "actor": {
    "account_homepage": "https://your-org.example.com",
    "account_name_format": "email"
  }
}
```

## Security Configuration

### Authentication

Configure authentication in `config/security_config.json`:

```json
{
  "authentication": {
    "method": "oauth2",
    "provider": "okta",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "redirect_uri": "https://your-lms.example.com/auth/callback",
    "scopes": ["openid", "profile", "email"]
  },
  "session": {
    "timeout_minutes": 120,
    "refresh_enabled": true,
    "secure_cookies": true
  }
}
```

### API Key Management

```bash
# Rotate API keys automatically
cat > deployment/scripts/rotate_keys.sh << 'EOF'
#!/bin/bash
# Generate new API keys
NEW_KEY=$(openssl rand -hex 32)

# Update in secrets manager
aws secretsmanager update-secret \
  --secret-id ncp-aai/nvidia-api-key \
  --secret-string $NEW_KEY

# Update in lab environments
# ... deployment logic ...

echo "API keys rotated successfully"
EOF
```

### Network Security

Configure firewall rules:

```bash
# AWS Security Group rules
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 22 \
  --cidr 10.0.0.0/8  # Internal only

aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 8888 \
  --cidr 0.0.0.0/0  # Jupyter access
```

## Monitoring Configuration

### Prometheus

Configure Prometheus in `deployment/monitoring/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'lab-instances'
    static_configs:
      - targets: ['localhost:9090']
    
  - job_name: 'jupyter-metrics'
    static_configs:
      - targets: ['*:8888']
    
  - job_name: 'nvidia-gpu'
    static_configs:
      - targets: ['*:9445']
```

### Grafana Dashboards

Import pre-configured dashboards:

```bash
# Copy dashboard configurations
cp deployment/monitoring/dashboards/*.json /var/lib/grafana/dashboards/

# Restart Grafana
sudo systemctl restart grafana-server
```

### Alerting

Configure alerts in `deployment/monitoring/alerts.yml`:

```yaml
groups:
  - name: lab_alerts
    rules:
      - alert: LabInstanceDown
        expr: up{job="lab-instances"} == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Lab instance is down"
          
      - alert: HighGPUUtilization
        expr: nvidia_gpu_utilization > 95
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "GPU utilization above 95%"
```

## Backup Configuration

### Automated Backups

Configure backup schedule in `config/backup_config.json`:

```json
{
  "schedule": {
    "frequency": "daily",
    "time": "02:00",
    "timezone": "America/New_York"
  },
  "retention": {
    "daily_backups": 7,
    "weekly_backups": 4,
    "monthly_backups": 12
  },
  "targets": [
    "course_content",
    "student_data",
    "lab_configurations",
    "assessment_results"
  ],
  "storage": {
    "type": "s3",
    "bucket": "ncp-aai-backups",
    "encryption": "AES256"
  }
}
```

## Performance Tuning

### Database Optimization

```sql
-- Optimize LMS database
-- For PostgreSQL
CREATE INDEX idx_student_progress ON student_progress(student_id, module_id);
CREATE INDEX idx_assessment_results ON assessment_results(student_id, assessment_id);

-- Vacuum and analyze
VACUUM ANALYZE;
```

### Caching Configuration

Configure Redis caching:

```bash
# Install Redis
sudo apt-get install redis-server

# Configure Redis
cat > /etc/redis/redis.conf << EOF
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
EOF

# Restart Redis
sudo systemctl restart redis-server
```

### Load Balancing

Configure NGINX load balancer:

```nginx
upstream lab_instances {
    least_conn;
    server lab1.example.com:8888;
    server lab2.example.com:8888;
    server lab3.example.com:8888;
}

server {
    listen 443 ssl;
    server_name labs.example.com;
    
    ssl_certificate /etc/ssl/certs/lab.crt;
    ssl_certificate_key /etc/ssl/private/lab.key;
    
    location / {
        proxy_pass http://lab_instances;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Customization

### Branding

Customize course branding:

```css
/* custom_styles.css */
:root {
    --primary-color: #76b900;  /* NVIDIA green */
    --secondary-color: #000000;
    --accent-color: #ffffff;
}

.course-header {
    background-color: var(--primary-color);
    color: var(--accent-color);
}

.module-card {
    border-left: 4px solid var(--primary-color);
}
```

### Email Templates

Customize email templates in `config/email_templates/`:

```html
<!-- welcome_email.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Welcome to NCP-AAI Course</title>
</head>
<body>
    <h1>Welcome {{student_name}}!</h1>
    <p>You have been enrolled in the Building Agentic AI Applications course.</p>
    <p>Your lab environment: <a href="{{lab_url}}">{{lab_url}}</a></p>
</body>
</html>
```

## Troubleshooting Configuration Issues

### Validate Configuration Files

```bash
# Validate JSON configuration
python -m json.tool config/course_config.json

# Validate Terraform configuration
terraform validate deployment/terraform/

# Validate Docker configuration
docker-compose -f deployment/docker/docker-compose.yml config
```

### Configuration Backup

```bash
# Backup all configuration files
tar -czf config_backup_$(date +%Y%m%d).tar.gz config/ deployment/
```

---

**Document Version:** 1.0  
**Last Updated:** January 2026
