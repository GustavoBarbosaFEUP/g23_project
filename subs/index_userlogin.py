from flask import render_template, request, session, redirect
from classes.userlogin import Userlogin

prev_option = ""

def index(path):
    global prev_option
    msg = ""
    ulogin = session.get("user")

    if ulogin is None:
        return redirect("/login")

    user_id = Userlogin.get_user_id(ulogin)
    group = Userlogin.obj[user_id].usergroup

    Userlogin.current(user_id)
    butshow = "enabled"
    butedit = "enabled" if group == "admin" else "disabled"

    option = request.args.get("option")

    if option == "edit":
        butshow, butedit = "disabled", "enabled"

    elif option == "delete":
        obj = Userlogin.current()
        if obj.id != user_id:
            Userlogin.remove(obj.id)
            if not Userlogin.previous():
                Userlogin.first()
        else:
            msg = "You cannot delete the same user"

    elif option == "insert":
        butshow, butedit = "disabled", "enabled"

    elif option == "cancel":
        pass

    elif prev_option == "insert" and option == "save":
        user = request.form["user"]
        if len(Userlogin.find(user, 'user')) == 0:
            usergroup = request.form["usergroup"]
            password = request.form["password"]
            obj = Userlogin(0, user, usergroup, Userlogin.set_password(password))
            Userlogin.insert(obj.id)
            Userlogin.last()
        else:
            msg = "duplicate username"
            Userlogin.current()

    elif prev_option == "edit" and option == "save":
        obj = Userlogin.current()
        if group == "admin":
            obj.usergroup = request.form["usergroup"]
        if request.form["password"] != "":
            obj.password = Userlogin.set_password(request.form["password"])
        Userlogin.update(obj.id)

    elif option == "first":
        Userlogin.first()
    elif option == "previous":
        Userlogin.previous()
    elif option == "next":
        Userlogin.nextrec()
    elif option == "last":
        Userlogin.last()
    elif option == "exit":
        return render_template("home.html", ulogin=session.get("user"))

    prev_option = option
    obj = Userlogin.current()

    if option == "insert" or len(Userlogin.lst) == 0:
        id = 0
        user = ""
        usergroup = ""
        password = ""
    else:
        id = obj.id
        user = obj.user
        usergroup = obj.usergroup
        password = ""

    return render_template("userlogin.html", butshow=butshow, butedit=butedit, msg=msg,
                           id=id, user=user, usergroup=usergroup, password=password,
                           ulogin=session.get("user"), group=group)


