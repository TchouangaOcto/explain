#-------------------------------------------------------------------------------
# OUTPUTS
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# - GOOGLE CLOUD STORAGE FOR LOGS
#-------------------------------------------------------------------------------
output "logs_id" {
  value       = google_storage_bucket.logs.id
  description = "logs bucket ID"
}

output "logs_name" {
  value       = google_storage_bucket.logs.name
  description = "logs bucket name"
}

output "vpc_logs_id" {
  value       = google_storage_bucket_object.vpc-logs.id
  description = "vpc logs folder ID"
}

output "vpc_logs_name" {
  value       = google_storage_bucket_object.vpc-logs.name
  description = "vpc logs folder name"
}

#-------------------------------------------------------------------------------
# - FIREWALL LOGS OUTPUTS
#-------------------------------------------------------------------------------
output "firewall_logs_id" {
  value       = google_storage_bucket_object.firewall-logs.id
  description = "firewall folder ID"
}

output "firewall_logs_name" {
  value       = google_storage_bucket_object.firewall-logs.name
  description = "firewall folder name"
}


#-------------------------------------------------------------------------------
# - GOOGLE CLOUD STORAGE DTA DOMAIN OUTPUTS
#-------------------------------------------------------------------------------
output "datadomain_stm_id" {
  value       = google_storage_bucket.datadomain-stm.id
  description = "datadomain stm ID"
}

output "datadomain_stm_name" {
  value       = google_storage_bucket.datadomain-stm.name
  description = "datadomain stm name"
}

output "datadomain_swe_id" {
  value       = google_storage_bucket.datadomain-swe.id
  description = "datadomain swe ID"
}

output "datadomain_swe_name" {
  value       = google_storage_bucket.datadomain-swe.name
  description = "datadomain swe name"
}

#-------------------------------------------------------------------------------
# - GOOGLE CLOUD STORAGE RAW OUTPUTS
#-------------------------------------------------------------------------------
output "datahub_raw_id" {
  value       = google_storage_bucket.datahub-raw.id
  description = "datahub raw bucket ID"
}

output "datahub_raw_name" {
  value       = google_storage_bucket.datahub-raw.name
  description = "datahub raw bucket name"
}

output "datahub_raw_stm_id" {
  value       = google_storage_bucket_object.raw-stm.id
  description = "datahub raw stm folder ID"
}

output "datahub_raw_stm_name" {
  value       = google_storage_bucket_object.raw-stm.name
  description = "datahub raw stm folder name"
}

output "datahub_raw_swe_id" {
  value       = google_storage_bucket_object.raw-swe.id
  description = "datahub raw swe folder ID"
}

output "datahub_raw_swe_name" {
  value       = google_storage_bucket_object.raw-swe.name
  description = "datahub raw swe folder name"

}

#-------------------------------------------------------------------------------
# - GOOGLE CLOUD STORAGE SILVER OUTPUTS
#-------------------------------------------------------------------------------
output "datahub_silver_id" {
  value       = google_storage_bucket.datahub-silver.id
  description = "datahub silver raw bucket ID"
}

output "datahub_silver_name" {
  value       = google_storage_bucket.datahub-silver.name
  description = "datahub silver raw bucket name"
}

output "datahub_silver_stm_id" {
  value       = google_storage_bucket_object.silver-stm.id
  description = "datahub silver stm folder ID"
}

output "datahub_silver_stm_name" {
  value       = google_storage_bucket_object.silver-stm.name
  description = "datahub silver stm folder name"
}


output "datahub_silver_swe_id" {
  value       = google_storage_bucket_object.silver-swe.id
  description = "datahub silver swe folder ID"
}

output "datahub_silver_swe_name" {
  value       = google_storage_bucket_object.silver-swe.name
  description = "datahub silver swe folder name"

}

#-------------------------------------------------------------------------------
# - GOOGLE CLOUD STORAGE GOLD OUTPUTS
#-------------------------------------------------------------------------------
output "datahub_gold_id" {
  value       = google_storage_bucket.datahub-silver.id
  description = "datahub silver raw bucket ID"
}

output "datahub_gold_name" {
  value       = google_storage_bucket.datahub-silver.name
  description = "datahub silver raw bucket name"
}

output "datahub_gold_stm_id" {
  value       = google_storage_bucket_object.gold-stm.id
  description = "datahub silver stm folder ID"
}

output "datahub_gold_stm_name" {
  value       = google_storage_bucket_object.gold-stm.name
  description = "datahub silver stm folder name"
}

output "datahub_gold_swe_id" {
  value       = google_storage_bucket_object.gold-swe.id
  description = "datahub silver swe folder ID"
}

output "datahub_gold_swe_name" {
  value       = google_storage_bucket_object.gold-swe.name
  description = "datahub silver swe folder name"

}

#-------------------------------------------------------------------------------
#                              --- END ---
#-------------------------------------------------------------------------------