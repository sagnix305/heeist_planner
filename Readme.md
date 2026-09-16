# Heist Planner

Heist Planner is a beginner-friendly Python game built with Tkinter. Assign
the right team member to each mission task and satisfy all constraints to
complete five heist missions.

## Features

- Five missions with different tasks and rules
- Constraint satisfaction puzzle validation
- Three attempts per game
- Three-minute timer for each mission
- Score tracking
- One-use hint for each mission
- Scrollable game screen
- Mission map and mission-specific rules

## Requirements

- Python 3.10 or newer
- Tkinter, usually included with Python

No third-party Python packages are required.

## Run the Game

Clone the repository:

```powershell
git clone https://github.com/sagnix305/heeist_planner.git
cd heeist_planner
```

Create and activate a virtual environment on Windows:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

Start the game:

```powershell
python main.py
```

If PowerShell blocks virtual-environment activation, run the game directly
with `python main.py`, or use Command Prompt with `venv\Scripts\activate`.

## How to Play

1. Click **START GAME**.
2. Assign one team member to every task.
3. Click **CHECK PLAN**.
4. Correct plans earn points and unlock the next mission.
5. Incorrect plans use one attempt.
6. Use **HINT (-25)** once per mission when needed.
7. Click **RESTART GAME** after losing all attempts or running out of time.

## Project Structure

```text
main.py                 Application entry point
gui/                    Tkinter screens and widgets
csp/                    Constraint validation code
game/                   Levels, scoring, and timer logic
data/                   Mission and constraint JSON files
assets/images/          Game image assets
requirements.txt        Dependency information
```

## License

This project is available for learning and personal use.
