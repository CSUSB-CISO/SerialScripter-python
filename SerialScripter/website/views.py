from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json
from datetime import datetime
import random
from .models import Key
from . import db
from src.razdavat import Razdavat

from os import getlogin

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
@login_required
def network_wide():
    """
    This page shows a summary of all port counts, etc
    across the entire network
    """
    # network = getNetworkWide()
    return render_template("network-wide.html", network={}, user=current_user)

@views.route("/terminal", methods=["GET"])
@login_required
def terminal():
    """
    This page shows a summary of all port counts, etc
    across the entire network
    """
    # network = getNetworkWide()
    return render_template("terminal.html", user=current_user)

@views.route("/key-management", methods=["GET", "POST"])
@login_required
def key_management():
    if request.method == 'POST':
        key = request.form.get('key')

        # checking if the key to be added matches any keys that are currently in the db
        is_duplicate = False
        for database_keys in current_user.keys:
            if database_keys.data.split()[1] == key.split()[1]:
                is_duplicate = True

        # ensure it a unique public key will be added
        if len(key) > 500 and is_duplicate == False:
            new_key = Key(data=key, user_id=current_user.id)
            db.session.add(new_key)
            db.session.commit()
            with open("website/data/hosts.json", "r") as f:
                hosts = json.load(f)["hosts"]
                try:
                    connection = Razdavat("127.0.0.1", key_path=f"/home/{getlogin()}/.ssh/id_rsa.pub", user="cm03")
                    connection.add_ssh_key(key)
                    # for host in hosts:
                    #     connection = Razdavat(host["ip"], key_path=f"/home/{getlogin()}/.ssh/id_rsa.pub", user="cm03")
                    #     connection.add_ssh_key(key)
                except:
                    connection = Razdavat("127.0.0.1", password="@11272003Cm!", user="cm03")
                    connection.add_ssh_key(key)
                    # for host in hosts:
                    #     connection = Razdavat(host["ip"], password="@11272003Cm!", user="cm03")
                    #     connection.add_ssh_key(key)

        else:
            flash('Note is too short!', category='error')


    return render_template("key-management.html", user=current_user)


@views.route('/delete-key', methods=['POST'])
def delete_key():
    # load the json object that was sent
    key = json.loads(request.data)
    # access the actual pair by using the keyId key
    keyId = key['keyId']
    key = Key.query.get(keyId)
    # reassigns key to true or false depending on if the key actually exists in the database
    if key:
        if key.user_id == current_user.id:
            db.session.delete(key)
            db.session.commit()
        print(key.data)
    return jsonify({})