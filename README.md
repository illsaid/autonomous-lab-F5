# Autonomous Lab F5

**What this became:** a long-tail explorer over CC0 museum collection metadata — a tool that surfaces artworks nobody looks at, from a dataset nobody maintains (the Tate collection snapshot, frozen since 2014).

## Quickstart

```
git clone https://github.com/illsaid/autonomous-lab-F5.git
cd autonomous-lab-F5
python3 longtail.py rare
```

That prints one neglected artwork: a random subject tag that exactly one work in the sample carries, with its live tate.org.uk URL. No dependencies beyond the Python 3 standard library; 3,458 real CC0 records ship in the repo. Add `--seed N` for a reproducible pick.

Other views:

```
python3 longtail.py tail -n 5        # random long-tail artworks
python3 longtail.py share            # long-tail share per classification
python3 longtail.py tags --rare      # all 1,345 singleton tags
python3 longtail.py show OBJECTID    # one record as JSON
```

`experiments/tate_fetch.sh` regenerates the sample deterministically, or fetches the full 69,202-record collection with `STRIDE=1`.

**[REPORT.md](REPORT.md)** is the final report: what the repo became, keyed to the judging criteria, with reproducible evidence for every claim.

## The experiment

This repository is part of an autonomous software experiment.

A scheduled F5 agent will periodically inspect this repo, read its prior state, choose one small next action, make limited changes, and record what it did.

The goal is not to begin with a fixed product idea. The goal is to see whether repeated, constrained autonomous work can turn an empty repository into something useful, strange, illuminating, or worth continuing.

## Core idea

The repo starts with a mission, a seed, rules, judging criteria, state files, and logs. The agent should use those files as memory.

The project may become a tool, dataset, simulator, game, research assistant, creative system, automation utility, knowledge base, story machine, visualizer, educational toy, or something else. The only requirement is that it must become increasingly concrete and usable over time.

## Important framing

Public repositories are allowed as research sources, but they are not the assignment.

The agent may explore neglected public artifacts of many kinds: public-domain material, open datasets, old web pages, small utilities, abandoned prototypes, documentation, APIs, archives, examples, games, simulations, lists, patterns, and cultural fragments.

Use exploration as raw material. Do not assume the final project has to be about GitHub, old code, or open-source archaeology.

## Key files

- `MISSION.md` — broad mission
- `SEED.md` — initial provocation
- `AGENT_RULES.md` — operating constraints
- `JUDGING.md` — how the project will be evaluated
- `AGENT_STATE.md` — current agent memory
- `CHANGELOG.md` — human-readable change log
- `DECISIONS.md` — decision and pivot log
- `RESEARCH_LOG.md` — public research notes
- `THIRD_PARTY_NOTICES.md` — license and attribution record
- `RUNS/` — machine-readable run records

## Experiment rule

Explore widely, but converge through artifacts.
