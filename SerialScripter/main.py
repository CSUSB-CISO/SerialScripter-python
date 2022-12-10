from os import environ
from os.path import exists
from website import create_app
from flask_bootstrap import Bootstrap


app = create_app()

# if the file doesn't exist then create it and fill it with base info
if not exists("website/data/users.json"):
    with open("website/data/users.json", 'w') as j:
        j.write('{"hosts":[{"hostname": "host-80", "users": [{"Username": "Isaac", "Fullname": "Isaac Cumsalot", "Enabled": "True", "Admin": "False", "Passwdage": "2 years", "LastLogon": "12/69/02", "BadPasswdAttempts": "69", "NumofLogons": "420"}]}]}')


if __name__ == '__main__':
    Bootstrap(app)
    port = int(environ.get("PORT", 10000))
    app.run(host='0.0.0.0', debug=True, port=port, ssl_context=('website/data/cert.pem', 'website/data/key.pem'))
