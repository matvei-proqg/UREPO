from flask import Flask, jsonify, send_from_directory
from lib.core.repository import Repository
import os

app = Flask(__name__)
repo = Repository(os.getenv("REPO_ROOT", "/var/lib/repo"))

@app.route("/api/v1/packages")
def list_packages():
    db = repo._load_db()
    return jsonify(list(db.keys()))

@app.route("/api/v1/packages/<name>")
def package_info(name):
    db = repo._load_db()
    if name in db:
        return jsonify(db[name])
    return jsonify({"error": "Package not found"}), 404

@app.route("/packages/binary/<name>/<filename>")
def download_package(name, filename):
    path = os.path.join(repo.root_dir, "storage/binary", name)
    return send_from_directory(path, filename)

@app.route("/")
def index():
    return """
    <h1>Package Repository</h1>
    <p>API endpoints:</p>
    <ul>
        <li><a href="/api/v1/packages">/api/v1/packages</a> - List packages</li>
        <li>/api/v1/packages/&lt;name&gt; - Package info</li>
        <li>/packages/binary/&lt;name&gt;/&lt;file&gt; - Download package</li>
    </ul>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
