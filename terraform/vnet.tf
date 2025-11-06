resource "azurerm_virtual_network" "vnet" {
  name                = "A5.2-SA-vnet"
  location            = "UKSouth"
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "subnet" {
  name                 = "A5.2-Subnet-Terraform"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}