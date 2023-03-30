from flask import Blueprint, render_template, request, jsonify
from json import load, loads, dumps
from . import db
from .models import IPs, Key, Host, from_host_to_dict, create_host_from_dict, Alert
from src.common import logging_serial, get_current_time
from datetime import datetime
api = Blueprint('api', __name__)

def user_agent(request):
    with open("config.json") as config:
        return request.headers.get('User-Agent') == load(config).get("configs").get("secret-agent")

@api.route('/api/v1/wingoEDR/updateconfig', methods=['GET'])
def update_config():
    if not user_agent(request):
        return render_template("404.html")
    return jsonify({})

# @api.route('/api/v1/linux/ischanged', methods=['POST'])
# def is_changed():
    
#     box_list = [from_host_to_dict(host) for host in Host.query.all()]

#     try:
#         for box in box_list:
#             # query hosts and grab host that has the name as the one given by the post request
#             if box.get("ip") == request.remote_addr:
#                 host = Host.query.filter_by(name=box["name"]).first()
#                 host.changed_password = True
#                 logging_serial(f"Password changed on host: {box['hostname']}, IP: {box['ip']}", True, "ischanged")

#     except Exception as e:
#         logging_serial(e, False, "ischanged")

#     db.session.commit()

#     return jsonify({})

@api.route('/api/v1/linux/ischanged', methods=['POST'])
def is_changed():
    
    box_list = [from_host_to_dict(host) for host in Host.query.all()]

    try:
        for box in box_list:
            # query hosts and grab host that has the name as the one given by the post request
            if box.get("ip") == request.remote_addr:
                host = Host.query.filter_by(name=box["name"]).first()
                host.changed_password = True
                logging_serial(f"Password changed on host: {box['hostname']}, IP: {box['ip']}", True, "ischanged")

    except Exception as e:
        logging_serial(e, False, "ischanged")

    db.session.commit()

    return jsonify({})

@api.route('/api/v1/wingoEDR/systemhealth/diskspace', methods=['POST'])
def disk_space():
    if not user_agent(request):
        return render_template("404.html")
    return jsonify({})

@api.route('/api/v1/wingoEDR/activeshares', methods=['POST'])
def active_shares():
    if not user_agent(request):
        return render_template("404.html")
    with open("website/data/hosts.json", 'r') as f:
        hosts = load(f)["hosts"]
    return jsonify({})

@api.route('/api/v1/wingoEDR/errors', methods=['POST'])
def errors():
    if not user_agent(request):
        return render_template("404.html")
    return jsonify({})

@api.route('/api/v1/common/heartbeat', methods=['POST'])
def heartbeat():
    if not user_agent(request):
        return render_template("404.html")
    
    box_list = [from_host_to_dict(host) for host in Host.query.all()]

    try:
        for box in box_list:
            # query hosts and grab host that has the name as the one given by the post request
            if box.get('ip') == request.remote_addr:
                host = Host.query.filter_by(name=box["name"]).first()
                host.time_connected = get_current_time()

    except Exception as e:
        logging_serial(str(e), False, "heartbeat")

    db.session.commit()

    return jsonify({})
    
    # box_list = [from_host_to_dict(host) for host in Host.query.all()]

    # try:
    #     for box in box_list:
    #         # query hosts and grab host that has the name as the one given by the post request
    #         if box.get('ip') == request.remote_addr:
    #             host = Host.query.filter_by(name=box["name"]).first()
    #             host.time_connected = get_current_time()

    # except Exception as e:
    #     logging_serial(str(e), False, "heartbeat")

    # db.session.commit()

    # return jsonify({})

@api.route('/api/v1/common/incidentalert', methods=['POST'])
def incidentalert():
    if not user_agent(request):
        return render_template("404.html")
    
    data = loads(request.data)
    db.session.add(Alert(
        type='Incident',
        host=data['Host'].lower(),
        name=data['Incident']['Name'].lower(),
        current_time=data['Incident']['CurrentTime'].lower(),
        user=data['Incident']['User'].lower(),
        severity=data['Incident']['Severity'].lower(),
        payload=str(data['Incident']['Payload']).lower()
    ))

    db.session.commit()

    return jsonify({"received": True})

@api.route('/api/v1/common/inventory', methods=['POST', 'GET'])
def inventory():
    if not user_agent(request):
        return render_template("404.html")
    # hosts = [from_host_to_dict(host) for host in Host.query.all()]

    # receives dictionary 
    # print(request.data)
    rhost_inventory = loads(request.data)

    # if rhost_inventory["hostname"] == "bingus":
    #     print(rhost_inventory["containers"])
    
    # query hosts and grab host that has the name as the one given by the post request
    host = Host.query.filter_by(name=rhost_inventory["name"]).first()

    # if host doesn't exist we add the table for it
    if not host:
        db.session.add(create_host_from_dict(rhost_inventory))
        db.session.commit()
    else:
        if not rhost_inventory.get("services"):
            rhost_inventory["services"] = from_host_to_dict(host)["services"]

        # if an os isn't passed then retain current os 
        if not rhost_inventory.get("OS"):
            rhost_inventory["OS"] = from_host_to_dict(host)["OS"]

        rhost_inventory["ip"] = from_host_to_dict(host)["ip"]
        rhost_inventory["timeConnected"] = get_current_time()
        # print(rhost_inventory["users"][0])
        db.session.delete(Host.query.filter_by(name=rhost_inventory["name"]).first())
        db.session.commit()
        db.session.add(create_host_from_dict(rhost_inventory))
        db.session.commit()

    # return jsonify({"hosts": [from_host_to_dict(host) for host in Host.query.all()]})

    return jsonify({})
 

# @api.route('/blacklist_ip/<ip_address>')
# def blacklist_ip(ip_address):
#     if not user_agent(request):
#         return render_template("404.html")
#     ip = IPs(ip_address=ip_address, type='blacklist')
#     db.session.add(ip)
#     db.session.commit()
#     return f'IP address {ip_address} blacklisted successfully.'
#     # return jsonify({"hosts": [from_host_to_dict(host) for host in Host.query.all()]})

#     return jsonify({})
 

@api.route('/blacklist_ip/<ip_address>')
def blacklist_ip(ip_address):
    if not user_agent(request):
        return render_template("404.html")
    ip = IPs(ip_address=ip_address, type='blacklist')
    db.session.add(ip)
    db.session.commit()
    return f'IP address {ip_address} blacklisted successfully.'

# @api.route('/whitelist_ip/<ip_address>')
# def whitelist_ip(ip_address):
#     if not user_agent(request):
#         return render_template("404.html")
#     ip = IPs(ip_address=ip_address, type='whitelist')
#     db.session.add(ip)
#     db.session.commit()
#     return f'IP address {ip_address} whitelisted successfully.'

@api.route('/whitelist_ip/<ip_address>')
def whitelist_ip(ip_address):
    if not user_agent(request):
        return render_template("404.html")
    ip = IPs(ip_address=ip_address, type='whitelist')
    db.session.add(ip)
    db.session.commit()
    return f'IP address {ip_address} whitelisted successfully.'


# @api.route('/get_blacklisted_ips')
# def get_blacklisted_ips():
#     if not user_agent(request):
#         return render_template("404.html")
#     ips = IPs.query.filter_by(type='blacklist').all()
#     return jsonify([ip.ip_address for ip in ips])

# @api.route('/get_whitelisted_ips')
# def get_whitelisted_ips():
#     if not user_agent(request):
#         return render_template("404.html")
#     ips = IPs.query.filter_by(type='whitelist').all()
#     return jsonify([ip.ip_address for ip in ips])

@api.route('/get_blacklisted_ips')
def get_blacklisted_ips():
    if not user_agent(request):
        return render_template("404.html")
    ips = IPs.query.filter_by(type='blacklist').all()
    return jsonify([ip.ip_address for ip in ips])

@api.route('/get_whitelisted_ips')
def get_whitelisted_ips():
    if not user_agent(request):
        return render_template("404.html")
    ips = IPs.query.filter_by(type='whitelist').all()
    return jsonify([ip.ip_address for ip in ips])
