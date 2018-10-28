from .middlewares import login_required
from flask import Flask, json, g, request
from app.kudo.service import Service as Kudo
from app.kudo.schema import GithubRepoSchema

app = Flask(__name__)

@app.route("/kudos", methods=["GET"])
@login_required
def index():
  kudo_service = Kudo(g.user)
  kudos = kudo_service.find_all_kudos()
  return json.dumps(kudos), 200, {'content-type': 'application/json'}

@app.route("/kudos", methods=["POST"])
@login_required
def create():
    github_repo = GithubRepoSchema().load(json.loads(request.data))
    
    if github_repo.errors:
      return json.dumps({'msg': 'invalid kudo', 'errors': github_repo.errors}), 422, {'content-type': 'application/json'}

    kudo_service = Kudo(g.user)
    kudo = kudo_service.create_kudo_for(github_repo)
    return json.dumps(kudo), 200, {'content-type': 'application/json'}
  
@app.route("/kudo/<int:repo_id>", methods=["GET"])
@login_required
def show(repo_id):
  kudo_service = Kudo(g.user)
  kudo = kudo_service.find_kudo(repo_id)
  if kudo:
    return json.dumps(kudo), 200, {'content-type': 'application/json'}
  else:
    return json.dumps({'error': 'kudo not found'}), 404, {'content-type': 'application/json'}
  
@app.route("/kudo/<int:repo_id>", methods=["PUT"])
@login_required
def update(repo_id):
    github_repo = GithubRepoSchema().load(json.loads(request.data))
    
    if github_repo.errors:
      return json.dumps({'msg': 'invalid kudo', 'errors': github_repo.errors}), 422, {'content-type': 'application/json'}

    kudo_service = Kudo(g.user)
    if kudo_service.update_kudo_with(repo_id, github_repo):
      return json.dumps(github_repo.data), 200, {'content-type': 'application/json'}
    else:
      return json.dumps({'error': 'kudo not found'}), 404, {'content-type': 'application/json'}

    
@app.route("/kudo/<int:repo_id>", methods=["DELETE"])
@login_required
def delete(repo_id):
  kudo_service = Kudo(g.user)
  if kudo_service.delete_kudo_for(repo_id):
    return json.dumps({}), 200, {'content-type': 'application/json'}
  else:
    return json.dumps({'error': 'kudo not found'}), 404, {'content-type': 'application/json'}