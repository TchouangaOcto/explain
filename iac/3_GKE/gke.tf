#-------------------------------------------------------------------------------
# GKE RESOURCE CONFIGURATION
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# - GOOGLE CLOUD STORAGE RAW
#-------------------------------------------------------------------------------
# This blocks creates the Kubernetes cluster
resource "google_container_cluster" "_" {
  name                     = "space-cluster"
  location                 = local.region
  remove_default_node_pool = true
  initial_node_count       = 1
}

# Creating and attaching the node-pool to the Kubernetes Cluster
resource "google_container_node_pool" "node-pool" {
  name               = "node-pool"
  cluster            = google_container_cluster._.id
  initial_node_count = 1
  autoscaling {
    max_node_count  = 2
    location_policy = "BALANCED"
  }
  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    preemptible  = false
    machine_type = "e2-standard-4"
  }
}


#-------------------------------------------------------------------------------
#                              --- END ---
#-------------------------------------------------------------------------------