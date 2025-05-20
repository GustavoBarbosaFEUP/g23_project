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

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

# Caminho para os ficheiros de base de dados
path = 'data/'
Designers.read(path + 'FashionDesigners.db')
Userlogin.read(path + 'Userlogin.db')
Collections.read(path + 'Collections.db')
Fashion_show.read(path + 'FashionShow.db')
Designers_collections.read(path + 'DesignersCollections.db')

# Página inicial
@app.route("/")
def main():
    return render_template("home.html", ulogin=session.get("user"))

# Login (sem validação)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        session["user"] = user
        return redirect("/dashboard")
    return render_template("login.html", msg="")

# Dashboard após login
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", ulogin=session["user"])

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

@app.route("/collections")
def collections():
    return render_template("collections.html", ulogin=session.get("user"))

@app.route("/fashionshows")
def fashionshows():
    return render_template("fashionshows.html", ulogin=session.get("user"))

@app.route("/designerscollections")
def designerscollections():
    return render_template("designers_collections.html", ulogin=session.get("user"))

#@app.route("/Userlogin", methods=["GET", "POST"])
#def userlogin():
 #   return indexUserlogin.index(path)

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
        nationality=nationality_query
    )

# Collections Page with Search
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
def fashion_shows_list():
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
                           venue=search_venue, date=search_date)

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
                           contribution_percentage=contribution_percentage)

if __name__ == "__main__":
    app.run(debug=True)

