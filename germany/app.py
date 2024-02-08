import os
import json
import secrets
import uuid

import flask

# Create a Flask Application
app = flask.Flask(__name__)

secret_key = secrets.token_urlsafe(32)
app.secret_key = secret_key
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = secret_key


@app.route('/map')
def map_json():
    path = f'{os.getcwd()}/germany/data'
    with open(f'{path}/relation/rel.json', 'r') as f:
        relations = json.loads(f.read()).get('relation')

    findings = []
    for cfile in os.listdir(f'{path}/json'):
        print(f'Parsing {cfile}')
        with open(f'{path}/json/{cfile}', 'r') as f:
            data = json.loads(f.read())
        parse_json(data, relations, findings)

    if findings:
        print('Wrote the findings to the file.')
        with open(f'{path}/output/{uuid.uuid4()}.json', 'w') as f:
            f.write(json.dumps(findings, indent=4))
    return "Something i am doing...."


def parse_json(data, relations, findings):
    if isinstance(data, dict):
        for key, value in data.items():
            if key in relations:
                findings.append(data)
            elif value and isinstance(value, (list, dict)):
                parse_json(value, relations, findings)
    elif isinstance(data, list):
        for li in data:
            if li:
                parse_json(li, relations, findings)
    return None


@app.route('/status')
def status():
    return 'Welcome to Flask Application...'


@app.route('/')
def search():
    return flask.render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
