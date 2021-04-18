from app import app
from flask_login import login_required,current_user
from flask import render_template

@app.route("/notepads")
@login_required
def notepads():
    data = {"admin":current_user.is_admin}
    return render_template("notepads/index.html",title="Notepads",OBJ=data)