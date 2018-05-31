from rest_framework import status
from rest_framework.response import Response


def rest_message(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
    return Response({"http_status": status_code, "message": message}, status=status_code)
