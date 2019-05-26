from src.utils import split_string


def test_split_string():
    splits = split_string('a b c', 3)

    assert len(splits) == 2
    assert splits[0] == 'a b'
    assert splits[1] == 'c'
