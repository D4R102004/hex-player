# HEX Player 🎮

Autonomous AI player for the HEX board game — University AI Project.

![HEX Board](hex-board-example.png)

## What is HEX?
HEX is a two-player strategy game on an NxN hexagonal grid.
- **Player 1 🔴** connects left side to right side
- **Player 2 🔵** connects top side to bottom side

No draws are possible. The first player to connect their sides wins.

## Strategy
This player uses **Monte Carlo Tree Search (MCTS)** with UCB1 selection
to decide the best move within a 4.5 second time budget.

## Project Structure
```
hex-player/
├── src/Urrutia_Dario_Alfonso/
│   ├── solution.py        ← SmartPlayer (MCTS)
│   ├── board.py           ← HexBoard class
│   └── player.py          ← Base Player class
├── tests/                 ← pytest test suite
├── .github/workflows/     ← CI pipeline
├── Dockerfile             ← reproducible environment
└── pyproject.toml         ← project config & dependencies
```

## Running Locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Running with Docker
```bash
docker build -t hex-player .
docker run hex-player
```