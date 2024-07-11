resource "google_storage_bucket_object" "index_folder" {
  name          = "index/"
  content       = "Empty directory"
  bucket        = "${google_storage_bucket.this.name}"
}

resource "google_vertex_ai_index" "this" {
  depends_on = [ google_storage_bucket_object.index_folder ]

  region   = var.location
  display_name = var.app_name
  description = "Vectorstore index"
  metadata {
    contents_delta_uri = "gs://${google_storage_bucket.this.name}/index/"
    config {
      dimensions = 1536
      approximate_neighbors_count = 150
      shard_size = "SHARD_SIZE_SMALL"
      distance_measure_type = "DOT_PRODUCT_DISTANCE"
      feature_norm_type = "NONE"
      algorithm_config {
        tree_ah_config {}
      }
    }
  }
  index_update_method = "STREAM_UPDATE"
}

resource "google_vertex_ai_index_endpoint" "this" {
  display_name = var.app_name
  description  = "Vectorstore index endpoint"
  region       = var.location

  public_endpoint_enabled = true
}

resource "null_resource" "index_deployment" {
  depends_on = [
    google_vertex_ai_index.this,
    google_vertex_ai_index_endpoint.this,
  ]

  triggers = {
    index_name        = "ragas_demo"
    project_id        = var.project_id
    location          = var.location
    index_id          = element(
      split("/", google_vertex_ai_index.this.id),
      length(split("/", google_vertex_ai_index.this.id)) - 1
    )
    index_endpoint_id = element(
      split("/", google_vertex_ai_index_endpoint.this.id),
      length(split("/", google_vertex_ai_index_endpoint.this.id)) - 1
    )
  }

  provisioner "local-exec" {
    command = <<EOT
    gcloud ai index-endpoints deploy-index ${self.triggers.index_endpoint_id} \
        --project=${self.triggers.project_id} \
        --region=${self.triggers.location} \
        --index=${self.triggers.index_id} \
        --deployed-index-id=${self.triggers.index_name} \
        --display-name=${self.triggers.index_name}
    EOT
  }
  
  provisioner "local-exec" {
    when    = destroy
    command = <<EOT
    gcloud ai index-endpoints undeploy-index ${self.triggers.index_endpoint_id} \
        --project=${self.triggers.project_id} \
        --region=${self.triggers.location} \
        --deployed-index-id=${self.triggers.index_name}
    EOT
  }
}
