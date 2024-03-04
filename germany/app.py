import copy
import os
import json
import secrets

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

    findings = {}
    for cfile in os.listdir(f'{path}/json'):
        print(f'Parsing {cfile}')
        with open(f'{path}/json/{cfile}', 'r') as f:
            data = json.loads(f.read())
        system = cfile.rstrip('.json').upper()
        parse_json(data, relations, findings, system)

    if findings:
        print('Wrote the findings to the file.')
        with open(f'{path}/output/parsed_data.json', 'w') as f:
            f.write(json.dumps(findings, indent=4))
    return "Something i am doing...."


def parse_json(data, relations, findings, system):
    if isinstance(data, dict):
        for key, value in data.items():
            if key in relations:
                if value in findings:
                    findings[value].update(data)
                    if system not in findings[value]['system']:
                        findings[value]['system'].append(system)
                else:
                    findings[value] = copy.deepcopy(data)
                    findings[value].setdefault('system', [system])
            elif value and isinstance(value, (list, dict)):
                parse_json(value, relations, findings, system)
    elif isinstance(data, list):
        for li in data:
            if li:
                parse_json(li, relations, findings, system)


@app.route('/search/<query>', methods=['GET'])
def search(query):
    path = f'{os.getcwd()}/germany/data'
    with open(f'{path}/output/parsed_data.json', 'r') as f:
        data = json.loads(f.read())

    result = []
    for key, val in data.items():
        if query in key:
            result.append({
                'key': key,
                'system': ', '.join(val['system']),
                'version_number': val.get('versionNumber'),
                'status_level': val.get('statusLevel'),
                'access_status': val.get('accessStatus'),
                'process_control': val.get('processControl')
            })
            if len(result) > 10:
                break
    return {
        'items': result
    }


@app.route('/status')
def status():
    return 'Welcome to Flask Application...'


@app.route('/')
def search_page():
    return flask.render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
