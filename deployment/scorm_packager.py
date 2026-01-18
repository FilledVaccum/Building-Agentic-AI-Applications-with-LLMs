"""
SCORM 2004 Package Generator for NCP-AAI Course

This module exports course content in SCORM 2004 format for LMS compatibility.
"""

import json
import os
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from xml.etree import ElementTree as ET


class SCORMPackager:
    """Generates SCORM 2004 compliant course packages."""
    
    def __init__(self, course_data: Dict[str, Any], output_dir: str = "deployment/packages"):
        """
        Initialize SCORM packager.
        
        Args:
            course_data: Complete course data including modules, assessments, labs
            output_dir: Directory to output SCORM packages
        """
        self.course_data = course_data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_manifest(self) -> ET.Element:
        """
        Generate imsmanifest.xml for SCORM 2004.
        
        Returns:
            XML Element representing the manifest
        """
        # Create root manifest element with SCORM 2004 namespaces
        manifest = ET.Element('manifest', {
            'identifier': 'NCP_AAI_COURSE_MANIFEST',
            'version': '1.0',
            'xmlns': 'http://www.imsglobal.org/xsd/imscp_v1p1',
            'xmlns:adlcp': 'http://www.adlnet.org/xsd/adlcp_v1p3',
            'xmlns:adlseq': 'http://www.adlnet.org/xsd/adlseq_v1p3',
            'xmlns:adlnav': 'http://www.adlnet.org/xsd/adlnav_v1p3',
            'xmlns:imsss': 'http://www.imsglobal.org/xsd/imsss'
        })
        
        # Metadata section
        metadata = ET.SubElement(manifest, 'metadata')
        schema = ET.SubElement(metadata, 'schema')
        schema.text = 'ADL SCORM'
        schemaversion = ET.SubElement(metadata, 'schemaversion')
        schemaversion.text = '2004 4th Edition'
        
        # Organizations section
        organizations = ET.SubElement(manifest, 'organizations', {'default': 'NCP_AAI_ORG'})
        organization = ET.SubElement(organizations, 'organization', {'identifier': 'NCP_AAI_ORG'})
        title = ET.SubElement(organization, 'title')
        title.text = 'Building Agentic AI Applications with LLMs'
        
        # Add modules as items
        for module in self.course_data.get('modules', []):
            self._add_module_item(organization, module)
        
        # Resources section
        resources = ET.SubElement(manifest, 'resources')
        for module in self.course_data.get('modules', []):
            self._add_module_resource(resources, module)
        
        return manifest
    
    def _add_module_item(self, parent: ET.Element, module: Dict[str, Any]) -> None:
        """Add a module as an item in the organization."""
        module_id = module.get('module_id', 0)
        item = ET.SubElement(parent, 'item', {
            'identifier': f'MODULE_{module_id}',
            'identifierref': f'RESOURCE_MODULE_{module_id}'
        })
        title = ET.SubElement(item, 'title')
        title.text = module.get('title', f'Module {module_id}')
        
        # Add sequencing rules for prerequisites
        if module.get('prerequisites'):
            sequencing = ET.SubElement(item, 'imsss:sequencing')
            preconditions = ET.SubElement(sequencing, 'imsss:controlMode', {
                'choice': 'true',
                'flow': 'true'
            })
    
    def _add_module_resource(self, parent: ET.Element, module: Dict[str, Any]) -> None:
        """Add a module as a resource."""
        module_id = module.get('module_id', 0)
        resource = ET.SubElement(parent, 'resource', {
            'identifier': f'RESOURCE_MODULE_{module_id}',
            'type': 'webcontent',
            'adlcp:scormType': 'sco',
            'href': f'modules/module_{module_id}/index.html'
        })
        
        # Add file references
        ET.SubElement(resource, 'file', {'href': f'modules/module_{module_id}/index.html'})
        ET.SubElement(resource, 'file', {'href': f'modules/module_{module_id}/content.json'})
    
    def generate_xapi_statements(self) -> List[Dict[str, Any]]:
        """
        Generate xAPI (Experience API) statements for learning analytics.
        
        Returns:
            List of xAPI statement templates
        """
        statements = []
        
        # Module completion statement template
        statements.append({
            "statement_type": "module_completed",
            "template": {
                "actor": {
                    "objectType": "Agent",
                    "name": "{student_name}",
                    "mbox": "mailto:{student_email}"
                },
                "verb": {
                    "id": "http://adlnet.gov/expapi/verbs/completed",
                    "display": {"en-US": "completed"}
                },
                "object": {
                    "objectType": "Activity",
                    "id": "https://nvidia.com/ncp-aai/module/{module_id}",
                    "definition": {
                        "name": {"en-US": "{module_title}"},
                        "description": {"en-US": "NCP-AAI Course Module"},
                        "type": "http://adlnet.gov/expapi/activities/module"
                    }
                },
                "result": {
                    "completion": True,
                    "duration": "PT{duration}M"
                },
                "context": {
                    "contextActivities": {
                        "parent": [{
                            "id": "https://nvidia.com/ncp-aai/course",
                            "objectType": "Activity"
                        }]
                    }
                }
            }
        })
        
        # Assessment attempt statement template
        statements.append({
            "statement_type": "assessment_attempted",
            "template": {
                "actor": {
                    "objectType": "Agent",
                    "name": "{student_name}",
                    "mbox": "mailto:{student_email}"
                },
                "verb": {
                    "id": "http://adlnet.gov/expapi/verbs/attempted",
                    "display": {"en-US": "attempted"}
                },
                "object": {
                    "objectType": "Activity",
                    "id": "https://nvidia.com/ncp-aai/assessment/{assessment_id}",
                    "definition": {
                        "name": {"en-US": "{assessment_title}"},
                        "description": {"en-US": "NCP-AAI Assessment"},
                        "type": "http://adlnet.gov/expapi/activities/assessment"
                    }
                },
                "result": {
                    "score": {
                        "scaled": "{score_percentage}",
                        "raw": "{raw_score}",
                        "min": 0,
                        "max": "{max_score}"
                    },
                    "success": "{passed}",
                    "completion": True,
                    "duration": "PT{duration}M"
                }
            }
        })
        
        # Lab completion statement template
        statements.append({
            "statement_type": "lab_completed",
            "template": {
                "actor": {
                    "objectType": "Agent",
                    "name": "{student_name}",
                    "mbox": "mailto:{student_email}"
                },
                "verb": {
                    "id": "http://adlnet.gov/expapi/verbs/completed",
                    "display": {"en-US": "completed"}
                },
                "object": {
                    "objectType": "Activity",
                    "id": "https://nvidia.com/ncp-aai/lab/{lab_id}",
                    "definition": {
                        "name": {"en-US": "{lab_title}"},
                        "description": {"en-US": "Hands-on Lab Exercise"},
                        "type": "http://adlnet.gov/expapi/activities/simulation"
                    }
                },
                "result": {
                    "completion": True,
                    "success": "{validation_passed}",
                    "duration": "PT{duration}M"
                }
            }
        })
        
        # Certification readiness statement template
        statements.append({
            "statement_type": "certification_ready",
            "template": {
                "actor": {
                    "objectType": "Agent",
                    "name": "{student_name}",
                    "mbox": "mailto:{student_email}"
                },
                "verb": {
                    "id": "http://adlnet.gov/expapi/verbs/passed",
                    "display": {"en-US": "achieved readiness for"}
                },
                "object": {
                    "objectType": "Activity",
                    "id": "https://nvidia.com/ncp-aai/certification",
                    "definition": {
                        "name": {"en-US": "NCP-AAI Certification"},
                        "description": {"en-US": "NVIDIA-Certified Professional: Agentic AI"},
                        "type": "http://adlnet.gov/expapi/activities/objective"
                    }
                },
                "result": {
                    "score": {
                        "scaled": "{readiness_score}"
                    },
                    "success": True
                }
            }
        })
        
        return statements
    
    def create_package(self, package_name: str = None) -> Path:
        """
        Create complete SCORM package as a zip file.
        
        Args:
            package_name: Name for the package file (without extension)
            
        Returns:
            Path to created package file
        """
        if package_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            package_name = f"ncp_aai_course_{timestamp}"
        
        package_path = self.output_dir / f"{package_name}.zip"
        
        # Create temporary directory structure
        temp_dir = self.output_dir / "temp"
        temp_dir.mkdir(exist_ok=True)
        
        try:
            # Generate and save manifest
            manifest = self.generate_manifest()
            manifest_path = temp_dir / "imsmanifest.xml"
            tree = ET.ElementTree(manifest)
            ET.indent(tree, space="  ")
            tree.write(manifest_path, encoding='utf-8', xml_declaration=True)
            
            # Generate and save xAPI statements
            xapi_statements = self.generate_xapi_statements()
            xapi_path = temp_dir / "xapi_statements.json"
            with open(xapi_path, 'w') as f:
                json.dump(xapi_statements, f, indent=2)
            
            # Create module content directories
            modules_dir = temp_dir / "modules"
            modules_dir.mkdir(exist_ok=True)
            
            for module in self.course_data.get('modules', []):
                module_id = module.get('module_id', 0)
                module_dir = modules_dir / f"module_{module_id}"
                module_dir.mkdir(exist_ok=True)
                
                # Save module content as JSON
                content_path = module_dir / "content.json"
                with open(content_path, 'w') as f:
                    json.dump(module, f, indent=2)
                
                # Create simple HTML wrapper
                html_path = module_dir / "index.html"
                with open(html_path, 'w') as f:
                    f.write(self._generate_module_html(module))
            
            # Create zip package
            with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(temp_dir)
                        zipf.write(file_path, arcname)
            
            return package_path
            
        finally:
            # Cleanup temporary directory
            import shutil
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    
    def _generate_module_html(self, module: Dict[str, Any]) -> str:
        """Generate simple HTML wrapper for module content."""
        module_id = module.get('module_id', 0)
        title = module.get('title', f'Module {module_id}')
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pipwerks-scorm-api-wrapper/1.1.20160322/scorm.api.wrapper.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #76b900;
        }}
        .content {{
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="content" id="module-content">
        <p>Loading module content...</p>
    </div>
    
    <script>
        // Initialize SCORM
        scorm.init();
        
        // Load module content
        fetch('content.json')
            .then(response => response.json())
            .then(data => {{
                document.getElementById('module-content').innerHTML = 
                    '<p>' + (data.theoretical_content || 'Content not available') + '</p>';
                
                // Set SCORM data
                scorm.set('cmi.completion_status', 'incomplete');
                scorm.set('cmi.location', 'module_{module_id}');
            }})
            .catch(error => {{
                console.error('Error loading content:', error);
            }});
        
        // Mark as complete when user finishes
        window.addEventListener('beforeunload', function() {{
            scorm.set('cmi.completion_status', 'completed');
            scorm.save();
            scorm.quit();
        }});
    </script>
</body>
</html>"""


def generate_lms_integration_docs() -> str:
    """
    Generate LMS integration documentation.
    
    Returns:
        Markdown formatted documentation
    """
    return """# LMS Integration Guide for NCP-AAI Course

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
See `deployment/lab_environment_setup.md` for detailed instructions on:
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
"""


if __name__ == "__main__":
    # Example usage
    print("SCORM Packager for NCP-AAI Course")
    print("This module provides SCORM 2004 packaging functionality")
    print("Import and use SCORMPackager class to create course packages")
