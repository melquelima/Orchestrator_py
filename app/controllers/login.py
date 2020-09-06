from app import app,lm
from app.models.forms import LoginForm
from flask_login import login_user,login_required,current_user,logout_user
from flask import render_template,redirect,url_for,jsonify,flash
from app.models.tables import Users,UserSchema,Bot,BotSchema
from datetime import timedelta
@lm.user_loader
def load_user(id):
    return Users.query.filter_by(id=id).first()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        usr = Users.query.filter_by(userName=form.userName.data,password=form.password.data).first()
        if usr:
            login_user(usr)
            return redirect(url_for("index"))
        flash("Login e(ou) senha invalido(s)!")
    return render_template("login.html",form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))




