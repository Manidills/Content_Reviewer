from flask import render_template, flash, redirect, request, url_for
from app import app
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

client = MongoClient(connect=False) 
db = client.base
user = {"nickname":"Tony"}

@app.route('/')
@app.route('/index')
def index():
    return render_template("home.html", user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("form.html")

    else:
        valid = request.form.get("Valid","No valid")
        info = {"Title":request.form["Title"],
        "Content": request.form["Content"],
        "Valid": valid}
        db.info.insert_one(info)
        flash('Created successfully')
        return redirect(url_for("list"))

@app.route('/information')
def list():
    return render_template("index.html",datos=db.info.find(),user=user)

@app.route('/detail/<id>')
def detail(id):
    detail = db.info.find_one({"_id": ObjectId(id)})
    return render_template("detail.html",dato=detail,user=user)

@app.route('/revalidate/<id>')
def revalidate(id):
    detail = db.info.find_one({"_id": ObjectId(id)})
    flash('Revalidate')
    if(detail["Valid"] == "Valid"):
        result = db.info.update_one({"_id": ObjectId(id)},{"$set": {"Valid": "No Valid"}})
    else:
        result = db.info.update_one({"_id": ObjectId(id)},{"$set": {"Valid": "Valid"}})
    return redirect(url_for("list"))

@app.route('/eliminate/<id>')
def eliminate(id):
    detail= db.info.delete_one({"_id": ObjectId(id)})
    flash('Eliminated')
    return redirect(url_for("list"))
