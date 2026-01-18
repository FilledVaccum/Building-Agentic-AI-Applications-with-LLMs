# LMS Integration Guide for NCP-AAI Course

## Overview

This guide provides instructions for integrating the "Building Agentic AI Applications with LLMs" course into Learning Management Systems (LMS) that support SCORM 2004 and xAPI standards.

## Supported LMS Platforms

The course package is compatible with:
- Moodle 3.9+
- Canvas LMS
- Blackboard Learn
- D2L Brightspace
- Adobe Captivate Prime
- Any SCORM 2004 4th Edition compliant LMS

## Package Contents

The SCORM package includes:
- `imsmanifest.xml` - SCORM 2004 manifest file
- `xapi_statements.json` - xAPI statement templates
- `modules/` - Module content and HTML wrappers
- Module-specific resources (JSON content files)

## Installation Steps

### 1. Upload SCORM Package

**Moodle:**
1. Navigate to your course
2. Turn editing on
3. Add an activity → SCORM package
4. Upload the `.zip` file
5. Configure settings (see Configuration section)

**Canvas:**
1. Go to Settings → Import Course Content
2. Select "SCORM Package" as content type
3. Upload the `.zip` file
4. Complete import process

**Blackboard:**
1. Navigate to Content area
2. Build Content → SCORM Package
3. Browse and upload `.zip` file
4. Submit

### 2. Configure Course Settings

Recommended settings for optimal experience:

**Completion Tracking:**
- Enable completion tracking
- Require: View all modules
- Require: Complete all assessments with 70%+ score
- Require: Complete all hands-on labs

**Grading:**
- Grading method: Highest attempt
- Maximum grade: 100
- Passing grade: 80% (for certification readiness)

**Attempts:**
- Number of attempts: Unlimited for practice exams
- Number of attempts: 3 for module quizzes
- Force new attempt: Yes

**Display:**
- Display package: New window
- Width: 100%
- Height: 600px
- Display course structure: Yes

### 3. Configure xAPI Integration

If your LMS supports xAPI (Experience API):

**Learning Record Store (LRS) Setup:**
1. Configure LRS endpoint in LMS settings
2. Set authentication credentials
3. Enable xAPI statement tracking

**Statement Configuration:**
The package includes templates for:
- Module completion statements
- Assessment attempt statements
- Lab completion statements
- Certification readiness statements

**Endpoint Configuration:**
```
LRS Endpoint: https://your-lrs-endpoint.com/xapi/
Auth Type: Basic Auth
Username: [Your LRS Username]
Password: [Your LRS Password]
```

## Data Tracking and Analytics

### SCORM Data Elements

The course tracks the following SCORM data elements:

**Core Elements:**
- `cmi.completion_status` - Module completion status
- `cmi.success_status` - Assessment pass/fail status
- `cmi.score.scaled` - Normalized score (0-1)
- `cmi.score.raw` - Raw score
- `cmi.score.min` - Minimum possible score
- `cmi.score.max` - Maximum possible score
- `cmi.session_time` - Time spent in session
- `cmi.location` - Current location in course

**Custom Elements:**
- `cmi.suspend_data` - Progress and state data
- `cmi.learner_preference` - Student preferences

### xAPI Statements

The course generates xAPI statements for:

**Module Completion:**
```json
{
  "actor": {"name": "Student Name", "mbox": "mailto:student@example.com"},
  "verb": {"id": "http://adlnet.gov/expapi/verbs/completed"},
  "object": {"id": "https://nvidia.com/ncp-aai/module/1"},
  "result": {"completion": true, "duration": "PT90M"}
}
```

**Assessment Attempt:**
```json
{
  "actor": {"name": "Student Name", "mbox": "mailto:student@example.com"},
  "verb": {"id": "http://adlnet.gov/expapi/verbs/attempted"},
  "object": {"id": "https://nvidia.com/ncp-aai/assessment/quiz_01"},
  "result": {
    "score": {"scaled": 0.85, "raw": 85, "max": 100},
    "success": true,
    "completion": true
  }
}
```

## Prerequisites and System Requirements

### Student Requirements:
- Modern web browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- JavaScript enabled
- Cookies enabled
- Minimum screen resolution: 1280x720
- Stable internet connection (minimum 5 Mbps)

### LMS Requirements:
- SCORM 2004 4th Edition support
- xAPI 1.0.3+ support (optional but recommended)
- HTML5 support
- JavaScript execution enabled

### External Dependencies:
- NVIDIA platform access (NIM, NeMo, etc.)
- Cloud GPU instances for labs (NVIDIA DGX Cloud or equivalent)
- Docker environment for containerized labs

## Lab Environment Integration

The course requires external lab environments that cannot be packaged in SCORM:

### Integration Options:

**Option 1: LTI Integration**
- Use LTI (Learning Tools Interoperability) to launch lab environments
- Configure LTI consumer keys in LMS
- Map lab activities to LTI resources

**Option 2: External Links**
- Provide direct links to lab environment portal
- Use SSO for seamless authentication
- Track completion via xAPI statements

**Option 3: Embedded iFrames**
- Embed lab interfaces within LMS
- Requires CORS configuration
- May have limitations based on LMS security policies

### Lab Environment Setup:
See `deployment/LAB_ENVIRONMENT_SETUP.md` for detailed instructions on:
- Provisioning cloud GPU instances
- Configuring Docker containers
- Setting up NVIDIA API access
- Managing student environments

## Troubleshooting

### Common Issues:

**Issue: SCORM package fails to upload**
- Solution: Ensure package is valid SCORM 2004 format
- Solution: Check file size limits in LMS (increase if needed)
- Solution: Verify zip file is not corrupted

**Issue: Content not displaying**
- Solution: Check browser console for JavaScript errors
- Solution: Verify SCORM API is properly initialized
- Solution: Ensure pop-up blockers are disabled

**Issue: Progress not saving**
- Solution: Verify SCORM communication is working
- Solution: Check LMS SCORM player settings
- Solution: Ensure cookies are enabled

**Issue: xAPI statements not recording**
- Solution: Verify LRS endpoint configuration
- Solution: Check authentication credentials
- Solution: Ensure LRS is accessible from LMS

### Support Resources:
- LMS-specific documentation
- SCORM 2004 specification: https://adlnet.gov/projects/scorm/
- xAPI specification: https://github.com/adlnet/xAPI-Spec
- Course support: ncp-aai-support@nvidia.com

## Customization Options

### Branding:
- Modify HTML templates in module directories
- Update CSS styles for institutional branding
- Add institutional logos and colors

### Content Adaptation:
- Adjust module sequencing in manifest
- Modify prerequisite rules
- Customize assessment scoring rules

### Integration Extensions:
- Add custom xAPI statements
- Integrate with institutional analytics platforms
- Connect to student information systems (SIS)

## Compliance and Accessibility

### Standards Compliance:
- SCORM 2004 4th Edition
- xAPI 1.0.3
- WCAG 2.1 AA accessibility standards
- Section 508 compliance

### Accessibility Features:
- Screen reader compatible
- Keyboard navigation support
- Closed captions for video content
- Alternative text for images
- Adjustable font sizes and contrast

## Updates and Maintenance

### Version Control:
- Package version is included in manifest metadata
- Check for updates quarterly
- Subscribe to update notifications

### Content Updates:
- Re-upload updated SCORM package
- Preserve student progress data
- Communicate changes to enrolled students

### Data Migration:
- Export student data before major updates
- Test new package in staging environment
- Provide rollback plan if needed

## Security Considerations

### Data Privacy:
- Student data is stored according to LMS privacy policies
- xAPI statements may contain PII - ensure LRS compliance
- Follow institutional data retention policies

### Access Control:
- Configure appropriate role permissions
- Restrict access to instructor materials
- Implement SSO for enhanced security

### API Security:
- Secure NVIDIA API keys
- Use environment variables for sensitive data
- Implement rate limiting for API calls

## Performance Optimization

### Caching:
- Enable browser caching for static resources
- Configure CDN for media files
- Optimize image and video sizes

### Load Balancing:
- Distribute lab environment load across regions
- Implement auto-scaling for peak usage
- Monitor resource utilization

## Support and Contact

For technical support with LMS integration:
- Email: ncp-aai-support@nvidia.com
- Documentation: https://docs.nvidia.com/ncp-aai
- Community Forum: https://forums.nvidia.com/ncp-aai

For NVIDIA platform access and lab environment support:
- NVIDIA Developer Portal: https://developer.nvidia.com
- DGX Cloud Support: https://www.nvidia.com/en-us/data-center/dgx-cloud/

---

**Document Version:** 1.0  
**Last Updated:** January 2026  
**Compatible with:** SCORM 2004 4th Edition, xAPI 1.0.3+
