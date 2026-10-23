from assistant_core.models import Intent
from assistant_core.router import route


def test_route_greeting():
    assert route("Hello!", set()) == Intent.GREETING


def test_route_vietnamese_greeting():
    assert route("Xin chào", set()) == Intent.GREETING


def test_route_fee():
    assert route("How much is tuition?", set()) == Intent.FEE


def test_route_credit_fee():
    assert route("Học phí 18 tín chỉ", set()) == Intent.FEE


def test_route_office():
    assert route("Where is the training office?", {"Training Office"}) == Intent.OFFICE


def test_route_office_case_insensitive():
    assert route("training office ở đâu?", {"Training Office"}) == Intent.OFFICE


def test_route_rule():
    assert route("Quy định thi như thế nào?", set()) == Intent.RULE


def test_route_unknown():
    assert route("The weather is nice", set()) == Intent.UNKNOWN
