def table_data(table):
    flag = 0
    tabledata = []
    row=[]
    header = table[0][0][0][1]
    row.append(table[0][1])
    isqty_present = False

    flagger = ['qty', 'quantity ordered','quantity','hours','hrs','no.','number','no','unit','units','no_']
    if table[0][1].lower() in flagger:
        col_to_remove=0
        isqty_present=True

    for i in table:
        if flag==0:
            flag=1
            continue

        if flag==1:
            if(abs(i[0][0][1] - header) < 20):
                row.append(i[1])
                if i[1].lower() in flagger:
                    col_to_remove = len(row)-1
                    isqty_present=True
            else:
                tabledata.append(row)
                row=[]
                header = i[0][0][1]
                row.append(i[1])

    tabledata.append(row)

    if isqty_present == True:
        expectedlen = len(tabledata[0])-1
        for i in tabledata:
            if(len(i)>expectedlen):
                del i[col_to_remove]
    
    return tabledata