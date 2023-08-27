#-------------------------------------------------------------------------------
# GCP TERRAFORM PROVIDER
# https://registry.terraform.io/providers/hashicorp/google/latest/docs
#-------------------------------------------------------------------------------
provider "google" {
  project = local.project_id
  region  = local.region
}

terraform {
  required_version = "1.5.3"
  backend "gcs" {
    bucket = "spaceable-mvp-terraform"
    prefix = "storage"
  }
}
#-------------------------------------------------------------------------------
#                              --- END ---
#-------------------------------------------------------------------------------