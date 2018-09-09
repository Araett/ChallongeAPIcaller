from .CAC import get_max_rounds, sort_this, get_active_players
import pytest

vals = [
    (
        [
            {'round': 1},
        ],
        1,
    ),
    (
        [
            {'round': 1},
            {'round': 2},
            {'round': 3},
        ],
        3,
    ),
    (
        [
            {'round': -1},
            {'round': 2},
            {'round': 3},
        ],
        3,
    ),
    (
        [
            {'round': -3},
            {'round': -2},
            {'round': -1},
            {'round': 2},
            {'round': 3},
        ],
        3,
    ),
    (
        [
            {'round': -5},
            {'round': -2},
            {'round': -1},
            {'round': 2},
            {'round': 4},
        ],
        5,
    ),
    (
        [
            {'round': -5},
            {'round': -2},
            {'round': -1},
            {'round': 0},
            {'round': 4},
            {'round': 6},
        ],
        6,
    ),
]

sort_this_list = [{'state': 'complete', 'id': 133062286, 'round': 1},
                  {'state': 'complete', 'id': 133062287, 'round': 1},
                  {'state': 'complete', 'id': 133062288, 'round': 1},
                  {'state': 'complete', 'id': 133062289, 'round': 1},
                  {'state': 'complete', 'id': 133062290, 'round': 1},
                  {'state': 'complete', 'id': 133062291, 'round': 1},
                  {'state': 'complete', 'id': 133062292, 'round': 1},
                  {'state': 'open', 'id': 133062293, 'round': 1},
                  {'state': 'open', 'id': 133062294, 'round': 2},
                  {'state': 'open', 'id': 133062295, 'round': 2},
                  {'state': 'open', 'id': 133062296, 'round': 2},
                  {'state': 'pending', 'id': 133062297, 'round': 2},
                  {'state': 'pending', 'id': 133062298, 'round': 3},
                  {'state': 'pending', 'id': 133062299, 'round': 3},
                  {'state': 'pending', 'id': 133062300, 'round': 4},
                  {'state': 'open', 'id': 133062301, 'round': -1},
                  {'state': 'open', 'id': 133062302, 'round': -1},
                  {'state': 'open', 'id': 133062303, 'round': -1},
                  {'state': 'pending', 'id': 133062304, 'round': -1},
                  {'state': 'pending', 'id': 133062305, 'round': -2},
                  {'state': 'pending', 'id': 133062306, 'round': -2},
                  {'state': 'pending', 'id': 133062307, 'round': -2},
                  {'state': 'pending', 'id': 133062308, 'round': -2},
                  {'state': 'pending', 'id': 133062309, 'round': -3},
                  {'state': 'pending', 'id': 133062310, 'round': -3},
                  {'state': 'pending', 'id': 133062311, 'round': -4},
                  {'state': 'pending', 'id': 133062312, 'round': -4},
                  {'state': 'pending', 'id': 133062313, 'round': -5},
                  {'state': 'pending', 'id': 133062314, 'round': -6},
                  {'state': 'pending', 'id': 133062315, 'round': 5},
                  {'state': 'pending', 'id': 133062316, 'round': 5}]


@pytest.mark.parametrize('matches, expected_res', vals)
def test_get_max_rounds_given_one(matches, expected_res):
    res = get_max_rounds(matches)
    assert res == expected_res


def test_sort_this():
    res = sort_this(sort_this_list)
    exp = [{'id': 133062286, 'round': 1, 'state': 'complete'},
           {'id': 133062287, 'round': 1, 'state': 'complete'},
           {'id': 133062288, 'round': 1, 'state': 'complete'},
           {'id': 133062289, 'round': 1, 'state': 'complete'},
           {'id': 133062290, 'round': 1, 'state': 'complete'},
           {'id': 133062291, 'round': 1, 'state': 'complete'},
           {'id': 133062292, 'round': 1, 'state': 'complete'},
           {'id': 133062293, 'round': 1, 'state': 'open'},
           {'id': 133062301, 'round': -1, 'state': 'open'},
           {'id': 133062302, 'round': -1, 'state': 'open'},
           {'id': 133062303, 'round': -1, 'state': 'open'},
           {'id': 133062304, 'round': -1, 'state': 'pending'},
           {'id': 133062294, 'round': 2, 'state': 'open'},
           {'id': 133062295, 'round': 2, 'state': 'open'},
           {'id': 133062296, 'round': 2, 'state': 'open'},
           {'id': 133062297, 'round': 2, 'state': 'pending'},
           {'id': 133062305, 'round': -2, 'state': 'pending'},
           {'id': 133062306, 'round': -2, 'state': 'pending'},
           {'id': 133062307, 'round': -2, 'state': 'pending'},
           {'id': 133062308, 'round': -2, 'state': 'pending'},
           {'id': 133062298, 'round': 3, 'state': 'pending'},
           {'id': 133062299, 'round': 3, 'state': 'pending'},
           {'id': 133062309, 'round': -3, 'state': 'pending'},
           {'id': 133062310, 'round': -3, 'state': 'pending'},
           {'id': 133062300, 'round': 4, 'state': 'pending'},
           {'id': 133062311, 'round': -4, 'state': 'pending'},
           {'id': 133062312, 'round': -4, 'state': 'pending'},
           {'id': 133062313, 'round': -5, 'state': 'pending'},
           {'id': 133062315, 'round': 5, 'state': 'pending'},
           {'id': 133062316, 'round': 5, 'state': 'pending'},
           {'id': 133062314, 'round': -6, 'state': 'pending'}]
    assert res == exp


def test_get_active_players():
    match = {'player1_id': 79835895, 'player2_id': 79835907}
    participants = [{'id': 79776462, 'name': 'Test1'},
                    {'id': 79776464, 'name': 'Test2'},
                    {'id': 79776466, 'name': 'Test3'},
                    {'id': 79776467, 'name': 'Test4'},
                    {'id': 79835895, 'name': 'Test5'},
                    {'id': 79835896, 'name': 'Test6'},
                    {'id': 79835898, 'name': 'Test7'},
                    {'id': 79835899, 'name': 'Test8'},
                    {'id': 79835901, 'name': 'Test9'},
                    {'id': 79835902, 'name': 'Test10'},
                    {'id': 79835904, 'name': 'Test11'},
                    {'id': 79835905, 'name': 'Test12'},
                    {'id': 79835906, 'name': 'Test13'},
                    {'id': 79835907, 'name': 'Test14'},
                    {'id': 79835910, 'name': 'Test15'},
                    {'id': 79835911, 'name': 'Test16'}]

    res = get_active_players(match, participants)
    assert res == ['Test5', 'Test14']
