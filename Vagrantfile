Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"

  # Definēt šablonu Vagrant VM
  def setup_vm(vm, hostname, ip, provision_script)
    vm.vm.hostname = hostname
    vm.vm.network "private_network", ip: ip
    vm.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
      vb.cpus = 1
    end
    vm.vm.provision "shell", inline: provision_script
  end

  # Jenkins serveris
  config.vm.define "jenkins" do |jenkins|
    setup_vm(
      jenkins,
      "jenkins",
      "192.168.56.10",
      <<-SHELL
        sudo apt-get update
        sudo apt-get install -y openjdk-17-jdk curl gnupg unzip openssh-client openssh-server

        # Jenkins instalācija
        curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
          /usr/share/keyrings/jenkins-keyring.asc > /dev/null
        echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
          https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
          /etc/apt/sources.list.d/jenkins.list > /dev/null
        sudo apt-get update
        sudo apt-get install -y jenkins

        # Instalēt OPA un Conftest
        curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64
        chmod +x opa
        sudo mv opa /usr/local/bin/opa

        wget https://github.com/open-policy-agent/conftest/releases/download/v0.24.0/conftest_0.24.0_Linux_x86_64.tar.gz
        tar xzf conftest_0.24.0_Linux_x86_64.tar.gz
        sudo mv conftest /usr/local/bin/

      SHELL
    )
  end

  # Terraform serveris
  config.vm.define "terraform" do |terraform|
    setup_vm(
      terraform,
      "terraform",
      "192.168.56.11",
      <<-SHELL
        sudo apt-get update
        sudo apt-get install -y unzip curl gnupg software-properties-common openssh-server

        # Uzstāda uz servera Terraform
        curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
        echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
          https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
          sudo tee /etc/apt/sources.list.d/hashicorp.list
        sudo apt-get update
        sudo apt-get install -y terraform

      SHELL
    )
  end
end

