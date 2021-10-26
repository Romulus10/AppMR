from model_bakery import baker


def test_support_ticket():
    st = baker.make('appMR.SupportTicket')
    assert str(st) == st.title
