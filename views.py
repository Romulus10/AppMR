"""
appMR view functions.
"""
import os

from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from appMR.background_tasks import check_old_tickets
from .forms import SupportTicketForm, CommentForm
from .models import SupportTicket


def not_logged_in(request):
    """

    :param request:
    :return:
    """
    return render(request, 'appMR/not_logged_in.html')


def __get_dev(request):
    """

    :param request:
    :return:
    """
    if request.user.groups.filter(name='Developer').exists():
        bug_list = SupportTicket.objects.filter(active=True)
        done_list = SupportTicket.objects.filter(active=False)
        dev = True
    else:
        bug_list = SupportTicket.objects.filter(
            reporter=request.user).filter(active=True)
        done_list = SupportTicket.objects.filter(
            reporter=request.user).filter(active=False)
        dev = False
    return dev, bug_list, done_list


def new_bug_view(request, ticket_type=0):
    """

    :param request:
    :param ticket_type:
    :return:
    """
    if request.user.is_authenticated:
        dev, bug_list, done_list = __get_dev(request)
        if request.method == 'POST':
            form = SupportTicketForm(request.POST, request.FILES)
            if form.is_valid():
                t = form.save()
                t.reporter = request.user
                t.status = '1'
                t.active = True
                t.last_updated = now()
                t.save()
                # noinspection LongLine
                send_mail(
                    "New AppMR Ticket {0}".format(t.id),
                    "{0}\n\n\nTHIS IS AN AUTOMATED MESSAGE. PLEASE DO NOT REPLY TO THIS EMAIL. PLEASE LOG IN TO REPLY.".format(
                        t.description),
                    os.environ.get('DEFAULT_FROM_EMAIL'),
                    [os.environ.get('DEV_EMAIL')])
                form = SupportTicketForm()
            return render(request, 'appMR/bug_list.html',
                          {'open': ticket_type, 'bug_list': bug_list, 'done_list': done_list, 'dev': dev, 'form': form})
        else:
            form = SupportTicketForm()
        return render(request, 'appMR/bug_list.html',
                      {'open': ticket_type, 'bug_list': bug_list, 'done_list': done_list, 'dev': dev, 'form': form})
    else:
        return redirect('appMR:not_logged_in')


def bug_list_view(request, ticket_type=0):
    """

    :param request:
    :param ticket_type:
    :return:
    """
    if request.user.is_authenticated:
        check_old_tickets()
        form = SupportTicketForm()
        dev, bug_list, done_list = __get_dev(request)
        return render(request, 'appMR/bug_list.html',
                      {'open': ticket_type, 'bug_list': bug_list, 'done_list': done_list, 'dev': dev, 'form': form})
    else:
        return redirect('appMR:not_logged_in')


def change_bug_list_view(request, ticket_type=0):
    """

    :param request:
    :param ticket_type:
    :return:
    """
    if request.user.is_authenticated:
        ticket_type = 0 if ticket_type == 1 else 1
        form = SupportTicketForm()
        dev, bug_list, done_list = __get_dev(request)
        return render(request, 'appMR/bug_list.html',
                      {'open': ticket_type, 'bug_list': bug_list, 'done_list': done_list, 'dev': dev, 'form': form})
    else:
        return redirect('appMR:not_logged_in')


def bug_detail_view(request, id=None):
    """

    :param request:
    :param id:
    :return:
    """
    if request.user.is_authenticated:
        m = get_object_or_404(SupportTicket, pk=id)
        comments = m.comments.all()
        comment_form = CommentForm()
        if request.user.groups.filter(name='Developer').exists():
            dev = True
        else:
            dev = False
        if request.method == 'POST':
            form = SupportTicketForm(request.POST or None, request.FILES, instance=m)
            if form.is_valid():
                t = form.save()
                t.status = m.status
                t.active = m.active
                if t.status == '6':
                    t.active = False
                else:
                    t.active = True
                t.save()
        else:
            form = SupportTicketForm(instance=m)
        return render(request, 'appMR/bug_detail.html',
                      {'bug_id': m.id, 'bug': m, 'dev': dev, 'form': form, 'comment_form': comment_form,
                       'comments': comments})
    else:
        return redirect('appMR:not_logged_in')


def post_comment_view(request, bug_id=None):
    """

    :param request:
    :param bug_id:
    :return:
    """
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Developer').exists():
            dev = True
        else:
            dev = False
        m = get_object_or_404(SupportTicket, pk=bug_id)
        form = SupportTicketForm(instance=m)
        comment_form = CommentForm()
        if request.method == 'POST':
            comment_form = CommentForm(request.POST, request.FILES)
            if comment_form.is_valid():
                t = comment_form.save()
                t.author = request.user
                t.save()
                m.comments.add(t)
                m.last_updated = now()
                m.save()
                if os.environ.get("EMAIL_HOST") != "":
                    # noinspection LongLine
                    send_mail(
                        "Response on AppMR Ticket {0}".format(bug_id),
                        "{0}\n\n\nTHIS IS AN AUTOMATED MESSAGE. PLEASE DO NOT REPLY TO THIS EMAIL. PLEASE LOG IN TO REPLY.".format(
                            t.comment),
                        os.environ.get('DEFAULT_FROM_EMAIL'),
                        [os.environ.get('DEV_EMAIL'), t.author.email, m.reporter.email])
                comment_form = CommentForm()
        comments = m.comments.all()
        return render(request, 'appMR/bug_detail.html',
                      {'bug_id': m.id, 'dev': dev, 'form': form, 'comment_form': comment_form, 'comments': comments})
    else:
        return redirect('appMR:not_logged_in')
