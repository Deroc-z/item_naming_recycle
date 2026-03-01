# Item Naming Recycle Plugin

A Frappe/ERPNext plugin that enables automatic recycling of item codes when items are deleted.

**[中文文档](README_zh.md)**

## Features

- Automatically saves deleted item codes to a recycling pool
- Reuses recycled codes when creating new items (prioritizes smallest available number)
- Works seamlessly with Document Naming Rules
- Zero configuration required after installation

## Installation

```bash
bench get-app item_naming_recycle https://github.com/Deroc-z/item_naming_recycle.git
bench --site your-site install-app item_naming_recycle
bench migrate
bench restart
```

## Prerequisites

Before using this plugin, you need to configure Document Naming Rules for your Item groups:

1. Go to **Stock Settings** and set **Item Naming By** to **Naming Series**
2. Go to **Document Naming Rule** and create rules for each Item Group with the desired prefix

Example: Document Type: Item, Prefix: `YL-`, Prefix Digits: 5, Condition: item_group = Raw Material

## How It Works

- **Delete** — When an item is deleted, its code is stored in the Recycled Item Code pool
- **Create** — When a new item is created, the system checks for available recycled codes with a smaller number
- **Swap** — If found, the new item is renamed to the recycled code and the naming counter is adjusted

## Requirements

- Frappe Framework >= 16.0.0
- ERPNext >= 16.0.0

## License

MIT
