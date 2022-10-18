from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from json import load, loads, dumps

from yaml import dump

api = Blueprint('api', __name__)

@api.route('/api/v1/wingoEDR/updateconfig', methods=['GET'])
def update_config():
    return jsonify({})

@api.route('/api/v1/wingoEDR/systemhealth/diskspace', methods=['POST'])
def disk_space():
    return jsonify({})

@api.route('/api/v1/wingoEDR/activeshares', methods=['POST'])
def active_shares():
    with open("website/data/hosts.json", 'r') as f:
        hosts = load(f)["hosts"]
    return jsonify({})

@api.route('/api/v1/wingoEDR/errors', methods=['POST'])
def errors():
    return jsonify({})

@api.route('/api/v1/common/heartbeat', methods=['POST'])
def heartbeat():
    return jsonify({})

@api.route('/api/v1/common/ipblacklist', methods=['GET', 'POST'])
def ip_blacklist():
    return jsonify({[]})

@api.route('/api/v1/common/incidentalert', methods=['POST'])
def incidentalert():
    return jsonify({[]})

# @api.route('/api/v1/common/ipwhitelist', methods=['GET'])
# def ip_whitelist():
#     return jsonify({[]})

@api.route('/api/v1/common/inventory', methods=['POST', 'GET'])
def ip_whitelist():
    with open("website/data/hosts.json", 'r') as f:
        hosts = load(f)["hosts"]

    a = loads(request.data)
    for host in hosts:
        if host["name"] == a["name"]:
            for item in a:
                host[item] = a[item]
            
    json_to_write = dumps({"hosts": hosts}, indent=4)

    with open("website/data/hosts.json", "w") as outfile:
        outfile.write(json_to_write)

    return jsonify(hosts)
