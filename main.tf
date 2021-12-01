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
resource "azurerm_cosmosdb_account" "acc" {
  name                  = "todoappacc"
  resource_group_name   = data.azurerm_resource_group.main.name
  location              = data.azurerm_resource_group.main.location
  offer_type            = "Standard"
  kind                  = "MongoDB"

  enable_automatic_failover = true

  capabilities {
      name = "EnableAggregationPipeline"
  }

  capabilities {
      name = "EnableServerless"
  }

  capabilities {
      name = "EnableMongo"
  }

  consistency_policy {
    consistency_level       ="BoundedStaleness" 
    max_interval_in_seconds = 10
    max_staleness_prefix    = 200
  }
 
  geo_location {
    location            = data.azurerm_resource_group.main.location
    failover_priority   = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "db" {
  name                = "todoappdb"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.acc.name
  throughput          = 800
  lifecycle {
    prevent_destroy = true
  }
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
        # pass envirionment variables
    }
}

variable "MONGODB_CONNECTION_STRING"{
    default = <<EOF
    mongodb://${azurerm_cosmosdb_account.acc.name}:
    ${azurerm_cosmosdb_account.acc.primary_key}@
    ${azurerm_cosmosdb_account.acc.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?
    ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000
    EOF
}