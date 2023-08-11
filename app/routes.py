import json
import os
from dataclasses import dataclass

from flask import render_template, request
from app import app, db
from app.models import User, Org, Dashboard, Logins, DashboardViews, Schools
from sqlalchemy import func


# root
@app.route("/")
def index():
    return render_template("index.html")


@dataclass
class CardData:
    title: str
    display: str


@app.route("/data/cards/<card>")
def data_cards(card):
    if card == "dashboards":
        data = CardData(
            "Dashboards",
            Dashboard.query.with_entities(func.count(Dashboard.id)).scalar(),
        )
        return render_template("data/cards.html", data=data)
    elif card == "users":
        data = CardData("Users", User.query.with_entities(func.count(User.id)).scalar())
        return render_template("data/cards.html", data=data)
    elif card == "orgs":
        num_orgs = Org.query.with_entities(func.count(Org.id)).scalar()
        num_schools = Schools.query.with_entities(
            func.count(Schools.school_id)
        ).scalar()
        data = CardData("Organizations / Schools", f"{num_orgs} / {num_schools}")
        return render_template("data/cards.html", data=data)
    elif card == "logins":
        num_logins = Logins.query.with_entities(func.count(Logins.id)).scalar()
        num_views = DashboardViews.query.with_entities(
            func.count(DashboardViews.id)
        ).scalar()
        data = CardData("Logins / Views", f"{num_logins} / {num_views}")
        return render_template("data/cards.html", data=data)
    else:
        return render_template("data/cards.html", data=CardData("TBD", "TBD"))


@app.route("/data/logins")
def data_logins():
    page = request.args.get("page", 1, type=int)
    records = (
        db.session.query(
            User.fname, User.lname, Org.name.label("organization"), Logins.timestamp
        )
        .join(Logins, Logins.user_id == User.id)
        .join(Org, Org.id == User.org)
        .order_by(Logins.timestamp.desc())
        .paginate(page=page, per_page=20, error_out=False)
    )
    return render_template(
        "data/logins_table.html", records=records, endpoint="data_logins"
    )


@app.route("/data/views")
def data_views():
    page = request.args.get("page", 1, type=int)
    records = (
        db.session.query(
            User.fname,
            User.lname,
            Org.name.label("organization"),
            Dashboard.title.label("dashboard"),
            DashboardViews.timestamp,
        )
        .join(DashboardViews, DashboardViews.user_id == User.id)
        .join(Org, Org.id == User.org)
        .join(Dashboard, Dashboard.id == DashboardViews.dashboard_id)
        .order_by(DashboardViews.timestamp.desc())
        .paginate(page=page, per_page=20, error_out=False)
    )

    return render_template(
        "data/views_table.html", records=records, endpoint="data_views"
    )


# test db connection
@app.route("/db")
def db_test():
    user = User.query.get(1)

    return user.email
