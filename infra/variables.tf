variable "project_id" {
  type = string
  description = "GCP Project Id"
}

variable "location" {
  type        = string
  default     = "europe-west4"
  description = "GCP location"
}

variable "app_name" {
  type        = string
  default     = "ragas-demo"
  description = "Application name"
}

variable "openai_api_key" {
  type        = string
}

variable "cohere_api_key" {
  type        = string
}

variable "langchain_api_key" {
  type        = string
}

variable "huggingface_token" {
  type        = string
}
