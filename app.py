#!/usr/bin/env python

import argparse
import json
import os

from flask import Flask, render_template, request, make_response, Response

import utils


app = Flask(__name__)
app.debug=True

@app.route('/elections/<raceyear>/nobake/', methods=['GET'])
def index(raceyear):

    context = utils.build_context()
    context['racedate'] = None

    return render_template('index.html', **context)

@app.route('/elections/<raceyear>/nobake/<racedate>/', methods=['GET'])
def racedate(raceyear, racedate):

    context = utils.build_context()
    context['racedate'] = racedate

    return render_template('index.html', **context)

@app.route('/elections/<raceyear>/nobake/<racedate>/script/<script_type>/', methods=['GET'])
def scripts(racedate, script_type, raceyear):
    base_command = '. /home/ubuntu/.virtualenvs/loaderpypy/bin/activate && cd /home/ubuntu/elex-loader/ && '
    if request.method == 'GET':
        o = "1"

        if script_type == 'bake':
            pass
        else:
            o = os.system('%s./scripts/prd/%s.sh %s' % (base_command, script_type, racedate))

        return json.dumps({"message": "success", "output": o})


@app.route('/elections/<raceyear>/nobake/loader/timeout/', methods=['POST'])
def set_loader_timeout(raceyear):
    if request.method == 'POST':
        payload = utils.clean_payload(dict(request.form))

        timeout = payload.get('timeout', '')
        os.system('echo export ELEX_LOADER_TIMEOUT=%s > /tmp/elex_loader_timeout.sh' % timeout)

        return json.dumps({"message": "success", "output": "0"})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port')
    args = parser.parse_args()
    server_port = 8000

    if args.port:
        server_port = int(args.port)

    app.run(host='0.0.0.0', port=server_port, debug=True)
