"""JSON schema validation for data models."""

import json
from pathlib import Path
from typing import Dict, Any
import jsonschema
from jsonschema import validate, ValidationError


class SchemaValidator:
    """Validates data models against JSON schemas."""
    
    def __init__(self):
        """Initialize validator with schemas."""
        self.schemas: Dict[str, dict] = {}
        self._load_schemas()
    
    def _load_schemas(self) -> None:
        """Load all JSON schemas from the schemas directory."""
        schema_dir = Path(__file__).parent / "schemas"
        
        schema_files = {
            "module": "module_schema.json",
            "assessment": "assessment_schema.json",
            "lab": "lab_schema.json",
        }
        
        for name, filename in schema_files.items():
            schema_path = schema_dir / filename
            if schema_path.exists():
                with open(schema_path, 'r') as f:
                    self.schemas[name] = json.load(f)
    
    def validate_module(self, data: dict) -> bool:
        """Validate module data against schema."""
        try:
            validate(instance=data, schema=self.schemas["module"])
            return True
        except ValidationError as e:
            raise ValueError(f"Module validation failed: {e.message}")
    
    def validate_assessment(self, data: dict) -> bool:
        """Validate assessment data against schema."""
        try:
            validate(instance=data, schema=self.schemas["assessment"])
            return True
        except ValidationError as e:
            raise ValueError(f"Assessment validation failed: {e.message}")
    
    def validate_lab(self, data: dict) -> bool:
        """Validate lab data against schema."""
        try:
            validate(instance=data, schema=self.schemas["lab"])
            return True
        except ValidationError as e:
            raise ValueError(f"Lab validation failed: {e.message}")


# Global validator instance
validator = SchemaValidator()
