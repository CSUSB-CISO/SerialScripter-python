from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from random import randint
from sqlalchemy import or_, and_
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

# # users that exist on each host
# class EnumeratedUser(db.Model):
#     __tablename__ = 'enumerated_users'

#     id = db.Column(db.Integer, primary_key=True)

#     # each of these columns are attributes of an enumerated user from a specific box
#     username = db.Column(db.String)
#     fullname = db.Column(db.String)
#     enabled = db.Column(db.Boolean, server_default="f", default=False)
#     locked = db.Column(db.Boolean, server_default="f", default=False)
#     admin = db.Column(db.Boolean, server_default="f", default=False)
#     passwordExpired = db.Column(db.Boolean, server_default="f", default=False)
#     cantChangePass = db.Column(db.Boolean, server_default="f", default=False)
#     passwordAge = db.Column(db.Integer)
#     lastLogon = db.Column(db.String)
#     badPasswdAttempts = db.Column(db.Integer)
#     numLogons = db.Column(db.Integer)

#     # defines the relationship between host object and enumerated user
#     # which is one to many meaning host object can have many enumerated users, but the users can only be tied to one host 
#     host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
#     host = db.relationship('Host', back_populates='enumerated_users')

# class Share(db.Model):
#     __tablename__ = 'shares'

#     id = db.Column(db.Integer, primary_key=True)
#     NetName = db.Column(db.String) 
#     Remark = db.Column(db.String) 
#     Path = db.Column(db.String)
#     Type = db.Column(db.Integer)
#     Permissions = db.Column(db.Integer) 
#     MaxUses = db.Column(db.Integer)
#     CurrentUses = db.Column(db.Integer)

#     host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
#     host = db.relationship('Host', back_populates='shares')

# users that are a part of shares
# class RemoteUser(db.Model):
#     __tablename__ = 'remote_users'

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String)
#     permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))
#     permission = db.relationship('Permission', back_populates='users')

# class Docker(db.Model):
#     __tablename__ = 'dockers'

#     id = db.Column(db.Integer, primary_key=True)

#     host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
#     host = db.relationship('Host', back_populates='docker')

# class Task(db.Model):
#     __tablename__ = 'tasks'

#     id = db.Column(db.Integer, primary_key=True)

#     host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
#     host = db.relationship('Host', back_populates='tasks')

# class Firewall(db.Model):
#     __tablename__ = 'firewalls'

#     id = db.Column(db.Integer, primary_key=True)

#     host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
#     host = db.relationship('Host', back_populates='firewall')

# class Host(db.Model):
#     __tablename__ = 'hosts'

#     # these columns are one to one
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True)
#     ip = db.Column(db.String)
#     os = db.Column(db.String)
#     hostname = db.Column(db.String)
#     changed_password = db.Column(db.Boolean, server_default="f", default=False)
#     is_connected = db.Column(db.Boolean, server_default="f", default=False)
#     time_connected = db.Column(db.String, default="")

#     # relationship() is defined as a one to many relationship meaning the host class can have many services, but each
#     # service can only be tied to one host
#     services = db.relationship('Service', back_populates='host')
#     isOn = db.Column(db.Boolean)
#     docker = db.relationship('Docker', back_populates='host')
#     tasks = db.relationship('Task', back_populates='host')
#     firewall = db.relationship('Firewall', back_populates='host')
#     shares = db.relationship('Share', back_populates='host')
#     enumerated_users = db.relationship('EnumeratedUser', back_populates='host')

class Alert(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    host = db.Column(db.String)
    name = db.Column(db.String)
    current_time = db.Column(db.String)
    user = db.Column(db.String)
    severity = db.Column(db.String)
    payload = db.Column(db.String)

def create_service_from_dict(service):
    # Create a Service object and set its attributes
    s = Service()
    s.port = service.get("port")
    s.name = service.get("service")
    s.shortName = service.get("SCname")
    s.descriptiveName = service.get("DisplayName")
    s.running = service.get("AcceptStop")
    s.PID = service.get("RunningPID")
    return s

def create_enumerated_user_from_dict(enumeratedUser):
    eU = EnumeratedUser()
    
    eU.username = enumeratedUser.get("Username") 
    eU.fullname = enumeratedUser.get("Fullname")
    eU.enabled = enumeratedUser.get("Enabled")  
    eU.locked = enumeratedUser.get("Locked")  
    eU.admin = enumeratedUser.get("Admin")  
    eU.passwordExpired = enumeratedUser.get("PasswdExpired")  
    eU.cantChangePass = enumeratedUser.get("CantChangePasswd")  
    eU.passwordAge = enumeratedUser.get("PasswdAge") 
    eU.lastLogon = enumeratedUser.get("LastLogon") 
    eU.numLogons = enumeratedUser.get("NumOfLogons")

    return eU 

def create_docker_from_dict(docker):
    # Create a Docker object and set its attributes
    d = Docker()
    # Set attributes of d here
    return d

# def create_task_from_dict(task):
#     # Create a Task object and set its attributes
#     t = Task()
#     # Set attributes of t here
#     return t

def create_firewall_from_dict(firewall):
    # Create a Firewall object and set its attributes
    f = Firewall()
    # Set attributes of f here
    return f

def create_share_from_dict(share):
    # Create a Share object and set its attributes
    s = Share()

    s.NetName = share.get("NetName")  
    s.Remark = share.get("Remark")  
    s.Path = share.get("Path") 
    s.Type = share.get("Type") 
    s.Permissions = share.get("Permissions")  
    s.MaxUses = share.get("MaxUses") 
    s.CurrentUses = share.get("CurrentUses") 
    
    return s

# def create_permission_from_dict(permission):
#     # Create a Permission object and set its attributes
#     p = Permission()
#     p.users = [create_remote_user_from_dict(user) for user in permission.get("users")]
#     # Set attributes of p here
#     return p

# def create_remote_user_from_dict(user):
#     # Create a RemoteUser object and set its attributes
#     u = RemoteUser()
#     u.username = user.get("username")
#     return u

def create_host_from_dict(dict):
    # Create host object and set its attributes
    host = Host()
    # host.id = randint(0,65535)
    host.name = dict.get("name")
    host.ip = dict.get("ip")
    host.os = dict.get("OS")
    host.hostname = dict.get("hostname")
    host.changed_password = dict.get("isChanged")
    host.is_connected = dict.get("isConnected")
    host.time_connected = dict.get("timeConnected")

    # Create a Service object for each service in the dict
    # and add it to the host.services list
    try:
        host.services = [create_service_from_dict(service) for service in dict.get("services")]
    except TypeError:
        pass
    # Set the host.isOn attribute
    host.isOn = dict.get("isOn")

    # creates new enumerated user tables for each user on specified box
    try:
        host.enumerated_users = [create_enumerated_user_from_dict(enumeratedUser) for enumeratedUser in dict.get("users")]
    except:
        pass
    # Create a Docker object for each docker in the dict
    # and add it to the host.docker list
    try:
        host.docker = [create_docker_from_dict(docker) for docker in dict.get("docker")]
    except TypeError as e:
        pass

    # Create a Task object for each task in the dict
    # and add it to the host.tasks list
    try:
        host.tasks = [create_task_from_dict(task) for task in dict.get("tasks")]
    except TypeError as e:
        pass
    # Create a Firewall object for each firewall in the dict
    # and add it to the host.firewall list

    try:
        host.firewall = [create_firewall_from_dict(firewall) for firewall in dict.get("firewall")]
    except TypeError as e:
        pass

    # create a Share object for each dictionary in the "shares" list

    try:
        host.shares = [create_share_from_dict(share) for share in dict.get("shares")]
    except TypeError as e:
        pass

    return host

def from_host_to_dict(host):
    # Create a dictionary with the host's name, ip, OS, and hostname attributes
    host_dict = {
        "name": host.name,
        "ip": host.ip,
        "OS": host.os,
        "hostname": host.hostname,
        "isChanged": host.changed_password,
        "isConnected": host.is_connected,
        "timeConnected": host.time_connected
    }
    # Create a dictionary for each service in the host's services list
    # and add it to the host_dict["services"] list
    host_dict["services"] = [
        {
        "port": s.port,
        "service": s.name,
        "SCname": s.shortName,
        "DisplayName": s.descriptiveName,
        "AcceptStop": s.running,
        "RunningPID": s.PID,
        } for s in host.services]

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

    host_dict["users"] = [
        {
            "Username": u.username,
            "Fullname": u.fullname,
            "Enabled": u.enabled,
            "Locked": u.locked,
            "Admin": u.admin,
            "PasswdExpired": u.passwordExpired,
            "CantChangePasswd": u.cantChangePass,
            "PasswdAge": u.passwordAge,
            "LastLogon": u.lastLogon,
            "NumOfLogons": u.numLogons
        } for u in host.enumerated_users]

    # Create a dictionary for each share in the host's shares list
    # and add it to the host_dict["shares"] list
    host_dict["shares"] = [
        {
            "NetName": s.NetName,
            "Remark": s.Remark,
            "Path": s.Path,
            "Type": s.Type,
            "Permissions": s.Permissions,
            "MaxUses": s.MaxUses,
            "CurrentUses": s.CurrentUses,

        } for s in host.shares]

    return host_dict

def get_incidents():
    alerts = Alert.query.all()
    return [{"Alert": {
                "Host": alert.host,
                "Incident": {
                    "Name": alert.name,
                    "CurrentTime": alert.current_time,
                    "User": alert.user,
                    "Severity": alert.severity,
                    "Payload": alert.payload
                }
            }
            } for alert in alerts]

class IPs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15))
    type = db.Column(db.String(10))  # "blacklist" or "whitelist"



class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    port = db.Column(db.Integer)
    name = db.Column(db.String)
    shortName = db.Column(db.String)
    descriptiveName = db.Column(db.String)
    running = db.Column(db.Boolean)
    PID = db.Column(db.Integer)

    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
    host = db.relationship('Host', back_populates='services')

# users that exist on each host
class EnumeratedUser(db.Model):
    __tablename__ = 'enumerated_users'

    id = db.Column(db.Integer, primary_key=True)

    # each of these columns are attributes of an enumerated user from a specific box
    username = db.Column(db.String)
    fullname = db.Column(db.String)
    enabled = db.Column(db.Boolean, server_default="f", default=False)
    locked = db.Column(db.Boolean, server_default="f", default=False)
    admin = db.Column(db.Boolean, server_default="f", default=False)
    passwordExpired = db.Column(db.Boolean, server_default="f", default=False)
    cantChangePass = db.Column(db.Boolean, server_default="f", default=False)
    passwordAge = db.Column(db.String)
    lastLogon = db.Column(db.String)
    badPasswdAttempts = db.Column(db.String)
    numLogons = db.Column(db.Integer)

    # defines the relationship between host object and enumerated user
    # which is one to many meaning host object can have many enumerated users, but the users can only be tied to one host 
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
    host = db.relationship('Host', back_populates='enumerated_users')

class Share(db.Model):
    __tablename__ = 'shares'

    id = db.Column(db.Integer, primary_key=True)
    NetName = db.Column(db.String) 
    Remark = db.Column(db.String) 
    Path = db.Column(db.String)
    Type = db.Column(db.Integer)
    Permissions = db.Column(db.Integer) 
    MaxUses = db.Column(db.Integer)
    CurrentUses = db.Column(db.Integer)

    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
    host = db.relationship('Host', back_populates='shares')

class Docker(db.Model):
    __tablename__ = 'dockers'

    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    status = db.Column(db.String)
    health = db.Column(db.String)
    dockerId = db.Column(db.String)
    cmd = db.Column(db.String)
    ports = db.Column(db.String)

    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
    host = db.relationship('Host', back_populates='dockers')


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    Version = db.Column(db.String)
    InstallPath = db.Column(db.String)
    Publisher = db.Column(db.String)
    UninstallString = db.Column(db.String)

    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
    host = db.relationship('Host', back_populates='applications')
class Firewall(db.Model):
    __tablename__ = 'firewalls'

    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    Description =  db.Column(db.String)
    ApplicationName =  db.Column(db.String)
    ServiceName =  db.Column(db.String)
    LocalPorts =  db.Column(db.String)
    RemotePorts =  db.Column(db.String)
    LocalAddresses =  db.Column(db.String)
    RemoteAddresses =  db.Column(db.String)
    Profile =  db.Column(db.Integer)

    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
    host = db.relationship('Host', back_populates='firewalls')
class Host(db.Model):
    __tablename__ = 'hosts'

    # these columns are one to one
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    ip = db.Column(db.String)
    os = db.Column(db.String)
    hostname = db.Column(db.String)
    changed_password = db.Column(db.Boolean, server_default="f", default=False)
    is_connected = db.Column(db.Boolean, server_default="f", default=False)
    time_connected = db.Column(db.String, default="")

    # relationship() is defined as a one to many relationship meaning the host class can have many services, but each
    # service can only be tied to one host
    services = db.relationship('Service', back_populates='host')
    isOn = db.Column(db.Boolean)
    dockers = db.relationship('Docker', back_populates='host')
    # tasks = db.relationship('Task', back_populates='host')
    firewalls = db.relationship('Firewall', back_populates='host')
    applications = db.relationship('Application', back_populates='host')
    shares = db.relationship('Share', back_populates='host')
    enumerated_users = db.relationship('EnumeratedUser', back_populates='host')


def create_service_from_dict(service):
    # Create a Service object and set its attributes
    s = Service()
    s.port = service.get("port")
    s.name = service.get("service")
    s.shortName = service.get("SCname")
    s.descriptiveName = service.get("DisplayName")
    s.running = service.get("AcceptStop")
    s.PID = service.get("RunningPID")
    return s

def create_enumerated_user_from_dict(enumeratedUser):
    eU = EnumeratedUser()
    
    eU.username = enumeratedUser.get("Username") 
    eU.fullname = enumeratedUser.get("Fullname")
    eU.enabled = enumeratedUser.get("Enabled")  
    eU.locked = enumeratedUser.get("Locked")  
    eU.admin = enumeratedUser.get("Admin")  
    eU.passwordExpired = enumeratedUser.get("PasswdExpired")  
    eU.cantChangePass = enumeratedUser.get("CantChangePasswd")  
    eU.passwordAge = enumeratedUser.get("PasswdAge") 
    eU.lastLogon = enumeratedUser.get("LastLogon") 
    eU.numLogons = enumeratedUser.get("NumOfLogons")
    eU.badPasswdAttempts = enumeratedUser.get("BadPasswdAttempts")

    return eU 

def create_docker_from_dict(docker):
    # Create a Docker object and set its attributes
    d = Docker()
    # Set attributes of d here

    d.Name = docker.get("name")
    d.status = docker.get("status")
    d.health = docker.get("health")
    d.dockerId = docker.get("dockerId")
    d.cmd = docker.get("cmd")
    d.ports = docker.get("ports")

    return d

def create_application_from_dict(application):

    a = Application()

    a.Name = application.get("Name")
    a.Version = application.get("Version")
    a.InstallPath = application.get("InstallPath")
    a.Publisher = application.get("Publisher")
    a.UninstallString = application.get("UninstallString")

    return a

def create_firewall_from_dict(firewall):
    # Create a Firewall object and set its attributes
    f = Firewall()
    # Set attributes of f here

    f.Name = firewall.get("Name")             
    f.Description = firewall.get("Description")      
    f.ApplicationName = firewall.get("ApplicationName")  
    f.ServiceName = firewall.get("ServiceName")      
    f.LocalPorts = firewall.get("LocalPorts")       
    f.RemotePorts = firewall.get("RemotePorts")      
    f.LocalAddresses = firewall.get("LocalAddresses")   
    f.RemoteAddresses = firewall.get("RemoteAddresses")  
    f.Profile = firewall.get("Profile")          

    return f

def create_share_from_dict(share):
    # Create a Share object and set its attributes
    s = Share()

    s.NetName = share.get("NetName")  
    s.Remark = share.get("Remark")  
    s.Path = share.get("Path") 
    s.Type = share.get("Type") 
    s.Permissions = share.get("Permissions")  
    s.MaxUses = share.get("MaxUses") 
    s.CurrentUses = share.get("CurrentUses") 
    
    return s

# def create_permission_from_dict(permission):
#     # Create a Permission object and set its attributes
#     p = Permission()
#     p.users = [create_remote_user_from_dict(user) for user in permission.get("users")]
#     # Set attributes of p here
#     return p

# def create_remote_user_from_dict(user):
#     # Create a RemoteUser object and set its attributes
#     u = RemoteUser()
#     u.username = user.get("username")
#     return u

def create_host_from_dict(dict):
    # Create host object and set its attributes
    host = Host()
    # host.id = randint(0,65535)
    host.name = dict.get("name")
    host.ip = dict.get("ip")
    host.os = dict.get("OS")
    host.hostname = dict.get("hostname")
    host.changed_password = dict.get("isChanged")
    host.is_connected = dict.get("isConnected")
    host.time_connected = dict.get("timeConnected")

    # Create a Service object for each service in the dict
    # and add it to the host.services list
    try:
        host.services = [create_service_from_dict(service) for service in dict.get("services")]
    except TypeError:
        pass
    # Set the host.isOn attribute
    host.isOn = dict.get("isOn")

    # creates new enumerated user tables for each user on specified box
    try:
        host.enumerated_users = [create_enumerated_user_from_dict(enumeratedUser) for enumeratedUser in dict.get("users")]
    except:
        pass
    # Create a Docker object for each docker in the dict
    # and add it to the host.docker list
    try:
        host.dockers = [create_docker_from_dict(docker) for docker in dict.get("containers")]
        # print("created docker")
    except TypeError as e:
        # print(f"{str(e)}")
        pass

    
    # create application object from dict
    try:
        host.applications = [create_application_from_dict(application) for application in dict.get("InstalledSoftware")]
    except Exception as e:
        # print(f"{e} \nError with application table")
        pass

    # Create a Firewall object for each firewall in the dict
    # and add it to the host.firewall list

    try:
        host.firewalls = [create_firewall_from_dict(firewall) for firewall in dict.get("FirewallList")]
    except Exception as e:
        # print(f"{e} \nError with firewall table")
        pass

    # create a Share object for each dictionary in the "shares" list

    try:
        host.shares = [create_share_from_dict(share) for share in dict.get("shares")]
    except TypeError as e:
        pass

    return host

def from_host_to_dict(host):
    # Create a dictionary with the host's name, ip, OS, and hostname attributes
    host_dict = {
        "name": host.name, 
        "ip": host.ip,
        "OS": host.os,
        "hostname": host.hostname,
        "isChanged": host.changed_password,
        "isConnected": host.is_connected,
        "timeConnected": host.time_connected
    }
    # Create a dictionary for each service in the host's services list
    # and add it to the host_dict["services"] list
    host_dict["services"] = [
        {
        "port": s.port,
        "service": s.name,
        "SCname": s.shortName,
        "DisplayName": s.descriptiveName,
        "AcceptStop": s.running,
        "RunningPID": s.PID,
        } for s in host.services]

    # Set the host_dict["isOn"] attribute
    host_dict["isOn"] = host.isOn

    # Create a dictionary for each docker in the host's docker list
    # and add it to the host_dict["docker"] list
    # host_dict["docker"] = [{} for d in host.docker]

    # Create a dictionary for each task in the host's tasks list
    # and add it to the host_dict["tasks"] list
    # host_dict["tasks"] = [{} for t in host.tasks]

    # Create a dictionary for each firewall in the host's firewall list
    # and add it to the host_dict["firewall"] list
    host_dict["FirewallList"] = [
        {
            "Name": f.Name,
            "Description": f.Description,
            "ApplicationName": f.ApplicationName,
            "ServiceName": f.ServiceName,
            "LocalPorts": f.LocalPorts,
            "RemotePorts": f.RemotePorts,
            "LocalAddresses": f.LocalAddresses,
            "RemoteAddresses": f.RemoteAddresses,
            "Profile": f.Profile
    } for f in host.firewalls]

    host_dict["InstalledSoftware"] = [
        {
            "Name": a.Name,
            "Version": a.Version,
            "InstallPath": a.InstallPath,
            "Publisher": a.Publisher,
            "UninstallString": a.UninstallString,

    } for a in host.applications]

    host_dict["users"] = [
        {
            "Username": u.username,
            "Fullname": u.fullname,
            "Enabled": u.enabled,
            "Locked": u.locked,
            "Admin": u.admin,
            "PasswdExpired": u.passwordExpired,
            "CantChangePasswd": u.cantChangePass,
            "PasswdAge": u.passwordAge,
            "LastLogon": u.lastLogon,
            "NumOfLogons": u.numLogons,
            "BadPasswdAttempts": u.badPasswdAttempts,
        } for u in host.enumerated_users]

    # Create a dictionary for each share in the host's shares list
    # and add it to the host_dict["shares"] list
    host_dict["shares"] = [
        {
            "NetName": s.NetName,
            "Remark": s.Remark,
            "Path": s.Path,
            "Type": s.Type,
            "Permissions": s.Permissions,
            "MaxUses": s.MaxUses,
            "CurrentUses": s.CurrentUses,

        } for s in host.shares]

    host_dict["containers"] = [
        {
            "name": d.Name,
            "status": d.status,
            "health": d.health,
            "dockerId": d.dockerId,
            "cmd": d.cmd,
            "ports": d.ports

        } for d in host.dockers]

    return host_dict
