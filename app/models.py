from app import db


class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(120), unique=True, index=True)
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.Text, unique=True)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    type = db.Column(db.String(10), unique=True)
    active = db.Column(db.Boolean)
    address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    uid = db.Column(db.Text(64), unique=True)
    groups = db.relationship('Group', backref='user')

    def __init__(self, email, password, firstname, lastname, utype, uid, active=True):
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.type = utype
        self.active = active
        self.uid = uid

    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.email


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    distance_matrix = db.Column(db.Text)
    user_list = db.Column(db.Text)
    routes = db.relationship('Route', backref='getgroup')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Group %r>' % self.user_list


class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.Text)
    group = db.Column(db.Integer, db.ForeignKey('groups.id'))

    def __repr__(self):
        return '<Route %r>' % self.id
