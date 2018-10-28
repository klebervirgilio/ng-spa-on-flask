from marshmallow import Schema, fields

class GithubRepoSchema(Schema):
    repo_id = fields.Int(required=True)
    repo_name = fields.Str()
    language = fields.Str()
    description = fields.Str()
    repo_url = fields.URL()

class KudoSchema(GithubRepoSchema):
    user_id = fields.Email(required=True)
