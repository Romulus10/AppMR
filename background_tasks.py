from datetime import timedelta
from django.utils import timezone
from appMR.models import Comment, SupportTicket, User


def check_old_tickets():
    now = timezone.now()
    d = now - timedelta(days=30)
    for ticket in SupportTicket.objects.all():
        stale = False
        for comment in ticket.comments:
            if comment.timestamp < d:
                stale = True
            elif comment.timestamp >= d:
                stale = False
        if stale:
            ticket.comments.add(
                Comment.objects.create(
                    author=User.objects.get(pk=0),
                    comment="Hi all - we haven't seen activity on this ticket for 30 days, so we're going to mark it as resolved. Please don't hesitate to open a new ticket if you need more help."
                )
            )