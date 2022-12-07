from flask import Blueprint, render_template, request, jsonify
from json import load, loads, dumps


api = Blueprint('api', __name__)

def user_agent(request):
    return request.headers.get('User-Agent') == "backshots"

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

@api.route('/api/v1/common/ipblacklist', methods=['GET', 'POST'])
def ip_blacklist():
    if not user_agent(request):
        return render_template("404.html")
    return jsonify({"ips":[]})

@api.route('/api/v1/common/incidentalert', methods=['POST'])
def incidentalert():
    if not user_agent(request):
        return render_template("404.html")
    return jsonify({"incidents":[]})

@api.route('/api/v1/common/ipwhitelist', methods=['GET'])
def ip_whitelist():
    if not user_agent(request):
        return render_template("404.html")
    return jsonify({"ips":[]})

@api.route('/api/v1/common/inventory', methods=['POST', 'GET'])
def inventory():
    if not user_agent(request):
        return render_template("404.html")
    with open("website/data/hosts.json", 'r') as f:
        hosts = load(f)["hosts"]

    print(request.data)
    a = loads(request.data)
    
    entered = False
    for host in hosts:
        if host["name"] == a["name"]:
            entered = True
            for item in a:
                host[item] = a[item]

    if not entered:
        hosts.append(a)
    
    json_to_write = dumps({"hosts": hosts}, indent=4)

    with open("website/data/hosts.json", "w") as f:
        f.write(json_to_write)

    return jsonify({"hosts": hosts})
 
