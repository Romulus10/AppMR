from django.contrib.auth.models import AnonymousUser
from django.test.client import Client, RequestFactory
from django.urls import reverse

from app_mr.views import bug_list_view, not_logged_in
from main.models import fEMRUser

from model_bakery import baker


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


def test_bug_list_logged():
    u = fEMRUser.objects.create_user(
        username="testhome",
        password="testingpasswordbuglist",
        email="hometestinguseremail@email.com",
    )
    u.change_password = False
    c = baker.make("main.Campaign")
    c.active = True
    c.save()
    u.campaigns.add(c)
    u.save()
    client = Client()
    client.post(
        "/login_view/", {"username": "testhome", "password": "testingpasswordbuglist"}
    )
    return_response = client.get(
        reverse("app_mr:bug_list_view", kwargs={"ticket_type": "0"})
    )
    u.delete()
    assert return_response.status_code == 200
    assert "Leave a Bug or Problem Report" in str(return_response.content)
