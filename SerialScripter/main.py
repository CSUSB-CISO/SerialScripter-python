from os import environ
from website import create_app
from flask_bootstrap import Bootstrap


app = create_app()

if __name__ == '__main__':
    Bootstrap(app)
    port = int(environ.get("PORT", 10000))
    app.run(host='0.0.0.0', debug=True, port=port, ssl_context=('website/data/cert.pem', 'website/data/key.pem'))
