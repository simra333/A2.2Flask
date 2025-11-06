resource "azurerm_network_interface" "main" {
  name                = "A5.2-SA-vm-nic"
  location            = "UKSouth"
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "testconfiguration1"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
  }
}