from flask import Flask,render_template,request,url_for,redirect,session
from data_create import data_Base,testData
from fetch_all import fetch,editData
from flask_bcrypt import Bcrypt
import os
app = Flask(__name__)
app.secret_key = "123abc"

root = os.path.dirname(os.path.abspath(__file__))


bcrypt = Bcrypt()




@app.route("/")
def register_page():
        return render_template("scene1.html")

@app.route("/",methods=["GET","POST"])
def register_contents():
    if request.method == "POST":
        DOB=request.form.get("DOB")
        Name=request.form.get("USERNAME")
        Password = request.form.get("PASSWORD")
        Email = request.form.get("EMAIL")
        Phone = request.form.get("PHONE")
        Address = request.form.get("ADDRESS")
        Confirm = request.form.get("CONFIRM")
        photo=request.files.get("IMAGE")
        saving1=request.form.get("SAVING")
        saving2=request.form.get("SALARY")
        deposits=request.form.getlist('DEPOSIT')
        photo1=photo.filename
        print(photo.mimetype)
        print(deposits)

        hashed_pw=bcrypt.generate_password_hash(Password).decode('utf-8')


        updated_DOB = DOB.replace("-", "")
        updated_username = updated_DOB + Name
        obj = testData(Name=Name, dob=DOB, eMail=Email, phone=Phone ,Password=hashed_pw ,addr=Address,upd=updated_username,photo=photo1,acc_type=f'{saving1,saving2}',deposits=f'{deposits}')

        target = os.path.join(root, 'static/images')
        if not os.path.isdir(target):
            os.mkdir(target)
        print(request.files.getlist("IMAGE"))

        photo.save(os.path.join(target,photo1))


        print(DOB,Name)
        if DOB!="" and Name != "" and Password != "" and Email != "" and Phone != "" and Address != "":
            print(Password,Confirm)
            if Password == Confirm:
                name=Name
                if photo.mimetype=="image/jpeg":
                    con = db.get_connection()
                    db.create_table(con)
                    db.insert_record(con, obj)
                    db.close_con(con)

                    return redirect(url_for("homePage",usr=name,photo=photo1))
                else:
                    alert="photo document type is invalid"
                    return render_template("scene1.html", alert=alert)
            else:
                alert="Password match failed"
                return render_template("scene1.html",alert=alert)
        else:
            alert="please fill all the credentials"
            return(render_template("scene1.html",alert=alert))


@app.route("/homePage <usr> <photo>",methods=["POST","GET"])
def homePage(usr,photo):
    print(usr)
    print(photo)

    return render_template("Homepage.html",usr=usr,photo=photo)

@app.route("/personal_Login",methods=["POST","GET"])
def login_page():
    if request.method=="POST":
        client=request.form.get("clientId")
        session['client']=client
        sec=request.form.get("sec_pass")

        conn = d_base.connection()
        x = d_base.select_all(conn,client,sec)
        d_base.conn_close(conn)
        print(x)
        if x==True:
            return redirect(url_for('details_Page'))
        else:
           alert="Ouch! wrong password"
           return render_template("loginpage.html",alert=alert)
    return render_template("loginPage.html")


@app.route("/Details_Page",methods=["GET","POST"])
def details_Page():
    client=session['client']
    conn = d_base.connection()
    x = d_base.type(conn,client)
    d_base.conn_close(conn)
    acc_type=[]
    for i in x:
        acc_type.append(i)
    print(acc_type)

    conn=d_base.connection()
    det=d_base.fetch_one(conn,client)
    d_base.conn_close(conn)
    lt=[]
    det_push={}
    for i in det:
        for j in i:
            lt.append(j)

    det_push["name"] = lt[0]
    det_push["D.O.B"] = lt[1]
    det_push["Email"] = lt[3]
    det_push["Phone"] = lt[4]
    det_push["address"] = lt[5]
    user = lt[6]
    session['account_t'] = lt[8]
    session['deposit'] = lt[9]
    print(lt[8])

    if request.method=="POST":
        name=request.form.get('name')
        dob = request.form.get('D.O.B')
        email = request.form.get('Email')
        phone = request.form.get('Phone')
        addr = request.form.get('address')



        conn = database.get_connection()
        obj = editData(Name=name, dob=dob, eMail=email, phone=phone, addr=addr)
        database.update(conn,user,obj)
        database.close_con(conn)

    print(acc_type)
    return render_template('details_page.html',det=det_push)

@app.route("/account_type",methods=['GET','POST'])
def type_acc():
    acc_type=session['account_t'].strip("()','").replace(" ","").split(",")



    if acc_type[0] != "None":
        return render_template('savings.html')
    elif acc_type[0] == "None":
        return render_template('salary.html')

@app.route("/savings",methods=['GET','POST'])
def savings():
    unpack_deposit = session['deposit'].strip('][').split(', ')
    print(unpack_deposit)
    lst_deposit=0
    for i in unpack_deposit:
        lst_deposit+=int(i.replace("'",''))
    print(lst_deposit)
    print(request.method)
    if request.method == 'POST':
        amount=request.form.get('Amount')
        n_val = request.form.get('n_val')
        year = request.form.get('year')
        principal,years=int(amount),int(year)
        percentage=int(n_val)/100
        total=principal*(1+percentage/4)**(4*years)
        val = "{:.2f}".format(total)
        return render_template('Fixed_Deposit.html', lst_deposit=lst_deposit,total=val,year=year)
    return render_template('Fixed_Deposit.html',lst_deposit=lst_deposit)


@app.route("/salary",methods=['GET','POST'])
def salary():
    if request.method == 'POST':
        salary=request.form.get('Salary')
        loan=request.form.get('Loan')
        year=request.form.get('Year')
        salary1=int(salary)*20
        year1=int(year)
        loan1=int(loan)
        print(salary1)
        print(year1)

        one = (loan1+(loan1*0.13))//12
        two = (loan1 + (loan1 * 0.13)) // 24
        three = (loan1 + (loan1 * 0.13)) // 36
        four = (loan1 + (loan1 * 0.13)) // 48
        five = (loan1 + (loan1 * 0.13)) // 60


        return render_template("Loan_page.html",salary1=salary1,one=one,two=two,three=three,four=four,five=five)
    return render_template("Loan_page.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))






if __name__ == '__main__':
    database=data_Base('create.db','bank')
    d_base=fetch('create.db','bank')
    db = data_Base('create.db', 'bank')
    app.run(debug=True, port=5055)
    
