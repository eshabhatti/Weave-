class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active
        self.auth = auth

    def is_active(self):
        # can return false for banned or deactivated users
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    
    def get_id(self):
        return str(self.id)