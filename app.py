from flask import Flask, render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors



app = Flask(__name__)


app.secret_key = 'your secrete key'


app.config['MYSQL_HOST'] = 'localhost' #hostname
app.config['MYSQL_USER'] = 'root'      #username
app.config['MYSQL_PASSWORD'] = ''      #password
#in my case password is null so i am keeping empty
app.config['MYSQL_DB'] = 'practice'    #database name

mysql = MySQL(app)

#------------------------------------- welcome page -----------------------------------

@app.route("/")
def home():
    #return render_template("welcome.html",username=session['username'])     I changed this
    return render_template("welcome.html")

#------------------------------------ Admin Login Page ------------------------------------

@app.route("/Admin_login", methods=['GET','POST'])
def Admin_login() :
        print('hi')
        error = None
        # print(f'value of request method #{request.method} #{request.form}')
        # a='username' in request.form
        # b='password' in request.form
        # print(f'value of request method #{a} #{b}')
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:   
            # print("Hello this my first project")
            if request.form['email'] != 'daniel123@gmail.com' or \
                request.form['password'] != 'dan123': 
                # print('inside 2 if')
                error = 'Invalid credentials'
                flash('Invalid Credentials')
            else:
                # print('inside 2 else')
                flash('You have logged in successfully!!')
                return redirect(url_for('admin_dashboard'))

        return render_template("Admin_login.html",error=error) 

@app.route('/Admin_logout')
def AdminLogout() :
    log1 = ''
    log1 = 'You have logged out successfully!!'
    return render_template('AdminLogin.html', log1=log1)   

#-------------------------------- Customer Login ----------------------------------------

@app.route("/Register", methods=['GET','POST'])
def Register():
    error = None
    if request.method == 'POST' and 'Name' in request.form and 'phNo' in request.form and 'Address' in request.form and 'pswd' in request.form:
        Phonenumber = request.form['phNo']
        Name = request.form['Name']
        Address = request.form['Address']
        pswd = request.form['pswd']
        #creating variable for connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #executing query to insert new data into MySQL
        cursor.execute('INSERT INTO CUSTOMER VALUES(% s, % s , % s, % s)',(Name,Phonenumber,Address,pswd))
        mysql.connection.commit()
        #displaying message
        flash('You have successfully Regsitered!')
        return redirect(url_for('cust_login')) #add a page here
    else :
        error = 'Please fill out the form!!'
        return render_template("register.html", error=error)


@app.route('/cust_login', methods = ['GET','POST'])
def cust_login():
    error = None
    if request.method == 'POST' and 'Name' in request.form and 'pswd' in request.form and 'mobile_no' in request.form:
        cust_name=request.form['Name']
        pswd = request.form['pswd']
        mobile_no = request.form['mobile_no']
        #creating variable for connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #executing query to insert new data into MySQL
        cursor.execute('SELECT * FROM CUSTOMER WHERE CUST_NAME=%s AND MOBILE_NO = % s AND PSWD=%s',(cust_name,mobile_no,pswd))
        account = cursor.fetchone()
        if account :
            flash('You have logged in successfully!!')
            return redirect(url_for('menu'))
        else:
            error='invalid credentials'
            return render_template('cust_login.html', error=error)
            
    elif request.method =='POST' :
        error = 'Please fill out the details!!'

    return render_template('cust_login.html', error=error)

        #displaying message
        # flash('You have successfully logged in !')
        # return redirect(url_for('menu'))
#    else :
#        error = 'Invalid Crendentials!!'
#     return render_template("cust_login.html", error=error)

@app.route('/Logout')
def Logout() :
    log2 = ''
    log2= 'You have logged out successfully!!'
    return render_template('cust_login.html', log2=log2)

#-------------------------------- Admin Dashboard ---------------------------------------

@app.route("/AdminDashboard")
def admin_dashboard():
    employees = 0
    orders = 0
    customers = 0
    # creating a variable connection
    #---------------*****displays on cards******------------
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT COUNT(DISTINCT EMP_ID) AS Employees FROM EMPLOYEE')        # gives the count of employee
    mysql.connection.commit()
    result1=cursor.fetchone()
    employees = result1['Employees']
    #---------------*****displays on cards******------------
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT COUNT(ORDER_NO) AS Orders FROM ORDERS')                     # gives the count of orders
    mysql.connection.commit()
    result2=cursor.fetchone()
    orders = result2['Orders']
    #---------------*****displays on cards******------------
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT COUNT(MOBILE_NO) AS Customers FROM CUSTOMER')               # gives the count of customer
    mysql.connection.commit()
    result3 = cursor.fetchone()
    customers = result3['Customers']
    #----------------*****displays on cards******------------
    return render_template("admin_dashboard.html",employees=employees,orders=orders,customers=customers)  

#-----------------******** side bars ********------------------
@app.route("/customers")
def customers():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT CUST_NAME,MOBILE_NO,ADDRESS FROM CUSTOMER')                    # fetches the attributes
    mysql.connection.commit()
    customers = cursor.fetchall()
    return render_template("index.html",customers=customers)

@app.route("/orders")
def orders():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT ORDER_NO,ITEM_NAME,ITEM_NO,MOB_NO,QUANTITY FROM ORDERS')       # fetches the attributes
    mysql.connection.commit()
    orders = cursor.fetchall()

    return render_template("orders.html",orders=orders)

@app.route("/employee",methods = ['GET','POST'])
def employees():
    error = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST' and 'emp_id' in request.form:
        emp_id= request.form['emp_id']
        cursor.execute('SELECT * FROM EMPLOYEE WHERE EMP_ID = % s',(emp_id,))
        result = cursor.fetchone()
        if  result :
            cursor.execute('DELETE FROM EMPLOYEE WHERE EMP_ID = % s',(emp_id,))
            mysql.connection.commit()
        else :
            error = 'Employee doesn\'t exists!!'
    cursor.execute('SELECT EMP_NAME,EMP_ID,DESIGNATION,GENDER,MOB_NO FROM EMPLOYEE')       # fetches the attributes
    mysql.connection.commit()
    employees = cursor.fetchall()
    return render_template("employee.html",employees=employees, error=error)

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")
#----------------------------*********************************------------------------------

#----------------------------*************Menu****************------------------------------
@app.route("/menu")
def menu():
    return render_template('menu.html')     

@app.route("/coffeemenu")
def coffeemenu():
    return render_template("coffeemenu.html")

@app.route("/pizzamenu")
def pizzamenu():
    return render_template("pizzamenu.html")

@app.route("/burgers")
def burgers():
    return render_template("burgers.html")

@app.route("/Sandwiches")
def Sandwiches():
    return render_template("Sandwiches.html")

@app.route("/shorteates")
def shorteates():
    return render_template("shorteates.html")

@app.route("/Beverages")
def Beverages():
    return render_template("Beverages.html")

@app.route("/reviews")
def reviews():
    return render_template("reviews.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/item", methods=['GET','POST'])
def item():
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        return redirect(url_for('receipt'))
    #     item1 = request.form.getlist('items')
    #     item2 = request.form.getlist('items')
    #     item3 = request.form.getlist('items')
    #     item4 = request.form.getlist('items')
    #     item5 = request.form.getlist('items')
    #     item6 = request.form.getlist('items')
    #     item7 = request.form.getlist('items')
    #     item8 = request.form.getlist('items')
    #     qty_item1 = request.form['item1']
    #     qty_item2 = request.form['item2']
    #     qty_item3 = request.form['item3']
    #     qty_item4 = request.form['item4']
    #     qty_item5 = request.form['item5']
    #     qty_item6 = request.form['item6']
    #     qty_item7 = request.form['item7']
    #     qty_item8 = request.form['item8']
    #     return render_template("item.html")

    return render_template("item.html")


@app.route("/receipt")
def receipt():
    return render_template("receipt.html")

if __name__ == "__main__":
    app.run(debug=True)

