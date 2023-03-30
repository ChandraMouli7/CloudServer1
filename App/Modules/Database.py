def get_invoice_items(tabledata, invoice_no):
    product_index = 0
    price_index = 1
    total_index = 2

    for i in range(len(tabledata[0])):
        if tabledata[0][i] == "product_name":
            product_index = i
        if tabledata[0][i] == "price":
            price_index = i
        if tabledata[0][i] == "total":
            total_index = i

    items=[]
    for i in range(1,len(tabledata)):
        product_name = tabledata[i][product_index]
        price = tabledata[i][price_index]
        total = tabledata[i][total_index]

        if(float(price)==0.0):
            price = '1' + price
        if(float(total)==0.0):
            total = '1' + total

        quantity = str((float(total)/float(price)))

        item=[]
        item.append(invoice_no)
        item.append(product_name)
        item.append(price)
        item.append(total)
        item.append(quantity)

        items.append(item)
        
    return items