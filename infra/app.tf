locals {
  app_name          = "streamlit-app"
  app_image_name    = "streamlit_app"
  app_image_version = "latest"
  app_image_tag     = "${local.registry_uri}/${local.app_image_name}:${local.app_image_version}"
}


resource "null_resource" "build_app_image" {
  depends_on = [
    google_artifact_registry_repository.this
  ]

  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = (templatefile("${path.module}/build_image.tpl", {
      source    = "${local.root_path}/src/app/"
      location  = var.location
      image_tag = local.app_image_tag
    }
    ))
  }
}

resource "google_cloud_run_v2_service" "app" {
  depends_on = [ 
    google_project_service.cloud_run,
    null_resource.build_app_image,
  ]

  name     = local.app_name
  location = var.location
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = local.app_image_tag 

      ports {
        container_port = 8501
      }

      env {
        name = "ENDPOINT_URL"
        value = google_cloud_run_v2_service.api.uri
      }

    }
  }
}

data "google_iam_policy" "noauth_app" {
  binding {
    role = "roles/run.invoker"
    members = ["allUsers"]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth_app" {
  location    = google_cloud_run_v2_service.app.location
  project     = google_cloud_run_v2_service.app.project
  service     = google_cloud_run_v2_service.app.name

  policy_data = data.google_iam_policy.noauth_app.policy_data
}
