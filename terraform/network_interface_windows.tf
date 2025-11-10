resource "azurerm_network_interface" "windows_nic" {
  name                = "windows-vm-nic"
  location            = "UKSouth"
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
  }
}