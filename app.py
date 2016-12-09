import tarfile, boto3, json
from cStringIO import StringIO
from flask import Flask, send_file
app = Flask(__name__)

@app.route("/")
def index():
    ecr = boto3.client('ecr')
    data = {
        "auths": {
            auth.get("proxyEndpoint"): {"auth": auth.get("authorizationToken"), "email": None} for auth in ecr.get_authorization_token().get("authorizationData")
        }
    }
    data = json.dumps(data)
    out = tarfile.open('/tmp/docker.tar.gz', mode='w:gz')
    try:
        info = tarfile.TarInfo('.docker/config.json')
        info.size = len(data)
        out.addfile(info, StringIO(data))
    finally:
        out.close()
    
    return send_file("/tmp/docker.tar.gz", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)