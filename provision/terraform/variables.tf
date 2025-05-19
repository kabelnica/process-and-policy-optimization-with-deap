# Optimizācijas modeļa Terraform projekta mainīgie
# Versija: 1.0
# Autors: Kaspars Ābelnīca

# Lielā konteinera mainīgie
variable "large_container_count" {
  description = "Number of large LXC containers to create"
  type        = number
  default     = 1
}

variable "large_container_password" {
  description = "Initial password for large containers"
  type        = string
  default     = "password"
}

variable "large_container_unprivileged" {
  description = "Set large LXC to run as unprivileged"
  type        = bool
  default     = false
}

variable "large_container_os" {
  description = "What LXC template should be used to provision large containers"
  type        = string
  default     = "local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst"
}

variable "large_container_memory" {
  description = "RAM to assign to specific large LXC"
  type        = number
  default     = 1024
}

variable "large_container_swap" {
  description = "Swap memory to assign to specific large LXC"
  type        = number
  default     = 512
}

variable "large_container_disk_size" {
  description = "What disk size should be used for large containers"
  type        = string
  default     = "16G"
}

variable "large_container_firewall" {
  description = "Set the large LXC to have firewall pre-configured"
  type        = bool
  default     = false
}

# Mazā konteinera mainīgie
variable "small_container_count" {
  description = "Number of small LXC containers to create"
  type        = number
  default     = 1
}

variable "small_container_password" {
  description = "Initial password for small containers"
  type        = string
  default     = "password"
}

variable "small_container_unprivileged" {
  description = "Set small LXC to run as unprivileged"
  type        = bool
  default     = false
}

variable "small_container_os" {
  description = "What LXC template should be used to provision small containers"
  type        = string
  default     = "local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst"
}

variable "small_container_memory" {
  description = "RAM to assign to specific small LXC"
  type        = number
  default     = 1024
}

variable "small_container_swap" {
  description = "Swap memory to assign to specific small LXC"
  type        = number
  default     = 512
}

variable "small_container_disk_size" {
  description = "What disk size should be used for small containers"
  type        = string
  default     = "16G"
}

variable "small_container_firewall" {
  description = "Set the small LXC to have firewall pre-configured"
  type        = bool
  default     = false
}

variable "small_container_cpu" {
  description = "CPU cores to assign to specific small LXC"
  type        = number
  default     = 1
}