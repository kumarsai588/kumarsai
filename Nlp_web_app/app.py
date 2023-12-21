from flask import Flask,render_template,request,redirect
from db import Database

app=Flask(__name__)
dbo=Database()

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/performRegistration",methods=['post'])
def performRegistration():
    name=request.form.get("user-name")
    password=request.form.get("user-password")
    email=request.form.get("user-email")
    phno=request.form.get("user-phno")
    response=dbo.insert(name,password,email,phno)
    if response==1:
        return render_template("login.html",message="Registration successful. kindly login to proceed!!!")
    else:
        return render_template("register.html",message="Email Already Exists!!!")
    
@app.route("/performLogin",methods=['post'])
def performLogin():
    email=request.form.get('user-email')
    password=request.form.get('user-password')
    response=dbo.search(email,password)
    if response==1:
        return redirect("profile.html")
    else:
        return render_template("login.html",message="Invalid credentials!!!")
    
@app.route("/ner")
def ner():
    return render_template("ner.html")

@app.route("/performNer",methods=['post'])
def performNer():
    txt=request.form.get('user-text')
    
    
app.run(debug=True)