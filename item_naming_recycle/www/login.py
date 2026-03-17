no_cache = 1

def get_context(context):
    import frappe
    from frappe.utils import cint

    # Logo
    context.logo = frappe.get_website_settings("app_logo") or frappe.get_hooks("app_logo_url")
    if isinstance(context.logo, list):
        context.logo = context.logo[0] if context.logo else None

    context.app_name = frappe.get_website_settings("app_name") or frappe.db.get_default("company") or "ERPNext"

    # Login settings
    context.disable_signup = cint(frappe.get_website_settings("disable_signup"))
    context.disable_user_pass_login = cint(frappe.db.get_single_value("System Settings", "disable_user_pass_login") or 0)
    context.login_label = frappe.db.get_single_value("System Settings", "login_label") or "Email"
    context.login_with_email_link = cint(frappe.db.get_single_value("System Settings", "login_with_email_link") or 0)
    context.show_footer_on_login = cint(frappe.get_website_settings("show_footer_on_login"))

    # Social login providers
    from frappe.utils.oauth import get_oauth2_providers
    try:
        context.provider_logins = frappe.get_all(
            "Social Login Key",
            filters={"enable_social_login": 1},
            fields=["name", "provider_name", "icon", "client_id"],
            order_by="name",
        )
        for provider in context.provider_logins:
            provider.auth_url = f"/api/method/frappe.integrations.oauth2_logins.login_via_{provider.name.lower()}"
    except Exception:
        context.provider_logins = []

    # Splash image
    context.splash_image = frappe.get_website_settings("splash_image") or None

    return context
