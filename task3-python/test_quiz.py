import builtins
import json
import os
from unittest import mock
import quiz

def sample_questions():
    return [
        quiz.Question("What is 2+2?", "4"),
        quiz.Question("What is the capital of France?", "Paris"),
    ]


def test_question_to_dict_and_from_dict():
    q = quiz.Question("Q?", "A")
    data = q.to_dict()
    assert data == {"prompt": "Q?", "answer": "A"}
    q2 = quiz.Question.from_dict(data)
    assert isinstance(q2, quiz.Question)
    assert q2.prompt == "Q?"
    assert q2.answer == "A"

def test_run_quiz_correct(monkeypatch, capsys):
    questions = [quiz.Question("Q1?", "yes")]
    
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    
    quiz.run_quiz(questions)
    
    captured = capsys.readouterr()
    assert "Correct!" in captured.out
    assert "Your final score is 1/1" in captured.out

def test_run_quiz_incorrect(monkeypatch, capsys):
    questions = [quiz.Question("Q1?", "yes")]
    
    monkeypatch.setattr("builtins.input", lambda _: "no")
    
    quiz.run_quiz(questions)
    
    captured = capsys.readouterr()
    assert "Wrong! The correct answer was: yes" in captured.out
    assert "Your final score is 0/1" in captured.out


def test_save_and_load_quiz(tmp_path):
    quiz_name = tmp_path / "myquiz"
    questions = sample_questions()
    
    quiz.save_quiz(str(quiz_name), questions)
    
    file_path = f"{quiz_name}.json"
    assert os.path.exists(file_path)
    
    loaded_questions = quiz.load_quiz(str(quiz_name))
    assert len(loaded_questions) == len(questions)
    assert loaded_questions[0].prompt == questions[0].prompt
    assert loaded_questions[0].answer == questions[0].answer

def test_load_quiz_nonexistent(tmp_path, capsys):
    quiz_name = tmp_path / "nonexistent"
    result = quiz.load_quiz(str(quiz_name))
    captured = capsys.readouterr()
    assert result == []
    assert f"No quiz found with the name '{quiz_name}'." in captured.out


def test_create_quiz(monkeypatch, tmp_path):
    inputs = iter([
        "Question1", "a",   
        "Question2", "b",   
        "done",             
        "testquiz"          
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    quiz.create_quiz()
    
    file_path = "testquiz.json"
    assert os.path.exists(file_path)
    with open(file_path, "r") as f:
        data = json.load(f)
        assert len(data) == 2
        assert data[0]["prompt"] == "Question1"
        assert data[0]["answer"] == "a"


def test_main_exit(monkeypatch):
    inputs = iter(["3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    quiz.main()

def test_main_invalid_choice(monkeypatch, capsys):
    inputs = iter(["invalid", "3"])  
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    quiz.main()
    captured = capsys.readouterr()
    assert "Invalid choice" in captured.out

def test_main_take_quiz(monkeypatch, tmp_path):
    questions = sample_questions()
    quiz_name = "quiz1"
    quiz.save_quiz(quiz_name, questions)
    
    inputs = iter(["1", quiz_name, "4", "Paris", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    monkeypatch.setattr("random.shuffle", lambda x: x)
    
    quiz.main()

def test_main_create_quiz_flow(monkeypatch, tmp_path):
    inputs = iter([
        "2", "Q?", "A", "done", "quiz2",  
        "3"  
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    quiz.main()
    assert os.path.exists("quiz2.json")
