from notifier import notify

_STATUS_CODE = "statusCode"
_BODY = "body"

def manageReponse(statusCode, message, notify=True):
    response = {
        _STATUS_CODE: statusCode,
        _BODY: message
    }
    if notify:
        notify(statusCode, message)
    return response