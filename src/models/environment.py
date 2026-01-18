"""Lab environment data models."""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum
import time


class CloudProvider(Enum):
    """Supported cloud providers for lab environments."""
    NVIDIA_DGX_CLOUD = "nvidia_dgx_cloud"
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


class InstanceStatus(Enum):
    """Instance status states."""
    PROVISIONING = "provisioning"
    RUNNING = "running"
    STOPPED = "stopped"
    TERMINATED = "terminated"
    FAILED = "failed"


@dataclass
class ContainerConfig:
    """Configuration for Docker containers."""
    
    image_name: str
    image_tag: str = "latest"
    base_image: str = "nvidia/cuda:12.0-runtime-ubuntu22.04"
    python_version: str = "3.10"
    nvidia_drivers_version: str = "latest"
    pre_installed_packages: List[str] = field(default_factory=lambda: [
        "torch",
        "transformers",
        "langchain",
        "langgraph",
        "numpy",
        "pandas",
        "jupyter",
    ])
    environment_variables: Dict[str, str] = field(default_factory=dict)
    exposed_ports: List[int] = field(default_factory=lambda: [8888, 8000])
    working_directory: str = "/workspace"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "image_name": self.image_name,
            "image_tag": self.image_tag,
            "base_image": self.base_image,
            "python_version": self.python_version,
            "nvidia_drivers_version": self.nvidia_drivers_version,
            "pre_installed_packages": self.pre_installed_packages,
            "environment_variables": self.environment_variables,
            "exposed_ports": self.exposed_ports,
            "working_directory": self.working_directory,
        }
    
    def get_full_image_name(self) -> str:
        """Get the full Docker image name with tag."""
        return f"{self.image_name}:{self.image_tag}"
    
    def generate_dockerfile(self) -> str:
        """
        Generate a Dockerfile for this container configuration.
        
        Returns:
            String containing the Dockerfile content
        """
        dockerfile_lines = [
            f"FROM {self.base_image}",
            "",
            "# Install Python and system dependencies",
            f"RUN apt-get update && apt-get install -y \\",
            f"    python{self.python_version} \\",
            f"    python{self.python_version}-pip \\",
            "    git \\",
            "    curl \\",
            "    wget \\",
            "    vim \\",
            "    && rm -rf /var/lib/apt/lists/*",
            "",
            "# Set Python alias",
            f"RUN ln -s /usr/bin/python{self.python_version} /usr/bin/python",
            "",
            "# Upgrade pip",
            "RUN python -m pip install --upgrade pip",
            "",
            "# Install Python packages",
        ]
        
        if self.pre_installed_packages:
            dockerfile_lines.append("RUN pip install \\")
            for i, package in enumerate(self.pre_installed_packages):
                suffix = " \\" if i < len(self.pre_installed_packages) - 1 else ""
                dockerfile_lines.append(f"    {package}{suffix}")
            dockerfile_lines.append("")
        
        # Add environment variables
        if self.environment_variables:
            for key, value in self.environment_variables.items():
                dockerfile_lines.append(f"ENV {key}={value}")
            dockerfile_lines.append("")
        
        # Set working directory
        dockerfile_lines.append(f"WORKDIR {self.working_directory}")
        dockerfile_lines.append("")
        
        # Expose ports
        if self.exposed_ports:
            for port in self.exposed_ports:
                dockerfile_lines.append(f"EXPOSE {port}")
            dockerfile_lines.append("")
        
        # Default command
        dockerfile_lines.append('CMD ["bash"]')
        
        return "\n".join(dockerfile_lines)


@dataclass
class DatasetConfig:
    """Configuration for sample datasets."""
    
    name: str
    source_url: str
    size_mb: float
    description: str
    file_format: str
    destination_path: str = "/workspace/datasets"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "source_url": self.source_url,
            "size_mb": self.size_mb,
            "description": self.description,
            "file_format": self.file_format,
            "destination_path": self.destination_path,
        }


@dataclass
class ModelConfig:
    """Configuration for pre-trained models."""
    
    name: str
    model_id: str
    source: str  # "huggingface", "nvidia_ngc", "local"
    size_gb: float
    description: str
    destination_path: str = "/workspace/models"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "model_id": self.model_id,
            "source": self.source,
            "size_gb": self.size_gb,
            "description": self.description,
            "destination_path": self.destination_path,
        }


@dataclass
class Instance:
    """Represents a lab environment instance."""
    
    instance_id: str
    student_id: str
    gpu_type: str
    container_image: str
    status: str  # "provisioning", "running", "stopped", "terminated", "failed"
    created_at: datetime
    nvidia_api_configured: bool = False
    datasets_loaded: bool = False
    provider: str = "nvidia_dgx_cloud"
    resource_quota: Optional[Dict[str, any]] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "instance_id": self.instance_id,
            "student_id": self.student_id,
            "gpu_type": self.gpu_type,
            "container_image": self.container_image,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "nvidia_api_configured": self.nvidia_api_configured,
            "datasets_loaded": self.datasets_loaded,
            "provider": self.provider,
            "resource_quota": self.resource_quota,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Instance":
        """Create from dictionary."""
        data_copy = data.copy()
        if "created_at" in data_copy and isinstance(data_copy["created_at"], str):
            data_copy["created_at"] = datetime.fromisoformat(data_copy["created_at"])
        return cls(**data_copy)


@dataclass
class ProvisioningConfig:
    """Configuration for instance provisioning."""
    
    max_retries: int = 3
    retry_delay_seconds: int = 5
    timeout_seconds: int = 300
    enable_auto_cleanup: bool = True
    resource_quota: Optional[Dict[str, any]] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "max_retries": self.max_retries,
            "retry_delay_seconds": self.retry_delay_seconds,
            "timeout_seconds": self.timeout_seconds,
            "enable_auto_cleanup": self.enable_auto_cleanup,
            "resource_quota": self.resource_quota,
        }


@dataclass
class LabEnvironment:
    """Manages lab environment provisioning and configuration."""
    
    environment_id: str
    gpu_instance_type: str
    container_image: str
    nvidia_api_keys: Dict[str, str]
    sample_datasets: List[str]
    pre_trained_models: List[str]
    provider: CloudProvider = CloudProvider.NVIDIA_DGX_CLOUD
    provisioning_config: ProvisioningConfig = field(default_factory=ProvisioningConfig)
    fallback_providers: List[CloudProvider] = field(default_factory=list)
    container_config: Optional[ContainerConfig] = None
    dataset_configs: List[DatasetConfig] = field(default_factory=list)
    model_configs: List[ModelConfig] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "environment_id": self.environment_id,
            "gpu_instance_type": self.gpu_instance_type,
            "container_image": self.container_image,
            "nvidia_api_keys": self.nvidia_api_keys,
            "sample_datasets": self.sample_datasets,
            "pre_trained_models": self.pre_trained_models,
            "provider": self.provider.value if isinstance(self.provider, CloudProvider) else self.provider,
            "provisioning_config": self.provisioning_config.to_dict(),
            "fallback_providers": [p.value if isinstance(p, CloudProvider) else p for p in self.fallback_providers],
            "container_config": self.container_config.to_dict() if self.container_config else None,
            "dataset_configs": [d.to_dict() for d in self.dataset_configs],
            "model_configs": [m.to_dict() for m in self.model_configs],
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "LabEnvironment":
        """Create from dictionary."""
        data_copy = data.copy()
        
        # Convert provider string to enum
        if "provider" in data_copy and isinstance(data_copy["provider"], str):
            data_copy["provider"] = CloudProvider(data_copy["provider"])
        
        # Convert provisioning_config dict to object
        if "provisioning_config" in data_copy and isinstance(data_copy["provisioning_config"], dict):
            data_copy["provisioning_config"] = ProvisioningConfig(**data_copy["provisioning_config"])
        
        # Convert fallback_providers strings to enums
        if "fallback_providers" in data_copy:
            data_copy["fallback_providers"] = [
                CloudProvider(p) if isinstance(p, str) else p 
                for p in data_copy["fallback_providers"]
            ]
        
        # Convert container_config dict to object
        if "container_config" in data_copy and data_copy["container_config"]:
            data_copy["container_config"] = ContainerConfig(**data_copy["container_config"])
        
        # Convert dataset_configs dicts to objects
        if "dataset_configs" in data_copy:
            data_copy["dataset_configs"] = [
                DatasetConfig(**d) if isinstance(d, dict) else d 
                for d in data_copy["dataset_configs"]
            ]
        
        # Convert model_configs dicts to objects
        if "model_configs" in data_copy:
            data_copy["model_configs"] = [
                ModelConfig(**m) if isinstance(m, dict) else m 
                for m in data_copy["model_configs"]
            ]
        
        return cls(**data_copy)
    
    def get_container_image(self) -> str:
        """Get the container image for this environment."""
        return self.container_image
    
    def build_container_image(self) -> bool:
        """
        Build Docker container image for lab environment.
        
        In production, this would:
        - Generate Dockerfile from container_config
        - Build image using Docker API
        - Tag and push to container registry
        - Verify image integrity
        
        Returns:
            True if build successful, False otherwise
        """
        try:
            if not self.container_config:
                return False
            
            # Generate Dockerfile
            dockerfile_content = self.container_config.generate_dockerfile()
            
            # In production, would:
            # 1. Write Dockerfile to temporary location
            # 2. Run docker build command
            # 3. Tag the image
            # 4. Push to registry
            # 5. Clean up temporary files
            
            # For now, just validate we can generate the Dockerfile
            return len(dockerfile_content) > 0
            
        except Exception:
            return False
    
    def setup_nvidia_api_access(self, instance: Instance) -> bool:
        """
        Set up NVIDIA API access in container.
        
        In production, this would:
        - Mount API key files into container
        - Set environment variables
        - Configure API endpoints
        - Test connectivity
        
        Args:
            instance: Instance to configure
            
        Returns:
            True if setup successful, False otherwise
        """
        try:
            if not self.nvidia_api_keys:
                return False
            
            # Validate instance state
            if instance.status != InstanceStatus.RUNNING.value:
                return False
            
            # In production, would configure actual API access
            # For now, just mark as configured
            instance.nvidia_api_configured = True
            
            return True
            
        except Exception:
            return False
    
    def load_sample_datasets(self, instance: Instance) -> bool:
        """
        Load sample datasets into container.
        
        In production, this would:
        - Download datasets from configured sources
        - Verify checksums
        - Extract archives
        - Set permissions
        - Create dataset index
        
        Args:
            instance: Instance to load datasets into
            
        Returns:
            True if loading successful, False otherwise
        """
        try:
            if instance.status != InstanceStatus.RUNNING.value:
                return False
            
            # In production, would:
            # 1. Iterate through dataset_configs
            # 2. Download each dataset
            # 3. Verify integrity
            # 4. Extract to destination
            # 5. Update instance metadata
            
            instance.datasets_loaded = True
            return True
            
        except Exception:
            return False
    
    def load_pretrained_models(self, instance: Instance) -> bool:
        """
        Load pre-trained models into container.
        
        In production, this would:
        - Download models from HuggingFace, NGC, etc.
        - Verify model integrity
        - Cache models appropriately
        - Set up model serving if needed
        
        Args:
            instance: Instance to load models into
            
        Returns:
            True if loading successful, False otherwise
        """
        try:
            if instance.status != InstanceStatus.RUNNING.value:
                return False
            
            # In production, would:
            # 1. Iterate through model_configs
            # 2. Download from appropriate source
            # 3. Verify model files
            # 4. Set up model cache
            # 5. Update instance metadata
            
            return True
            
        except Exception:
            return False
    
    def configure_development_environment(self, instance: Instance) -> bool:
        """
        Configure development environment in container.
        
        Sets up:
        - Jupyter notebook server
        - VS Code server (if applicable)
        - Git configuration
        - Shell environment
        
        Args:
            instance: Instance to configure
            
        Returns:
            True if configuration successful, False otherwise
        """
        try:
            if instance.status != InstanceStatus.RUNNING.value:
                return False
            
            # In production, would:
            # 1. Start Jupyter server
            # 2. Configure authentication
            # 3. Set up Git
            # 4. Configure shell environment
            # 5. Create workspace directories
            
            return True
            
        except Exception:
            return False
    
    def _generate_instance_id(self, student_id: str) -> str:
        """Generate a unique instance ID."""
        import uuid
        # Use UUID to ensure uniqueness even for rapid successive calls
        unique_suffix = str(uuid.uuid4())[:8]
        timestamp = int(datetime.now().timestamp() * 1000)
        return f"inst-{student_id}-{timestamp}-{unique_suffix}"
    
    def provision_complete_environment(self, student_id: str) -> Instance:
        """
        Provision a complete lab environment with all components.
        
        This orchestrates the full provisioning workflow:
        1. Provision cloud instance
        2. Configure NVIDIA API access
        3. Load datasets
        4. Load pre-trained models
        5. Configure development environment
        
        Args:
            student_id: Unique identifier for the student
            
        Returns:
            Fully configured Instance
            
        Raises:
            RuntimeError: If any provisioning step fails
        """
        try:
            # Step 1: Provision instance with retry logic
            instance = self.provision_instance_with_retry(student_id)
            
            # Step 2: Configure NVIDIA API access
            if not self.setup_nvidia_api_access(instance):
                instance.status = InstanceStatus.FAILED.value
                raise RuntimeError("Failed to configure NVIDIA API access")
            
            # Step 3: Load datasets
            if not self.load_sample_datasets(instance):
                instance.status = InstanceStatus.FAILED.value
                raise RuntimeError("Failed to load sample datasets")
            
            # Step 4: Load pre-trained models
            if not self.load_pretrained_models(instance):
                instance.status = InstanceStatus.FAILED.value
                raise RuntimeError("Failed to load pre-trained models")
            
            # Step 5: Configure development environment
            if not self.configure_development_environment(instance):
                instance.status = InstanceStatus.FAILED.value
                raise RuntimeError("Failed to configure development environment")
            
            # Validate resource quota
            if not self.validate_resource_quota(instance):
                instance.status = InstanceStatus.FAILED.value
                raise RuntimeError("Instance exceeds resource quota")
            
            return instance
            
        except Exception as e:
            # Clean up on failure
            if 'instance' in locals():
                self.teardown_instance(instance)
            raise RuntimeError(f"Failed to provision complete environment: {str(e)}") from e
    
    def teardown_with_cleanup(self, instance: Instance, save_student_work: bool = True) -> bool:
        """
        Teardown instance with comprehensive cleanup.
        
        Performs:
        1. Save student work (if requested)
        2. Stop running processes
        3. Clean up temporary files
        4. Terminate cloud instance
        5. Update billing records
        6. Remove from active instances
        
        Args:
            instance: Instance to teardown
            save_student_work: Whether to save student work before teardown
            
        Returns:
            True if teardown successful, False otherwise
        """
        try:
            # Step 1: Save student work if requested
            if save_student_work:
                # In production, would backup student files
                pass
            
            # Step 2: Stop running processes
            # In production, would gracefully stop Jupyter, etc.
            pass
            
            # Step 3: Clean up temporary files
            # In production, would remove temp files
            pass
            
            # Step 4: Terminate instance
            success = self.teardown_instance(instance)
            
            # Step 5: Update billing records
            # In production, would finalize billing
            pass
            
            return success
            
        except Exception:
            return False
    
    def auto_cleanup_expired_instances(self, instances: List[Instance], max_age_hours: int = 24) -> int:
        """
        Automatically clean up expired instances.
        
        Args:
            instances: List of instances to check
            max_age_hours: Maximum age in hours before cleanup
            
        Returns:
            Number of instances cleaned up
        """
        if not self.provisioning_config.enable_auto_cleanup:
            return 0
        
        cleaned_count = 0
        current_time = datetime.now()
        
        for instance in instances:
            age_hours = (current_time - instance.created_at).total_seconds() / 3600
            
            if age_hours > max_age_hours:
                if self.teardown_with_cleanup(instance, save_student_work=True):
                    cleaned_count += 1
        
        return cleaned_count
    
    def get_instance_status(self, instance: Instance) -> Dict[str, any]:
        """
        Get detailed status information for an instance.
        
        Args:
            instance: Instance to check
            
        Returns:
            Dictionary with status information
        """
        age_seconds = (datetime.now() - instance.created_at).total_seconds()
        
        return {
            "instance_id": instance.instance_id,
            "student_id": instance.student_id,
            "status": instance.status,
            "age_seconds": age_seconds,
            "age_hours": age_seconds / 3600,
            "nvidia_api_configured": instance.nvidia_api_configured,
            "datasets_loaded": instance.datasets_loaded,
            "provider": instance.provider,
            "gpu_type": instance.gpu_type,
            "container_image": instance.container_image,
        }
        """Generate a unique instance ID."""
        timestamp = int(datetime.now().timestamp() * 1000)
        return f"inst-{student_id}-{timestamp}"
    
    def provision_instance(self, student_id: str) -> Instance:
        """
        Provision a new lab instance for a student.
        
        This is a simplified implementation. In production, this would:
        - Make API calls to the cloud provider
        - Handle authentication and authorization
        - Configure networking and security groups
        - Set up monitoring and logging
        
        Args:
            student_id: Unique identifier for the student
            
        Returns:
            Instance object representing the provisioned instance
        """
        instance = Instance(
            instance_id=self._generate_instance_id(student_id),
            student_id=student_id,
            gpu_type=self.gpu_instance_type,
            container_image=self.container_image,
            status=InstanceStatus.PROVISIONING.value,
            created_at=datetime.now(),
            provider=self.provider.value if isinstance(self.provider, CloudProvider) else self.provider,
            resource_quota=self.provisioning_config.resource_quota,
        )
        return instance
    
    def provision_instance_with_retry(self, student_id: str) -> Instance:
        """
        Provision instance with retry logic and fallback providers.
        
        Implements retry logic with exponential backoff and supports
        falling back to alternative cloud providers if primary fails.
        
        Args:
            student_id: Unique identifier for the student
            
        Returns:
            Instance object representing the provisioned instance
            
        Raises:
            RuntimeError: If provisioning fails after all retries and fallbacks
        """
        providers_to_try = [self.provider] + self.fallback_providers
        
        for provider in providers_to_try:
            original_provider = self.provider
            self.provider = provider
            
            for attempt in range(self.provisioning_config.max_retries):
                try:
                    instance = self.provision_instance(student_id)
                    
                    # Simulate provisioning process
                    # In production, this would poll the cloud provider API
                    time.sleep(0.1)  # Minimal delay for testing
                    
                    instance.status = InstanceStatus.RUNNING.value
                    return instance
                    
                except Exception as e:
                    if attempt < self.provisioning_config.max_retries - 1:
                        # Exponential backoff
                        delay = self.provisioning_config.retry_delay_seconds * (2 ** attempt)
                        time.sleep(min(delay, 60))  # Cap at 60 seconds
                    else:
                        # Last attempt with this provider failed
                        if provider == providers_to_try[-1]:
                            # No more providers to try
                            raise RuntimeError(
                                f"Failed to provision instance after {self.provisioning_config.max_retries} "
                                f"attempts across {len(providers_to_try)} providers"
                            ) from e
            
            # Restore original provider for next attempt
            self.provider = original_provider
        
        raise RuntimeError("Failed to provision instance - no providers available")
    
    def configure_nvidia_access(self, instance: Instance) -> bool:
        """
        Configure NVIDIA API access for an instance.
        
        In production, this would:
        - Install NVIDIA API credentials
        - Configure environment variables
        - Test API connectivity
        - Set up API rate limiting
        
        Args:
            instance: Instance to configure
            
        Returns:
            True if configuration successful, False otherwise
        """
        try:
            # Validate instance is in correct state
            if instance.status not in [InstanceStatus.RUNNING.value, InstanceStatus.PROVISIONING.value]:
                return False
            
            # Simulate API configuration
            # In production, this would make actual API calls
            instance.nvidia_api_configured = True
            return True
            
        except Exception:
            return False
    
    def load_datasets(self, instance: Instance) -> bool:
        """
        Load sample datasets into an instance.
        
        In production, this would:
        - Download datasets from storage
        - Verify checksums
        - Extract and organize files
        - Set appropriate permissions
        
        Args:
            instance: Instance to load datasets into
            
        Returns:
            True if loading successful, False otherwise
        """
        try:
            # Validate instance is in correct state
            if instance.status != InstanceStatus.RUNNING.value:
                return False
            
            # Simulate dataset loading
            # In production, this would transfer actual data
            instance.datasets_loaded = True
            return True
            
        except Exception:
            return False
    
    def teardown_instance(self, instance: Instance) -> bool:
        """
        Teardown a lab instance.
        
        In production, this would:
        - Save any student work
        - Clean up resources
        - Terminate cloud instance
        - Update billing records
        
        Args:
            instance: Instance to teardown
            
        Returns:
            True if teardown successful, False otherwise
        """
        try:
            instance.status = InstanceStatus.TERMINATED.value
            return True
        except Exception:
            return False
    
    def validate_resource_quota(self, instance: Instance) -> bool:
        """
        Validate that instance is within resource quota limits.
        
        Args:
            instance: Instance to validate
            
        Returns:
            True if within quota, False otherwise
        """
        if not self.provisioning_config.resource_quota:
            return True
        
        quota = self.provisioning_config.resource_quota
        
        # Check GPU quota
        if "max_gpus" in quota:
            # In production, would check actual GPU allocation
            pass
        
        # Check memory quota
        if "max_memory_gb" in quota:
            # In production, would check actual memory allocation
            pass
        
        # Check storage quota
        if "max_storage_gb" in quota:
            # In production, would check actual storage allocation
            pass
        
        return True
