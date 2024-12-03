from app.database import db
import uuid

class Suspect(db.Model):
    __tablename__ = 'suspects'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=True)
    nic = db.Column(db.String(50), nullable=True)
    social_media = db.Column(db.String(255), nullable=True)

class Connection(db.Model):
    __tablename__ = 'connections'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_id = db.Column(db.String(36), db.ForeignKey('suspects.id'), nullable=False)
    target_id = db.Column(db.String(36), db.ForeignKey('suspects.id'), nullable=False)
    db.UniqueConstraint('source_id', 'target_id', name='unique_connection')
