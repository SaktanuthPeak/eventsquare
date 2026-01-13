from apiapp import models


def create_logs(action, request, current_user):
    request_log = models.RequestLog(
        user=current_user,
        ip_address=request.client.host,
        action=action,
        user_agent=request.headers.get("user-agent", ""),
    )
    return request_log
