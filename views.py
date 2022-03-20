"""
appMR view functions.
"""
import os

from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from appMR.background_tasks import check_old_tickets
from appMR.signals import ticket_activity
from appMR.forms import SupportTicketForm, CommentForm
from appMR.models import SupportTicket


def not_logged_in(request):
    return render(request, "appMR/not_logged_in.html")


def __get_dev(request):
    if request.user.groups.filter(name="Developer").exists():
        bug_list = SupportTicket.objects.filter(active=True)
        done_list = SupportTicket.objects.filter(active=False)
        dev = True
    else:
        bug_list = SupportTicket.objects.filter(reporter=request.user).filter(
            active=True
        )
        done_list = SupportTicket.objects.filter(reporter=request.user).filter(
            active=False
        )
        dev = False
    return dev, bug_list, done_list


def new_bug_view(request, ticket_type=0):
    if request.user.is_authenticated:
        dev, bug_list, done_list = __get_dev(request)
        if request.method == "POST":
            form = SupportTicketForm(request.POST, request.FILES)
            if form.is_valid():
                ticket = form.save()
                ticket.reporter = request.user
                ticket.status = "1"
                ticket.active = True
                ticket.last_updated = now()
                ticket.save()
                # noinspection LongLine
                send_mail(
                    f"New AppMR Ticket {ticket.id}",
                    f"{ticket.description}\n\n\nTHIS IS AN AUTOMATED MESSAGE. "
                    "PLEASE DO NOT REPLY TO THIS EMAIL. "
                    "PLEASE LOG IN TO REPLY.",
                    os.environ.get("DEFAULT_FROM_EMAIL"),
                    [os.environ.get("DEV_EMAIL")],
                )
                ticket_activity.send(sender=new_bug_view, ticket=ticket.id)
                form = SupportTicketForm()
        else:
            form = SupportTicketForm()
        return_response = render(
            request,
            "appMR/bug_list.html",
            {
                "open": ticket_type,
                "bug_list": bug_list,
                "done_list": done_list,
                "dev": dev,
                "form": form,
            },
        )
    else:
        return_response = redirect("appMR:not_logged_in")
    return return_response


def bug_list_view(request, ticket_type=0):
    if request.user.is_authenticated:
        check_old_tickets()
        form = SupportTicketForm()
        dev, bug_list, done_list = __get_dev(request)
        return_response = render(
            request,
            "appMR/bug_list.html",
            {
                "open": ticket_type,
                "bug_list": bug_list,
                "done_list": done_list,
                "dev": dev,
                "form": form,
            },
        )
    else:
        return_response = redirect("appMR:not_logged_in")
    return return_response


def change_bug_list_view(request, ticket_type=0):
    if request.user.is_authenticated:
        ticket_type = 0 if ticket_type == 1 else 1
        form = SupportTicketForm()
        dev, bug_list, done_list = __get_dev(request)
        return_response = render(
            request,
            "appMR/bug_list.html",
            {
                "open": ticket_type,
                "bug_list": bug_list,
                "done_list": done_list,
                "dev": dev,
                "form": form,
            },
        )
    else:
        return_response = redirect("appMR:not_logged_in")
    return return_response


def bug_detail_view(request, ticket_id=None):
    if request.user.is_authenticated:
        ticket = get_object_or_404(SupportTicket, pk=ticket_id)
        comments = ticket.comments.all()
        comment_form = CommentForm()
        dev = request.user.groups.filter(name="Developer").exists()
        if request.method == "POST":
            form = SupportTicketForm(
                request.POST or None, request.FILES, instance=ticket
            )
            if form.is_valid():
                updated_ticket = form.save()
                updated_ticket.status = ticket.status
                updated_ticket.active = ticket.active
                if updated_ticket.status == "6":
                    updated_ticket.active = False
                else:
                    updated_ticket.active = True
                updated_ticket.save()
                ticket_activity.send(sender=bug_detail_view, ticket=updated_ticket.id)
        else:
            form = SupportTicketForm(instance=ticket)
        return_response = render(
            request,
            "appMR/bug_detail.html",
            {
                "bug_id": ticket.id,
                "bug": ticket,
                "dev": dev,
                "form": form,
                "comment_form": comment_form,
                "comments": comments,
            },
        )
    else:
        return_response = redirect("appMR:not_logged_in")
    return return_response


def post_comment_view(request, bug_id=None):
    if request.user.is_authenticated:
        dev = request.user.groups.filter(name="Developer").exists()
        ticket = get_object_or_404(SupportTicket, pk=bug_id)
        form = SupportTicketForm(instance=ticket)
        comment_form = CommentForm()
        if request.method == "POST":
            comment_form = CommentForm(request.POST, request.FILES)
            if comment_form.is_valid():
                comment = comment_form.save()
                comment.author = request.user
                comment.save()
                ticket.comments.add(comment)
                ticket.last_updated = now()
                ticket.save()
                if os.environ.get("EMAIL_HOST") != "":
                    # noinspection LongLine
                    send_mail(
                        f"Response on AppMR Ticket {bug_id}",
                        f"{comment.comment}\n\n\nTHIS IS AN AUTOMATED MESSAGE. "
                        "PLEASE DO NOT REPLY TO THIS EMAIL. "
                        "PLEASE LOG IN TO REPLY.",
                        os.environ.get("DEFAULT_FROM_EMAIL"),
                        [
                            os.environ.get("DEV_EMAIL"),
                            comment.author.email,
                            ticket.reporter.email,
                        ],
                    )
                ticket_activity.send(sender=post_comment_view, ticket=ticket.id)
                comment_form = CommentForm()
        comments = ticket.comments.all()
        return_response = render(
            request,
            "appMR/bug_detail.html",
            {
                "bug_id": ticket.id,
                "dev": dev,
                "form": form,
                "comment_form": comment_form,
                "comments": comments,
            },
        )
    else:
        return_response = redirect("appMR:not_logged_in")
    return return_response
