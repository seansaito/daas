#!/bin/bash

# Set the path to your Ansible playbook within the Terraform directory
ANSIBLE_PLAYBOOK="setup.yaml"

# Set the user for SSH (change 'ubuntu' to 'ec2-user' or your specific user if using a different AMI)
SSH_USER="ubuntu"

# Set the path to your SSH private key
PRIVATE_KEY_PATH="~/.ssh/id_rsa"

# Initialize Terraform (optional if already initialized)
echo "Initializing Terraform"
terraform init

# Plan
echo "Planning configuration"
terraform plan

# Apply Terraform configuration
echo "Applying configurations"
terraform apply -auto-approve

# Get the public IP address of the provisioned EC2 instance
EC2_IP=$(terraform output -raw instance_ip)
echo "IP address is ${EC2_IP}"

# Check if the IP address is empty
if [ -z "$EC2_IP" ]; then
    echo "Failed to get EC2 IP address from Terraform output."
    exit 1
fi

echo "Sleeping to wait for startup"
sleep 10

# Execute the Ansible playbook
echo "Running Ansible playbook"
ansible-playbook -i "$EC2_IP," -u $SSH_USER --private-key="$PRIVATE_KEY_PATH" $ANSIBLE_PLAYBOOK -v
