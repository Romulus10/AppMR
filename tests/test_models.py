from pprint import pprint

from model_bakery import baker


def test_support_ticket():
    st = baker.make('appMR.SupportTicket')
    pprint(st)
    assert str(st) == st.title
