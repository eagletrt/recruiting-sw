# The dataset

One session logged by **Hydra** (our 2024 electric car) at the **Varano** circuit on 8 September 2024: the Endurance run of a multi-day test.

This is raw data off the car. It has not been cleaned, trimmed or relabelled for you — we only left out what is empty or known to be wrong (see [What is not in the package](#what-is-not-in-the-package)).

## How a session is recorded

The car has two CAN buses (`primary` and `secondary`) plus a u-blox GPS. The telemetry unit on board dumps every frame it sees to `candump.log` and the GPS stream to `gps_0.log`; after the session an offline parser decodes those dumps into one CSV per CAN message, under `parsed/`.

```
<time>_<LAYOUT>_<run>/
├── session_config.json      track, layout, run name, driver
├── laps.json                lap and sector boundaries from the on-track lap counter
├── car_config.json          setup of the car for this run (camber, toe, pressures, ...)
├── centerline.json          reference line of the layout (see below)
└── parsed/
    ├── primary/             CAN 1: ECU, inverters, HV and LV batteries, telemetry
    ├── secondary/           CAN 2: sensors and estimated vehicle state
    ├── inverters/           inverter-specific messages
    └── gps_0/               decoded u-blox UBX messages
```

Every CSV has the same shape: a `_timestamp` column, then one column per signal of that CAN message.

**`_timestamp` is a Unix timestamp in microseconds**, taken when the telemetry unit received the frame. It is the only thing that links the files together: each message has its own rate and its own timeline, so **nothing is sampled on a common clock**. Aligning them is your job (`pandas.merge_asof` is your friend, but think about what you are doing with it).

## The channels that matter for this project

All of these are in `parsed/secondary/` unless stated otherwise.

### Driver inputs

| File | Columns | Meaning |
|---|---|---|
| `pedal_throttle.csv` | `throttle` | Accelerator position, normalised **0 → 1** (APPS sensor). It never quite reaches 1.0: the pedal travel is calibrated with a margin, so ~0.95 is full throttle. |
| `pedal_brakes_pressure.csv` | `front`, `rear` | Hydraulic pressure in the two brake circuits, in **bar**. This is the real braking effort — there is no "brake %" channel. Typical peak braking is 15–25 bar front. |
| `steer_angle.csv` | `angle` | **Steering wheel** angle in **degrees**, signed (roughly ±110° lock to lock). Not the wheel angle at the tyre: divide by the steering ratio if you need that. |

Sampled at roughly 100 Hz each.

### Inertial sensors

| File | Columns | Meaning |
|---|---|---|
| `imu_acceleration.csv` | `x`, `y`, `z` | Accelerations in **g**, in the vehicle frame: `x` longitudinal, `y` lateral, `z` vertical. At standstill `z ≈ -1`, so gravity is included. ~235 Hz. Raw and noisy, it needs filtering before you can do anything with it. **Check the sign convention yourself** on a known braking event before you trust it. |
| `imu_angular_rate.csv` | `x`, `y`, `z` | Roll / pitch / yaw rates in **deg/s**. `z` is the yaw rate, which is what tells you how much the car is actually rotating. |

### Estimated vehicle state (the Kalman filter output)

These are **not sensors**. They are produced on board by our state estimator, which fuses GPS, IMU, wheel speeds and the vehicle model into a single consistent estimate of where the car is and how fast it is going. They are smooth and mutually consistent, but they are an *estimate*: they carry the noise and the assumptions of the filter, not just of one sensor.

| File | Columns | Meaning |
|---|---|---|
| `vehicle_speed.csv` | `u`, `v` | Longitudinal and lateral velocity in the vehicle frame, **m/s**. `v` is the sideslip velocity — small, and interesting. |
| `vehicle_position.csv` | `x`, `y`, `heading` | Position in a local ENU track frame, **metres** from the Varano origin (lat 44.680525, lon 10.022198); `heading` in **radians**. This is what you draw the track map with. |
| `primary/control_output.csv` | `estimated_velocity` | The scalar speed estimate the traction control actually runs on, **m/s**. Same estimator, published on the primary bus at ~100 Hz. In practice this is the cleanest speed channel in the log; `GPS_NAV_PVT.gSpeed` is the independent ground truth you can validate it against. |

### Powertrain and controls

| File | Columns | Meaning |
|---|---|---|
| `primary/control_output.csv` | `torque_l`, `torque_r`, `torque_max_l`, `torque_max_r` | Torque requested to the left and right motor, **Nm**, and the instantaneous limit imposed by the control (power limit, traction control, derating). Useful to tell "the driver asked for it" from "the car allowed it". |
| `primary/control_status.csv` | `map_power`, `sc_state`, `tv_state`, `reg_state` | Which power map is selected and whether traction control, torque vectoring and regen are enabled. **Check these before you compare anything**: a difference in how the car is configured is not a difference in how it is being driven. |
| `primary/hv_power.csv` | `power` | Power drawn from the HV pack, **kW**. |
| `front_angular_velocity.csv` | `fl`, `fr` | Front wheel angular speeds, **rad/s** (multiply by ~0.2 m rolling radius for the speed at the contact patch). Slip between these and `estimated_velocity` is how you see a locked or spinning wheel. |
| `inverters/` | | Motor speed, phase current and IGBT/motor temperatures per inverter. Vendor scaling, not needed for this project. |

### GPS

`parsed/gps_0/GPS_NAV_PVT.csv` is the full u-blox navigation solution at ~7.6 Hz: `lat`, `lon` (degrees), `gSpeed` (ground speed, m/s), `headMot`, plus quality indicators (`fixType`, `numSV`, `hAcc`). In the Endurance session the fix is 3D with ~30 satellites and ~17 cm horizontal accuracy, so it is a solid reference — but at 7.6 Hz it is far too slow to see a braking event.

### Lap timing

`laps.json` is the output of the on-track lap counter: a list of laps with `startTimestamp`, `endTimestamp` and the sector crossing timestamps, all in the same microsecond Unix clock as the CSVs. **This is the reliable source of lap boundaries.** The first entry has no `number`: it is everything recorded before the first crossing of the finish line, which here includes the whole time the logger was running in the paddock.

Lap boundaries being reliable does not make every lap a racing lap. Read the list before you use it.

Do *not* use `secondary/tlm_lap_time.csv` for lap times: `lap_time` there is the live running timer shown on the steering wheel (it ramps up during the lap and starts at a placeholder of 1000).

### The reference line

`centerline.json` holds a reference line for the layout, in the same frame as `vehicle_position.csv`:

- `x`, `y` — the line, resampled at 1 m spacing, closed
- `s` — arc length along the line, 0 → `length`
- `theta` — heading of the line, unwrapped, in radians
- `curvature` — 1/m, signed; **the cheapest way to find where the corners are** without any detection at all

For the Endurance layout this line is 805 m long and was rebuilt from the median of 17 clean laps; the individual laps sit within ~1.1 m of it. Projecting a lap onto it gives a monotonic distance coordinate — but doing that projection, and deciding whether you even want to, is up to you.

## Known issues

We are telling you these up front because they are properties of the log, not puzzles:

1. **Estimated position is noisy at full rate.** `vehicle_position` is published at ~97 Hz, and the jitter on it is comparable to the distance travelled between two samples. Integrate it raw and you get 856 m for a lap that is really ~805 m — a 6% error that is pure noise, not drift. Low-pass it before you differentiate or integrate anything. Decimated to ~10 Hz it agrees with GPS to within a metre.
2. **Laps are not all the same length.** The reference line is the median of the clean laps, 805 m, but the individual laps spread over roughly ±8 m around it, because different lines through the same corner are different distances. Do not expect your distance axis to close on exactly the same number every lap — that spread is part of what you are measuring.
3. **A third of the session is not running.** Of 2207 s of acquisition, about 1480 s have the car moving; the rest is paddock, pit and standing still with the logger on. Filter it out, and say how.
4. **Metadata is not gospel.** `session_config.json` has a single `driver` field, filled in by whoever started the acquisition. It is right about the track and the layout. It is not always the whole story about who drove.
5. **Sensor offsets.** Brake pressure and steering do not always read exactly zero at rest. Check the offsets before thresholding on them.

## What is not in the package

For the record, so that you know what exists on the car and why you are not seeing it:

- **Channels that are empty in this session** — sensors that were not mounted or not working that day (rear wheel speeds, damper travel, tyre pressures and temperatures). They are in the log as a header with no rows; we dropped them rather than have you discover them one by one.
- **The on-board curvilinear coordinate** (`vehicle_curvilinear_coordinates.csv`, the car's own `s`/`n` along the track) and the baseline files it is derived from. The baseline generator of that season had a bug, so the coordinate it produces in this log runs backwards for half the samples. It has since been fixed on the car; the `centerline.json` you get was rebuilt from this session's own laps. This is the reason requirement 2 exists.
- **The raw dumps** (`candump.log`, ~500 MB, and `gps_0.log`) and the battery, charger and low-voltage messages. Nothing there is useful for driving style, and the decoded CSVs already contain everything you need.
- **The `simulator/` folder**, which holds signals replayed from our simulator rather than measured on track.
