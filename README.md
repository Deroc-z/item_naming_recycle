# Item Naming Recycle Plugin

A Frappe/ERPNext plugin that enables automatic recycling of item codes when items are deleted.

## 功能特性 / Features

- Automatically saves deleted item codes to a recycling pool  
  自动将删除的物料编码保存到回收池中
- Reuses recycled codes when creating new items (prioritizes smallest available number)  
  创建新物料时优先复用最小的回收编码
- Works seamlessly with Document Naming Rules  
  与文档命名规则无缝协作
- Zero configuration required after installation  
  安装后零配置即可使用

## 安装方法 / Installation

```bash
bench get-app item_naming_recycle https://github.com/yourusername/item_naming_recycle.git
bench --site your-site install-app item_naming_recycle
bench migrate
bench restart
```

## 使用前提 / Prerequisites

Before using this plugin, you need to configure Document Naming Rules for your Item groups:

使用此插件前，您需要为物料分组配置文档命名规则：

1. Go to **Stock Settings** and set **Item Naming By** to **Naming Series**  
   进入 **库存设置**，将 **Item Naming By** 设置为 **Naming Series**

2. Go to **Document Naming Rule** and create rules for each Item Group with the desired prefix  
   进入 **文档命名规则**，为每个物料分组创建带有期望前缀的规则

Example:  
示例：
- Document Type: Item, Prefix: `YL-`, Prefix Digits: 5, Condition: item_group = Raw Material  
  文档类型：Item，前缀：`YL-`，前缀位数：5，条件：item_group = 原材料

## 工作原理 / How It Works

- **Delete**: When an item is deleted, its code is stored in the `Recycled Item Code` pool  
  **删除**：物料删除时，其编码会被保存到 `Recycled Item Code` 回收池中
- **Create**: When a new item is created, the system checks for available recycled codes with a smaller number  
  **创建**：创建新物料时，系统会检查是否存在编号更小的可复用编码
- **Swap**: If found, the new item is renamed to the recycled code and the naming counter is adjusted  
  **交换**：如果找到，则将新物料重命名为回收编码并调整命名计数器

## 系统要求 / Requirements

- Frappe Framework >= 16.0.0
- ERPNext >= 16.0.0

## 许可证 / License

MIT
