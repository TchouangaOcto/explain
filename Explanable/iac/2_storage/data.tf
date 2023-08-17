data "google_compute_subnetwork" "run_subnet" {
  name = "spaceable-mvp-subnet-dat"
}

data "google_kms_key_ring" "key-ring" {
  name     = "spaceable-mvp-kms"
  location = var.region
}

data "google_kms_crypto_key" "key-cloudstorage" {
  name     = "spaceable-mvp-kms-cloudstorage"
  key_ring = data.google_kms_key_ring.key-ring.id
}