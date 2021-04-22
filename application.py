from cs50 import SQL
from tempfile import mkdtemp
from flask_session import Session
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from helpersRecetas import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///recetas.db")

@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/crear")
@login_required
def crear():
        return render_template("crear.html")


@app.route("/recetas", methods=["GET", "POST", "DELETE", "PUT"])
@login_required
def recetas():
    if request.method == "POST":

        # check that exists
        rows = db.execute("SELECT name FROM recetas WHERE name=? AND user_id=?", request.form.get("name"), session["user_id"])
        if len(rows) == 1:
            return "La receta que quieres crear ya existe!", 400;

        db.execute("INSERT INTO recetas (name, ingredients, howto, user_id) VALUES (?, ?, ?, ?)",
                   request.form.get("name"),
                   request.form.get("ingredients"),
                   request.form.get("howto"),
                   session["user_id"]
        )

        flash("Receta creada!")
        return redirect("/recetas")

    else:
        rows = db.execute("SELECT id, name, ingredients, howto FROM recetas WHERE user_id = (:user_id)"
            , user_id=session["user_id"])
        return render_template("recetas.html", rows=rows)


@app.route("/editar/<id>", methods=["GET", "POST"])
@login_required
def editar(id):
        rows = db.execute("SELECT id, name, ingredients, howto FROM recetas WHERE id=?", id)
        return render_template("editar.html", rows=rows)


@app.route("/editar/<id>/edit", methods=["POST", "GET"])
@login_required
def edit(id):
    rows = db.execute("SELECT id FROM recetas WHERE id=? AND user_id=?", id, session["user_id"])
    if len(rows) != 1:
        return "La receta que quieres editar no existe!", 400;

    # save the new edit
    db.execute("UPDATE recetas SET name = ?, ingredients = ?, howto =? WHERE ID = ?",
               request.form.get("name"),
               request.form.get("ingredients"),
               request.form.get("howto"),
               id
    )

    flash("Receta editada!")
    return redirect("/recetas")



@app.route("/delete/<id>")
@login_required
def delete(id):
    # check that exists
        rows = db.execute("SELECT id FROM recetas WHERE id=? AND user_id=?", id, session["user_id"])
        if len(rows) != 1:
            return "La receta que quieres eliminar no existe!", 400;

        # delete
        db.execute("DELETE FROM recetas WHERE id=? AND user_id=?", id, session["user_id"])
        flash("Receta eliminada!")
        return redirect("/recetas")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('Debes ingresar usuario', 'error')
            return render_template("register.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Debes ingresar contraseña", 'error')
            return render_template("register.html")

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            flash("Debes ingresar confirmacion de contraseña", 'error')
            return render_template("register.html")

        # Ensure password confirmation matches password was submitted
        elif request.form.get("confirmation") != request.form.get("password"):
            flash("Las contraseñas no coinciden", 'error')
            return render_template("register.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE name = ?", request.form.get("username"))

        # Ensure username doesnt exists, else register
        if len(rows) == 1:
            flash("Nombre de usuario en uso, intenta con otro", 'error')
            return render_template("register.html")

        prim_key = db.execute("INSERT INTO users (name, hash) VALUES (:username, :hash)",
                              username=request.form.get("username"),
                              hash=generate_password_hash(request.form.get("password")))

        session["user_id"] = prim_key
        return redirect("/")

    else:
        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Debes ingresar un nombre", 'error')
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Debes ingresar una constraseña", 'error')
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE name = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Nombre de usuario o constraseña invalidos", 'error')
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
