from datetime import timedelta

from django.utils.timezone import now
from model_bakery import baker

from appMR.background_tasks import check_old_tickets
from appMR.models import User, SupportTicket


def test_check_old_tickets_not_expired():
    s = baker.make('appMR.SupportTicket')
    s.comments.add(
        baker.make('appMR.Comment')
    )
    check_old_tickets()
    assert s.active


def test_check():
    User.objects.create()
    s = baker.make('appMR.SupportTicket')
    s.comments.add(
        baker.make('appMR.Comment')
    )
    n = now() + timedelta(days=35)
    check_old_tickets(now=n)
    n = SupportTicket.objects.get(title=s.title)
    assert not n.active
