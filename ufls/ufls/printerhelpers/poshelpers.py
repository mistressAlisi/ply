def center42(line):
    if(len(line) >= 42):
        return line[:41]
    i = int((42 - len(line)) / 2)
    ret = ''
    ret += ' ' * i
    return ret + line + ret

def receiptHeader():
    # 36 length for item
    # 3 for qty
    return "Item                                | Qty "

def receiptLineItem(item, qty):
    return (item[:35].ljust(35) + ' | ' + qty)

def receiptSignatureLine():
    return "I acknowledge I have recieved all items.\n\n\n\n__________________________________________"