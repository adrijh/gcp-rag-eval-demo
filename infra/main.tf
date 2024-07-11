locals {
  root_path    = abspath("${path.root}/../")
  project_name = "${var.location}-${var.app_name}"
  registry_uri = "${var.location}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.this.name}"
}

data "google_project" "this" {
  project_id = var.project_id
}

resource "google_project_service" "cloud_run" {
  project = data.google_project.this.id
  service = "run.googleapis.com"

  disable_dependent_services = false
}

resource "google_project_service" "project_services" {
  project = data.google_project.this.project_id
  service = "appengine.googleapis.com"

  disable_dependent_services = false
}

resource "google_project_service" "app_engine" {
  project = data.google_project.this.project_id
  service = "appengineflex.googleapis.com"

  disable_dependent_services = false
}


resource "random_integer" "bucket_suffix" {
  min = 1000
  max = 9999
}

resource "google_storage_bucket" "this" {
  force_destroy = true

  name     = "${var.app_name}-${random_integer.bucket_suffix.result}"
  location = var.location
  uniform_bucket_level_access = true
}

resource "google_artifact_registry_repository" "this" {
  location      = var.location
  repository_id = var.app_name
  description   = "Container Registry"
  format        = "DOCKER"
}
