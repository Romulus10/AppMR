from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory

from appMR.views import bug_list_view, not_logged_in


def test_not_logged_in():
    factory = RequestFactory()
    request = factory.get("/not_logged_in")
    return_response = not_logged_in(request)
    assert return_response.status_code == 200


def test_bug_list_view_redirect():
    factory = RequestFactory()
    request = factory.get("/bug_list_view")
    request.user = AnonymousUser()
    return_response = bug_list_view(request)
    assert return_response.status_code == 302
