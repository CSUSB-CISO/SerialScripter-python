from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
import json
from datetime import datetime
from random import randint, choice
from .models import Key
from . import db
from src.razdavat import Razdavat
from threading import Thread
from queue import Queue
from selenium import webdriver
from os import getlogin, system
from subprocess import Popen, PIPE, STDOUT
from socket import socket

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

    return render_template("index.html", boxes=box_list, lastupdate=datetime.now(), emoji=choice(emoji_list), user=current_user)

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
            "isOn": False,
            "docker": [],
            "tasks": [{}],
            "firewall": []
        },
        user=current_user
    )


@views.route("/open-shell/<ip>", methods=["GET"])
@login_required
def pop_a_shell(ip):
    """
    This page shows a summary of all port counts, etc
    across the entire network
    """
    def get_url(proc):
        for line in iter(proc.stdout.readline, b''):
            a = line.decode('utf-8')
            if "URL" in a and "127.0.0.1" not in a and "::1" not in a:
                return a.split("URL:")[-1].strip()

    sock = socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]

    que = Queue()

    p = Popen(f"./gotty --timeout 10 -p {port} -t --tls-crt website/data/cert.pem --tls-key website/data/key.pem -w -r ssh cm03@localhost", shell=True, stdout=PIPE, stderr=STDOUT)

    t = Thread(target=lambda q, arg1: q.put(get_url(arg1)), args=(que, p,))
    t.start()
    t.join()
    
    url = que.get()
    print(url)
    return redirect(url)

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
                    connection = Razdavat("127.0.0.1", password="<REDACTED>", user="cm03")
                    connection.add_ssh_key(key)
                    # for host in hosts:
                    #     connection = Razdavat(host["ip"], password="<REDACTED>", user="cm03")
                    #     connection.add_ssh_key(key)

        else:
            flash('Note is too short!', category='error')


    return render_template("key-management.html", user=current_user)

@views.route('/visualize', methods=["POST", "GET"])
@login_required
def graph():
    with open("website/data/hosts.json", "r") as f:
        box_list = json.dumps(json.load(f))

    return render_template("chart.html", hosts=box_list, user=current_user)

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