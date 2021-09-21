from database import User


class UserObj:
    def __init__(self, uid):
        self.uid = uid
        self.user = User.objects(uid=int(uid)).first()

    @classmethod
    def create_user(cls, uid, name):
        us = User.objects(uid=str(uid)).first()
        if not us:
            us = User(uid=str(uid), status='new', name=name).save()
        return us

    def status(self):
        return self.user.status

    def set_status(self, status):
        self.user.update(set__status=str(status))
        self.user.save()
        return self


def check_status(uid):
    user = User.objects(uid=str(uid)).first()
    return user.status
