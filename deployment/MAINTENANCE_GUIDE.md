# Maintenance Guide: NCP-AAI Course

## Overview

This guide provides procedures for ongoing maintenance, updates, and operational management of the NCP-AAI course deployment.

## Table of Contents

1. [Daily Maintenance](#daily-maintenance)
2. [Weekly Maintenance](#weekly-maintenance)
3. [Monthly Maintenance](#monthly-maintenance)
4. [Quarterly Maintenance](#quarterly-maintenance)
5. [Update Procedures](#update-procedures)
6. [Backup and Recovery](#backup-and-recovery)
7. [Monitoring and Alerts](#monitoring-and-alerts)

## Daily Maintenance

### Health Checks

Run daily health checks to ensure all systems are operational:

```bash
#!/bin/bash
# deployment/scripts/daily_health_check.sh

echo "=== Daily Health Check: $(date) ==="

# Check lab instances
echo "Checking lab instances..."
python deployment/provision_labs.py --action status

# Check Docker containers
echo "Checking Docker containers..."
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Check GPU availability
echo "Checking GPU availability..."
nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total --format=csv

# Check disk space
echo "Checking disk space..."
df -h | grep -E '^/dev/'

# Check API connectivity
echo "Checking NVIDIA API..."
curl -s -o /dev/null -w "%{http_code}" https://api.nvidia.com/nim/v1/models

# Check LMS connectivity
echo "Checking LMS..."
curl -s -o /dev/null -w "%{http_code}" https://your-lms.example.com

echo "=== Health Check Complete ==="
```

Schedule daily execution:

```bash
# Add to crontab
crontab -e
# Add line:
0 6 * * * /path/to/deployment/scripts/daily_health_check.sh >> /var/log/ncp-aai/health_check.log 2>&1
```

### Log Review

Review system logs daily:

```bash
# Check application logs
tail -n 100 /var/log/ncp-aai/application.log

# Check error logs
grep -i error /var/log/ncp-aai/*.log

# Check Docker logs
docker logs --tail 100 ncp-aai-lab

# Check system logs
journalctl -u docker --since today
```

### Student Support

Monitor and respond to student issues:

```bash
# Check support tickets
# Review LMS help desk or support system

# Monitor forum activity
# Check community forum for questions

# Review lab access issues
# Check failed login attempts
grep "Failed" /var/log/auth.log
```

## Weekly Maintenance

### Performance Review

Analyze system performance weekly:

```bash
#!/bin/bash
# deployment/scripts/weekly_performance_review.sh

echo "=== Weekly Performance Review: $(date) ==="

# GPU utilization statistics
echo "GPU Utilization (past week):"
# Query Prometheus or monitoring system

# API usage statistics
echo "API Usage:"
# Query NVIDIA API usage metrics

# Student activity
echo "Student Activity:"
# Query LMS database for active users

# Lab instance usage
echo "Lab Instance Usage:"
aws ec2 describe-instances \
  --filters "Name=tag:Course,Values=NCP-AAI" \
  --query 'Reservations[*].Instances[*].[InstanceId,State.Name,LaunchTime]' \
  --output table

echo "=== Performance Review Complete ==="
```

### Backup Verification

Verify backups are running successfully:

```bash
# Check backup status
ls -lh /backups/ncp-aai/

# Verify backup integrity
tar -tzf /backups/ncp-aai/content_latest.tar.gz > /dev/null
echo "Backup integrity: $?"

# Test restore procedure (in staging)
tar -xzf /backups/ncp-aai/content_latest.tar.gz -C /tmp/restore_test/
```

### Security Updates

Apply security updates weekly:

```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Update Docker images
docker pull nvidia/cuda:12.2.0-cudnn8-devel-ubuntu22.04
docker pull ncp-aai-lab:latest

# Update Python packages
pip list --outdated
pip install --upgrade pip setuptools wheel

# Scan for vulnerabilities
docker scan ncp-aai-lab:latest
```

### Certificate Management

Check SSL certificate expiration:

```bash
# Check certificate expiration
openssl x509 -in /etc/ssl/certs/lab.crt -noout -dates

# Renew if expiring within 30 days
# For Let's Encrypt:
sudo certbot renew

# For custom certificates:
# Generate new certificate and update configuration
```

## Monthly Maintenance

### Capacity Planning

Review resource usage and plan for capacity:

```bash
#!/bin/bash
# deployment/scripts/monthly_capacity_review.sh

echo "=== Monthly Capacity Review: $(date) ==="

# Student enrollment trends
echo "Current enrollment: $(wc -l < students.csv)"
echo "Active students: $(grep -c "active" students.csv)"

# Resource utilization
echo "Average GPU utilization: "
# Query monitoring system

echo "Average instance uptime: "
# Calculate from CloudWatch or monitoring

# Cost analysis
echo "Monthly costs:"
python deployment/provision_labs.py --action estimate --count 100

# Forecast next month
echo "Projected enrollment: "
# Based on registration trends

echo "=== Capacity Review Complete ==="
```

### Content Updates

Review and update course content:

```bash
# Check for NVIDIA platform updates
# Visit https://developer.nvidia.com/blog

# Update code examples
# Test with latest API versions

# Update documentation
# Reflect any platform changes

# Regenerate SCORM package
python -c "
from deployment.scorm_packager import SCORMPackager
import json
with open('integrated_course.json', 'r') as f:
    course_data = json.load(f)
packager = SCORMPackager(course_data)
packager.create_package('ncp_aai_course_updated')
"
```

### Database Maintenance

Optimize database performance:

```sql
-- For PostgreSQL (LMS database)
VACUUM ANALYZE;

-- Reindex tables
REINDEX DATABASE lms_database;

-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;

-- Archive old data
-- Move completed course data to archive tables
```

### User Account Cleanup

Clean up inactive accounts:

```bash
# Identify inactive students
# Query LMS for users with no activity in 90 days

# Archive completed student data
# Export to archive storage

# Remove test accounts
# Clean up development/testing accounts

# Update user roles
# Ensure proper permissions
```

## Quarterly Maintenance

### Comprehensive System Audit

Perform thorough system audit:

```bash
#!/bin/bash
# deployment/scripts/quarterly_audit.sh

echo "=== Quarterly System Audit: $(date) ==="

# Security audit
echo "Running security audit..."
# Check for unauthorized access
# Review firewall rules
# Audit API key usage

# Performance audit
echo "Running performance audit..."
# Analyze response times
# Review resource utilization
# Identify bottlenecks

# Cost audit
echo "Running cost audit..."
# Review cloud spending
# Identify optimization opportunities
# Compare against budget

# Compliance audit
echo "Running compliance audit..."
# Verify data retention policies
# Check privacy compliance
# Review access logs

echo "=== Audit Complete ==="
```

### Disaster Recovery Testing

Test disaster recovery procedures:

```bash
# 1. Simulate failure
# Stop critical services

# 2. Execute recovery plan
# Restore from backups
# Recreate infrastructure

# 3. Verify recovery
# Test all functionality
# Verify data integrity

# 4. Document results
# Update recovery procedures
# Identify improvements
```

### Platform Upgrades

Plan and execute major upgrades:

```bash
# 1. Review release notes
# Check NVIDIA platform updates
# Review LMS updates
# Check dependency updates

# 2. Test in staging
# Deploy to staging environment
# Run comprehensive tests
# Verify compatibility

# 3. Schedule maintenance window
# Notify users
# Plan rollback procedure

# 4. Execute upgrade
# Follow upgrade procedures
# Monitor for issues
# Verify functionality

# 5. Post-upgrade validation
# Run test suite
# Check monitoring
# Gather user feedback
```

### Training and Documentation

Update training materials and documentation:

```bash
# Review instructor materials
# Update for platform changes
# Add new best practices

# Update student guides
# Reflect UI changes
# Add troubleshooting tips

# Update API documentation
# Document new endpoints
# Update code examples

# Conduct instructor training
# Schedule training sessions
# Cover new features
# Share best practices
```

## Update Procedures

### Course Content Updates

```bash
#!/bin/bash
# deployment/scripts/update_content.sh

echo "Updating course content..."

# 1. Pull latest changes
git pull origin main

# 2. Update dependencies
pip install -r requirements.txt --upgrade

# 3. Validate content
python src/content_validation.py

# 4. Run tests
pytest tests/ -v

# 5. Regenerate SCORM package
python -c "
from deployment.scorm_packager import SCORMPackager
import json
with open('integrated_course.json', 'r') as f:
    course_data = json.load(f)
packager = SCORMPackager(course_data)
packager.create_package('ncp_aai_course_v1_1')
"

# 6. Upload to LMS
# Manual step: Upload new SCORM package

echo "Content update complete"
```

### Lab Environment Updates

```bash
#!/bin/bash
# deployment/scripts/update_lab_environment.sh

echo "Updating lab environment..."

# 1. Build new Docker image
cd deployment/docker
docker build -t ncp-aai-lab:latest .

# 2. Tag with version
docker tag ncp-aai-lab:latest ncp-aai-lab:v1.1

# 3. Push to registry
docker push ncp-aai-lab:latest
docker push ncp-aai-lab:v1.1

# 4. Update running instances
# Rolling update to minimize disruption
for instance in $(aws ec2 describe-instances --filters "Name=tag:Course,Values=NCP-AAI" --query 'Reservations[*].Instances[*].InstanceId' --output text); do
    echo "Updating instance: $instance"
    aws ec2 send-command \
        --instance-ids $instance \
        --document-name "AWS-RunShellScript" \
        --parameters 'commands=["docker pull ncp-aai-lab:latest","docker restart ncp-aai-lab"]'
    sleep 60  # Wait between updates
done

echo "Lab environment update complete"
```

### NVIDIA Platform Updates

```bash
# Monitor NVIDIA platform changes
# Subscribe to: https://developer.nvidia.com/blog

# Test new API versions
# Update API endpoints
# Test compatibility

# Update code examples
# Reflect API changes
# Add new features

# Update documentation
# Document breaking changes
# Provide migration guide
```

## Backup and Recovery

### Backup Schedule

```bash
# Daily backups
0 2 * * * /path/to/deployment/scripts/backup.sh daily

# Weekly backups
0 3 * * 0 /path/to/deployment/scripts/backup.sh weekly

# Monthly backups
0 4 1 * * /path/to/deployment/scripts/backup.sh monthly
```

### Backup Script

```bash
#!/bin/bash
# deployment/scripts/backup.sh

BACKUP_TYPE=$1
BACKUP_DIR="/backups/ncp-aai"
DATE=$(date +%Y%m%d_%H%M%S)

echo "Starting $BACKUP_TYPE backup: $DATE"

# Backup course content
tar -czf ${BACKUP_DIR}/content_${BACKUP_TYPE}_${DATE}.tar.gz content/

# Backup configuration
tar -czf ${BACKUP_DIR}/config_${BACKUP_TYPE}_${DATE}.tar.gz config/ deployment/

# Backup student data (from LMS)
# Export from LMS database

# Upload to S3
aws s3 sync ${BACKUP_DIR}/ s3://ncp-aai-backups/${BACKUP_TYPE}/

# Clean old backups
find ${BACKUP_DIR} -name "*${BACKUP_TYPE}*" -mtime +30 -delete

echo "Backup complete: $DATE"
```

### Recovery Procedures

```bash
#!/bin/bash
# deployment/scripts/recover.sh

BACKUP_DATE=$1

echo "Starting recovery from backup: $BACKUP_DATE"

# 1. Download backup from S3
aws s3 cp s3://ncp-aai-backups/daily/content_daily_${BACKUP_DATE}.tar.gz /tmp/

# 2. Extract backup
tar -xzf /tmp/content_daily_${BACKUP_DATE}.tar.gz -C /tmp/restore/

# 3. Verify backup integrity
# Check file counts and sizes

# 4. Stop services
docker stop ncp-aai-lab

# 5. Restore files
cp -r /tmp/restore/content/* content/

# 6. Restart services
docker start ncp-aai-lab

# 7. Verify recovery
python src/content_validation.py

echo "Recovery complete"
```

## Monitoring and Alerts

### Configure Monitoring

```yaml
# deployment/monitoring/alerts.yml
groups:
  - name: daily_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(errors_total[5m]) > 0.05
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          
      - alert: LowDiskSpace
        expr: node_filesystem_avail_bytes / node_filesystem_size_bytes < 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Disk space below 10%"
```

### Alert Notifications

```bash
# Configure email notifications
cat > /etc/prometheus/alertmanager.yml << EOF
route:
  receiver: 'email'
  
receivers:
  - name: 'email'
    email_configs:
      - to: 'ncp-aai-ops@nvidia.com'
        from: 'alerts@nvidia.com'
        smarthost: 'smtp.gmail.com:587'
        auth_username: 'alerts@nvidia.com'
        auth_password: 'your-password'
EOF
```

## Maintenance Calendar

### Suggested Schedule

| Task | Frequency | Day/Time | Duration |
|------|-----------|----------|----------|
| Health checks | Daily | 6:00 AM | 15 min |
| Log review | Daily | 9:00 AM | 30 min |
| Performance review | Weekly | Monday 10:00 AM | 1 hour |
| Security updates | Weekly | Tuesday 2:00 AM | 2 hours |
| Capacity planning | Monthly | 1st Monday | 2 hours |
| Content updates | Monthly | 2nd Tuesday | 4 hours |
| System audit | Quarterly | 1st of quarter | 1 day |
| DR testing | Quarterly | 15th of quarter | 4 hours |

## Emergency Contacts

- **Technical Lead**: tech-lead@nvidia.com
- **Operations Team**: ops@nvidia.com
- **NVIDIA Support**: +1-800-NVIDIA-HELP
- **Cloud Provider Support**: See provider documentation
- **LMS Support**: See LMS documentation

## Maintenance Checklist

### Pre-Maintenance

- [ ] Review maintenance procedures
- [ ] Notify stakeholders
- [ ] Create backup
- [ ] Prepare rollback plan
- [ ] Schedule maintenance window

### During Maintenance

- [ ] Execute maintenance tasks
- [ ] Monitor for issues
- [ ] Document changes
- [ ] Test functionality
- [ ] Verify monitoring

### Post-Maintenance

- [ ] Verify all systems operational
- [ ] Review logs for errors
- [ ] Update documentation
- [ ] Notify stakeholders of completion
- [ ] Schedule follow-up review

---

**Document Version:** 1.0  
**Last Updated:** January 2026  
**Review Schedule:** Quarterly
