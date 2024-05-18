# Define a random pet resource for resource group name
resource "random_pet" "rg_name" {
  prefix = var.resource_group_name_prefix
}

# Define the Azure resource group
resource "azurerm_resource_group" "rg" {
  location = var.resource_group_location
  name     = "travel-rg"
}

# Define random pet resources for Kubernetes cluster name and DNS prefix
resource "random_pet" "azurerm_kubernetes_cluster_name" {
  prefix = "cluster"
}

resource "random_pet" "azurerm_kubernetes_cluster_dns_prefix" {
  prefix = "dns"
}

# Define the Azure Kubernetes Service (AKS) cluster
resource "azurerm_kubernetes_cluster" "k8s" {
  location            = azurerm_resource_group.rg.location
  name                = "kubernetes-travel"
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = random_pet.azurerm_kubernetes_cluster_dns_prefix.id

  identity {
    type = "SystemAssigned"
  }

  default_node_pool {
    name       = "agentpool"
    vm_size    = "Standard_D2_v2"
    node_count = var.node_count
  }
  
  linux_profile {
    admin_username = var.username

    ssh_key {
      key_data = azapi_resource_action.ssh_public_key_gen.output.publicKey
    }
  }

  network_profile {
    network_plugin    = "kubenet"
    load_balancer_sku = "standard"
  }
}

# Define the Kubernetes namespace for ingress
resource "kubernetes_namespace" "ingress" {
  metadata {
    name = "ingress"
  }
}

# Define the Helm release for the NGINX Ingress Controller
resource "helm_release" "ingress-nginx-controller-interno" {
  name       = "ingress-nginx-controller-interno"
  namespace  = "ingress"
  repository = "https://helm.nginx.com/stable"
  chart      = "nginx-ingress"
  version    = "0.16.2"
  create_namespace = true

  set {
    name  = "controller.service.externalTrafficPolicy"
    value = "Local"
  }

  set {
    name  = "controller.service.annotations.service\\.beta\\.kubernetes\\.io/azure-load-balancer-internal"
    value = "true"
  }

  set {
    name  = "controller.ingressClass"
    value = "nginx"
  }

  set {
    name  = "controller.setAsDefaultIngress"
    value = true
  }

  set {
    name  = "controller.ingressClassResource.name"
    value = "class1"
  }

  set {
    name  = "controller.ingressClassResource.enabled"
    value = "true"
  }

  set {
    name  = "controller.ingressClassByName"
    value = "true"
  }

  set {
    name  = "controller.electionID"
    value = "nginx-interno"
  }

  set {
    name  = "controller.ingressClassResource.controllerValue"
    value = "k8s/api.deployment.yml"
  }

  depends_on = [
    kubernetes_namespace.ingress,
  ]
}
