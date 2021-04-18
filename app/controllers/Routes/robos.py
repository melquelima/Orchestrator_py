from app import app
from flask_login import login_required,current_user
from flask import render_template

@app.route("/robos")
@login_required
def robos():
    data = {"admin":current_user.is_admin}
    return render_template("robos/robos.html",title="Robôs",OBJ=data)

@app.route("/novorobo")
@login_required
def novorobo():
    data = {"admin":current_user.is_admin}
    return render_template("robos/novo.html",title="Novo Robô",OBJ=data)