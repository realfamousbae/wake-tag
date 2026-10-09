from types import SimpleNamespace as User

from src.bot import MENTIONS_PER_MESSAGE, _chunks, _mention


def test_mention_with_username():
    assert _mention(User(username="john", first_name="John", id=1)) == "@john"


def test_mention_without_username_uses_link():
    assert _mention(User(username=None, first_name="Jo[hn]", id=7)) == "[John](tg://user?id=7)"


def test_chunks_respect_mention_count():
    chunks = _chunks(["@a"] * 120)
    assert [len(c.split()) for c in chunks] == [MENTIONS_PER_MESSAGE, MENTIONS_PER_MESSAGE, 20]


def test_chunks_respect_length():
    assert all(len(c) <= 3500 for c in _chunks(["@" + "a" * 100] * 200, per_message=1000))


def test_chunks_empty():
    assert _chunks([]) == []
