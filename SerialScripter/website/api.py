from flask import Blueprint, render_template, request, jsonify
from json import load, loads, dumps
from . import db
from .models import IPs, Key, Host, from_host_to_dict, create_host_from_dict, Alert, search_alerts
api = Blueprint('api', __name__)

def user_agent(request):
    return request.headers.get('User-Agent') == "secret"

@api.route('/api/v1/wingoEDR/updateconfig', methods=['GET'])
def update_config():
    if not user_agent(request):
        return render_template("404.html")
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
    return jsonify({"Hello": loads(request.data)["IP"]})

@api.route('/api/v1/common/incidentalert', methods=['POST'])
def incidentalert():
    if not user_agent(request):
        return render_template("404.html")
    return jsonify({"incidents":[]})

@api.route('/api/v1/common/inventory', methods=['POST', 'GET'])
def inventory():
    if not user_agent(request):
        return render_template("404.html")
    # hosts = [from_host_to_dict(host) for host in Host.query.all()]


    print(request.data)
    a = loads(request.data)
    
    host = Host.query.filter_by(name=a["name"]).first()

    if not host:
        db.session.add(create_host_from_dict(a))
        db.session.commit()
    else:
        if not a.get("services"):
            a["services"] = from_host_to_dict(host)["services"]
        a["ip"] = from_host_to_dict(host)["ip"]
        db.session.delete(Host.query.filter_by(name=a["name"]).first())
        db.session.commit()
        db.session.add(create_host_from_dict(a))
        db.session.commit()

    

    # with open("website/data/hosts.json", "w") as f:
    #     f.write(json_to_write)

    return jsonify({"hosts": [from_host_to_dict(host) for host in Host.query.all()]})
 

@api.route('/blacklist_ip/<ip_address>')
def blacklist_ip(ip_address):
    if not user_agent(request):
        return render_template("404.html")
    ip = IPs(ip_address=ip_address, type='blacklist')
    db.session.add(ip)
    db.session.commit()
    return f'IP address {ip_address} blacklisted successfully.'

@api.route('/whitelist_ip/<ip_address>')
def whitelist_ip(ip_address):
    if not user_agent(request):
        return render_template("404.html")
    ip = IPs(ip_address=ip_address, type='whitelist')
    db.session.add(ip)
    db.session.commit()
    return f'IP address {ip_address} whitelisted successfully.'


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
