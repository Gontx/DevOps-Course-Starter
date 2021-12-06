output "webapp_url" {
    value = "hhtps://${azurerm_app_service.main.default_site_hostname}"
}

output "webhook_url" {
    value = <<EOF
    https://${azurerm_app_service.main.site_credential[0].username}:
    ${azurerm_app_service.main.site_credential[0].password}@
    ${azurerm_app_service.main.name}.scm.azurewebsites.net/docker/hook"
    EOF
}