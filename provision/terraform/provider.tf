terraform {
  required_providers {
    proxmox = {
      source  = "Telmate/proxmox"
      version = "3.0.1-rc4"
    }
  }
}

provider "proxmox" {
  pm_tls_insecure     = true
  pm_api_url          = "https://<PROXMOX_IP>:8006/api2/json"
  pm_user             = <PROXMOX_USER>
  pm_api_token_secret = <PROXMOX_TOKEN_SECRET>
  pm_api_token_id     = <PROXMOX_TOKEN_ID>
}