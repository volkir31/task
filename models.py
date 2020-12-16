from main import db, session, base

class LevelDB(base):
    __tablename__ = 'LevelDB'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(500), nullable=False)
    transliter = db.Column(db.String(500), nullable=False)