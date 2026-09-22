# Project 3

> ⚠️ This document is fairly technical to maintain brevity, if you have **any** questions ask your recruiter or come visit us at floor -2 of Povo 2.

## Abstract

Our live telemetry UI is written in C++, but everything that happens *after* the session — post-processing, vehicle dynamics analysis, prototyping of engineering tools — is done in Python. This project is about that side of the job.

You are given a **raw log recorded by our car (Hydra) at Varano in September 2024**, during an Endurance run of a test weekend. Your task is to build a **standalone, interactive Streamlit application** that a trackside engineer can use to compare how the track is being attacked across the laps and the stints of that session.

This is not a "plot the CSV" exercise: the data is exactly as it came off the car, with all the noise, the asynchronous sampling and the approximate metadata that a real log has. **Handling that is part of the task.** We care more about the soundness of your reasoning than about the number of features you cram into the UI.

Read [`data.md`](./data.md) before starting: it describes the log structure, the physical meaning and units of every channel you need, and the known issues of this dataset.

## The dataset

Download link: **TBD — ask your recruiter**

You get **one session**: the Endurance run of 8 September 2024 at Varano. 2207 s of acquisition, 23 timed laps, about 20 km covered — the richest log of that test. One folder, containing:

- `session_config.json` — track, layout, driver, run name
- `laps.json` — lap and sector boundaries as detected on track by the lap counter
- `car_config.json` — setup of the car for this run
- `centerline.json` — the reference line of the layout, resampled at 1 m
- `parsed/` — the CAN bus and GPS logs already decoded into CSV, one file per message

> This is a full FSAE Endurance run. Keep in mind **how an Endurance event is run** when you look at the lap list — the session metadata does not tell you the whole story.

One session is enough: there is more usable driving in it than in the rest of the test weekend put together, and everything you need to compare two ways of driving the same track is already inside it.

## Core requirements

### 1. Data loading and preprocessing

Every CAN message is logged on its own timeline, at its own rate, with microsecond Unix timestamps. Build a loader that turns a session folder into something you can actually do vehicle dynamics on.

We expect you to reason about (and document) at least: the common time base you resample onto and why, how you filter the signals that need it, how you deal with channels logged at rates that differ by an order of magnitude, and how you decide what is "the car moving on track" versus paddock, pit and stationary time.

### 2. A distance axis

Comparing laps in the time domain is useless — two laps drift apart after the first corner. You need a **distance (or track position) axis** shared by all laps.

The car does not log one you can use, so you have to build it. You get a reference line for the layout (`centerline.json`, see `data.md`): project onto it, integrate speed, or do something else entirely. Explain the method you chose and show that it is consistent lap to lap.

### 3. Lap and corner-phase segmentation

Split the session into laps, discarding in-laps, out-laps and anything that is not a representative flying lap. Justify what you discard — and look at the lap list before you assume it is 23 equivalent laps.

Then, inside a lap, segment the corners into driving phases. We are interested in how a driver approaches a corner, so at a minimum: **braking point, braking phase, trail braking, minimum speed / apex, throttle application on exit**. The algorithm is yours to design — thresholds, state machine, change-point detection, clustering on the pedal/steer/acceleration signals, whatever you can defend.

### 4. Driving style characterisation

Turn the segmentation into a quantitative description of a driver's style: per-corner and per-lap features (braking point and intensity, how long throttle and brake overlap, how aggressively the steering is applied, how the car is rotated, consistency between laps, ...) and an analysis on top of them — statistics, clustering, dimensionality reduction, your call.

The question you are answering is the one an engineer actually asks: **"in what way do these two drivers drive this corner differently, and what does it cost in lap time?"**

### 5. The Streamlit dashboard

Build a dashboard that lets a race engineer:

- select and overlay laps and stints, individually or grouped;
- see the raw traces (speed, pedals, steering, accelerations) plotted against the distance axis, overlaid and aligned;
- see the output of your segmentation and of your style analysis — for example the phases highlighted on the traces, the corners coloured on a track map, a scatter or table comparing corners between drivers;
- get to an actionable insight quickly. Assume the person using it has 5 minutes between two runs, not an afternoon.

## What we evaluate

- **Data handling** — how you deal with raw, asynchronous, multi-variate, imperfect time series.
- **Analytical approach** — the logic behind your definition of "driving style" and how mathematically sound it is. A simple method you can defend beats a complex one you cannot.
- **Code quality and architecture** — clean, modular, documented Python. Data layer, analysis layer and UI layer should not be the same file.
- **UI/UX for engineers** — is this usable trackside, or is it a demo?
- **Honesty about the data** — we know what is wrong with these logs. Telling us what you found, and what you decided to do about it, counts in your favour.

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
- The dataset (ask your recruiter for the link)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install streamlit pandas numpy scipy scikit-learn plotly
streamlit run app.py
```

You are free to use any other library, as long as `requirements.txt` is complete and the app starts on a clean machine.
