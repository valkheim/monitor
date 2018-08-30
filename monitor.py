import unicodedata
from flask import Flask, jsonify, request
from circus_api.client import Client

client = None
app = Flask(__name__)


def stringify(s):
    """Convert string from unicode to ascii charset"""
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')


def shutdown_server():
    """Shutdown server after finishing handling the current request"""
    f = request.environ.get('werkzeug.server.shutdown')
    if f is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    f()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Will shutdown server"""
    shutdown_server()
    return 'Monitor shutting down...\n'


@app.route('/stats/<watcher>', methods=['GET'])
def stats_handler(watcher):
    """Get stats about a watcher"""
    return jsonify(client.stats(stringify(watcher)))


@app.route('/watcher/<watcher>', methods=['GET', 'DELETE'])
def watcher_handler(watcher):
    if request.method == 'DELETE':
        """Delete a watcher"""
        if client.rm_watcher(watcher=stringify(watcher)) is True:
            return jsonify({'status': 200, 'reason': 'Watcher deleted successfully'}), 200
        else:
            return jsonify({'status': 400, 'reason': 'Cannot delete watcher'}), 400
    else:
        """Get the list of PIDs handled by a watcher"""
        return jsonify(client.list(watcher=stringify(watcher)))


@app.route('/watchers', methods=['GET', 'POST'])
def watchers():
    if request.method == 'POST':
        """Add a new watcher"""
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
        """Get the list of watchers names handled by the main arbiter"""
        return jsonify(client.list())

if __name__ == '__main__':
    client = Client(host='127.0.0.1', port=5555, timeout=15)
    app.run(port=8080, debug=False)
