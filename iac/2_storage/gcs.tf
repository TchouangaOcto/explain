#-------------------------------------------------------------------------------
# RESOURCES DE STOCKAGE DANS MEDAILLON LAKEHOUS
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# - GOOGLE CLOUD STORAGE RAW
#     * Dossier SWT
#     * Dossier SWE
#-------------------------------------------------------------------------------
resource "google_storage_bucket" "datahub-raw" {
  name     = "spaceable-mvp-datahub-raw"
  location = local.region

  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true
  versioning {
    enabled = false
  }
  encryption {
    default_kms_key_name = data.google_kms_crypto_key.key-cloudstorage.id
  }

}
resource "google_storage_bucket_object" "raw-stm" {
  name    = "STM/"
  content = "stm raw"
  bucket  = google_storage_bucket.datahub-raw.name
}

resource "google_storage_bucket_object" "raw-swe" {
  name    = "SWE/"
  content = "swe raw"
  bucket  = google_storage_bucket.datahub-raw.name
}

#-------------------------------------------------------------------------------
# - GOOGLE CLOUD STORAGE SILVER
#     * Dossier SWT
#     * Dossier SWE
#-------------------------------------------------------------------------------

resource "google_storage_bucket" "datahub-silver" {
  name     = "spaceable-mvp-datahub-silver"
  location = local.region

  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true
  versioning {
    enabled = false
  }
  encryption {
    default_kms_key_name = data.google_kms_crypto_key.key-cloudstorage.id
  }
}
resource "google_storage_bucket_object" "silver-stm" {
  name    = "STM/"
  content = "stm silver"
  bucket  = google_storage_bucket.datahub-silver.name
}

resource "google_storage_bucket_object" "silver-swe" {
  name    = "SWE/"
  content = "swe silver"
  bucket  = google_storage_bucket.datahub-silver.name
}


#-------------------------------------------------------------------------------
# - GOOGLE CLOUD STORAGE GOLD
#     * Dossier SWT
#     * Dossier SWE
#-------------------------------------------------------------------------------
resource "google_storage_bucket" "datahub-gold" {
  name     = "spaceable-mvp-datahub-gold"
  location = local.region

  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true
  versioning {
    enabled = false
  }
  encryption {
    default_kms_key_name = data.google_kms_crypto_key.key-cloudstorage.id
  }
}
resource "google_storage_bucket_object" "gold-stm" {
  name    = "STM/"
  content = "stm gold"
  bucket  = google_storage_bucket.datahub-gold.name
}

resource "google_storage_bucket_object" "gold-swe" {
  name    = "SWE/"
  content = "swe gold"
  bucket  = google_storage_bucket.datahub-gold.name
}


#-------------------------------------------------------------------------------
# RESOURCES DE STOCKAGE DANS LE DATA DOMAIN
# - GOOGLE CLOUD STORAGE STM PRODUCT
# - GOOGLE CLOUD STORAGE SWE PRODUCT
#-------------------------------------------------------------------------------
resource "google_storage_bucket" "datadomain-stm" {
  name     = "spaceable-mvp-data-domain-stm-product"
  location = local.region

  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true
  versioning {
    enabled = false
  }
  encryption {
    default_kms_key_name = data.google_kms_crypto_key.key-cloudstorage.id
  }
}

resource "google_storage_bucket" "datadomain-swe" {
  name     = "spaceable-mvp-data-domain-swe-product"
  location = local.region

  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true
  versioning {
    enabled = false
  }
  encryption {
    default_kms_key_name = data.google_kms_crypto_key.key-cloudstorage.id
  }
}

#-------------------------------------------------------------------------------
# RESOURCES DE STOCKAGE POUR LES LOGS
# - GOOGLE CLOUD STORAGE LOGS
#     * Dossier vpc flow logs
#     * Dossier firewall rules
#-------------------------------------------------------------------------------
resource "google_storage_bucket" "logs" {
  name     = "spaceable-mvp-logs"
  location = local.region

  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true
  versioning {
    enabled = false
  }
  encryption {
    default_kms_key_name = data.google_kms_crypto_key.key-cloudstorage.id
  }
}

resource "google_storage_bucket_object" "vpc-logs" {
  name    = "vpc_flow_logs/"
  content = "dossier de vpc flow logs"
  bucket  = google_storage_bucket.logs.name
}

resource "google_storage_bucket_object" "firewall-logs" {
  name    = "firewall_rules/"
  content = "dossier pour les firewall rules"
  bucket  = google_storage_bucket.logs.name
}

#-------------------------------------------------------------------------------
#                              --- END ---
#-------------------------------------------------------------------------------