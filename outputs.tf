output "webapp_url" {
    value = "https://${azurerm_app_service.my_app_service_container.default_site_hostname}"
}

output "webhook_url" {
    value = "https://${azurerm_app_service.my_app_service_container.site_credential[0].username}:${azurerm_app_service.my_app_service_container.site_credential[0].password}@${azurerm_app_service.my_app_service_container.name}.scm.azurewebsites.net/docker/hook"
    
}