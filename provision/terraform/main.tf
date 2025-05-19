# Optimizācijas modeļa Terraform projekts
# Versija: 1.0
# Autors: Kaspars Ābelnīca

# Lielais konteineris
resource "proxmox_lxc" "ubuntu_container" {
  count        = var.large_container_count
  target_node  = "pve"
  hostname     = "lxc-large-${count.index + 1}"
  vmid = 100 + count.index
  ostemplate   = "${var.large_container_os}"
  password     = "${var.large_container_password}${count.index}"
  cores        = 2
  memory       = var.large_container_memory
  swap         = var.large_container_swap

  rootfs {
    storage = "local-lvm"
    size    = var.large_container_disk_size
  }

  network {
    name   = "eth0"
    bridge = "vmbr0"
    ip     = "dhcp"
    gw     = "192.168.1.1"
    firewall = var.large_container_firewall
  }

  unprivileged = var.large_container_unprivileged
  start        = true
  onboot       = true
}

# Mazais konteineris
resource "proxmox_lxc" "small_container" {
  count        = var.small_container_count
  target_node  = "pve"
  hostname     = "lxc-small-${count.index + 1}"
  vmid = 200 + count.index
  ostemplate   = "${var.small_container_os}"
  password     = "${var.small_container_password}${count.index}"
  cores        = var.small_container_cpu
  memory       = var.small_container_memory
  swap         = var.small_container_swap

  rootfs {
    storage = "local-lvm"
    size    = var.small_container_disk_size
  }

  network {
    name   = "eth0"
    bridge = "vmbr0"
    ip     = "dhcp"
    gw     = "192.168.1.1"
    firewall = var.small_container_firewall
  }

  unprivileged = var.small_container_unprivileged
  start        = true
  onboot       = true
}