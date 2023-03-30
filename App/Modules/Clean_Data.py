def clean_data(tabledata):

    name_mapping = {'product_name': ['item name', 'product','item','description','name','item description','pdt','product description','services','service',''], 
                'quantity': ['qty', 'quantity ordered','quantity','hours','hrs','no.','number','no','unit','units'], 
                'price': ['unit price', 'cost per item','price','cost','cost per unit','fees','rate','unit price'],
               'total':['amount','total','subtotal']}

    for i in range(len(tabledata[0])):
        tabledata[0][i] = tabledata[0][i].lower()
        if tabledata[0][i] in name_mapping['product_name']:
            tabledata[0][i] = 'product_name'
        elif tabledata[0][i] in name_mapping['quantity']:
            tabledata[0][i] = 'quantity'
        elif tabledata[0][i] in name_mapping['price']:
            tabledata[0][i] = 'price'
        elif tabledata[0][i] in name_mapping['total']:
            tabledata[0][i] = 'total'

    price=1
    total=2
    for i in range(len(tabledata[0])):
        if tabledata[0] == 'price':
            price=i
        elif tabledata[0] == 'total':
            total=i

    for i in range(1,len(tabledata)):
            tabledata[i][price] = tabledata[i][price].partition('/')[0]
            tabledata[i][price] = tabledata[i][price].replace("$", "")
            tabledata[i][price] = tabledata[i][price].replace("S", "")
            tabledata[i][price] = tabledata[i][price].replace("s", "")
            tabledata[i][price] = tabledata[i][price].replace("O", "0")
            tabledata[i][price] = tabledata[i][price].replace("o", "0")
            tabledata[i][price] = tabledata[i][price].replace("z", "2")
            tabledata[i][price] = tabledata[i][price].replace("Z", "2")
            tabledata[i][price] = tabledata[i][price].replace("l", "1")

            tabledata[i][total] = tabledata[i][total].replace("$", "")
            tabledata[i][total] = tabledata[i][total].replace("S", "")
            tabledata[i][total] = tabledata[i][total].replace("s", "")
            tabledata[i][total] = tabledata[i][total].replace("O", "0")
            tabledata[i][total] = tabledata[i][total].replace("o", "0")
            tabledata[i][total] = tabledata[i][total].replace("z", "2")
            tabledata[i][total] = tabledata[i][total].replace("Z", "2")
            tabledata[i][total] = tabledata[i][total].replace("l", "1")
    
    return tabledata