# Item Naming Recycle Plugin

A Frappe/ERPNext plugin that enables automatic recycling of item codes when items are deleted.

一个用于 Frappe/ERPNext 的插件，实现物料编码删除后自动回收复用。

---

## Features

- Automatically saves deleted item codes to a recycling pool
- Reuses recycled codes when creating new items (prioritizes smallest available number)
- Works seamlessly with Document Naming Rules
- Zero configuration required after installation

## 功能特性

- 物料删除时自动将编码保存到回收池
- 创建新物料时优先复用最小的可用回收编码
- 与文档命名规则（Document Naming Rule）无缝协作
- 安装后零配置即可使用

---

## Installation

```bash
bench get-app item_naming_recycle https://github.com/yourusername/item_naming_recycle.git
bench --site your-site install-app item_naming_recycle
bench migrate
bench restart
```

## 安装方法

```bash
bench get-app item_naming_recycle https://github.com/yourusername/item_naming_recycle.git
bench --site 你的站点名 install-app item_naming_recycle
bench migrate
bench restart
```

---

## Prerequisites

Before using this plugin, you need to configure Document Naming Rules for your Item groups:

1. Go to **Stock Settings** and set **Item Naming By** to **Naming Series**
2. Go to **Document Naming Rule** and create rules for each Item Group with the desired prefix

Example: Document Type: Item, Prefix: `YL-`, Prefix Digits: 5, Condition: item_group = Raw Material

## 使用前提

使用此插件前，需要先为物料分组配置文档命名规则：

1. 进入 **库存设置（Stock Settings）**，将 **Item Naming By** 设置为 **Naming Series**
2. 进入 **文档命名规则（Document Naming Rule）**，为每个物料分组创建对应前缀的规则

示例：文档类型：Item，前缀：`YL-`，前缀位数：5，条件：item_group = 原材料

---

## How It Works

- **Delete** — When an item is deleted, its code is stored in the Recycled Item Code pool
- **Create** — When a new item is created, the system checks for available recycled codes with a smaller number
- **Swap** — If found, the new item is renamed to the recycled code and the naming counter is adjusted

## 工作原理

- **删除** — 物料删除时，编码被保存到回收池（Recycled Item Code）
- **创建** — 创建新物料时，系统检查回收池中是否存在编号更小的可用编码
- **交换** — 如果找到，将新物料重命名为回收编码，并自动调整命名计数器

---

## Requirements

- Frappe Framework >= 16.0.0
- ERPNext >= 16.0.0

## License

MIT
