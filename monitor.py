from unicodedata import normalize
from flask import Flask, jsonify, request
from flask_cors import CORS
from circus_api.client import Client


client = None
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


def stringify(s):
    return normalize('NFKD', s).encode('ascii', 'ignore')


def shutdown_server():
    f = request.environ.get('werkzeug.server.shutdown')
    if f is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    #client.quit()
    f()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Shutdown server after finishing handling the current request"""
    shutdown_server()
    return 'Monitor shutting down...\n'


@app.route('/all', methods=['GET'])
def all():
    """Get all informations on one route"""
    watchers = {}
    for w in client.list():
        watchers[w] = {}
        watchers[w]['status'] = client.status(w)
        watchers[w]['pids'] = client.list(w)
        watchers[w]['cmd'] = client.options(w)['cmd']
        watchers[w]['args'] = client.options(w)['args']
    return jsonify(watchers)


@app.route('/stats/<watcher>', methods=['GET'])
def stats_handler(watcher):
    """Get stats about a watcher"""
    return jsonify(client.stats(stringify(watcher)))


@app.route('/watcher/<watcher>', methods=['GET', 'DELETE'])
def watcher_handler(watcher):
    """handle specific watcher given as parameter <watcher>
    GET     Retrieve a list of PIDs handled by watcher
    DELETE  Delete the watcher
    """
    watcher = stringify(watcher)
    if request.method == 'DELETE':
        """Delete a watcher"""
        if client.rm_watcher(watcher) is True:
            return jsonify({'status': 200, 'reason': 'Watcher deleted successfully'}), 200
        else:
            return jsonify({'status': 400, 'reason': 'Cannot delete watcher'}), 400
    else:
        """Get the list of PIDs handled by a watcher"""
        return jsonify({
                       'status': client.status(watcher),
                       'pids': client.list(watcher)
                       })


@app.route('/watchers', methods=['GET', 'POST'])
def watchers():
    """handle watchers
    GET     Retrieve watchers names list
    POST    Add a new watcher and start it
            Parameters  - name (string)
                        - command (string)
                        - args (array of strings)
    """
    if request.method == 'POST':
        if not request.json or \
                'name' not in request.json or \
                'command' not in request.json or \
                'args' not in request.json:
                    return jsonify({'status': 400, 'reason': 'Either [name|command|args] are missing'}), 400
        if client.add_watcher(name=stringify(request.json['name']),
                           command=stringify(request.json['command']),
                           args=request.json['args'],
                           autostart=True) is True:
            return jsonify({'status': 201, 'reason': 'Watcher created'}), 201
        else:
            return jsonify({'status': 400, 'reason': 'Cannot create watcher'}), 400
    else:
        return jsonify(client.status())


if __name__ == '__main__':
    client = Client(host='127.0.0.1', port=5555, timeout=15)
    app.run(port=8080, debug=False)
