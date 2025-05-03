from flask import render_template, request, session
from classes.designers import Designers

prev_option = ""

def index(path):
    global prev_option
    butshow, butedit = "enabled", "disabled"
    option = request.args.get("option")

    if option == "edit":
        butshow, butedit = "disabled", "enabled"
    elif option == "delete":
        obj = Designers.current()
        Designers.remove(obj.designer_id)
        if not Designers.previous():
            Designers.first()
    elif option == "insert":
        butshow, butedit = "disabled", "enabled"
    elif option == "cancel":
        pass
    elif prev_option == "insert" and option == "save":
        new_id = Designers.get_id(0)
        strobj = f"{new_id};{request.form['name']};{request.form['nationality']}"
        obj = Designers.from_string(strobj)
        Designers.insert(obj.designer_id)
        Designers.last()
    elif prev_option == "edit" and option == "save":
        obj = Designers.current()
        obj.name = request.form["name"]
        obj.nationality = request.form["nationality"]
        Designers.update(obj.designer_id)
    elif option == "first":
        Designers.first()
    elif option == "previous":
        Designers.previous()
    elif option == "next":
        Designers.nextrec()
    elif option == "last":
        Designers.last()
    elif option == "exit":
        return "<h1>Obrigado por usar a aplicação</h1>"

    prev_option = option
    obj = Designers.current()

    if option == "insert" or len(Designers.lst) == 0:
        id = Designers.get_id(0)
        name = ""
        nationality = ""
    else:
        id = obj.designer_id
        name = obj.name
        nationality = obj.nationality

    return render_template("index.html", butshow=butshow, butedit=butedit,
                           id=id, name=name, nationality=nationality,
                           ulogin=session.get("user"))


