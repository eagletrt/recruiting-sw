# Project 3

> ⚠️ This document is fairly technical to maintain brevity, if you have **any** questions ask your recruiter or come visit us at floor -2 of Povo 2.

## Abstract

Our live telemetry UI is written in C++, but everything that happens *after* the session — post-processing, vehicle dynamics analysis, machine learning, prototyping of engineering tools — is done in Python. This project is about that side of the job.

You are given a **raw log recorded by our car (Hydra) at Varano in September 2024**. Your task is to build a **standalone, interactive Streamlit application** that answers the question a race engineer asks after every session:

> **Where is the car being driven differently, what is that worth in lap time, and what would have to change to get it back?**

This is not a "plot the CSV" exercise. The log is what came off the car: channels on their own clocks, no lap list, no annotations, nothing telling you how the session is structured. Working that out is the first half of the task.

Read [`data.md`](./data.md) before starting: it describes the log structure and the physical meaning and units of every channel.

## The objective

By the end you should be able to put a number on a sentence like *"through the corner at 580 m the car is 4 m/s slower, which costs 0.3 s a lap, and it is because the brakes are released 10 m earlier and the throttle comes back 15 m later."*

Getting there means, roughly:

1. deciding what a comparable piece of driving is, and finding those pieces in the log;
2. describing how each corner is attacked, in numbers rather than in pictures;
3. turning those numbers into time won and lost, and into something actionable.

How you get there is yours to design. What we care about is that each step holds up when we ask why.

## The dataset

The log is in this folder, under [`2024_09_08_14_38_41_ENDURANCE_run1/`](./2024_09_08_14_38_41_ENDURANCE_run1): 2207 s of acquisition, about 20 km covered. It contains:

- `parsed/` — the CAN bus and GPS logs decoded into CSV, one file per message
- `centerline.json` — the reference line of the layout

> The car does not run continuously for 2207 s, and it is not driven the same way throughout. Work out the structure of the session from the data before you assume anything about it.

## Core requirements

### 1. Data loading and preprocessing

Every CAN message is logged on its own timeline, at its own rate, with microsecond Unix timestamps. Build a loader that turns the session folder into something you can actually do vehicle dynamics on.

We expect you to reason about (and document) at least: the common time base you resample onto and why, how you filter the signals that need it, how you deal with channels logged at rates that differ by an order of magnitude, and how you separate the car driving on track from everything else in the log.

### 2. A distance axis

Comparing laps in the time domain is useless — two laps drift apart after the first corner. Everything you compare has to live on a **distance axis**.

The raw material is there: every position sample carries the distance along the track (`s`, see `data.md`). What is not done for you is the part that matters. `s` is sampled on the position channel's clock, not on a regular distance grid; every other channel sits on its own timeline; and no two laps are exactly the same length. Getting speed, pedals, steering and accelerations onto one common distance grid, so that two laps can actually be subtracted from each other, is your job.

Show that your grid is consistent lap to lap, and say what you did at the seams.

### 3. Segmentation

Split the session into laps, and the laps into the pieces worth comparing. Discard whatever is not representative, and justify what you discard.

Then, inside a lap, segment the corners into driving phases: at a minimum **braking point, braking phase, trail braking, minimum speed / apex, throttle application on exit**. The algorithm is yours to design — thresholds, state machine, change-point detection, clustering on the pedal, steering and acceleration signals, whatever you can defend.

### 4. Driving style, and what it costs

Turn the segmentation into a quantitative description of how the car is being driven: per-corner and per-lap features — braking point and intensity, how long throttle and brake overlap, how quickly the steering is applied, how much the car is rotated, how consistent one lap is with the next.

Then close the loop and **put time on it**. The speed difference between two pieces of driving integrates into a time difference along the lap, and that tells you where it is won and where it is lost. A corner where one is 4 m/s faster and a corner where the other gains half of it back are a different story from an overall pace gap, and only the distance-resolved version distinguishes them.

**Machine learning is welcome here**, and this dataset gives it real things to chew on:

- **unsupervised clustering** of the per-corner feature vectors — do corner approaches fall into distinct styles on their own, without you labelling anything?
- **dimensionality reduction** on those features, to see how laps sit relative to each other in one picture;
- **change-point or anomaly detection** over the session, to find where behaviour shifts rather than assuming where it should;
- a **supervised model** that predicts which part of the session a lap or a corner comes from — interesting not for its accuracy, but for what its feature importances say about where the difference actually lives.

Two caveats, and we mean both. First, the output has to be interpretable: an engineer cannot act on "cluster 2", they act on "here the car brakes 8 m later and carries 3 km/h more through the apex". Translating the model's output back into vehicle dynamics is the part we will ask you about. Second, a well-chosen statistical approach is a complete answer too — do not add a model in order to have one, and do not hide a weak feature set behind a strong classifier.

### 5. The Streamlit dashboard

Build a dashboard that lets a race engineer:

- select and overlay laps, individually or grouped;
- see the traces (speed, pedals, steering, accelerations) plotted against the distance axis, overlaid and aligned;
- see where time is won and lost along the lap, not just in total;
- see the output of your segmentation and of your style analysis — the phases highlighted on the traces, the corners coloured on a track map, a table comparing corners;
- get to an actionable insight quickly. Assume the person using it has 5 minutes between two runs, not an afternoon.

## What we evaluate

- **Data handling** — how you deal with raw, asynchronous, multi-variate, imperfect time series.
- **Analytical approach** — the logic behind your definition of "driving style" and how mathematically sound it is. A simple method you can defend beats a complex one you cannot.
- **Code quality and architecture** — clean, modular, documented Python. Data layer, analysis layer and UI layer should not be the same file.
- **UI/UX for engineers** — is this usable trackside, or is it a demo?
- **Honesty about the data** — this log has its quirks. Telling us what you found, and what you decided to do about it, counts in your favour.

Not required, but appreciated: tests on the analysis functions, a short profiling note if you had to deal with the size of the logs, a request to us for anything that is missing.

## Deliverables

- A **public GitHub repository** named `recruiting-sw-telemetry` containing your source code (`.py` files, `requirements.txt`). Do **not** commit the dataset.
- A `readme.md` explaining your analytical approach, how to run the app locally, and every assumption you made about the data.
- Commit as you go: we look at the history, not only at the final state.
- Deployment is not required, but the app must run locally with a clean `pip install -r requirements.txt`.

## Getting started

### Prerequisites

- `git` and a [GitHub](https://github.com) account
- Python 3.10+

### Setup

- Download the project files [here](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Feagletrt%2Frecruiting-sw%2Ftree%2Fmaster%2Ftelemetry%2Fproject_3) — the log comes with them
- Create a new GitHub repository and upload your work via git
- Start working on the task, creating git commits as you make progress
- When it's time to deliver, please send your recruiter a link to your github repository

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install streamlit pandas numpy scipy scikit-learn plotly
streamlit run app.py
```

You are free to use any other library, as long as `requirements.txt` is complete and the app starts on a clean machine.
