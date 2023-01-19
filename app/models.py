from app import db
print('models.py')


class Weight(db.Model):
    rowid = db.Column(db.Integer, primary_key=True)
    mtime = db.Column(db.Integer, index=True, unique=True)
    yard = db.Column(db.String(8), index=True)
    rbook = db.Column(db.Integer())
    typ = db.Column(db.String(1))
    weight = db.Column(db.Integer)
    pid = db.Column(db.String(12))

    def __repr__(self):
        return '<Weight {}>'.format(self.weight)
