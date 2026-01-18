# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this project, please report it by emailing the maintainers. Please do not create public GitHub issues for security vulnerabilities.

## Security Best Practices

### 1. API Keys and Credentials

**Never commit API keys, passwords, or credentials to the repository.**

- Use environment variables for all sensitive configuration
- Copy `.env.example` to `.env` and fill in your credentials
- The `.env` file is gitignored and will not be committed
- Use secrets management services in production (AWS Secrets Manager, Azure Key Vault, etc.)

### 2. NVIDIA Platform Access

To use NVIDIA NIM and other NVIDIA services:

1. Obtain API keys from [build.nvidia.com](https://build.nvidia.com)
2. Set environment variables:
   ```bash
   export NVIDIA_API_KEY="your-key-here"
   export NEMO_API_KEY="your-nemo-key-here"
   ```
3. Never hardcode these keys in source code

### 3. Lab Environment Security

When setting up lab environments:

- Use temporary credentials with minimal required permissions
- Rotate credentials regularly
- Implement network isolation for lab instances
- Enable audit logging for all API calls
- Use HTTPS/TLS for all communications

### 4. Code Security

- All lab solution code uses environment variables for credentials
- No hardcoded secrets in any Python files
- Input validation and sanitization in all agent implementations
- Rate limiting and circuit breakers for external API calls

### 5. Data Privacy

- Do not commit any personally identifiable information (PII)
- Use placeholder data in examples and tests
- Sanitize logs before sharing
- Follow GDPR, HIPAA, and other relevant regulations

### 6. Dependency Security

Keep dependencies up to date:

```bash
pip install --upgrade -r requirements.txt
pip-audit  # Check for known vulnerabilities
```

### 7. Production Deployment

For production deployments:

- Use container image scanning (Trivy, Clair)
- Implement network policies and firewalls
- Enable encryption at rest and in transit
- Use managed identity/service accounts instead of API keys
- Implement comprehensive monitoring and alerting
- Regular security audits and penetration testing

## Secure Configuration Examples

### Environment Variables (Recommended)

```python
import os

api_key = os.getenv("NVIDIA_API_KEY")
if not api_key:
    raise ValueError("NVIDIA_API_KEY environment variable not set")
```

### AWS Secrets Manager (Production)

```python
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

credentials = get_secret('nvidia-api-credentials')
api_key = credentials['NVIDIA_API_KEY']
```

### Docker Secrets (Kubernetes)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: nvidia-credentials
type: Opaque
stringData:
  nvidia-api-key: your-key-here
```

## Security Checklist Before Deployment

- [ ] All credentials stored in environment variables or secrets manager
- [ ] No hardcoded API keys in source code
- [ ] `.env` file is gitignored
- [ ] Dependencies are up to date and scanned for vulnerabilities
- [ ] Input validation implemented for all user inputs
- [ ] Rate limiting configured for API endpoints
- [ ] HTTPS/TLS enabled for all communications
- [ ] Logging configured (without sensitive data)
- [ ] Monitoring and alerting set up
- [ ] Backup and disaster recovery plan in place
- [ ] Security audit completed
- [ ] Compliance requirements verified (GDPR, HIPAA, etc.)

## Compliance

This course material is designed to help students understand security best practices for agentic AI systems, including:

- NVIDIA NeMo Guardrails implementation
- Bias detection and mitigation
- Privacy preservation techniques
- Regulatory compliance frameworks
- Audit trails and accountability

Refer to Module 10 (Safety, Ethics, and Guardrails) for detailed guidance.

## Contact

For security concerns, contact the course maintainers or your organization's security team.

---

**Last Updated**: January 2026
