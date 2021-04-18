from app import app
from flask import request
from flask_login import current_user
from random import randint
from flask import url_for

@app.context_processor
def page():
    def pg():
        pass
    func = lambda jsFile: jsFile + "?u=" + str(randint(0, 100000))
    return dict(randomJs=func)

@app.context_processor
def tag_property():
    def func(tag,value): 
        v = value.replace(" ",' ') #nao é vazio e sim alt+255
        v = f'{tag}={v}'
        return v if value else ""
    return dict(tagProp=func)


@app.template_filter()
def url_to(text):
    return url_for('static', filename=text)


@app.context_processor
def random_Js():
    func = lambda jsFile: jsFile + "?u=" + str(randint(0, 100000))
    return dict(randomJs=func)


@app.context_processor
def utility_processor():
    activeMenu = lambda text: "active" if text in request.url_rule.rule else ""
    return dict(activeMenu=activeMenu)

# TITLE
@app.context_processor
def utility_processor():
    return dict(title = lambda:app.config["NOME_EMPRESA"])


#capitalize name
@app.context_processor
def utility_processor():
    return dict(capitalizeName = lambda name:" ".join([x.capitalize() for x in name.split(" ")]))


# menuLateral
@app.context_processor
def utility_processor():
    def menuLateral():
        if current_user.is_gerente():
            return 'gerente'
        elif current_user.is_representante():
            return 'representante'
        elif current_user.is_admin():
            return 'admin'
        else:
            return 'usuario invalido'

    return dict(menuLateral = menuLateral)