import frappe


def recycle_item_code(doc, method):
    """Save deleted item code to the recycling pool."""
    name = doc.name
    last_dash = name.rfind('-')

    if last_dash <= 0:
        return

    number_part = name[last_dash + 1:]
    if not number_part.isdigit():
        return

    prefix_part = name[:last_dash + 1]
    number = int(number_part)

    recycled = frappe.new_doc('Recycled Item Code')
    recycled.prefix = prefix_part
    recycled.number = number
    recycled.item_code = name
    recycled.insert(ignore_permissions=True)

    rule = frappe.db.get_value('Document Naming Rule',
        {'document_type': 'Item', 'prefix': prefix_part, 'disabled': 0},
        'name')

    if rule:
        last_item = frappe.db.sql("""
            SELECT name FROM `tabItem`
            WHERE name LIKE %s AND name != %s
            ORDER BY CAST(SUBSTRING_INDEX(name, '-', -1) AS UNSIGNED) DESC
            LIMIT 1
        """, (prefix_part + '%', doc.name))

        if last_item:
            max_number = int(last_item[0][0][last_item[0][0].rfind('-') + 1:])
        else:
            max_number = 0

        frappe.db.set_value('Document Naming Rule', rule, 'counter',
            max_number, update_modified=False)


def swap_recycled_code(doc, method):
    """After inserting an item, check the recycling pool for a smaller available code."""
    name = doc.name
    last_dash = name.rfind('-')

    if last_dash <= 0:
        return

    prefix = name[:last_dash + 1]
    number_part = name[last_dash + 1:]
    if not number_part.isdigit():
        return

    current_number = int(number_part)

    recycled = frappe.db.sql("""
        SELECT r.name, r.item_code FROM `tabRecycled Item Code` r
        WHERE r.prefix = %s AND r.number < %s
        AND r.item_code NOT IN (SELECT name FROM `tabItem`)
        ORDER BY r.number ASC
        LIMIT 1
    """, (prefix, current_number), as_dict=True)

    if recycled:
        old_name = doc.name
        new_name = recycled[0].item_code

        frappe.rename_doc('Item', old_name, new_name, force=True)
        frappe.db.delete('Recycled Item Code', recycled[0].name)

        rule = frappe.db.get_value('Document Naming Rule',
            {'document_type': 'Item', 'prefix': prefix, 'disabled': 0},
            'name')
        if rule:
            counter = frappe.db.get_value('Document Naming Rule', rule, 'counter') or 0
            frappe.db.set_value('Document Naming Rule', rule, 'counter',
                counter - 1, update_modified=False)
