#-------------------------------------------------------------------------------
# VARIBALES
#-------------------------------------------------------------------------------
variable "organization_id" {
  type        = string
  description = "SpaceAble host organization ID"
  default     = "1050138996742"
}

variable "project_id" {
  type        = string
  default     = "spaceable-cluster-sandbox"
  description = "The project id"
}

variable "region" {
  type        = string
  default     = "europe-west9"
  description = "The GCP region name"
}

variable "gcp_service_list" {
  type        = any
  description = "All needed gcp services"
}
#-------------------------------------------------------------------------------
#                              --- END ---
#-------------------------------------------------------------------------------