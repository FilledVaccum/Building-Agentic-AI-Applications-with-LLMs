# Lab Environment Setup Guide

## Overview

This guide provides comprehensive instructions for setting up and managing the lab environment for the "Building Agentic AI Applications with LLMs" course. The lab environment provides students with cloud-based GPU instances, pre-configured Docker containers, and access to NVIDIA platforms.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                  Lab Management Portal                   │
│         (Provisioning, Monitoring, Teardown)            │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼────────┐ ┌──────▼──────┐ ┌───────▼────────┐
│  NVIDIA DGX    │ │   AWS with  │ │  Azure with    │
│    Cloud       │ │  GPU (A100) │ │  GPU (A100)    │
│  (Primary)     │ │  (Fallback) │ │  (Fallback)    │
└────────────────┘ └─────────────┘ └────────────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
┌───────▼────────┐              ┌───────────▼──────────┐
│ Docker         │              │ NVIDIA Platform      │
│ Containers     │              │ Access (NIM, NeMo)   │
│ (Per Student)  │              │                      │
└────────────────┘              └──────────────────────┘
```

## Prerequisites

### Infrastructure Requirements:
- Cloud provider account (NVIDIA DGX Cloud, AWS, or Azure)
- GPU quota allocation (minimum 1 A100 GPU per 5 students)
- Container registry access (Docker Hub or private registry)
- Network bandwidth: 10 Gbps minimum
- Storage: 500GB per student instance

### Access Requirements:
- NVIDIA Developer Program membership
- NVIDIA NIM API keys
- NVIDIA NeMo access credentials
- Cloud provider admin credentials
- Docker registry credentials

### Software Requirements:
- Docker 20.10+
- Kubernetes 1.24+ (for orchestration)
- Terraform 1.0+ (for infrastructure as code)
- kubectl CLI
- Cloud provider CLI tools

## Cloud Provider Setup

### Option 1: NVIDIA DGX Cloud (Recommended)

**Advantages:**
- Optimized for NVIDIA platforms
- Pre-configured GPU drivers
- Direct access to NVIDIA services
- Best performance for course labs

**Setup Steps:**

1. **Create DGX Cloud Account:**
   ```bash
   # Visit https://www.nvidia.com/en-us/data-center/dgx-cloud/
   # Sign up for DGX Cloud access
   # Request quota for A100 GPUs
   ```

2. **Configure Access:**
   ```bash
   # Install NVIDIA Cloud CLI
   pip install nvidia-cloud-cli
   
   # Authenticate
   nvidia-cloud login --api-key YOUR_API_KEY
   
   # Verify access
   nvidia-cloud instances list
   ```

3. **Set Resource Quotas:**
   ```bash
   # Request quota increase for course
   nvidia-cloud quota request \
     --resource gpu.a100 \
     --quantity 20 \
     --reason "NCP-AAI Course - 100 students"
   ```

### Option 2: AWS with GPU Instances

**Instance Types:**
- Primary: `p4d.24xlarge` (8x A100 40GB)
- Alternative: `p3.8xlarge` (4x V100 16GB)
- Budget: `g5.xlarge` (1x A10G 24GB)

**Setup Steps:**

1. **Configure AWS CLI:**
   ```bash
   aws configure
   # Enter AWS Access Key ID
   # Enter AWS Secret Access Key
   # Default region: us-east-1
   # Default output format: json
   ```

2. **Request GPU Quota:**
   ```bash
   # Request service quota increase
   aws service-quotas request-service-quota-increase \
     --service-code ec2 \
     --quota-code L-417A185B \
     --desired-value 20
   ```

3. **Create VPC and Security Groups:**
   ```bash
   # Create VPC
   aws ec2 create-vpc --cidr-block 10.0.0.0/16
   
   # Create security group
   aws ec2 create-security-group \
     --group-name ncp-aai-lab-sg \
     --description "Security group for NCP-AAI labs" \
     --vpc-id vpc-xxxxx
   
   # Allow SSH and Jupyter
   aws ec2 authorize-security-group-ingress \
     --group-id sg-xxxxx \
     --protocol tcp \
     --port 22 \
     --cidr 0.0.0.0/0
   
   aws ec2 authorize-security-group-ingress \
     --group-id sg-xxxxx \
     --protocol tcp \
     --port 8888 \
     --cidr 0.0.0.0/0
   ```

### Option 3: Azure with GPU Instances

**Instance Types:**
- Primary: `Standard_ND96asr_v4` (8x A100 40GB)
- Alternative: `Standard_NC24ads_A100_v4` (1x A100 80GB)

**Setup Steps:**

1. **Configure Azure CLI:**
   ```bash
   az login
   az account set --subscription "Your Subscription Name"
   ```

2. **Request GPU Quota:**
   ```bash
   # Check current quota
   az vm list-usage --location eastus --output table
   
   # Request quota increase via Azure Portal
   # Navigate to: Subscriptions → Usage + quotas
   # Request increase for NDasrA100v4 family
   ```

3. **Create Resource Group:**
   ```bash
   az group create \
     --name ncp-aai-labs \
     --location eastus
   ```

## Docker Container Configuration

### Base Container Image

Create a Dockerfile for the lab environment:

```dockerfile
# deployment/docker/Dockerfile
FROM nvidia/cuda:12.2.0-cudnn8-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    curl \
    wget \
    vim \
    htop \
    tmux \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir \
    torch==2.1.0 \
    transformers==4.35.0 \
    langchain==0.1.0 \
    langgraph==0.0.20 \
    openai==1.3.0 \
    nvidia-nim-client==0.1.0 \
    nvidia-nemo==1.22.0 \
    tensorrt-llm==0.6.0 \
    tritonclient[all]==2.40.0 \
    jupyter==1.0.0 \
    jupyterlab==4.0.0 \
    ipywidgets==8.1.0 \
    matplotlib==3.8.0 \
    pandas==2.1.0 \
    numpy==1.24.0 \
    scikit-learn==1.3.0 \
    requests==2.31.0 \
    pydantic==2.5.0 \
    python-dotenv==1.0.0

# Install vector databases
RUN pip3 install --no-cache-dir \
    pymilvus==2.3.0 \
    pinecone-client==2.2.0 \
    chromadb==0.4.0 \
    faiss-gpu==1.7.2

# Install monitoring and observability tools
RUN pip3 install --no-cache-dir \
    prometheus-client==0.19.0 \
    opentelemetry-api==1.21.0 \
    opentelemetry-sdk==1.21.0

# Create working directory
WORKDIR /workspace

# Copy lab materials
COPY labs/ /workspace/labs/
COPY datasets/ /workspace/datasets/
COPY models/ /workspace/models/

# Set up Jupyter
RUN jupyter notebook --generate-config && \
    echo "c.NotebookApp.token = ''" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.password = ''" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.allow_root = True" >> ~/.jupyter/jupyter_notebook_config.py

# Expose Jupyter port
EXPOSE 8888

# Start Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
```

### Build and Push Container:

```bash
# Build container
docker build -t ncp-aai-lab:latest -f deployment/docker/Dockerfile .

# Tag for registry
docker tag ncp-aai-lab:latest your-registry/ncp-aai-lab:latest

# Push to registry
docker push your-registry/ncp-aai-lab:latest
```

## Provisioning Scripts

### Terraform Configuration

Create infrastructure as code for automated provisioning:

```hcl
# deployment/terraform/main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  default = "us-east-1"
}

variable "student_count" {
  default = 100
}

variable "instance_type" {
  default = "g5.xlarge"
}

# Launch template for GPU instances
resource "aws_launch_template" "lab_instance" {
  name_prefix   = "ncp-aai-lab-"
  image_id      = data.aws_ami.gpu_ami.id
  instance_type = var.instance_type

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    docker_image = "your-registry/ncp-aai-lab:latest"
  }))

  block_device_mappings {
    device_name = "/dev/sda1"
    ebs {
      volume_size = 500
      volume_type = "gp3"
    }
  }

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.lab_sg.id]
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name        = "ncp-aai-lab-instance"
      Environment = "production"
      Course      = "NCP-AAI"
    }
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "lab_asg" {
  name                = "ncp-aai-lab-asg"
  vpc_zone_identifier = [aws_subnet.lab_subnet.id]
  desired_capacity    = var.student_count
  max_size            = var.student_count + 20
  min_size            = 0

  launch_template {
    id      = aws_launch_template.lab_instance.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "ncp-aai-lab-instance"
    propagate_at_launch = true
  }
}

# Security Group
resource "aws_security_group" "lab_sg" {
  name        = "ncp-aai-lab-sg"
  description = "Security group for NCP-AAI lab instances"
  vpc_id      = aws_vpc.lab_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8888
    to_port     = 8888
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# VPC Configuration
resource "aws_vpc" "lab_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "ncp-aai-lab-vpc"
  }
}

resource "aws_subnet" "lab_subnet" {
  vpc_id                  = aws_vpc.lab_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "ncp-aai-lab-subnet"
  }
}

resource "aws_internet_gateway" "lab_igw" {
  vpc_id = aws_vpc.lab_vpc.id

  tags = {
    Name = "ncp-aai-lab-igw"
  }
}

resource "aws_route_table" "lab_rt" {
  vpc_id = aws_vpc.lab_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.lab_igw.id
  }

  tags = {
    Name = "ncp-aai-lab-rt"
  }
}

resource "aws_route_table_association" "lab_rta" {
  subnet_id      = aws_subnet.lab_subnet.id
  route_table_id = aws_route_table.lab_rt.id
}

# Data source for GPU-enabled AMI
data "aws_ami" "gpu_ami" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["Deep Learning AMI GPU PyTorch*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Outputs
output "asg_name" {
  value = aws_autoscaling_group.lab_asg.name
}

output "launch_template_id" {
  value = aws_launch_template.lab_instance.id
}
```

### User Data Script

```bash
#!/bin/bash
# deployment/terraform/user_data.sh

# Update system
apt-get update
apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  tee /etc/apt/sources.list.d/nvidia-docker.list

apt-get update
apt-get install -y nvidia-container-toolkit
systemctl restart docker

# Pull and run lab container
docker pull ${docker_image}
docker run -d \
  --gpus all \
  --name ncp-aai-lab \
  -p 8888:8888 \
  -v /home/ubuntu/workspace:/workspace \
  --restart unless-stopped \
  ${docker_image}

# Configure NVIDIA API access
mkdir -p /home/ubuntu/.nvidia
cat > /home/ubuntu/.nvidia/credentials << EOF
NVIDIA_API_KEY=${nvidia_api_key}
NVIDIA_NIM_ENDPOINT=${nvidia_nim_endpoint}
EOF

# Set up monitoring
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v /etc/prometheus:/etc/prometheus \
  prom/prometheus

# Health check endpoint
cat > /usr/local/bin/health-check.sh << 'EOF'
#!/bin/bash
if docker ps | grep -q ncp-aai-lab; then
  echo "Lab container is running"
  exit 0
else
  echo "Lab container is not running"
  exit 1
fi
EOF
chmod +x /usr/local/bin/health-check.sh
```

### Provisioning Script

```python
# deployment/provision_labs.py
"""
Lab environment provisioning script.
"""

import subprocess
import json
import time
from typing import List, Dict


def provision_lab_environments(student_count: int, cloud_provider: str = "aws") -> List[Dict]:
    """
    Provision lab environments for students.
    
    Args:
        student_count: Number of student environments to provision
        cloud_provider: Cloud provider to use (aws, azure, dgx)
        
    Returns:
        List of provisioned instance details
    """
    print(f"Provisioning {student_count} lab environments on {cloud_provider}...")
    
    if cloud_provider == "aws":
        return provision_aws_labs(student_count)
    elif cloud_provider == "azure":
        return provision_azure_labs(student_count)
    elif cloud_provider == "dgx":
        return provision_dgx_labs(student_count)
    else:
        raise ValueError(f"Unsupported cloud provider: {cloud_provider}")


def provision_aws_labs(student_count: int) -> List[Dict]:
    """Provision labs on AWS using Terraform."""
    # Initialize Terraform
    subprocess.run(["terraform", "init"], cwd="deployment/terraform", check=True)
    
    # Apply Terraform configuration
    subprocess.run([
        "terraform", "apply",
        "-auto-approve",
        f"-var=student_count={student_count}"
    ], cwd="deployment/terraform", check=True)
    
    # Get outputs
    result = subprocess.run(
        ["terraform", "output", "-json"],
        cwd="deployment/terraform",
        capture_output=True,
        text=True,
        check=True
    )
    
    outputs = json.loads(result.stdout)
    
    # Wait for instances to be ready
    print("Waiting for instances to be ready...")
    time.sleep(60)
    
    # Get instance details
    instances = get_aws_instances()
    
    print(f"Successfully provisioned {len(instances)} lab environments")
    return instances


def get_aws_instances() -> List[Dict]:
    """Get details of running AWS instances."""
    result = subprocess.run([
        "aws", "ec2", "describe-instances",
        "--filters", "Name=tag:Course,Values=NCP-AAI",
        "--query", "Reservations[*].Instances[*].[InstanceId,PublicIpAddress,State.Name]",
        "--output", "json"
    ], capture_output=True, text=True, check=True)
    
    instances_data = json.loads(result.stdout)
    instances = []
    
    for reservation in instances_data:
        for instance in reservation:
            if instance[2] == "running":
                instances.append({
                    "instance_id": instance[0],
                    "public_ip": instance[1],
                    "jupyter_url": f"http://{instance[1]}:8888",
                    "status": instance[2]
                })
    
    return instances


def teardown_lab_environments(cloud_provider: str = "aws") -> None:
    """
    Teardown all lab environments.
    
    Args:
        cloud_provider: Cloud provider to use
    """
    print(f"Tearing down lab environments on {cloud_provider}...")
    
    if cloud_provider == "aws":
        subprocess.run([
            "terraform", "destroy",
            "-auto-approve"
        ], cwd="deployment/terraform", check=True)
    
    print("Lab environments successfully torn down")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Provision lab environments")
    parser.add_argument("--count", type=int, default=100, help="Number of students")
    parser.add_argument("--provider", default="aws", choices=["aws", "azure", "dgx"])
    parser.add_argument("--action", default="provision", choices=["provision", "teardown"])
    
    args = parser.parse_args()
    
    if args.action == "provision":
        instances = provision_lab_environments(args.count, args.provider)
        print("\nProvisioned Instances:")
        for inst in instances:
            print(f"  - {inst['instance_id']}: {inst['jupyter_url']}")
    else:
        teardown_lab_environments(args.provider)
```

## NVIDIA Platform Access Configuration

### API Key Setup

```bash
# deployment/scripts/configure_nvidia_access.sh
#!/bin/bash

# Configure NVIDIA NIM access
export NVIDIA_API_KEY="your-nvidia-api-key"
export NVIDIA_NIM_ENDPOINT="https://api.nvidia.com/nim/v1"

# Configure NeMo access
export NEMO_API_KEY="your-nemo-api-key"
export NEMO_ENDPOINT="https://api.nvidia.com/nemo/v1"

# Configure TensorRT-LLM
export TENSORRT_LLM_PATH="/usr/local/tensorrt_llm"

# Configure Triton
export TRITON_SERVER_URL="http://localhost:8000"

# Save to environment file
cat > /workspace/.env << EOF
NVIDIA_API_KEY=${NVIDIA_API_KEY}
NVIDIA_NIM_ENDPOINT=${NVIDIA_NIM_ENDPOINT}
NEMO_API_KEY=${NEMO_API_KEY}
NEMO_ENDPOINT=${NEMO_ENDPOINT}
TENSORRT_LLM_PATH=${TENSORRT_LLM_PATH}
TRITON_SERVER_URL=${TRITON_SERVER_URL}
EOF

echo "NVIDIA platform access configured successfully"
```

## Monitoring and Management

### Health Check Script

```python
# deployment/scripts/health_check.py
"""
Health check script for lab environments.
"""

import requests
import subprocess
from typing import List, Dict


def check_lab_health(instances: List[Dict]) -> Dict:
    """
    Check health of all lab instances.
    
    Args:
        instances: List of instance details
        
    Returns:
        Health status report
    """
    report = {
        "total": len(instances),
        "healthy": 0,
        "unhealthy": 0,
        "details": []
    }
    
    for instance in instances:
        status = check_instance_health(instance)
        report["details"].append(status)
        
        if status["healthy"]:
            report["healthy"] += 1
        else:
            report["unhealthy"] += 1
    
    return report


def check_instance_health(instance: Dict) -> Dict:
    """Check health of a single instance."""
    status = {
        "instance_id": instance["instance_id"],
        "public_ip": instance["public_ip"],
        "healthy": True,
        "checks": {}
    }
    
    # Check if instance is reachable
    try:
        response = requests.get(
            f"http://{instance['public_ip']}:8888",
            timeout=5
        )
        status["checks"]["jupyter"] = response.status_code == 200
    except:
        status["checks"]["jupyter"] = False
        status["healthy"] = False
    
    # Check GPU availability
    try:
        result = subprocess.run([
            "ssh", f"ubuntu@{instance['public_ip']}",
            "nvidia-smi"
        ], capture_output=True, timeout=10)
        status["checks"]["gpu"] = result.returncode == 0
    except:
        status["checks"]["gpu"] = False
        status["healthy"] = False
    
    return status


if __name__ == "__main__":
    # Load instances from Terraform output
    import json
    instances = get_aws_instances()  # From provision_labs.py
    
    report = check_lab_health(instances)
    print(json.dumps(report, indent=2))
```

## Cost Management

### Cost Estimation

```python
# deployment/scripts/cost_estimator.py
"""
Estimate costs for lab environment.
"""

def estimate_lab_costs(
    student_count: int,
    hours_per_student: int = 40,
    instance_type: str = "g5.xlarge"
) -> Dict:
    """
    Estimate total costs for lab environment.
    
    Args:
        student_count: Number of students
        hours_per_student: Expected hours per student
        instance_type: AWS instance type
        
    Returns:
        Cost breakdown
    """
    # AWS pricing (as of 2026)
    instance_costs = {
        "g5.xlarge": 1.006,      # per hour
        "g5.2xlarge": 1.212,
        "p3.8xlarge": 12.24,
        "p4d.24xlarge": 32.77
    }
    
    hourly_rate = instance_costs.get(instance_type, 1.0)
    
    # Calculate costs
    compute_cost = student_count * hours_per_student * hourly_rate
    storage_cost = student_count * 500 * 0.10  # 500GB at $0.10/GB/month
    network_cost = student_count * 100 * 0.09  # 100GB transfer at $0.09/GB
    
    total_cost = compute_cost + storage_cost + network_cost
    
    return {
        "student_count": student_count,
        "hours_per_student": hours_per_student,
        "instance_type": instance_type,
        "hourly_rate": hourly_rate,
        "compute_cost": compute_cost,
        "storage_cost": storage_cost,
        "network_cost": network_cost,
        "total_cost": total_cost,
        "cost_per_student": total_cost / student_count
    }


if __name__ == "__main__":
    costs = estimate_lab_costs(100, 40, "g5.xlarge")
    print(f"Total estimated cost: ${costs['total_cost']:,.2f}")
    print(f"Cost per student: ${costs['cost_per_student']:,.2f}")
```

## Troubleshooting

### Common Issues

**Issue: Container fails to start**
- Check Docker logs: `docker logs ncp-aai-lab`
- Verify GPU access: `nvidia-smi`
- Check resource limits: `docker stats`

**Issue: Jupyter not accessible**
- Verify port forwarding: `netstat -tulpn | grep 8888`
- Check security group rules
- Verify container is running: `docker ps`

**Issue: NVIDIA API authentication fails**
- Verify API keys are set correctly
- Check network connectivity to NVIDIA services
- Verify API key permissions

## Support

For lab environment support:
- Technical issues: ncp-aai-lab-support@nvidia.com
- Infrastructure questions: cloud-support@nvidia.com
- Emergency hotline: +1-800-NVIDIA-HELP

---

**Document Version:** 1.0  
**Last Updated:** January 2026
