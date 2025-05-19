#!groovy

pipeline {
  agent any
  // Piekļuve Terraform serverim ar SSH, kā arī visi mainīgie ko padod plānam
  environment {
    TF_VM = "192.168.56.11"
    TF_USER = "vagrant"
    TF_VAR_LARGE_CONTAINER_COUNT = "${LARGE_CONTAINER_COUNT}"
    TF_VAR_LARGE_CONTAINER_PASSWORD = "${LARGE_CONTAINER_PASSWORD}"
    TF_VAR_LARGE_CONTAINER_UNPRIVILEGED = "${LARGE_CONTAINER_UNPRIVILEGED}"
    TF_VAR_LARGE_CONTAINER_OS = "${LARGE_CONTAINER_OS}"
    TF_VAR_LARGE_CONTAINER_MEMORY = "${LARGE_CONTAINER_MEMORY}"
    TF_VAR_LARGE_CONTAINER_SWAP = "${LARGE_CONTAINER_SWAP}"
    TF_VAR_LARGE_CONTAINER_DISK_SIZE = "${LARGE_CONTAINER_DISK_SIZE}"
    TF_VAR_LARGE_CONTAINER_FIREWALL = "${LARGE_CONTAINER_FIREWALL}"
    TF_VAR_SMALL_CONTAINER_COUNT = "${SMALL_CONTAINER_COUNT}"
    TF_VAR_SMALL_CONTAINER_PASSWORD = "${SMALL_CONTAINER_PASSWORD}"
    TF_VAR_SMALL_CONTAINER_UNPRIVILEGED = "${SMALL_CONTAINER_UNPRIVILEGED}"
    TF_VAR_SMALL_CONTAINER_OS = "${SMALL_CONTAINER_OS}"
    TF_VAR_SMALL_CONTAINER_MEMORY = "${SMALL_CONTAINER_MEMORY}"
    TF_VAR_SMALL_CONTAINER_SWAP = "${SMALL_CONTAINER_SWAP}"
    TF_VAR_SMALL_CONTAINER_DISK_SIZE = "${SMALL_CONTAINER_DISK_SIZE}"
    TF_VAR_SMALL_CONTAINER_FIREWALL = "${SMALL_CONTAINER_FIREWALL}"
    TF_VAR_SMALL_CONTAINER_CPU = "${SMALL_CONTAINER_CPU}"
  }
  parameters {
    // Mainīgie pēc kuriem DEAP modificē cauruļvadu
    // Lielais konteiners
    string(name: 'LARGE_CONTAINER_COUNT', defaultValue: '1', description: 'Izveidoto LXC lielo konteineru skaits')
    string(name: 'LARGE_CONTAINER_PASSWORD', defaultValue: 'passwd', description: 'Izveidoto LXC lielo konteineru paroles šablons')
    booleanParam(name: 'LARGE_CONTAINER_UNPRIVILEGED', defaultValue: false, description: 'Vai LXC lielo konteineru konfigurēt ar ierobežotu lietotāju')
    string(name: 'LARGE_CONTAINER_OS', defaultValue: 'local:vztmpl/ubuntu-25.04-standard_25.04-1.1_amd64.tar.zst', description: 'Kādu šablonu izmantot, lai izveidotu LXC lielo konteineri')
    string(name: 'LARGE_CONTAINER_MEMORY', defaultValue: '1024', description: 'Lielā LXC konteinera RAM')
    string(name: 'LARGE_CONTAINER_SWAP', defaultValue: '512', description: 'Lielā LXC konteinera Swap')
    string(name: 'LARGE_CONTAINER_DISK_SIZE', defaultValue: '16G', description: 'Lielā LXC konteinera diska izmērs (piem. "16G")')
    booleanParam(name: 'LARGE_CONTAINER_FIREWALL', defaultValue: false, description: 'Vai LXC lielo konteineru konfigurēt ar ugunsmūri')
    // Mazais konteiners
    string(name: 'SMALL_CONTAINER_COUNT', defaultValue: '1', description: 'Izveidoto LXC mazo konteineru skaits')
    string(name: 'SMALL_CONTAINER_PASSWORD', defaultValue: 'passwd', description: 'Izveidoto LXC mazo konteineru paroles šablons')
    booleanParam(name: 'SMALL_CONTAINER_UNPRIVILEGED', defaultValue: false, description: 'Vai LXC mazo konteineru konfigurēt ar ierobežotu lietotāju')
    string(name: 'SMALL_CONTAINER_OS', defaultValue: 'local:vztmpl/ubuntu-25.04-standard_25.04-1.1_amd64.tar.zst', description: 'Kādu šablonu izmantot, lai izveidotu LXC mazo konteineri')
    string(name: 'SMALL_CONTAINER_MEMORY', defaultValue: '1024', description: 'Mazā LXC konteinera RAM')
    string(name: 'SMALL_CONTAINER_SWAP', defaultValue: '512', description: 'Mazā LXC konteinera Swap')
    string(name: 'SMALL_CONTAINER_DISK_SIZE', defaultValue: '16G', description: 'Mazā LXC konteinera diska izmērs (piem. "16G")')
    booleanParam(name: 'SMALL_CONTAINER_FIREWALL', defaultValue: false, description: 'Vai LXC mazo konteineru konfigurēt ar ugunsmūri')
    string(name: 'SMALL_CONTAINER_CPU', defaultValue: '2', description: 'Mazā LXC konteinera CPU kodoli')
    }
  
  stages {
    // Inicializē Terraform projektu
    stage('Terraform Init') {
      steps {
        // Pieslēdzas Terraform serverim as SSH Agent
        sshagent (credentials: ['jenkins-tf-key']) {
          sh """
            ssh -o StrictHostKeyChecking=no $TF_USER@$TF_VM 'cd ~/terraform-proxmox-test/ && terraform init'
          """
        }
      }
    } 
   // Izveido Terraform plānu
    stage('Terraform Plan') {
      steps {
        sshagent (credentials: ['jenkins-tf-key']) {
          sh """
            ssh -o StrictHostKeyChecking=no $TF_USER@$TF_VM '
              cd ~/terraform-proxmox-test/ && terraform plan -out=tfplan \\
              -var "large_container_count=${LARGE_CONTAINER_COUNT}" \\
              -var "large_container_password=${LARGE_CONTAINER_PASSWORD}" \\
              -var "large_container_unprivileged=${LARGE_CONTAINER_UNPRIVILEGED}" \\
              -var "large_container_os=${LARGE_CONTAINER_OS}" \\
              -var "large_container_memory=${LARGE_CONTAINER_MEMORY}" \\
              -var "large_container_swap=${LARGE_CONTAINER_SWAP}" \\
              -var "large_container_disk_size=${LARGE_CONTAINER_DISK_SIZE}" \\
              -var "large_container_firewall=${LARGE_CONTAINER_FIREWALL}" \\
              -var "small_container_count=${SMALL_CONTAINER_COUNT}" \\
              -var "small_container_password=${SMALL_CONTAINER_PASSWORD}" \\
              -var "small_container_unprivileged=${SMALL_CONTAINER_UNPRIVILEGED}" \\
              -var "small_container_os=${SMALL_CONTAINER_OS}" \\
              -var "small_container_memory=${SMALL_CONTAINER_MEMORY}" \\
              -var "small_container_swap=${SMALL_CONTAINER_SWAP}" \\
              -var "small_container_disk_size=${SMALL_CONTAINER_DISK_SIZE}" \\
              -var "small_container_firewall=${SMALL_CONTAINER_FIREWALL}" \\
              -var "small_container_cpu=${SMALL_CONTAINER_CPU}"
            '
          """
        }
      }
    }
    // Izveido JSON datni, ko analizēt ar Open Policy Agent
    stage('Create JSON of Terraform for OPA') {
      steps {
        sshagent (credentials: ['jenkins-tf-key']) {
          sh """
            ssh -o StrictHostKeyChecking=no $TF_USER@$TF_VM 'cd ~/terraform-proxmox-test/ && terraform show -json tfplan > plan.json'
          """
        }
      }
    }
    // Pārnes iegūto plānu uz Jenkins
    stage('Retrieve plan.json') {
      steps {
        sshagent (credentials: ['jenkins-tf-key']) {
          sh "scp -o StrictHostKeyChecking=no $TF_USER@$TF_VM:~/terraform-proxmox-test/plan.json ."
        }
      }
    }
    // Iegūst OPA politikas
    stage('Load list of policies') {
      steps {
            sh "cp -a ~/opa-gala-modelis/. ./policy/"
      }
    }
    // Pārbauda politikas ar Conftest
    stage('Conftest Policy Check') {
      steps {
          script {
            def conftestStatus = sh(returnStatus: true, script: 'conftest test plan.json --no-color')
            if (conftestStatus != 0) {
                echo "COMPLIANCE: FAIL"
                echo "Policy violations found"
                currentBuild.result = "UNSTABLE"
            } else {
                echo "COMPLIANCE: PASS"
            }
          }
      }
    }
    // Izpilda Terraform
    stage('Execute the Terraform build') {
      steps {
        script{
          def start = System.currentTimeMillis()
          sshagent (credentials: ['jenkins-tf-key']) {
          sh """
            ssh -o StrictHostKeyChecking=no $TF_USER@$TF_VM 'cd ~/terraform-proxmox-test/ && terraform apply tfplan'
          """
          }
          def end = System.currentTimeMillis()
          def tfDuration = (end - start) / 1000

          echo "Deployment time: ${tfDuration} seconds"
          writeFile file: 'deploy_time.txt', text: "${tfDuration}"
          archiveArtifacts artifacts: 'deploy_time.txt', fingerprint: true
        }
      }
    }
    stage('Terraform Destroy') {
      steps {
        // Iznīcina esošo infrastruktūru uz Proxmox, lai izvairītos no Proxmox resursu izbeigšanās
        retry(3) {
            sshagent (credentials: ['jenkins-tf-key']) {
              sh """
                ssh -o StrictHostKeyChecking=no $TF_USER@$TF_VM 'cd ~/terraform-proxmox-test/ && terraform destroy -auto-approve'
              """
            }
        }
      }
    }     
  }
}