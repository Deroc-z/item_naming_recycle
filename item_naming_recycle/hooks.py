app_name = "item_naming_recycle"
app_title = "Item Naming Recycle"
app_publisher = "Your Name"
app_description = "Item naming with automatic code recycling for ERPNext"
app_email = "your@email.com"
app_license = "MIT"

doc_events = {
    "Item": {
        "on_trash": "item_naming_recycle.api.recycle_item_code",
        "after_insert": "item_naming_recycle.api.swap_recycled_code"
    }
}
