# 🧪 TeleGame Testing Guide

TeleGame utilizes `pytest` and `pytest-asyncio` for unit, integration, and service tests.

## Running Tests

Execute the complete test suite:
```bash
python -m pytest -v --asyncio-mode=auto
```

## Coverage Report

Generate code coverage report:
```bash
python -m pytest --cov=app --cov-report=term-missing
```

## Test Structure

- `tests/test_engine.py`: Dynamic plugin discovery, BaseGame contract, FSM state machine transitions.
- `tests/test_games.py`: Gameplay logic for Tic-Tac-Toe, Rock Paper Scissors, Connect Four, Hangman, Trivia.
- `tests/test_services.py`: Elo rating mathematical formulas, virtual economy balances, and security rate limiting.
