#-------------------------------------------------------------------------------
# VARIBALES
#-------------------------------------------------------------------------------
variable "organization_id" {
  type        = string
  description = "SpaceAble host organization ID"
  default     = "504780162421"
}

variable "project_id" {
  type        = string
  default     = "spaceable-mvp-datamesh-215"
  description = "The project id"
}

variable "region" {
  type        = string
  default     = "europe-west9"
  description = "The GCP region name"
}

#-------------------------------------------------------------------------------
#                              --- END ---
#-------------------------------------------------------------------------------