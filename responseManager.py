import notifier

_STATUS_CODE = "statusCode"
_BODY = "body"

def manageReponse(statusCode, message, notify=True):
    response = {
        "statusCode": statusCode,
        "body": message
    }
    if notify:
        notifier.notify(statusCode, message)
    return response