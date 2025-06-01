from flask import Flask, render_template, session, request, redirect
import pandas as pd

# Importar todas as classes do projeto
from classes.designers import Designers
from classes.userlogin import Userlogin
from classes.collections import Collections
from classes.fashion_show import Fashion_show
from classes.designers_collections import Designers_collections

# Importar os ficheiros de gestão
import subs.index_subs as indexSubs
import subs.index_userlogin as indexUserlogin
from subs.apps_plot import apps_plot
from subs.apps_plotly import apps_plotly


app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

# Filtro customizado para formatação de datas no Jinja2
from datetime import datetime

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d %b, %Y'):
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%d')  # adapta se o formato da tua data for diferente
    return value.strftime(format)


# Caminho para os ficheiros de base de dados
path = 'data/'
Designers.read(path + 'FashionDesigners.db')
Userlogin.read(path + 'FashionDesigners.db')
Collections.read(path + 'Collections.db')
Fashion_show.read(path + 'FashionShow.db')
Designers_collections.read(path + 'DesignersCollections.db')

# Página inicial
@app.route("/")
def main():
    return render_template("home.html", ulogin=session.get("user"))

@app.route("/login")
def login():
    return render_template("login.html", id= 0, user= "", password="", ulogin=session.get("user"),resul = "")
@app.route("/chklogin", methods=["post","get"])
def chklogin():
    user = request.form["user"]
    password = request.form["password"]
    resul = Userlogin.chk_password(user, password)
    if resul == "Valid":
        session["user"] = user
        return render_template("home.html", ulogin=session.get("user"))
    return render_template("login.html", user=user, password = password, ulogin=session.get("user"),resul = resul)

@app.route("/Userlogin", methods=["post","get"])
def userlogin():
    global prev_option
    msg = ""
    ulogin=session.get("user")
    if (ulogin != None):
        user_id = Userlogin.get_user_id(ulogin)
        group = Userlogin.obj[user_id].usergroup
        if group != "admin":
            Userlogin.current(user_id)
        butshow = "enabled"
        butedit = "disabled"
        option = request.args.get("option")
        if option == "edit":
            butshow = "disabled"
            butedit = "enabled"
        elif option == "delete":
            obj = Userlogin.current()
            if obj.id != user_id:
                Userlogin.remove(obj.id)
                if not Userlogin.previous():
                    Userlogin.first()
            else:
                msg = 'You cannot delete the same user'
        elif option == "insert":
            butshow = "disabled"
            butedit = "enabled"
        elif option == 'cancel':
            pass
        elif prev_option == 'insert' and option == 'save':
            user = request.form["user"]
            if len(Userlogin.find(user, 'user')) == 0:
                usergroup = request.form["usergroup"]
                password =  request.form["password"]
                obj = Userlogin(0, user, usergroup, Userlogin.set_password(password))
                Userlogin.insert(obj.id)
                Userlogin.last()
            else:
                msg = 'duplicate username'
                Userlogin.current()
        elif prev_option == 'edit' and option == 'save':
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
        elif option == 'exit':
            return render_template("index1.html", ulogin=session.get("user"))
        prev_option = option
        obj = Userlogin.current()
        if option == 'insert' or len(Userlogin.lst) == 0:
            id = 0
            user = ""
            usergroup = ""
            password = ""
        else:
            id = obj.id
            user = obj.user
            usergroup = obj.usergroup
            password = ""
        return render_template("userlogin.html", butshow=butshow, butedit=butedit, msg=msg,id=id, user=user,
                               usergroup = usergroup,password=password,ulogin=session.get("user"), group=group)
# Dashboard após login
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", ulogin=session["user"])

@app.route("/plot", methods=["POST", "GET"])
def plot():
    return apps_plot()

@app.route("/plotly", methods=["POST", "GET"])
def plotly():
    return apps_plotly()

# Logout
@app.route("/logoff")
def logoff():
    session.clear()
    return redirect("/")

# Visualização de dados CSV (opcional)
@app.route("/data_overview")
def data_overview():
    df = pd.read_csv("data/G23_Fashion – Designers  Collections with Fashion Shows_merged (1).csv")
    return render_template("data_overview.html", tables=[df.to_html(classes='data', header="true")], ulogin=session.get("user"))

@app.route("/collections", methods=["GET"])
def collections_list():
    search_id = request.args.get("collection_id", "").lower()
    search_style = request.args.get("style", "").lower()
    search_theme = request.args.get("theme", "").lower()
    search_season = request.args.get("season", "").lower()
    search_year = request.args.get("release_year", "").lower()

    all_collections = list(Collections.obj.values())

    filtered_collections = [
        c for c in all_collections if
        (not search_id or search_id in str(c.collection_id).lower()) and
        (not search_style or search_style in c.style.lower()) and
        (not search_theme or search_theme in c.theme.lower()) and
        (not search_season or search_season in c.season.lower()) and
        (not search_year or search_year in str(c.release_year).lower())
    ]

    return render_template(
        "collections.html",
        collections=filtered_collections,
        collection_id=search_id,
        style=search_style,
        theme=search_theme,
        season=search_season,
        release_year=search_year,
        ulogin=session.get("user")
    )

@app.route("/fashion_shows", methods=["GET"])
def fashionshows():
    search_id = request.args.get("fashion_id", "")
    search_show_name = request.args.get("show_name", "").lower()
    search_venue = request.args.get("venue", "").lower()
    search_date = request.args.get("date", "")

    fashion_shows = [f for f in Fashion_show.obj.values() if 
                      (search_id == "" or str(f.fashion_id) == search_id) and 
                      (search_show_name == "" or search_show_name in f.show_name.lower()) and 
                      (search_venue == "" or search_venue in f.venue.lower()) and 
                      (search_date == "" or str(f.date) == search_date)]

    return render_template("fashion_shows.html", fashion_shows=fashion_shows, 
                           fashion_id=search_id, show_name=search_show_name, 
                           venue=search_venue, date=search_date, ulogin=session.get("user"))

@app.route("/designers_collections", methods=["GET"])
def designers_collections():
    designer_id = request.args.get("designer_id", "")
    collections_id = request.args.get("collections_id", "")
    contribution_percentage = request.args.get("contribution_percentage", "")

    all_dc = [obj for obj in Designers_collections.obj.values()]

    filtered_dc = [dc for dc in all_dc if 
                   (designer_id == "" or str(dc.designer_id) == designer_id) and
                   (collections_id == "" or str(dc.collections_id) == collections_id) and
                   (contribution_percentage == "" or str(dc.contribution_percentage) == contribution_percentage)]

    return render_template("designers_collections.html",
                           designers_collections=filtered_dc,
                           designer_id=designer_id,
                           collections_id=collections_id,
                           contribution_percentage=contribution_percentage,
                           ulogin=session.get("user"))

@app.route("/designers", methods=["GET"])
def designers_search():
    id_query = request.args.get("id", "").lower()
    name_query = request.args.get("name", "").lower()
    nationality_query = request.args.get("nationality", "").lower()

    all_designers = list(Designers.obj.values())

    filtered_designers = [
        d for d in all_designers
        if (not id_query or id_query in str(d.designer_id).lower()) and
           (not name_query or name_query in d.name.lower()) and
           (not nationality_query or nationality_query in d.nationality.lower())
    ]

    return render_template(
        "designers.html",
        designers=filtered_designers,
        id=id_query,
        name=name_query,
        nationality=nationality_query,
        ulogin=session.get("user")
    )

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
