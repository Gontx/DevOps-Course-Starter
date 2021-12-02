variable "prefix" {
    description = "The prefix used for all resources in this environment"
    default = "todo-app"
}

variable "location" {
    description = "The Azure location where all resources in thisdeployment should be created"
    default = "uksouth"
}

variable "client_id" {
    description = "Client ID for AUTH"
}