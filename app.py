from flask import Flask, render_template ,request,url_for, redirect,flash
from flask_sqlalchemy import SQLAlchemy  

app = Flask(__name__)

app.secret_key = "abc"  

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stud.db"
db = SQLAlchemy(app)

class student(db.Model):
    
    id = db.Column(db.String(10),primary_key = True)
    name = db.Column(db.String(20),nullable = False)
    branch = db.Column(db.String(100),nullable = False)

    def __init__(self,id,name,branch):
        self.id = id
        self.name = name
        self.branch = branch

@app.route("/")
def Add():
    return render_template("Add.html")

@app.route("/success",methods = ["GET","POST"])
def success():
    if request.method == "POST":
        if request.form['sid'] != "" and request.form['sname'] != "" and  request.form['sbranch'] != "" : 
            if db.session.query(db.exists().where(student.id==request.form['sid'])).scalar() == False :
                add_details = student(request.form["sid"],request.form["sname"],request.form["sbranch"])
                db.session.add(add_details)
                db.session.commit()
                return render_template("success.html")
            else:
                flash("ID Exists")
                return render_template("Add.html")
        else:
            flash("Enter all details")
            return render_template("Add.html")

@app.route("/view",methods=["POST","GET"])
def view():
    all_details = student.query.all()
    return render_template("view.html",all_detail=all_details)

@app.route("/delete",methods=["POST","GET"])
def delete():
    all_details = student.query.all()
    return render_template("delete.html",all_detail=all_details)

@app.route("/delsuc/<sid>",methods=["POST","GET"])
def delsuc(sid):
    if request.method=="POST" and request.form["sid"] !="":
        if db.session.query(db.exists().where(student.id==request.form['sid'])).scalar() == True :
            id = request.form['sid']
            rno = student.query.get(id)
            db.session.delete(rno)
            db.session.commit()
            flash("Successfully deleted")
            return redirect("/delete")
        else:
            flash("ID Doesn't Exist, Enter Valid ID")
            return redirect("/delete")
    else:
        flash("Enter Id")
        all_details = student.query.all()
        return render_template("delete.html",all_detail=all_details)

@app.route("/update",methods=["POST","GET"])
def update():
    all_details = student.query.all()
    return render_template("update.html",all_detail=all_details)

@app.route("/updsuc/<uid>",methods=["POST","GET"])
def updsuc(uid):
    if request.method=="POST" and request.form["uid"] !="" and request.form['uname'] != "" and  request.form['ubra'] != "":
        if db.session.query(db.exists().where(student.id==request.form['uid'])).scalar() == True :
            id = request.form['uid']
            rno = student.query.get(id)
            db.session.delete(rno)
            db.session.commit()
            add_details = student(request.form["uid"],request.form["uname"],request.form["ubra"])
            db.session.add(add_details)
            db.session.commit()
            flash("Successfully Updated")
            return redirect("/update")
        else:
            flash("ID Doesn't Exist, Enter Valid ID")
            return redirect("/update")
    else:
        flash("Enter Details")
        all_details = student.query.all()
        return render_template("update.html",all_detail=all_details)

if __name__ == "__main__":
    app.run(debug = True)