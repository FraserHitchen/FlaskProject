from flask import Flask, redirect, url_for, render_template, request, session, flash, Response
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=5)

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(100))
    admin = db.Column(db.Boolean, unique=False, default=False)

    def __init__(self, name, password, email, address, admin):
        self.name = name
        self.password = password
        self.email = email
        self.address = address
        self.admin = admin


class orders(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer)
    type = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __init__(self, user_id, type, description):
        self.user_id = user_id
        self.type = type
        self.description = description


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST" and "name" not in session:
        session.permanent = True
        name = request.form["name"]
        password = request.form["password"]

        found_user = users.query.filter_by(name=name, password=password).first()
        if found_user:
            session["name"] = name
            session["email"] = found_user.email
            session["address"] = found_user.address
            session["admin"] = found_user.admin
        else:
            flash(f"Incorrect name or password!", "info")
            return redirect(url_for("login"))

        flash(f"Login Successful!", "info")
        return redirect(url_for("user"))
    else:
        if "name" in session:
            flash(f"Already Logged In!", "info")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "name" in session:
        name = session["name"]

        if request.method == "POST":
            if "name" in request.form and request.form["name"] != session["name"]:
                new_name = request.form["name"]
                session["name"] = new_name
                found_user = users.query.filter_by(name=name).first()
                found_user.name = new_name
                db.session.commit()
                name = new_name

                flash(f"Name was saved.", "info")

            if "email" in request.form and request.form["email"] != session["email"]:
                email = request.form["email"]
                session["email"] = email
                found_user = users.query.filter_by(name=name).first()
                found_user.email = email
                db.session.commit()
                flash(f"Email was saved.", "info")

            if "address" in request.form and request.form["address"] != session["address"]:
                address = request.form["address"]
                session["address"] = address
                found_user = users.query.filter_by(name=name).first()
                found_user.address = address
                db.session.commit()
                flash(f"Address was saved.", "info")

        return render_template("user.html", name=session["name"], email=session["email"], address=session["address"])
    else:
        flash(f"You are not logged in!", "info")
        return redirect(url_for("login"))


@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


@app.route("/admin", methods=["POST", "GET"])
def admin():
    if "admin" in session:
        if session["admin"]:
            if request.method == "POST":
                if "id" in request.form:
                    found_user = users.query.filter_by(_id=request.form["id"]).first()

                    if not found_user:
                        flash(f"No user with that ID could be found!", "info")
                        return redirect(url_for("admin"))

                    return render_template("admin.html", values=users.query.all(), user_values=found_user)
                elif "uo_id" in request.form:
                    found_orders = orders.query.filter_by(user_id=request.form["uo_id"])

                    if not found_orders.first():
                        flash(f"No orders from that user were found.", "info")
                        return redirect(url_for("admin"))

                    return render_template("admin.html", values=users.query.all(), user_orders=found_orders)
                elif "order_id" in request.form:
                    found_order = orders.query.filter_by(_id=request.form["order_id"]).first()
                    if not found_order:
                        flash(f"No order with that ID could be found!", "info")
                        return redirect(url_for("admin"))

                    return render_template("admin.html", values=users.query.all(), req_order=found_order)
                elif "see_all" in request.form:
                    return render_template("admin.html", values=users.query.all(), all_orders=orders.query.all())
            else:
                return render_template("admin.html", values=users.query.all())
        else:
            flash(f"You do not have permission to access this page!", "info")
            return redirect(url_for("user"))
    else:
        flash(f"You are not logged in!", "info")
        return redirect(url_for("login"))


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        session.permanent = True
        name = request.form["name"]
        password = request.form["password"]
        email = request.form["email"]
        address = request.form["address"]
        is_admin = True if "admin" in request.form else False
        session["name"] = name
        session["email"] = email
        session["address"] = address
        session["admin"] = is_admin

        found_user = users.query.filter_by(email=email).first()
        if found_user:
            return "That email is already in use", 400
        else:
            new_user = users(name, password, email, address, is_admin)
            db.session.add(new_user)
            db.session.commit()

        flash(f"Registration Successful!", "info")
        return redirect(url_for("user"))
    else:
        if "name" in session:
            flash(f"Already Logged In!", "info")
            return redirect(url_for("user"))
        return render_template("register.html")


@app.route("/logout")
def logout():
    if "name" in session:
        name = session["name"]
        flash(f"You have been logged out, {name}", "info")
    else:
        flash(f"You are not logged in!", "info")
    session.pop("name", None)
    session.pop("email", None)
    session.pop("address", None)
    session.pop("admin", None)
    return redirect(url_for("login"))


@app.route("/order", methods=["POST", "GET"])
def order():
    if request.method == "POST":
        if "name" in session:
            name = session["name"]
            found_user = users.query.filter_by(name=name).first()
            found_orders = orders.query.filter_by(user_id=found_user._id)

            if "type" in request.form and request.form["type"] != "None":
                type = request.form["type"]

                new_order = orders(found_user._id, type, "")
                db.session.add(new_order)
                db.session.commit()

                flash(f"Order Successful!", "info")
                return redirect(url_for("order"))

            if "id" in request.form:

                found_order = orders.query.filter_by(_id=request.form["id"]).first()
                if not found_order:
                    flash(f"No order with that ID was found.", "info")
                    return redirect(url_for("order"))

                if found_order.user_id != found_user._id and not found_user.admin:
                    flash(f"You cannot edit other user's orders!", "info")
                    return render_template("order.html", user_orders=found_orders)
                else:
                    session["edit_order"] = found_order._id
                    return render_template("order.html", user_orders=found_orders, edit_order=found_order)
            else:
                if "delete" in request.form and "edit_order" in session:
                    orders.query.filter_by(_id=session["edit_order"]).delete()
                    db.session.commit()
                    flash(f"Order was deleted.", "info")
                    return render_template("order.html", user_orders=found_orders)

                if "new_type" in request.form and "edit_order" in session:
                    new_type = request.form["new_type"]
                    found_order = orders.query.filter_by(_id=session["edit_order"]).first()
                    found_order.type = new_type
                    db.session.commit()

                    flash(f"Type was changed.", "info")

                if "new_desc" in request.form and "edit_order" in session:
                    new_desc = request.form["new_desc"]
                    found_order = orders.query.filter_by(_id=session["edit_order"]).first()
                    found_order.description = new_desc
                    db.session.commit()
                    flash(f"Description was changed.", "info")
                session.pop("edit_order", None)

            return render_template("order.html", user_orders=found_orders)

        else:
            flash(f"You are not logged in!", "info")
            return redirect(url_for("login"))

    else:
        if "name" in session:
            name = session["name"]
            found_user = users.query.filter_by(name=name).first()
            found_orders = orders.query.filter_by(user_id=found_user._id)
            return render_template("order.html", user_orders=found_orders)
        else:
            flash(f"You are not logged in!", "info")
            return redirect(url_for("login"))


@app.route("/reset")
def reset():
    db.session.query(orders).delete()
    db.session.query(users).delete()
    db.session.commit()
    flash(f"Tables reset!", "info")
    return redirect(url_for("home"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
