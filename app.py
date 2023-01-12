from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask_mysqldb import MySQL
import mysql
import mysql.connector
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import mysql
import json
import more_itertools as mt

app = Flask(__name__)

db = MySQL(app);

@app.route('/enterPO', methods=['GET','POST'])
def enterPO():
    return render_template("enterPO.html")

@app.route('/searchPO', methods=['GET','POST'])
def fetchDetails():
    #print("Hello")
    po_number=request.args.get("po_number")
    conn = mysql.connector.connect(user='root', password='BTWin123!', host='127.0.0.1', database='world')
    cursor = conn.cursor()

    query="""SELECT sender, DESTINATION, Currency, Company_Name_and_Address, PO_Date, Buyer_Name, Vendor_Name_and_Address, Important_Instructions, Payment_Details FROM po_master WHERE PO_Number=(%s)"""
    cursor.execute(query,(po_number,))
    result=cursor.fetchone()
    cursor.close()
    #print(len(result))
    
    From=result[0]
    destination=result[1]
    currency=result[2]
    companyNameAndAddress=result[3]
    PONumber=po_number

    PODate=result[4]
    #converting from datetime to string.
    PODate=PODate.strftime('%Y/%m/%d')
    #print(PODate)
    buyerName=result[5]
    VendorNameAndAddress=result[6]
    importantInstructions=result[7]
    paymentDetailing=result[8]
    
    return From + ',' + destination + ',' + currency + ',' + companyNameAndAddress + ',' + PONumber + ',' + PODate + ',' + buyerName + ',' + VendorNameAndAddress + ',' + importantInstructions + ',' + paymentDetailing

def executeQuery(query,values):
	conn = mysql.connector.connect(user='root', password='BTWin123!', host='127.0.0.1', database='world')
	cursor = conn.cursor()
	cursor.execute(query, values)
	conn.commit()
	cursor.close()

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'passwd':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('editOrNew'))
    return render_template('login.html', error=error)

@app.route('/editOrNew')
def editOrNew():
    return render_template('editOrNew.html')

@app.route('/purchaseOrder', methods=['GET','POST'])
def purchaseOrder():
    return render_template('purchaseOrder.html')

@app.route('/editOrder',methods=['GET','POST'])
def editOrder():
    return render_template("editOrder.html")

@app.route('/insertOrder', methods=['GET','POST'])
def insertOrder():
    #print("hello")
    From=request.args.get("from")
    destination=request.args.get("destination")
    currency=request.args.get("currency")
    companyNameAndAddress=request.args.get("companyDetails")
    PONumber=request.args.get("PONumber")
    PODate=request.args.get("PODate")
    buyerName=request.args.get("buyerName")
    VendorNameAndAddress=request.args.get("vendorDetails")
    importantInstructions=request.args.get("impInstructions")
    paymentDetailing=request.args.get("paymentDetails")

    conn = mysql.connector.connect(user='root', password='BTWin123!', host='127.0.0.1', database='world')
    cursor = conn.cursor()
    query1="SELECT COUNT(PO_Number) FROM po_master WHERE PO_Number=%s"
    values1=[PONumber,]
    cursor.execute(query1,values1)
    result=cursor.fetchone()
    cnt=result[0]
    print("the number of PO number:")
    print(cnt)
    if(cnt==0):
        values=[From, destination, currency, companyNameAndAddress, PONumber, PODate, buyerName, VendorNameAndAddress, importantInstructions, paymentDetailing]
        query="INSERT INTO po_master(sender, DESTINATION, Currency, Company_Name_and_Address, PO_Number, PO_Date, Buyer_Name, Vendor_Name_and_Address, Important_Instructions, Payment_Details) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        return "I"
    else:
        cursor = conn.cursor()
        values=[From, destination, currency, companyNameAndAddress, PODate, buyerName, VendorNameAndAddress, importantInstructions, paymentDetailing, PONumber]
        query="""UPDATE po_master SET sender=(%s), destination=(%s), Currency=(%s), Company_Name_and_Address=(%s), PO_Date=(%s), Buyer_Name=(%s), Vendor_Name_and_Address=(%s), Important_Instructions=(%s), Payment_Details=(%s) where PO_Number=(%s)"""
        cursor.execute(query,values)
        conn.commit()
        cursor.close()
        return "I"

def insertItem():
    print("Entered insertItem()")
    data=json.loads(request.data)
    print("Update method called")
    length=len(data)
    sep=" !$ "
    itemDetails=[]
    for item in range(length):
        itemDetails.append(data[item]['qty']+sep+data[item]['unit']+sep+data[item]['description']+sep+data[item]['deliveryDate']+sep+data[item]['UnitPrice']+sep+data[item]['total'])
    print(itemDetails)
    query="INSERT INTO po_master(sender, DESTINATION, Currency, Company_Name_and_Address, PO_Number, PO_Date, Buyer_Name, Vendor_Name_and_Address, Important_Instructions, Payment_Details) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for i in range(length):
        executeQuery()
    
    return "I"
        
@app.route('/printReport')
def printReport():
    From=request.args.get("from")
    destination=request.args.get("destination")
    currency=request.args.get("currency")
    companyNameAndAddress=request.args.get("companyDetails")
    PONumber=request.args.get("PONumber")
    PODate=request.args.get("PODate")
    buyerName=request.args.get("buyerName")
    VendorNameAndAddress=request.args.get("vendorDetails")
    importantInstructions=request.args.get("impInstructions")
    paymentDetailing=request.args.get("paymentDetails")
    
    values=[From, destination, currency, companyNameAndAddress, PONumber, PODate, buyerName, VendorNameAndAddress, importantInstructions, paymentDetailing]

    return render_template("purchaseOrder.html", input=values)

@app.route('/poNumber')
def poNumber():
    poNum=request.args.get("poNum")
    conn = mysql.connector.connect(user='root', password='BTWin123!', host='127.0.0.1', database='world')
    cursor = conn.cursor()
    query="SELECT COUNT(PO_Number) FROM po_master WHERE PO_Number=%s"
    values=[poNum,]
    cursor.execute(query,values)
    result=cursor.fetchone()
    cursor.close()
    cnt=result[0]
    result=str(cnt)
    return result

@app.route('/itemDetailsInsert', methods=['GET','POST'])
def itemDetailsInsert():
    data=json.loads(request.data)
    print(type(data))
    print(data[0])
    return "I"

@app.route('/itemDetailsUpdate', methods=['GET','POST'])
def itemDetailsUpdate():
    data=json.loads(request.data)
    print(data)
    poNum=data[0]['po_num']
    print("PO NUMBER IN INSERTDETAILSUPDATE IS",poNum)
    conn = mysql.connector.connect(user='root', password='BTWin123!', host='127.0.0.1', database='world')
    cursor = conn.cursor()
    query1="SELECT COUNT(PO_Number) FROM po_master WHERE PO_Number=%s"
    values1=[poNum,]
    cursor.execute(query1,values1)
    result=cursor.fetchone()
    cnt=result[0]
    print("the number of PO number:")
    print("THE COUNT OF PONUMBER FOR ITEM DETAILS UPDATE IS:",cnt)
    #insert op
    if(cnt==0):
        length=len(data)
        sep=" !$ "
        itemDetails=[]
        for item in range(length):
            itemDetails.append(data[item]['po_num']+sep+data[item]['qty']+sep+data[item]['unit']+sep+data[item]['description']+sep+data[item]['deliveryDate']+sep+data[item]['UnitPrice']+sep+data[item]['total'])
        arr=[]
        print(itemDetails)
        conn = mysql.connector.connect(user='root', password='BTWin123!', host='127.0.0.1', database='world')
        cursor = conn.cursor()
        query="INSERT INTO po_item(PONumber, item_qty, item_number, item_description, delivery_date, unit_price, item_total) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        print(query)
        for i in range(length):
            arr=itemDetails[i].split(sep)
            print(arr)
            cursor.execute(query, arr)
            conn.commit()
        cursor.close()
        return render_template("purchaseOrder.html")

    #update op
    else:
        print("UPDATING STUFF")
        cursor = conn.cursor()
        query1="""DELETE FROM po_item WHERE PONumber=(%s)"""
        values1=[poNum,]
        cursor.execute(query1,values1)
        conn.commit()
        print("UPDATING STUFF1")
        length=len(data)
        sep=" !$ "
        itemDetails=[]
        for item in range(length):
            itemDetails.append(data[item]['po_num']+sep+data[item]['qty']+sep+data[item]['unit']+sep+data[item]['description']+sep+data[item]['deliveryDate']+sep+data[item]['UnitPrice']+sep+data[item]['total'])
        arr=[]
        print(itemDetails)
        conn = mysql.connector.connect(user='root', password='BTWin123!', host='127.0.0.1', database='world')
        cursor = conn.cursor()
        query="INSERT INTO po_item(PONumber, item_qty, item_number, item_description, delivery_date, unit_price, item_total) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        print(query)
        for i in range(length):
            arr=itemDetails[i].split(sep)
            print(arr)
            cursor.execute(query, arr)
            conn.commit()
        cursor.close()
        return render_template("purchaseOrder.html")

@app.route('/fetchItemDetails', methods=['GET','POST'])
def fetchItemDetails():
    poNumber=request.args.get("po_number")
    conn = mysql.connector.connect(user='root', password='BTWin123!', host='127.0.0.1', database='world')
    cursor = conn.cursor()
    query="""SELECT item_qty, item_number, item_description, delivery_date, unit_price, item_total FROM po_item WHERE PONumber=(%s)"""
    values=[poNumber,]
    cursor.execute(query,values)
    result=cursor.fetchall()
    tot=len(result)
    sep=" !$ "
    newArr="{\"podata\":["
    
    for i in range(tot):
        if(i==0):
            newArr=newArr+"{\"item_qty\":" + "\"" + str(result[i][0]) + "\"" + ","
        else:
            newArr=newArr+",{\"item_qty\":" + "\"" + str(result[i][0]) + "\"" + ","
        newArr=newArr+"\"item_number\":" + "\"" + str(result[i][1]) + "\"" + ","
        newArr=newArr+"\"item_description\":" + "\"" + str(result[i][2]) + "\"" + ","
        newArr=newArr+"\"delivery_date\":" + "\"" + str(result[i][3]) + "\"" + ","
        newArr=newArr+"\"unit_price\":" + "\"" + str(result[i][4]) + "\"" + ","
        
        newArr=newArr+"\"item_total\":" +  str(result[i][5]) + "}"
    newArr=newArr+"]}"   
    return newArr

if __name__ == '__main__':
    app.run(debug=True)