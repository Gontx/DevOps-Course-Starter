variable "location" {
    description = "The Azure location where all resources in thisdeployment should be created"
    default = "uksouth"
}

variable "client_id" {
    description = "Client ID for AUTH"
    sensitive = true
}
variable "client_secret" {
    description = "Client secret for AUTH"
    sensitive = true
}

variable "secret_key" {
    description = "Secret Key for Flask application"
    sensitive = true
}