from firebase_admin import messaging

from notifications.models import Notification
from users.models import User


def notify(title, body, userId):
    try:
        user = User.objects.prefetch_related("fcm_tokens").get(pk=userId)
        message = messaging.MulticastMessage(
            notification=messaging.Notification(body=body, title=title),
            tokens=[token.key for token in user.fcm_tokens.all()],  # type:ignore
        )
        response = messaging.send_multicast(message)
        print("gui ne", response)
        Notification.objects.create(user=user, title=title, body=body)
    except:  # noqa: E722
        pass
