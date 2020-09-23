from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        # can return false for banned or deactivated users
        return self.active

    def is_anonymous(self):
        # if anonymous user, this will be true
        return False

    def is_authenticated(self):
        # if not anonymous, this will be true
        return True
    
    def get_id(self):
        return str(self.id)