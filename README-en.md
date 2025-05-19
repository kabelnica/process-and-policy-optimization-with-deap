# Infrastructure Deployment Process Optimization Algorithm

## Technical Requirements
To deploy the model on a host machine without modifications, the user must have the following installed:
- Vagrant 2.4.5+
- VirtualBox 7.1.8+
- Python 3.12+ with the DEAP library (or Anaconda)
- Proxmox VE hypervisor

## Proxmox VE
The Proxmox VE hypervisor must be manually installed on dedicated infrastructure. It is recommended to deploy it on a physical machine, but a virtual machine can also be used if the CPU supports *nested virtualization*.  
During installation, it is recommended to follow the [Proxmox documentation](https://www.proxmox.com/en/products/proxmox-virtual-environment/get-started)

The optimization model expects the following LXC templates to be available on Proxmox VE:
- local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst
- local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst
- local:vztmpl/ubuntu-25.04-standard_25.04-1.1_amd64.tar.zst
- alpine-3.21-default_20241217_amd64.tar.xz

These templates can be downloaded using the `pveam download` command.

## Vagrant Infrastructure Setup
From the root directory of the repository, the infrastructure can be deployed using the command `vagrant up`. After successful execution, Jenkins and Terraform servers should appear in VirtualBox.  
The virtual machines can be accessed using `vagrant ssh jenkins` and `vagrant ssh terraform`.

To enable Jenkins to communicate with Terraform, an SSH key must be generated on the Jenkins server using the `ssh-keygen` command. The public key (`id_rsa.pub`) must then be added to the `.ssh/authorized_keys` file on the Terraform server:
```
ssh-rsa <PUBLIC_KEY> vagrant@jenkins
```

## Jenkins Server
After running Vagrant, navigate to the Jenkins web interface to complete the Jenkins installation.  
Jenkins URL: http://192.168.56.10:8080/  
After installation, perform the following steps:
- Install the SSH Agent plugin
- Create a [new API token](https://plugins.jenkins.io/ssh-agent/), **jenkins-tf-key**, which contains the private key (`id_rsa`) of the Vagrant user.
- Generate a Jenkins API token (Dashboard -> User -> Security), and add its value to the `optimization_model.py` source code of the optimization model

After configuring Jenkins, create a new pipeline called `OPA-gala-modelis`, including the contents of the **Jenkinsfile** in the script section.

For more details, see the [Jenkins documentation](https://www.jenkins.io/doc/).

## Terraform Server
To verify the installation of the Terraform server, log in to the virtual machine via the command line and run:

```
terraform -v 
```

In the Terraform server's user directory, a folder **/terraform-proxmox-test** has been created. In its **variables.tf** file, Proxmox VE user credentials must be added. The Proxmox user must have permissions to create and delete virtual machines for Terraform to function properly.

## DEAP Optimization Algorithm
The optimization algorithm is already configured with the modeling parameters discussed in the paper. To run the Python script, only the Jenkins user API information needs to be added.
The modeling results are saved in the **/results** directory. It also includes the modeling results discussed in the thesis.


