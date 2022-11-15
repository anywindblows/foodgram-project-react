from config import config_messages as msg
from users.models import Follow


class UserServices:
    validate_status = dict()

    def validate_post_method(self, author, user):
        if user == author:
            self.validate_status['errors'] = msg.SELF_SUBSCRIPTION
            return self.validate_status

        if Follow.objects.filter(user=user, author=author).exists():
            self.validate_status['errors'] = msg.ALREADY_SIGNED
            return self.validate_status
        return None

    def validate_delete_method(self, author, user):
        if user == author:
            self.validate_status['errors'] = msg.SELF_UNSUBSCRIPTION
            return self.validate_status
        return None
