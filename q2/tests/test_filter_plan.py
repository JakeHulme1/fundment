import pytest

from q2.filter_plan import filter_plan

# The algorithm currently picks a" first when both "a" and "b" are valid; tests allow any result belonging to a complete set of all valid solutions.

def test_left_peek_only_returns_correct_solution():
    string = "aa?"
    result = filter_plan(string)
    solution = "aab"
    assert result == solution, f"Invalid solution. Expected {solution}, got {result}"

def test_middle_peek_only_returns_correct_solution():
    string = "a?a"
    result = filter_plan(string)
    solution = "aba"
    assert result == solution, f"Invalid solution. Expected {solution}, got {result}"

def test_right_peek_only_returns_correct_solution():
    string = "?aa"
    result = filter_plan(string)
    solution = "baa"
    assert result == solution, f"Invalid solution. Expected {solution}, got {result}"

def test_single_char_string_returns_correct_solution():
    string = "?"
    result = filter_plan(string)
    solution = ["a", "b"]
    assert result in solution, f"Invalid solution. Expected {solution}, got {result}"

def test_single_char_string_solution_returns_the_same():
    string = "a"
    result = filter_plan(string)
    solution = "a"
    assert result == solution, f"Invalid solution. Expected {solution}, got {result}"

def test_fixed_followed_by_question():
    string = "a?"
    result = filter_plan(string)
    solution = ["ab", "aa"]
    assert result in solution, f"Invalid solution. Expected {solution}, got {result}"

def test_question_followed_by_fixed():
    string = "?a"
    result = filter_plan(string)
    solution = ["ba", "aa"]
    assert result in solution, f"Invalid solution. Expected {solution}, got {result}"

def test_a_q_bb_returns_aabb():
    string = "a?bb"
    result = filter_plan(string)
    solution = "aabb"
    assert result == solution, f"Invalid solution. Expected {solution}, got {result}"

def test_q_q_abb_returns_correct_solution():
    string = "??abb"
    result = filter_plan(string)
    solution = ["ababb", "bbabb", "baabb"]
    assert result in solution, f"Invalid solution. Expected one of {solution}, got {result}"

def test_aa_qq_aa_returns_aabbaa():
    string = "aa??aa"
    result = filter_plan(string)
    solution = "aabbaa"
    assert result == solution, f"Invalid solution. Expected {solution}, got {result}"

def test_no_question_marks_returns_same():
    string = "abba"
    result = filter_plan(string)
    solution = "abba"
    assert result == solution, f"The solution was already valid, so expected {solution}, got {result}"

def test_double_question_returns_valid_two_letter_string():
    string = "??"
    result = filter_plan(string)
    solution = ["aa", "ab", "ba", "bb"]
    assert result in solution, f"Invalid solution. Expected one of {solution}, got {result}."

def test_triple_question_returns_valid_three_letter_string():
    string = "???"
    result = filter_plan(string)
    solution = ["aab", "abb", "bba", "baa", "bab", "aba"]
    assert result in solution, f"Invalid solution. Expected one of {solution}, got {result}."

def test_multiple_question_marks():
    string = "a?b?a?b"
    result = filter_plan(string)
    solution = ["aabaabb", "aabbaab", "aabbabb", "abbaabb"]
    assert result in solution

def test_only_question_marks_contains_no_triples():
    string = "???????????????????????????????????????????????????????????????"
    result = filter_plan(string)
    assert "aaa" not in result and "bbb" not in result