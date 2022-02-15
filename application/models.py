from . import db

class Knowledge(db.Model):
    __tablename__ = 'knowledge'
    
    id = db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String, unique=True)
    title = db.Column(db.String)
    json_tree = db.Column(db.String)
    raw_text = db.Column(db.String)