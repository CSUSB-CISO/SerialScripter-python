from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from json import load

auth = Blueprint('api', __name__)

@auth.route('/api/v1/wingoEDR/updateconfig', methods=['GET'])
def update_config():
    return jsonify({})

@auth.route('/api/v1/wingoEDR/systemhealth/diskspace', methods=['POST'])
def disk_space():
    return jsonify({})

@auth.route('/api/v1/wingoEDR/systemhealth/diskusage', methods=['POST'])
def disk_usage():
    return jsonify({})

@auth.route('/api/v1/wingoEDR/activeshares', methods=['POST'])
def active_shares():
    with open("website/data/hosts.json", 'r') as f:
        hosts = load(f)["hosts"]
    return jsonify({})

@auth.route('/api/v1/wingoEDR/errors', methods=['POST'])
def errors():
    return jsonify({})

@auth.route('/api/v1/common/heartbeat', methods=['POST'])
def heartbeat():
    return jsonify({})

@auth.route('/api/v1/common/ipblacklist', methods=['GET'])
def ip_blacklist():
    return jsonify({[]})

@auth.route('/api/v1/common/incidentalert', methods=['POST'])
def incidentalert():
    return jsonify({[]})

@auth.route('/api/v1/common/ipwhitelist', methods=['GET'])
def ip_whitelist():
    return jsonify({[]})