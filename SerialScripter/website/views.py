from flask import Blueprint, render_template, request, session, flash, jsonify, redirect, url_for, json, send_file
from flask_login import login_required, current_user
from json import load, loads, dumps
from datetime import datetime
from random import randint, choice
from .models import Key, Host, from_host_to_dict, Alert, or_, and_ #, create_host_from_dict,  search_alerts
from . import db
from src.razdavat import Razdavat
from threading import Thread
from queue import Queue
from src.get_boxes import Recon
from os import getlogin, listdir, system, path, walk, scandir
from subprocess import Popen, PIPE, STDOUT, run
from socket import socket
from flask_paginate import Pagination, get_page_parameter


#from src.search import search, sort
from src.common import from_json_to_csv, from_host_to_csv, upload_csv, get_rsyslog_list, logging_serial, get_log_lines, filter_log_list, get_password, get_serial_log_list, get_current_time

views = Blueprint('views', __name__)

def user_agent(request):
    with open("config.json") as config:
        config = load(config)
        return request.headers.get('User-Agent') == config.get("configs").get("secret-agent")

    
@views.route("/", methods=['GET', 'POST'])
@login_required
def home():
    if not user_agent(request):
        return render_template("apache.html")
    # Cringe feature jaylon wanted me to make
    emoji_list = ["🫣", "🫡", "🤔", "🙂", "🫠", "🥲", "🤑", "🤐", "😶‍🌫️", "😮‍💨", "😵", "🤯", "🥸", "😲", "😈", 
    "👿", "👾", "💥", "👨‍💻", "🦸‍♀️", "🦠"]
    
    # Load hosts
    try:
        box_list = [from_host_to_dict(host) for host in Host.query.all()]

        # for box in box_list:
        #     if box.get("changed_password"):
        #         print(box)
    except Exception as e:
        logging_serial(e, False, "host-enum")
        box_list = {}

    if request.method == "POST":
        with open("config.json") as config:
            config = load(config)
            config = config.get("configs")

            if request.form.get("rescan"):
                Recon(config.get("out-ip")).save_box_data(db)

            elif request.form.get("download_host_info") or request.form.get("upload_host_info"):

                try:
                    filename = from_host_to_csv(box_list, config.get("UID"))

                    if request.form.get("download_host_info"):
                        return send_file(f'../{filename}', as_attachment=True)
                
                    elif request.form.get("upload_host_info"):
                        try: 
                            upload_csv(config.get("url"), config.get("port"), filename=filename)
                        except Exception as e:
                            flash("Unable to upload csv. Check url/port settings")
                            logging_serial(e, False, "upload-csv")

                except Exception as e:
                    flash("Unable to create csv. Hosts not enumerated")
                    logging_serial(e, False, "convert-csv")
                



    # Startup index.html
    return render_template("index.html", boxes=box_list, lastupdate=datetime.now(), emoji=choice(emoji_list), user=current_user, timestamp=get_current_time())

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

    box_list = [from_host_to_dict(host) for host in Host.query.all()]

    for i, box in enumerate(box_list):
        if box["name"] == name: # Return correct template based on searched box
            if request.method == "POST":
                with open("config.json") as config:
                    config = load(config)
                    config = config.get("configs")

                    # check if post request is coming from download or upload button on user pane 
                    if request.form.get("users-download") or request.form.get("users-upload"):
                        try:
                            filename = from_json_to_csv(box, "users", config.get("UID"))
                            # utilize different methods for upload and download methods
                            if request.form.get("users-download"):
                                return send_file(f'../{filename}', as_attachment=True)
                            
                            elif request.form.get("users-upload"):
                                try: 
                                    upload_csv(config.get("url"), config.get("port"), filename=filename)
                                except Exception as e:
                                    flash("Unable to upload csv. Check url/port settings")
                                    logging_serial(e, False, "upload-csv")
                        except Exception as e:
                            flash("Unable to create csv. No users exist.")
                            logging_serial(e, False, "convert-csv")

                            
                    # check if post is from download or upload button on ports pane
                    elif request.form.get("ports-download") or request.form.get("ports-upload"):
                        try:
                            filename = from_json_to_csv(box, "services", config.get("UID"), ("service", "port"))
                            # utilize different methods for upload and download methods
                            if request.form.get("ports-download"):
                                return send_file(f'../{filename}', as_attachment=True)

                            elif request.form.get("ports-upload"):
                                try: 
                                    upload_csv(config.get("url"), config.get("port"), filename=filename)
                                except Exception as e:
                                    flash("Unable to upload csv. Check url/port settings")
                                    logging_serial(e, False, "upload-csv")

                        except Exception as e:
                            flash("Unable to create csv. No services exist.")
                            logging_serial(e, False, "convert-csv")


                    # check if post request is coming from download or upload button on user pane 
                    elif request.form.get("services-download") or request.form.get("services-upload"):
                        try:
                            filename = from_json_to_csv(box, "services", config.get("UID"))
                            # utilize different methods for upload and download methods
                            if request.form.get("services-download"):
                                return send_file(f'../{filename}', as_attachment=True)
                            
                            elif request.form.get("services-upload"):
                                try: 
                                    upload_csv(config.get("url"), config.get("port"), filename=filename)
                                except Exception as e:
                                    flash("Unable to upload csv. Check url/port settings")
                                    logging_serial(e, False, "upload-csv")

                        except Exception as e:
                            flash("Unable to create csv. No services exist.")
                            logging_serial(e, False, "convert-csv")


            return render_template(
                "manage.html",
                title=name,
                box=box_list[i],
                user=current_user,
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

    # load list of boxes 
    box_list = [from_host_to_dict(host) for host in Host.query.all()]

    if request.method == 'POST':

        # initializings vars
        scripts_checked = list()
        parameters_list = list()
        selected_boxes = list()
        
        # iterates through all scripts in scripts directory
        for script in scripts_list:

            # checks if box corresponding to script name is checked
            if request.form.get(script):

                """
                this checks for scripts without any extensions 
                ex: gomemento is identified by gom

                whatever parameters are inputted are saved and appended to parameters_list
                
                """ 
                if len(script.split(".")) == 1:
                    parameters = request.form.getlist(script[0:3])

                else:    
                    parameters = request.form.getlist(script.split(".")[0])

                # name of script that was checked
                scripts_checked.append(script)
                
                """
                    if parameter has spaces, flask returns a list with two values ["", "parameter space"]
                    if no spaces it'll be only one value 
                    thats the reason for try except
                """
                try:
                    parameters_list.append(parameters[1])
                except IndexError:
                    parameters_list.append(parameters[0])
        for num_boxes, box in enumerate(box_list):
            #  gather every box that was checked 
            if request.form.get(box["name"]):
                selected_boxes.append(box)
        
        # flashing messages on web server
        if not (scripts_checked and selected_boxes):
            flash("No scripts or boxes were checked...")
            flash("Nothing Deployed.")
        elif not selected_boxes:
            flash("No boxes selected. Nothing Deployed.")
        elif not scripts_checked:
            flash("No scripts selected. Nothing Deployed.")
        else:

            for box in selected_boxes:
                if box.get("ip").split('.')[-1] != "1":
                    try:   
                        rhost = Razdavat(box["ip"], password=get_password(box), os=box["OS"])
                        # Only deploy the script to box if Run Script box is checked 
                        if (request.form.get('Deploy')): 
                            for i, script in enumerate(scripts_checked):

                                # deploy script and check if no parameters exist
                                if len(parameters_list) == 1 and parameters_list[0] == "":
                                    rhost.deploy(script, parameters_list[0])
                                    logging_serial(f"Deployed script: '{script}' to IP: {box.get('ip')}", True, "Scripting-Hub")

                                # deploy script and check if there are parameters
                                elif len(parameters_list) == 1:
                                    rhost.deploy(script, parameters_list[0])
                                    logging_serial(f"Deployed script: '{script}' with Parameter\s: '{parameters_list[0]}' to IP: {box.get('ip')}", True, "Scripting-Hub")
                                
                                # deploy scripts one by one and append parameter as needed
                                else:
                                    rhost.deploy(script, parameters_list[i])
                                    logging_serial(f"Deployed script: '{script}' with Parameter\s: '{parameters_list[i]}' to IP: {box.get('ip')}", True, "Scripting-Hub")

                        else:
                            # put script onto box without running it and log it
                            for i, script in enumerate(scripts_checked):
                                rhost.put(script_name=script)
                                logging_serial(f"Put script '{script}' on IP: {box.get('ip')}", True, "Scripting-Hub")

                    except Exception as e: 
                        logging_serial(f'{str(e)} for IP: {box.get("ip")}', False, "Scripting-Hub")

            flash(f"Attempted to deploy {len(scripts_checked)}/{len(scripts_list)} scripts to {len(selected_boxes)}/{num_boxes+1} boxes.")

    return render_template(
        "scripting-hub.html",
        scripts=scripts_list,
        boxes=box_list,
        user=current_user
    )


@views.route("/test")
def test():

    matching_alerts = search_alerts("(hunte or john) and sshd.exe")
    for alert in matching_alerts:
        print(alert.host)
        
    return ""


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
    
    try:
        user = "Administrator" if "window" in from_host_to_dict(Host.query.filter_by(ip=ip).first()).get("OS").lower() else "root"
        # print(from_host_to_dict(Host.query.filter_by(ip=ip).first()))
    except AttributeError:
        print(from_host_to_dict(Host.query.filter_by(ip=ip).first()))

    p = Popen(
        f"./gotty --timeout 10 -p {port} -t --tls-crt website/data/cert.pem --tls-key website/data/key.pem -w -r ssh {user}@{ip}",
        shell=True, 
        stdout=PIPE, 
        stderr=STDOUT
     )
    
    # Start thread to run shell sessions concurrently
    # Give it Queue object to allow for retrieval or return value
    t = Thread(target=lambda q, arg1: q.put(get_url(arg1)), args=(que, p,))
    t.start()
    t.join()
    
    # Get return value from Queue
    url = que.get()
    return redirect(url) # Redirect to randomly created gotty instance

@views.route("/delete/<name>", methods=["GET", "POST"])
@login_required
def delete_host(name: str):
    db.session.delete(Host.query.filter_by(name=name).first())
    db.session.commit()
    return jsonify({})


@views.route("/key-management", methods=["GET", "POST"])
@login_required
def key_management():

    if not user_agent(request):
        return render_template("404.html")
    # load list of boxes 
    box_list = [from_host_to_dict(host) for host in Host.query.all()]
    

    if request.method == 'POST':
        key = request.form.get('key')
        # print(key)

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
            # for box in box_list:
            #     connection = Razdavat(box["ip"], key_path=f"/home/{getlogin()}/.ssh/id_rsa.pub", password=password)
            #     connection.add_ssh_key(key)
            for box in box_list:
                if box.get("ip").split('.')[-1] != "1" and "windows" not in box.get("OS").lower():
                    try:
                        connection = Razdavat(box["ip"], password=get_password(box), os=box["OS"])
                        connection.add_ssh_key(key)
                        logging_serial(f"Added ssh-key from {key.split()[2].split('@')[1]} to: {box['ip']}", True, "Key-Management")
                    except Exception as e:
                        if "Errno" in str(e):
                            logging_serial(e, False, "Key-Management")
                        else:
                            logging_serial(f"{e} {box.get('ip')}", False, "Key-Management")

        elif len(key) < 500:
            flash("Key is too short!!")


    return render_template("key-management.html", user=current_user)

@views.route('/visualize', methods=["GET"])
@login_required
def visualize():
    if not user_agent(request):
        return render_template("404.html")
    # Load hosts.json object
    # with open("website/data/hosts.json", "r") as f:
    #     # load dict from hosts.json then convert it to formatted json string using dumps
    #     box_list = dumps(load(f)) 

    box_list = dumps([from_host_to_dict(host) for host in Host.query.all()])
    
    # print(box_list)
    # Pass current user to only allow authenticated view of the network and box_list (hosts.json object to graph)
    return render_template("visualize.html", hosts=box_list, user=current_user)

@views.route("/rsyslog", methods=["GET", "POST"])
@login_required
def rsyslog():
    if not user_agent(request):
        return render_template("404.html")

    box_list = [from_host_to_dict(host) for host in Host.query.all()]

    host_list = [box.get("hostname") for box in box_list if box.get("hostname")]

    try:
        # get current page number
        page = request.args.get(get_page_parameter(), type=int, default=1)

        # total num of lines in file
        line_count = get_log_lines("/var/log/rsyslog.log")

        # amount of lines per page determined by file size
        if line_count > 5000:
            per_page = 5000
        else:
        # at most 3 pages will be displayed when file is smaller than 5000 lines
            per_page = line_count//3
        
        # determine start position
        offset = (page - 1) * per_page

        # offest + lines per page creates a range to iterate through
        log_file = get_rsyslog_list(offset=slice(offset, offset+per_page))

        # depending on the number of pages and lines allowed per page a group of links to the different pages is created.
        pagination = Pagination(page=page, total=line_count, per_page=per_page)

    except FileNotFoundError:
        log_file = [{'hostname': 'Cowboy', 'syslogtag_pid': 'n/a', 'IP': 'localhost','timestamp': 'time', 'log_level': 'severity', 'log_message': "Keyboard Cowboys"}]
        flash(f"Log file does not exist")     
    
    return render_template(
            "rsyslog.html",
            log = log_file,
            hosts = host_list,
            pagination=pagination,
            user=current_user,
        )


@views.route("/rsyslog/<sort>", methods=["GET"])
@login_required
def rsyslog_sort(sort: str):
    if not user_agent(request):
        return render_template("404.html")
    
    host_list = [box.get("hostname") for box in [from_host_to_dict(host) for host in Host.query.all()] if box.get("hostname")]

    try:
        # total num of lines in file
        line_count = get_log_lines("/var/log/rsyslog.log")

        # amount of lines per page determined by file size
        if line_count > 5000:
            per_page = 5000
        else:
        # at most 3 pages will be displayed when file is smaller than 5000 lines
            per_page = line_count//3        

        
        page = request.args.get(get_page_parameter(), type=int, default=1)
        offset = (page - 1) * per_page

        filtered_log_file = filter_log_list(sort_by=sort, offset=slice(offset, offset+per_page))

        if not log_file:
            log_file = [{'hostname': 'Cowboy', 'syslogtag_pid': 'n/a', 'IP': 'localhost','timestamp': 'time', 'log_level': 'severity', 'log_message': "Keyboard Cowboys"}]
            line_count = 0
            flash(f"Logs do not contain: {sort}")

        pagination = Pagination(page=page, total=line_count, per_page=per_page)


    except FileNotFoundError:
        log_file = [{'hostname': 'Cowboy', 'syslogtag_pid': 'n/a', 'IP': 'localhost','timestamp': 'time', 'log_level': 'severity', 'log_message': "Keyboard Cowboys"}]
        flash(f"Log file does not exist")    

    return render_template(
            "rsyslog.html",
            log = log_file,
            hosts = host_list,
            pagination=pagination,
            user=current_user,
        )

@views.route("/serial-logs", methods=["GET", "POST"])
@login_required
def serial_logs():
    if not user_agent(request):
        return render_template("404.html")

    try:
        # get current page number
        page = request.args.get(get_page_parameter(), type=int, default=1)

        # total num of lines in file
        line_count = get_log_lines("serial_logs.log")

        # amount of lines per page determined by file size
        if line_count > 100:
            per_page = 100
            pagination = Pagination(page=page, total=line_count, per_page=per_page)
            offset = (page - 1) * per_page
            # offest + lines per page creates a range to iterate through
            log_file = get_serial_log_list(offset=slice(offset, offset+per_page))
        else:
            offset = (page - 1) * line_count
            pagination = Pagination(page=page, total=line_count, per_page=line_count)
            # offest + lines per page creates a range to iterate through
            log_file = get_serial_log_list(offset=slice(offset, offset+line_count))
            # determine start position

        # depending on the number of pages and lines allowed per page a group of links to the different pages is created.

    except FileNotFoundError:
        log_file = [{"timestamp": "the-time",
                    "err_succ": "Fail",
                    "module": "Missing",
                    "log_content": "No logs!"}]
        pagination = Pagination(page=page, total=0, per_page=0)
        flash(f"Log file does not exist")      
    
    return render_template(
            "serial-logs.html",
            log = log_file,
            pagination=pagination,
            user=current_user,
        )

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

    # reassigns key to true or false depending on if the key actually exists in the database
    box_list = [from_host_to_dict(host) for host in Host.query.all()]

    if key:

        if key.user_id == current_user.id:
            flash(f'Key: {key.id} has been deleted.')
            db.session.delete(key)
            db.session.commit()
            for box in box_list:
                try:
                    if box.get("ip").split('.')[-1] != "1" and "windows" not in box.get("OS").lower():
                        connection = Razdavat(box["ip"], password=get_password(box), os=box["OS"])
                        connection.remove_ssh_key(key.data)
                        logging_serial(f"Removed {key.data.split()[2].split('@')[1]}'s public key from: {box['ip']}", True, "Delete-Key")
                except Exception as e:
                    if "Errno" in str(e):
                        logging_serial(e, False, "Delete-Key")
                    else:
                        logging_serial(f"{e} {box.get('ip')}", False, "Delete-Key")
    return jsonify({})

from sqlalchemy import or_, and_
from difflib import SequenceMatcher

def search_alerts(query):
    alerts = Alert.query.all()
    search_terms = query.split()

    # Parse the OR conditions into a list of lists
    or_conditions = []
    current_or_condition = []
    for term in search_terms:
        if term.lower() == "or":
            or_conditions.append(current_or_condition)
            current_or_condition = []
        else:
            current_or_condition.append(term)
    or_conditions.append(current_or_condition)

    # Loop through each alert and check for matches
    matching_alerts = []
    for alert in alerts:
        # Check if the alert matches any of the OR conditions
        or_match = False
        for condition in or_conditions:
            and_match = True
            for term in condition:
                if not (
                    SequenceMatcher(None, term.lower(), alert.host.lower()).ratio() < 0.5
                    and SequenceMatcher(None, term.lower(), alert.name.lower()).ratio() < 0.5
                    and SequenceMatcher(None, term.lower(), alert.user.lower()).ratio() < 0.5
                    and SequenceMatcher(None, term.lower(), alert.process.lower()).ratio() < 0.5
                    and SequenceMatcher(None, term.lower(), alert.remote_ip.lower()).ratio() < 0.5
                    and SequenceMatcher(None, term.lower(), alert.cmd.lower()).ratio() < 0.5
                ):
                    and_match = False
                    break
            if and_match:
                or_match = True
                break
        if not or_match:
            continue

        # Check if the alert matches any of the AND conditions
        and_match = True
        for term in search_terms:
            if term.lower() == "or":
                continue
            if not (
                SequenceMatcher(None, term.lower(), alert.host.lower()).ratio() < 0.5
                or SequenceMatcher(None, term.lower(), alert.name.lower()).ratio() < 0.5
                or SequenceMatcher(None, term.lower(), alert.user.lower()).ratio() < 0.5
                or SequenceMatcher(None, term.lower(), alert.process.lower()).ratio() < 0.5
                or SequenceMatcher(None, term.lower(), alert.remote_ip.lower()).ratio() < 0.5
                or SequenceMatcher(None, term.lower(), alert.cmd.lower()).ratio() < 0.5
            ):
                and_match = False
                break
        if and_match:
            matching_alerts.append(alert)

    return matching_alerts

