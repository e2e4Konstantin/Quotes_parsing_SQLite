from data_storage.re_patterns import identify_item, items_data

items = [(items_data[item].name, item, items_data[item].parent, items_data[item].rank) for item in items_data.keys()]
print(items)
