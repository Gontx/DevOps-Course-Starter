terraform {
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = ">= 2.49"
        }       
    }
}

# Provides configuration details for the azure terraform provider
provider "azurerm" {
    features{}
}

# Adding my resource group
data "azurerm_resource_group" "main" {
    name = "McLaren1_GonzaloOtegui_ProjectExercise"
}

# CosmosDB
data "azurerm_cosmosdb_account" "acc" {
  name                = "todoappacc"
  resource_group_name = data.azurerm_resource_group.main.name
}

resource "azurerm_cosmosdb_mongo_database" "db" {
  name                = "todoappdb"
  resource_group_name = data.azurerm_cosmosdb_account.acc.resource_group_name
  account_name        = data.azurerm_cosmosdb_account.acc.name
  throughput          = 400
}

# Application
resource "azurerm_app_service_plan" "main" {
    name                    = "gontx-terraformed-asp"
    location                = data.azurerm_resource_group.main.location
    resource_group_name     = data.azurerm_resource_group.main.name
    kind                    = "Linux"
    reserved                = true

    sku {
        tier = "Basic"
        size = "B1"
    }
}

resource "azurerm_app_service" "my_app_service_container" {
    name                    = "gontx-todo-app"
    location                = data.azurerm_resource_group.main.location
    resource_group_name     = data.azurerm_resource_group.main.name
    app_service_plan_id     = azurerm_app_service_plan.main.id

    site_config {
        app_command_line = ""
        linux_fx_version = "DOCKER|gontx/todo-app:latest"
    }

    app_settings = {
        "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    }
}