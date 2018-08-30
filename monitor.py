import unicodedata
from flask import Flask, jsonify, request
from circus_api.client import Client

client = None
app = Flask(__name__)


#client.add_watcher(name="a_watcher", command='bin/dummy', args=[], autostart=True)

#print client.list()
#print client.list(watcher="a_watcher")

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/watchers', methods=['GET', 'POST'])
def list_watcher():
    if request.method == 'POST':
        if not request.json or \
                'name' not in request.json or \
                'command' not in request.json or \
                'args' not in request.json:
                    return jsonify({"status": 400, "reason": "login is missing"}), 400
        client.add_watcher(name=unicodedata.normalize('NFKD', request.json['name']).encode('ascii', 'ignore'),
                           command=unicodedata.normalize('NFKD', request.json['command']).encode('ascii', 'ignore'),
                           args=request.json['args'],
                           autostart=True)
        return jsonify({"status": 201, "reason": "Watcher created"}), 201
    else:
        return jsonify(client.list())

if __name__ == '__main__':
    client = Client(host='127.0.0.1', port=5555, timeout=15)
    app.run(port=8080, debug=False)
