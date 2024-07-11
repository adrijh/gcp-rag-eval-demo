locals {
  api_name          = "langchain-api"
  api_image_name    = "langchain_api"
  api_image_version = "latest"
  api_image_tag     = "${local.registry_uri}/${local.api_image_name}:${local.api_image_version}"
}


resource "null_resource" "build_api_image" {
  depends_on = [
    google_artifact_registry_repository.this
  ]

  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = (templatefile("${path.module}/build_image.tpl", {
      source    = "${local.root_path}/src/api/"
      location  = var.location
      image_tag = local.api_image_tag
    }
    ))
  }
}

resource "google_cloud_run_v2_service" "api" {
  depends_on = [ 
    google_project_service.cloud_run,
    null_resource.build_api_image,
  ]

  name     = local.api_name
  location = var.location
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = local.api_image_tag 

      env {
        name = "OPENAI_API_KEY"
        value = var.openai_api_key
      }

      env {
        name = "HUGGINGFACE_TOKEN"
        value = var.huggingface_token
      }

      env {
        name = "COHERE_API_KEY"
        value = var.cohere_api_key
      }

      env {
        name = "LANGCHAIN_API_KEY"
        value = var.langchain_api_key
      }

      env {
        name = "LANGCHAIN_TRACING_V2"
        value = "v2"
      }

      env {
        name = "VECTOR_ENDPOINT"
        value = google_vertex_ai_index_endpoint.this.public_endpoint_domain_name
      }

      env {
        name = "VECTOR_INDEX_NAME"
        value = "doc-vector"
      }

    }
  }
}

data "google_iam_policy" "noauth_api" {
  binding {
    role = "roles/run.invoker"
    members = ["allUsers"]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth_api" {
  location    = google_cloud_run_v2_service.api.location
  project     = google_cloud_run_v2_service.api.project
  service     = google_cloud_run_v2_service.api.name

  policy_data = data.google_iam_policy.noauth_api.policy_data
}
