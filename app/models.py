from app import db


# TODO: Add more syntax comments


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True)
    password = db.Column(db.Text, unique=True)
    email = db.Column(db.String(120), unique=True, index=True)
    type = db.Column(db.String(10), unique=True)
    active = db.Column(db.Boolean)
    address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, username, password, email, utype, address, active=True):
        self.username = username
        self.password = password
        self.email = email
        self.type = utype
        self.active = active
        self.address = address

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

    def set_active(self, active):
        self.active = active

    def set_address(self, address):
        self.address = address

    def set_geoloc(self, latitude, longitude):
        self.latitude = latitude
        self.logitude = longitude

    def __repr__(self):
        return '<User %r>' % self.username


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    distance_matrix = db.Column(db.Text)
    user_list = db.Column(db.Text)
    routes = db.relationship('routes')

    def __repr__(self):
        return '<Group %r>' % self.user_list


class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.Text)
    group = db.Column(db.Integer, db.ForeignKey('groups.id'))

    def __repr__(self):
        return '<Route %r>' % self.id
