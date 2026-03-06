import frappe
import re


def split_code(name):
    """Split item code into prefix and number, supporting both 'YL-00001' and 'YL00001' formats."""
    m = re.match(r'^(.*?)(\d+)$', name)
    if not m:
        return None, None
    prefix = m.group(1)
    number_str = m.group(2)
    if not prefix:
        return None, None
    return prefix, int(number_str)


def recycle_item_code(doc, method):
    """Save deleted item code to the recycling pool."""
    prefix, number = split_code(doc.name)
    if prefix is None:
        return

    recycled = frappe.new_doc('Recycled Item Code')
    recycled.prefix = prefix
    recycled.number = number
    recycled.item_code = doc.name
    recycled.insert(ignore_permissions=True)

    rule = frappe.db.get_value('Document Naming Rule',
        {'document_type': 'Item', 'prefix': prefix, 'disabled': 0},
        'name')

    if rule:
        last_item = frappe.db.sql("""
            SELECT name FROM `tabItem`
            WHERE name LIKE %s AND name != %s
            ORDER BY name DESC
            LIMIT 1
        """, (prefix + '%', doc.name))

        if last_item:
            _, max_number = split_code(last_item[0][0])
            max_number = max_number or 0
        else:
            max_number = 0

        frappe.db.set_value('Document Naming Rule', rule, 'counter',
            max_number, update_modified=False)


def swap_recycled_code(doc, method):
    """After inserting an item, check the recycling pool for a smaller available code."""
    prefix, current_number = split_code(doc.name)
    if prefix is None:
        return

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
