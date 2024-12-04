from datetime import date
from flask import Flask, json, render_template, request
from flaskext.mysql import MySQL
import pyodbc

app = Flask(__name__)
mysql = MySQL()

#MySql Configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'Concerts'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/empregister')
def empregister():
    return render_template('empregister.html')

@app.route('/viewShow')
def viewshow():
    return render_template('viewshow.html')

@app.route('/buytickets')
def buytickets():
    return render_template('buytickets.html')

@app.route('/showTable', methods=['GET'])
def showTable():
    # Get the argument from the URL
    data_arg = request.args.get('data', default=1, type=int)
    
    # Connect to the database and fetch data
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('viewShow', (data_arg,))
    data_results = cursor.fetchall()
    
    # Pass both the argument and the results to the template
    return render_template("showtable.html", data_arg=data_arg, data_results=data_results)

@app.route('/performance', methods=['GET'])
def performance():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select * from Performance;')
    data = cursor.fetchall()
    return render_template("performance.html", data=data)

@app.route('/nextRevenue', methods = ['GET'])
def nextRevenue():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select * from RevenueNextShow;')
    data = cursor.fetchall()
    return render_template("nextRevenue.html", data=data)

@app.route('/inputMonth')
def inputMonth():
    return render_template("monthhours.html")

@app.route('/getHours', methods=['GET'])
def getHours():
    # Get the argument from the URL
    data_arg = request.args.get('data', default=1, type=int)
    
    # Connect to the database and fetch data
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('monthHours', (data_arg,))
    data_results = cursor.fetchall()
    
    # Pass both the argument and the results to the template
    return render_template("getHours.html", data_arg=data_arg, data_results=data_results)

@app.route('/api/empregister', methods=['POST'])
def empRegister():
    _fname = request.form['inputFname']
    _lname = request.form['inputLname']
    _depID = request.form['inputDep']
    _dob = request.form['inputDob']
    _wage = request.form['inputWage']

    # validate inputs
    if _fname and _lname and _depID and _dob and _wage:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('createEmployee', (_depID, _fname, _lname, _dob, _wage))
        data = cursor.fetchall()
        conn.commit()
        if conn:
            print("Connection established.")
        else:
            print("Failed to establish connection.")
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})
@app.route('/api/buyTickets', methods=['POST'])    
def buyTickets():
    _showID = request.form['showID']
    _seatNum = request.form['seatNum']
    _accountID = request.form['accountID']

    # validate inputs
    if _showID and _seatNum and _accountID:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('purchaseTicket', (_showID, _seatNum, _accountID))
        data = cursor.fetchall()
        conn.commit()
        if conn:
            print("Connection established.")
        else:
            print("Failed to establish connection.")
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


if __name__ == "__main__":
    app.run()

