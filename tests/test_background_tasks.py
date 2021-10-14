from unittest import TestCase
from appMR.background_tasks import check_old_tickets

from appMR.models import Comment, SupportTicket, User


class Test(TestCase):
    def setUp(self):
        u = User.objects.get_or_create(username="test")[0]
        s = SupportTicket.objects.create(
            reporter=u,
            title="Test",
            description="This is a test ticket.",
            status='1'
        )
        s.comments.add(
            Comment.objects.create(
                author=u,
                comment="This is a test comment.",
            )
        )

    def test_check_old_tickets_not_expired(self):
        s = SupportTicket.objects.get(pk=1)
        check_old_tickets()
        self.assertTrue(s.active)
