"""
Lab environment provisioning script for NCP-AAI Course.

This script automates the provisioning and teardown of lab environments
across different cloud providers.
"""

import subprocess
import json
import time
import argparse
from typing import List, Dict, Optional


class LabProvisioner:
    """Manages lab environment provisioning across cloud providers."""
    
    def __init__(self, cloud_provider: str = "aws"):
        """
        Initialize lab provisioner.
        
        Args:
            cloud_provider: Cloud provider to use (aws, azure, dgx)
        """
        self.cloud_provider = cloud_provider
        self.terraform_dir = "deployment/terraform"
    
    def provision(self, student_count: int) -> List[Dict]:
        """
        Provision lab environments for students.
        
        Args:
            student_count: Number of student environments to provision
            
        Returns:
            List of provisioned instance details
        """
        print(f"Provisioning {student_count} lab environments on {self.cloud_provider}...")
        
        if self.cloud_provider == "aws":
            return self._provision_aws(student_count)
        elif self.cloud_provider == "azure":
            return self._provision_azure(student_count)
        elif self.cloud_provider == "dgx":
            return self._provision_dgx(student_count)
        else:
            raise ValueError(f"Unsupported cloud provider: {self.cloud_provider}")
    
    def _provision_aws(self, student_count: int) -> List[Dict]:
        """Provision labs on AWS using Terraform."""
        try:
            # Initialize Terraform
            print("Initializing Terraform...")
            subprocess.run(
                ["terraform", "init"],
                cwd=self.terraform_dir,
                check=True,
                capture_output=True
            )
            
            # Apply Terraform configuration
            print("Applying Terraform configuration...")
            subprocess.run([
                "terraform", "apply",
                "-auto-approve",
                f"-var=student_count={student_count}"
            ], cwd=self.terraform_dir, check=True)
            
            # Wait for instances to be ready
            print("Waiting for instances to be ready...")
            time.sleep(60)
            
            # Get instance details
            instances = self._get_aws_instances()
            
            print(f"Successfully provisioned {len(instances)} lab environments")
            return instances
            
        except subprocess.CalledProcessError as e:
            print(f"Error provisioning labs: {e}")
            raise
    
    def _provision_azure(self, student_count: int) -> List[Dict]:
        """Provision labs on Azure."""
        print("Azure provisioning not yet implemented")
        return []
    
    def _provision_dgx(self, student_count: int) -> List[Dict]:
        """Provision labs on NVIDIA DGX Cloud."""
        print("DGX Cloud provisioning not yet implemented")
        return []
    
    def _get_aws_instances(self) -> List[Dict]:
        """Get details of running AWS instances."""
        try:
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
            
        except subprocess.CalledProcessError as e:
            print(f"Error getting AWS instances: {e}")
            return []
    
    def teardown(self) -> None:
        """Teardown all lab environments."""
        print(f"Tearing down lab environments on {self.cloud_provider}...")
        
        try:
            if self.cloud_provider == "aws":
                subprocess.run([
                    "terraform", "destroy",
                    "-auto-approve"
                ], cwd=self.terraform_dir, check=True)
            
            print("Lab environments successfully torn down")
            
        except subprocess.CalledProcessError as e:
            print(f"Error tearing down labs: {e}")
            raise
    
    def get_status(self) -> Dict:
        """Get status of all lab environments."""
        if self.cloud_provider == "aws":
            instances = self._get_aws_instances()
            return {
                "provider": self.cloud_provider,
                "total_instances": len(instances),
                "running_instances": len([i for i in instances if i["status"] == "running"]),
                "instances": instances
            }
        return {"provider": self.cloud_provider, "status": "unknown"}


def estimate_costs(
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
        "compute_cost": round(compute_cost, 2),
        "storage_cost": round(storage_cost, 2),
        "network_cost": round(network_cost, 2),
        "total_cost": round(total_cost, 2),
        "cost_per_student": round(total_cost / student_count, 2)
    }


def main():
    """Main entry point for lab provisioning script."""
    parser = argparse.ArgumentParser(
        description="Provision and manage NCP-AAI lab environments"
    )
    parser.add_argument(
        "--action",
        default="provision",
        choices=["provision", "teardown", "status", "estimate"],
        help="Action to perform"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="Number of students"
    )
    parser.add_argument(
        "--provider",
        default="aws",
        choices=["aws", "azure", "dgx"],
        help="Cloud provider to use"
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=40,
        help="Expected hours per student (for cost estimation)"
    )
    parser.add_argument(
        "--instance-type",
        default="g5.xlarge",
        help="Instance type (for cost estimation)"
    )
    
    args = parser.parse_args()
    
    if args.action == "estimate":
        costs = estimate_costs(args.count, args.hours, args.instance_type)
        print("\n=== Cost Estimation ===")
        print(f"Student Count: {costs['student_count']}")
        print(f"Hours per Student: {costs['hours_per_student']}")
        print(f"Instance Type: {costs['instance_type']}")
        print(f"Hourly Rate: ${costs['hourly_rate']}")
        print(f"\nCompute Cost: ${costs['compute_cost']:,.2f}")
        print(f"Storage Cost: ${costs['storage_cost']:,.2f}")
        print(f"Network Cost: ${costs['network_cost']:,.2f}")
        print(f"\nTotal Cost: ${costs['total_cost']:,.2f}")
        print(f"Cost per Student: ${costs['cost_per_student']:,.2f}")
        return
    
    provisioner = LabProvisioner(args.provider)
    
    if args.action == "provision":
        instances = provisioner.provision(args.count)
        print("\n=== Provisioned Instances ===")
        for inst in instances:
            print(f"  {inst['instance_id']}: {inst['jupyter_url']}")
    
    elif args.action == "teardown":
        confirm = input("Are you sure you want to teardown all lab environments? (yes/no): ")
        if confirm.lower() == "yes":
            provisioner.teardown()
        else:
            print("Teardown cancelled")
    
    elif args.action == "status":
        status = provisioner.get_status()
        print("\n=== Lab Environment Status ===")
        print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
