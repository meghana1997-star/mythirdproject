from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

connection =""
cur = ""

def connectToDB():
    global connection,cur
    connection = pymysql.connect(host="localhost",user="root", password="",database="lms")
    cur = connection.cursor()
    print("Database Connected")

def disconnectDB():
    cur.close()
    connection.close()
    print("Database Disconnected")

def insertbook( bid,title, author, status):
    try:
        insert_query ="INSERT into books(bid,title,author,status) values(%s, %s, %s, %s);"
        cur.execute(insert_query, ( bid, title, author, status))
        connection.commit()
        return True
    except:
        return False

def getonebook(bid):
    select_query = "SELECT * FROM books WHERE bid = %s;"  
    cur.execute(select_query, (bid,))
    data = cur.fetchone()
    return data      

def updatebook(bid, title, author, status):
    try:
        update_query ="UPDATE books SET title=%s, author=%s, status=%s WHERE bid=%s;"
        cur.execute(update_query, (bid,title, author, status))
        connection.commit()
        return True
    except:
        return False

def deletebook(bid):
    try:
        delete_query = "DELETE FROM books WHERE bid=%s;"
        cur.execute(delete_query, (bid, ))
        connection.commit()
        return True
    except:
        return False

def getallbooks():
    select_query = "SELECT * FROM `books`;"

    cur.execute(select_query)
    data = cur.fetchall()

   # print(data)
    return data


@app.route("/", methods=['GET', 'POST'])
def index():
    html_data = {}
    connectToDB()
        
    books = getallbooks()
    html_data['book_list'] = books
    disconnectDB()
    return render_template('index.html', data=html_data)

@app.route("/edit/", methods=['GET', 'POST'])
def update_book():
    connectToDB()
    if request.method == 'GET':
        bid = request.args.get('bd',type=int, default=1)
        data = getonebook(bid)
       # disconnectDB()
        return render_template('update.html', books=data)
    if request.method == "POST":
        form_data = request.form
        
        bid = form_data.get("txtBid")
        title = form_data.get("txtTitle")
        author = form_data.get("txtAuthor")
        status = form_data.get("txtStatus")
        html_data = {}
        if updatebook(bid, title, author, status):
            html_data['success'] = 'Record updated successfully'
        else:
            html_data['error'] = 'Unable to update record'    
        html_data['book_list'] = getallbooks()
        #disconnectDB()
        return render_template('index.html', data=html_data)

    return "Update form"


@app.route("/delete/", methods=['GET'])
def delete_book():
    connectToDB()
    html_data ={}
    bid = request.args.get('bd',type=int, default=1)
    if deletebook(bid):
            html_data['success'] = 'Record deleted successfully'
    else:
            html_data['error'] = 'Unable to delete record' 
    html_data['book_list'] = getallbooks()
    disconnectDB()
    return render_template('index.html', data=html_data)

@app.route("/insert/", methods=['GET', 'POST'])
def insert_book():
    if request.method == 'GET':
        return render_template('insert.html')
    if request.method == "POST":
        connectToDB()
        html_data = {}
        form_data = request.form
        #print(form_data)
        bid = form_data.get("txtBid")
        title = form_data.get("txtTitle")
        author = form_data.get("txtAuthor")
        status = form_data.get("txtStatus")
        if insertbook(bid, title, author, status):
            html_data['success'] = " book's record stored succesfully."
        else:
            html_data['error'] = "couldn't  save data,please try again!"        
        html_data['book_list'] = getallbooks()
        disconnectDB()
        return render_template('index.html', data=html_data)
if __name__ == '__main__':
    app.run()