from django.middleware.csrf import get_token
from django.http import JsonResponse

def csrf_response(request, data):
    """
    Utility function to return a JsonResponse with CSRF token
    """
    response = JsonResponse(data)
    response['X-CSRFToken'] = get_token(request)
    return response


def get_csrf_token(request):
    """
    Get CSRF token for AJAX requests
    """
    return JsonResponse({'csrfToken': get_token(request)})
