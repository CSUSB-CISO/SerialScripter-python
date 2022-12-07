from flask import Blueprint, render_template, request, session, flash, jsonify, redirect, url_for, json
from flask_login import login_required, current_user
from json import load, loads, dumps
from datetime import datetime
from random import randint, choice
from .models import Key
from . import db
from src.razdavat import Razdavat
from threading import Thread
from queue import Queue
from src.get_boxes import Recon
from os import getlogin, listdir
from subprocess import Popen, PIPE, STDOUT
from socket import socket
from src.search import search, sort

views = Blueprint('views', __name__)

def user_agent(request):
    return request.headers.get('User-Agent') == "backshots"

    
@views.route("/", methods=['GET', 'POST'])
@login_required
def home():
    if not user_agent(request):
        return render_template("apache.html")
    # Cringe feature jaylon wanted me to make
    emoji_list = ["🫣", "🫡", "🤔", "🙂", "🫠", "🥲", "🤑", "🤐", "😶‍🌫️", "😮‍💨", "😵", "🤯", "🥸", "😲", "😈", 
    "👿", "👾", "💥", "👨‍💻", "🦸‍♀️", "🦠"]

    if request.method == "POST":
        Recon("10.100.112.0/24").save_box_data()
        # Recon("192.168.220.0/24").save_box_data()

    # Load hosts
    try:
        with open("website/data/hosts.json", "r") as f:
            box_list = load(f)["hosts"]
    except:
        box_list = {}

    # Startup index.html
    return render_template("index.html", boxes=box_list, lastupdate=datetime.now(), emoji=choice(emoji_list), user=current_user)


@views.after_request
def apply_caching(response):
    response.headers["Server"] = "Apache/2.4.41 (Ubuntu)"
    return response

@views.route("/<name>", methods=["GET", "POST"])
@login_required
def box_management(name: str):
    """
    This page shows detailed stats on an individual switch
    queried by name number
    """
    
    if not user_agent(request):
        return render_template("404.html")

    with open("website/data/hosts.json", "r") as f:
        box_list = load(f)["hosts"]
    

    for i, box in enumerate(box_list):
        if box["name"] == name: # Return correct template based on searched box
            total_ports = 0
            for service in box["services"]:
                total_ports += 1

            return render_template(
                "manage.html",
                title=name,
                box=box_list[i],
                ports=total_ports,
                user=current_user
            )


    # Box doesnt exist
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

@views.route("/scripting-hub", methods=["GET", "POST"])
@login_required
def scripting_hub():
    if not user_agent(request):
        return render_template("404.html")
    
    # gather scripts from linux and windows' scripts directories
    scripts_list = listdir('scripts/windows/') + listdir('scripts/linux/') 

    # load list of boxes from hosts.json 
    with open("website/data/hosts.json", "r") as f:
        box_list = load(f)["hosts"]

    if request.method == 'POST':
        # initializings vars
        scripts_checked = []
        parameters_list = []
        selected_boxes = []
        

        for script in scripts_list:
            # checks if checkbox corresponding to script name is checked
            if request.form.get(script):
                # only grabbing params if corresponding box is checked
                # parameters that are inputted within the website
                parameters = request.form.get(script.split(".")[0])

                # name of script that was checked
                scripts_checked.append(script)
                parameters_list.append(parameters)

        for num_boxes, box in enumerate(box_list):
            # gathering total num of boxes and gathering every box that was checked 
            if request.form.get(box["name"]):
                selected_boxes.append(box)
        
        if not (scripts_checked and selected_boxes):
            flash("No scripts or boxes were checked...")
            flash("Nothing Deployed.")
        elif not selected_boxes:
            flash("No boxes selected. Nothing Deployed.")
        elif not scripts_checked:
            flash("No scripts selected. Nothing Deployed.")
        else:
            
            for box in selected_boxes:
                print(box)
                a = Razdavat(box["ip"], password="ILoveBackshots123!", os=box["OS"])
                for script in scripts_checked:
                    print(script)
                    a.deploy(script)
            flash(f"Deployed {len(scripts_checked)}/{len(scripts_list)} scripts to {len(selected_boxes)}/{num_boxes+1} boxes.")
 
    
    return render_template(
        "scripting-hub.html",
        scripts=scripts_list,
        boxes=box_list,
        user=current_user
    )


@views.route("/open-shell/<ip>", methods=["GET"])
@login_required
def pop_a_shell(ip: str) -> None:
    """
    Allows authenitcated users to open a shell on any given host at the click of a button

    :param str ip: The ip to connect to via ssh
    :rtype redirect url: A redirect to a gotty instance of the selected machine
    """
    def get_url(proc) -> str:
        """
        Reads STDOUT from a process until it fetches a useable URL

        :param :class <'subprocess.Popen'> proc: The process that we will monitor for output
        :rtype str url: Gotty instance url
        """
        for line in iter(proc.stdout.readline, b''):
            a = line.decode('utf-8') # decode url from bytes
            if "URL" in a and "127.0.0.1" not in a and "::1" not in a: # make sure url is not localhost
                return a.split("URL:")[-1].strip() # return url if valid

    if not user_agent(request):
        return render_template("404.html")

    # Find open port
    sock = socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1] # Fetch port number

    que = Queue() #  Queue object to pass

    """
    Start a gotty process

    Flags:
        --timeout 10 - kills process if no connection for 10 seconds
        -p {port} - gives gotty open port to run on
        -t - use TLS
        --tls-crt website/data/cert.pem  - tls cert to use
        --tls-key website/data/key.pem  - tls key to use
        -w - allow user to type in gotty instance
        -r - make url random
        ssh <user>@<ip>
    """ 
    p = Popen(f"./gotty --timeout 10 -p {port} -t --tls-crt website/data/cert.pem --tls-key website/data/key.pem -w -r ssh root@{ip}", shell=True, stdout=PIPE, stderr=STDOUT)
    # Start thread to run shell sessions concurrently
    # Give it Queue object to allow for retrieval or return value
    t = Thread(target=lambda q, arg1: q.put(get_url(arg1)), args=(que, p,))
    t.start()
    t.join()
    
    # Get return value from Queue
    url = que.get()
    print(url)

    return redirect(url) # Redirect to randomly created gotty instance

@views.route("/key-management", methods=["GET", "POST"])
@login_required
def key_management():
    if not user_agent(request):
        return render_template("404.html")
    if request.method == 'POST':
        key = request.form.get('key')

        is_duplicate = False

        # needs to be an ssh key to even add it to the database
        if key.split()[0] != "ssh-rsa":
            is_duplicate = True
            flash('Not an ssh key!')
        else:
        # needs to be an ssh key to even check
        # checking if the key to be added matches any keys that are currently in the db
            for ssh_key in current_user.keys:
                if ssh_key.data.split()[1] == key.split()[1]:
                    is_duplicate = True
                    flash(f'Inserted key is duplicate of Key Number: {ssh_key.id}')
        

        # ensure a unique public key will be added
        if len(key) > 500 and not is_duplicate:
            flash("Key added successfully")
            new_key = Key(data=key, user_id=current_user.id)
            db.session.add(new_key)
            db.session.commit()
            with open("website/data/hosts.json", "r") as f:
                hosts = load(f)["hosts"]
                try:

                    for host in hosts:
                        connection = Razdavat(host["ip"], key_path=f"/home/{getlogin()}/.ssh/id_rsa.pub", user="root")
                        connection.add_ssh_key(key)
                except:
                    
                    for host in hosts:
                        connection = Razdavat(host["ip"], password="GibM3Money123!", user="root")
                        connection.add_ssh_key(key)

        elif len(key) < 500:
            flash("Key is too short!!")


    return render_template("key-management.html", user=current_user)

@views.route('/visualize', methods=["GET"])
@login_required
def visualize():
    if not user_agent(request):
        return render_template("404.html")
    # Load hosts.json object
    with open("website/data/hosts.json", "r") as f:
        # load dict from hosts.json then convert it to formatted json string using dumps
        box_list = dumps(load(f)) 
    print(box_list)
    # Pass current user to only allow authenticated view of the network and box_list (hosts.json object to graph)
    return render_template("visualize.html", hosts=box_list, user=current_user)

@views.route('/incidents', methods=["GET", "POST"])
@login_required
def incidents():
    with open("website/data/incidents.json", "r") as f:
        incidents = load(f)["Alerts"]

    search_words = request.args.get("search")

    switch = {
        "ip": "RemoteIP",
        "host": "Host",
        "name": "Name",
        "user": "User",
        "process": "Process",
        "cmd": "Cmd"
    }

    if search_words:
        match_all = "and" in search_words

        queries = list()
        filters = list()


        for term in search_words.split():
            if term == "and" or term.startswith("sort_by"):
                continue
            try:
                x = term.split(":")
                if len(x) > 1:
                    filters.append(x[0])
                    queries.append(x[1])
                else:
                    filters.append("")
                    queries.append(x[1])
            except:
                queries.append(term)
        filters = tuple(map(lambda a: switch[a] if a else "", filters))
        results = search(incidents, search_words=queries, filters=filters, match_all=match_all) 
        
        if results:
            incidents = results
        
        if search_words.startswith("sort_by"):
            try:
                incidents = sort(incidents, by=switch[search_words[search_words.index(":")+1:search_words.index(" ")]])
            except:
                incidents = sort(incidents, by=switch[search_words[search_words.index(":")+1:]])

    # Pass current user to only allow authenticated view of the network and box_list (hosts.json object to graph)
    return render_template("incidents.html", incidents=incidents, user=current_user)


@views.route('/delete-key', methods=['POST'])
def delete_key():
    # load the json object that was sent
    key = loads(request.data)
    # access the actual pair by using the keyId key
    keyId = key['keyId']
    key = Key.query.get(keyId)
    print(key.data)
    # reassigns key to true or false depending on if the key actually exists in the database
    if key:
        if key.user_id == current_user.id:
            flash(f'Key: {key.id} has been deleted.')
            with open("website/data/hosts.json", "r") as f:
                hosts = load(f)["hosts"]
                try:
                    for host in hosts:
                        connection = Razdavat(host["ip"], key_path=f"/home/{getlogin()}/.ssh/id_rsa.pub", user="root")
                        connection.remove_ssh_key(key)
                except:
                    for host in hosts:
                        connection = Razdavat(host["ip"], password="GibM3Money123!", user="root")
                        connection.remove_ssh_key(key)

            db.session.delete(key)
            db.session.commit()
    return jsonify({})


