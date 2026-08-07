# FLOWW 💸

A personal budget management app written in Python.
Philosophy: Make managing money “as easy as saying hello”—no stress, no complicated spreadsheets.

## Features

- Track daily expenses from the terminal
- Remaining budget calculated in real time (income − savings goal − expenses)
- Daily budget limit until the end of the month
- Projection: at your current pace, how much you’ll have saved by the end of the month
- Alert if you’re at risk of missing your savings goal
- Automatic month change: balance archived and reset to zero
- History of past months (total expenses, actual savings)
- Data saved in JSON—nothing is lost between sessions

## How to Use

```
pip install matplotlib
python floww.py
python floww_web.py
```

When you first launch FLOWW, it asks for your monthly income and your savings goal,
and then you’re good to go.

## Stack

Python + matplotlib for charts. The data is stored in a local
`floww.json` file (unversioned).

## Roadmap

- [x] Phase 1 — Terminal Core Loop
- [x] Phase 2 — JSON Persistence
- [x] Phase 3 — Projections and monthly history
- [x] Phase 4 — Graphical visualization (matplotlib)
- [x] Phase 5 — Web interface (Flask)

## Background

Project built as part of my Python learning journey: 90 days, 6 days a week, understanding every line of code. Building in public since day 68.


