resource "azurerm_kubernetes_cluster" "aks" {
  name                = "pythonapp-aks-cluster-sa"
  location            = "UKSouth"
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "pythonappaks"

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "Standard_B2ms"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    Environment = "Development"
  }
}

output "kube_config" {
  value     = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}

output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "aks_resource_group" {
  value = azurerm_kubernetes_cluster.aks.resource_group_name
}