#-------------------------------------------------------------------------------
# GCP TERRAFORM PROVIDER
# https://registry.terraform.io/providers/hashicorp/google/latest/docs
#-------------------------------------------------------------------------------
terraform {
  required_providers {
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = "= 1.14.0"
    }
  }
}

provider "google" {
  project = local.project_id
  region  = local.region
}

#provider "helm" {
#  kubernetes {
#    config_path = "~/.kube/config"  # Path to your kubeconfig file
#  }
#}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

provider "kubernetes" {
  #host = "https://${google_container_cluster._.endpoint}"
  config_path = "~/.kube/config"
  #version     = "1.18.16"

}

provider "kubectl" {
  config_path = "~/.kube/config"
}
#-------------------------------------------------------------------------------
#                              --- END ---
#-------------------------------------------------------------------------------