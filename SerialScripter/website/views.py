from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import json
from datetime import datetime
import random

views = Blueprint('views', __name__)


@views.route("/", methods=['GET', 'POST'])
@login_required
def home():
    emoji_list = ["🫣", "🫡", "🤔", "🙂", "🫠", "🥲", "🤑", "🤐", "😶‍🌫️", "😮‍💨", "😵", "🤯", "🥸", "😲", "😈", 
    "👿", "👾", "💥", "👨‍💻", "🦸‍♀️", "🦠",]

    if request.method == "POST":
        pass
        # Recon("192.168.1.0/24").save_box_data()

    with open("website/data/hosts.json", "r") as f:
        box_list = json.load(f)["hosts"]

    return render_template("index.html", boxes=box_list, lastupdate=datetime.now(), emoji=random.choice(emoji_list), user=current_user)

@views.route("/<name>", methods=["GET"])
@login_required
def box_management(name: str):
    """
    This page shows detailed stats on an individual switch
    queried by name number
    """
    with open("website/data/hosts.json", "r") as f:
        box_list = json.load(f)["hosts"]


    for i, box in enumerate(box_list):
        if box["name"] == name:
            return render_template(
                "manage.html",
                title=name,
                box=box_list[i],
                user=current_user
            )

    return render_template(
        "manage.html",
        title=name,
        box={
            "name": "host-00",
            "ip": "0.0.0.0",
            "OS": "Null",
            "services": [],
            "isOn": False
        },
        user=current_user
    )

@views.route("/network-wide", methods=["GET"])
def network_wide():
    """
    This page shows a summary of all port counts, etc
    across the entire network
    """
    # network = getNetworkWide()
    return render_template("network-wide.html", network={})
