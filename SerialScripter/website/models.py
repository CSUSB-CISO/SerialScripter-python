from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from random import randint
from sqlalchemy import or_, and_

class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # type of column is integer and foreign key means that we must pass a valid id of existing user to that column
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    keys = db.relationship('Key')

class IPs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15))
    type = db.Column(db.String(10))  # "blacklist" or "whitelist"



class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    port = db.Column(db.Integer)
    name = db.Column(db.String)

    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
    host = db.relationship('Host', back_populates='services')

class Share(db.Model):
    __tablename__ = 'shares'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    fullpath = db.Column(db.String)
    SMBversion = db.Column(db.String)

    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
    host = db.relationship('Host', back_populates='shares')

    permissions = db.relationship('Permission', back_populates='share')

class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)

    share_id = db.Column(db.Integer, db.ForeignKey('shares.id'))
    share = db.relationship('Share', back_populates='permissions')

    users = db.relationship('RemoteUser', back_populates='permission')

class RemoteUser(db.Model):
    __tablename__ = 'remote_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)

    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))
    permission = db.relationship('Permission', back_populates='users')

class Docker(db.Model):
    __tablename__ = 'dockers'

    id = db.Column(db.Integer, primary_key=True)

    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
    host = db.relationship('Host', back_populates='docker')

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)

    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
    host = db.relationship('Host', back_populates='tasks')

class Firewall(db.Model):
    __tablename__ = 'firewalls'

    id = db.Column(db.Integer, primary_key=True)

    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
    host = db.relationship('Host', back_populates='firewall')
class Host(db.Model):
    __tablename__ = 'hosts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    ip = db.Column(db.String)
    os = db.Column(db.String)
    hostname = db.Column(db.String)
    changed_password = db.Column(db.Boolean, server_default="f", default=False)
    added_ssh_key = db.Column(db.Boolean, server_default="f", default=False)


    services = db.relationship('Service', back_populates='host')
    isOn = db.Column(db.Boolean)
    docker = db.relationship('Docker', back_populates='host')
    tasks = db.relationship('Task', back_populates='host')
    firewall = db.relationship('Firewall', back_populates='host')
    shares = db.relationship('Share', back_populates='host')

class Alert(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String)
    name = db.Column(db.String)
    user = db.Column(db.String)
    process = db.Column(db.String)
    remote_ip = db.Column(db.String)
    cmd = db.Column(db.String)
    type = db.Column(db.String)



def create_service_from_dict(service):
    # Create a Service object and set its attributes
    s = Service()
    s.port = service.get("port")
    s.name = service.get("service")
    return s

def create_docker_from_dict(docker):
    # Create a Docker object and set its attributes
    d = Docker()
    # Set attributes of d here
    return d

def create_task_from_dict(task):
    # Create a Task object and set its attributes
    t = Task()
    # Set attributes of t here
    return t

def create_firewall_from_dict(firewall):
    # Create a Firewall object and set its attributes
    f = Firewall()
    # Set attributes of f here
    return f

def create_share_from_dict(share):
    # Create a Share object and set its attributes
    s = Share()
    s.name = share.get("name")
    s.fullpath = share.get("fullpath")
    s.SMBversion = share.get("SMBversion")
    s.permissions = [create_permission_from_dict(permission) for permission in share.get("permissions")]
    return s

def create_permission_from_dict(permission):
    # Create a Permission object and set its attributes
    p = Permission()
    p.users = [create_remote_user_from_dict(user) for user in permission.get("users")]
    # Set attributes of p here
    return p

def create_remote_user_from_dict(user):
    # Create a RemoteUser object and set its attributes
    u = RemoteUser()
    u.username = user.get("username")
    return u

def create_host_from_dict(dict):
    # Create host object and set its attributes
    host = Host()
    # host.id = randint(0,65535)
    host.name = dict.get("name")
    host.ip = dict.get("ip")
    host.os = dict.get("OS")
    host.hostname = dict.get("hostname")
    host.changed_password = dict.get("isOn")
    host.added_ssh_key = dict.get("isOn")

    # Create a Service object for each service in the dict
    # and add it to the host.services list
    try:
        host.services = [create_service_from_dict(service) for service in dict.get("services")]
    except TypeError:
        print("No services")
    # Set the host.isOn attribute
    host.isOn = dict.get("isOn")

    # Create a Docker object for each docker in the dict
    # and add it to the host.docker list
    try:
        host.docker = [create_docker_from_dict(docker) for docker in dict.get("docker")]
    except TypeError as e:
        print("No dockers ")

    # Create a Task object for each task in the dict
    # and add it to the host.tasks list
    try:
        host.tasks = [create_task_from_dict(task) for task in dict.get("tasks")]
    except TypeError as e:
        print("No tasks")
    # Create a Firewall object for each firewall in the dict
    # and add it to the host.firewall list

    try:
        host.firewall = [create_firewall_from_dict(firewall) for firewall in dict.get("firewall")]
    except TypeError as e:
        print("No Firewall")

    # create a Share object for each dictionary in the "shares" list

    try:
        host.shares = [create_share_from_dict(share) for share in dict.get("shares")]
    except TypeError as e:
        print("No shares ")

    return host

def from_host_to_dict(host):
    # Create a dictionary with the host's name, ip, OS, and hostname attributes
    host_dict = {
        "name": host.name,
        "ip": host.ip,
        "OS": host.os,
        "hostname": host.hostname,
        "changed_password": host.changed_password,
        "added_ssh_key": host.added_ssh_key
    }
    # Create a dictionary for each service in the host's services list
    # and add it to the host_dict["services"] list
    host_dict["services"] = [{"port": s.port, "service": s.name} for s in host.services]

    # Set the host_dict["isOn"] attribute
    host_dict["isOn"] = host.isOn

    # Create a dictionary for each docker in the host's docker list
    # and add it to the host_dict["docker"] list
    host_dict["docker"] = [{} for d in host.docker]

    # Create a dictionary for each task in the host's tasks list
    # and add it to the host_dict["tasks"] list
    host_dict["tasks"] = [{} for t in host.tasks]

    # Create a dictionary for each firewall in the host's firewall list
    # and add it to the host_dict["firewall"] list
    host_dict["firewall"] = [{} for f in host.firewall]

    # Create a dictionary for each share in the host's shares list
    # and add it to the host_dict["shares"] list
    host_dict["shares"] = [
        {
            "name": s.name, "fullpath": s.fullpath, "SMBversion": s.SMBversion, "permissions": [
                {
                    "users": [
                        {
                            "username": u.username
                        } for u in p.users
                    ] 
                } for p in s.permissions
            ]
        } for s in host.shares]

    return host_dict


import re
def search_alerts(search_string):
    search_terms = re.findall(r'([^\s:]+):([^\s]+)', search_string)
    filters = []
    for term in search_terms:
        column, value = term
        column = column.lower()
        if column == 'host':
            filters.append(Alert.host.like(f'%{value}%'))
        elif column == 'name':
            filters.append(Alert.name.like(f'%{value}%'))
        elif column == 'user':
            filters.append(Alert.user.like(f'%{value}%'))
        elif column == 'process':
            filters.append(Alert.process.like(f'%{value}%'))
        elif column == 'remoteip':
            filters.append(Alert.remote_ip.like(f'%{value}%'))
        elif column == 'cmd':
            filters.append(Alert.cmd.like(f'%{value}%'))
        elif column == 'type':
            filters.append(Alert.type.like(f'%{value}%'))

    # If no search terms were found, search all columns
    if not filters:
        filters = [
            Alert.host.like(f'%{search_string}%'),
            Alert.name.like(f'%{search_string}%'),
            Alert.user.like(f'%{search_string}%'),
            Alert.process.like(f'%{search_string}%'),
            Alert.remote_ip.like(f'%{search_string}%'),
            Alert.cmd.like(f'%{search_string}%'),
            Alert.type.like(f'%{search_string}%')
        ]

    return Alert.query.filter(or_(*filters)).all()
