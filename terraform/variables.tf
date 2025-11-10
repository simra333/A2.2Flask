variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
  sensitive   = true  # Marks this as sensitive so it won't show in logs
}

variable "windows_vm_admin_password" {
  description = "Admin password for Windows VM"
  type        = string
  sensitive   = true
}

variable "linux_vm_admin_password" {
  description = "Admin password for Linux VM"
  type        = string
  sensitive   = true
  
}