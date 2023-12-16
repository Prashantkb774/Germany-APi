import secrets

import flask

# Create a Flask Application
app = flask.Flask(__name__)

secret_key = secrets.token_urlsafe(32)
app.secret_key = secret_key
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = secret_key


@app.route('/status')
def status():
    return 'Welcome to Flask Application...'


@app.route('/')
def search():
    return flask.render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
