from website import create_app
from flask_bootstrap import Bootstrap

app = create_app()

if __name__ == '__main__':
    Bootstrap(app)
    app.run(debug=True)
