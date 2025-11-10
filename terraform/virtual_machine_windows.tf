resource "azurerm_virtual_machine" "windows_vm" {
  name                  = "A5.2-SA-windows-vm"
  location              = "UKSouth"
  resource_group_name   = azurerm_resource_group.rg.name
  network_interface_ids = [azurerm_network_interface.windows_nic.id]
  vm_size               = "Standard_B4as_v2"
  
  # Uncomment this line to delete the OS disk automatically when deleting the VM
  # delete_os_disk_on_termination = true
  
  # Uncomment this line to delete the data disks automatically when deleting the VM
  # delete_data_disks_on_termination = true
  
  storage_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2022-Datacenter"
    version   = "latest"
  }
  
  storage_os_disk {
    name              = "windows-osdisk1"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }
  
  os_profile {
    computer_name  = "winhost"
    admin_username = "testadmin"
    admin_password = var.windows_vm_admin_password
  }
  
  os_profile_windows_config {
    provision_vm_agent        = true
    enable_automatic_upgrades = true
  }
  
  tags = {
    environment = "staging"
  }
}