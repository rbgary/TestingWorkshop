import pytest
from leaderboard import Leaderboard


def test_add_player():
    lb = Leaderboard()
    lb.add_player("Alice")
    assert len(lb) == 1


def test_add_player_with_initial_score():
    lb = Leaderboard()
    lb.add_player("Alice", initial_score=500)
    assert lb.get_top_n(1) == [("Alice", 500)]


def test_record_match_updates_scores():
    lb = Leaderboard()
    lb.add_player("Alice", 100)
    lb.add_player("Bob", 100)
    lb.record_match("Alice", "Bob")
    assert lb.get_top_n(2) == [("Alice", 110), ("Bob", 90)]


def test_get_rank():
    lb = Leaderboard()
    lb.add_player("Alice", 300)
    lb.add_player("Bob", 100)
    lb.add_player("Carol", 200)
    assert lb.get_rank("Alice") == 1
    assert lb.get_rank("Carol") == 2
    assert lb.get_rank("Bob") == 3

# New Tests
def test_add_player_negScore():
    lb = Leaderboard()
    with pytest.raises(ValueError):
        lb.add_player("Alice", -1)

def test_add_player_RegisteredAlready():
    lb = Leaderboard()
    lb.add_player("Alice", 100)
    with pytest.raises(ValueError):
        lb.add_player("Alice", 100)

def test_record_match_NotValidWinner():
    lb = Leaderboard()
    with pytest.raises(KeyError):
        lb.record_match("Bob", "Alice")


def test_record_match_NotValidLoser():
    lb = Leaderboard()
    lb.add_player("Alice", 100)
    with pytest.raises(KeyError):
        lb.record_match("Alice", "Bob")

def test_record_match_NotValidScore():
    lb = Leaderboard()
    lb.add_player("Alice", 100)
    lb.add_player("Bob", 100)
    with pytest.raises(ValueError):
        lb.record_match("Alice", "Bob", -1)       


def test_rank_not_valid_plaer():
    lb = Leaderboard()
    with pytest.raises(KeyError):
        lb.get_rank("Frank")

def test_get_top_n_negative_n():
    lb = Leaderboard()
    with pytest.raises(ValueError):
        lb.get_top_n(-1)

def test_get_percentile_not_registered():
    lb = Leaderboard()
    with pytest.raises(KeyError):
        lb.get_percentile("Alice")

def test_get_percentile_one_player():
    lb = Leaderboard()
    lb.add_player("Alice", 100)
    assert lb.get_percentile("Alice") == 100.0

def test_get_percentile_multiple_player():
    lb = Leaderboard()
    lb.add_player("Alice", 100)
    lb.add_player("Bob", 50)
    assert lb.get_percentile("Alice") == 50

def test_apply_bonus_non_player():
    lb = Leaderboard()
    with pytest.raises(KeyError):
        lb.apply_bonus("Alice", 12.0)

def test_apply_bonus_negative():
    lb = Leaderboard()
    lb.add_player("Alice", 100)
    with pytest.raises(ValueError):
        lb.apply_bonus("Alice", -12.0)