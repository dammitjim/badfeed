from rest_framework.response import Response


def rest_message(message, status_code):
    return Response({"status_code": status_code, "detail": message}, status=status_code)
