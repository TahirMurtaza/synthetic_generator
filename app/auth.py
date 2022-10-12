from flask import Blueprint, render_template, redirect, url_for, request,jsonify,make_response
from flask_login import login_user
from flask.helpers import flash
from flask_login import login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Rights, User
from main import db


auth = Blueprint('auth', __name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/login", methods=["POST"])
def login_post():
    # login code goes here
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('main.index'))

@auth.route('/users', methods=['GET'])
def get_users():
    userlist = []
    users = User.query.all() 
    for user in users:
        userlist.append(user.to_dict())
    return make_response(jsonify(userlist), 200)

@auth.route('/rights', methods=['GET'])
def get_rights():
    rightList = []
    rights = Rights.query.all() 
    for right in rights:
        rightList.append(right.to_dict())
    return make_response(jsonify(rightList), 200)

@auth.route('/createuser', methods=['POST'])
def create_user():
    # code to validate and add user to database goes here
    username = request.form.get('username')
    password = request.form.get('password')
    rights = request.form.get('rights')
    user = User.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found then send a message
        resp = {"error":"Username already exist."}

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username, rights=rights, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    resp = {"message":"User created Successfully!"}
    return make_response(jsonify(resp), 200)




@auth.route('/updateuser/<id>', methods=['POST'])
def update_user(id):
    #code to validate and add user to database goes here
    username = request.form.get('username')
    password = request.form.get('password')
    rights = request.form.get('rights')
    user = User.query.filter(User.id==id) # if this returns a user, then the email already exists in database
    try:
        if user: # if a user is found
            # update a user with the form data. Hash the password so the plaintext version isn't saved.
            user.update(dict(username=username, rights=rights, password=generate_password_hash(password, method='sha256')))
            db.session.commit()
            resp = {"message":"User updated Successfully!"}
        else:
            resp = {"error":"User Id doesn't exist!"}
    except Exception as e:
        resp = {"error": str(e)}
    
    return make_response(jsonify(resp), 200)

@auth.route('/rights', methods=['POST'])
def rights_post():
    
    # code to validate and add user to database goes here
    rights = request.form.get('rights')
    name = request.form.get('name')
    user_rights = Rights.query.filter_by(name=name).first()

    if user_rights: # if a user right is found.
        resp = {"error":"Rights already exist."}

    # create a new user with the form data.
    new_rights = Rights(rights=rights,name=name)

    # add the new user rights to the database
    db.session.add(new_rights)
    db.session.commit()
    resp = {"message":"User Rights created Successfully!"}
    return make_response(jsonify(resp), 200)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))