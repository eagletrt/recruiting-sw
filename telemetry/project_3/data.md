# The dataset

One session logged by **Hydra** (our 2024 electric car) at the **Varano** circuit on 8 September 2024: the Endurance run of a multi-day test.

## How a session is recorded

The car has two CAN buses (`primary` and `secondary`) plus a u-blox GPS. The telemetry unit on board dumps every frame it sees, and an offline parser decodes those dumps into one CSV per CAN message, under `parsed/`.

```
2024_09_08_14_38_41_ENDURANCE_run1/
├── centerline.json          reference line of the layout
└── parsed/
    ├── primary/             CAN 1
    ├── secondary/           CAN 2: sensors and estimated vehicle state
    ├── inverters/           inverter messages
    └── gps_0/               decoded u-blox UBX messages
```

The CSVs are gzipped; `pandas.read_csv` opens them directly. Every one has the same shape: a `_timestamp` column, then one column per signal of that CAN message.

**`_timestamp` is a Unix timestamp in microseconds**, taken when the telemetry unit received the frame. It is the only thing that links the files together: each message has its own rate and its own timeline, so **nothing is sampled on a common clock**. Aligning them is your job (`pandas.merge_asof` is your friend, but think about what you are doing with it).

## The channels

All in `parsed/secondary/` unless stated otherwise.

### Driver inputs

| File                          | Columns             | Meaning                                                                                                               |
| ----------------------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `pedal_throttle.csv`        | `throttle`        | Accelerator position,**0 → 1**. Full travel is about 0.95.                                                     |
| `pedal_brakes_pressure.csv` | `front`, `rear` | Pressure in the two brake circuits, in**bar**. Peak braking is 15–25 bar front.                                |
| `steer_angle.csv`           | `angle`           | **Steering wheel** angle in **degrees**, signed, roughly ±110° lock to lock. Not the angle at the tyre. |

About 100 Hz each.

### Inertial sensors

| File                     | Columns             | Meaning                                                                                                                                                                |
| ------------------------ | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `imu_acceleration.csv` | `x`, `y`, `z` | Accelerations in**g**, vehicle frame: `x` longitudinal, `y` lateral, `z` vertical. Gravity included, so `z ≈ -1` at standstill. ~235 Hz, raw and noisy. |
| `imu_angular_rate.csv` | `x`, `y`, `z` | Roll, pitch and yaw rates in**deg/s**. `z` is the yaw rate.                                                                                                    |

### Wheels and motors

| File                                        | Columns         | Meaning                                                                                        |
| ------------------------------------------- | --------------- | ---------------------------------------------------------------------------------------------- |
| `front_angular_velocity.csv`              | `fl`, `fr`  | Front wheel angular speeds,**rad/s**. Rolling radius is about 0.19 m.                    |
| `inverters/inv_l_id_a8_n_actual_filt.csv` | `n_act_filt`  | Rear left wheel angular speed from the motor encoder,**rad/s**, same scale as the front. |
| `inverters/inv_r_id_a8_n_actual_filt.csv` | `n_act_filt`  | Rear right, same.                                                                              |
| `inverters/inv_l_id_27_iq_actual.csv`     | `iq_act_filt` | Torque at the left wheel**A.**                                                           |
| `inverters/inv_r_id_27_iq_actual.csv`     | `iq_act_filt` | Right wheel, same.                                                                             |
| `primary/hv_power.csv`                    | `power`       | Power drawn from the HV pack,**kW**.                                                     |

The rears are driven and the fronts are not, so the difference between the two pairs is wheel slip.

### Estimated vehicle state

Produced on board by the state estimator, which fuses GPS, IMU and wheel speeds into one consistent estimate. These are not sensor readings.

| File                                    | Columns                   | Meaning                                                                                                                                                                                                                                                                                                                                                                 |
| --------------------------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `vehicle_speed.csv`                   | `u`, `v`              | Longitudinal and lateral velocity in the vehicle frame,**m/s**. `v` is the sideslip velocity.                                                                                                                                                                                                                                                                   |
| `vehicle_position.csv`                | `x`, `y`, `heading` | Position in a local ENU track frame,**metres** from the Varano origin (lat 44.680525, lon 10.022198); `heading` in **radians**.                                                                                                                                                                                                                           |
| `vehicle_curvilinear_coordinates.csv` | `s`, `n`              | Where the car is along the track rather than in x/y.`s` is how far round the lap it has got, in **metres** from the start/finish line: it runs 0 → 805 and wraps once per lap, so it is *not* sorted within a lap. `n` is how far it sits to the side of the reference line, in **metres**, signed, positive to the left of the direction of travel. |

### GPS

`parsed/gps_0/GPS_NAV_PVT.csv` is the u-blox navigation solution at ~7.6 Hz: `lat`, `lon` (degrees), `gSpeed` (ground speed, m/s), `headMot`, plus quality indicators (`fixType`, `numSV`, `hAcc`). Accurate, but far too slow to see a braking event.

### The reference line

`centerline.json` describes the layout in the same frame as `vehicle_position.csv`:

- `x`, `y` — the line, at 1 m spacing, closed
- `s` — distance along the line, 0 → `length` (805 m)
- `theta` — heading of the line, unwrapped, in radians
- `curvature` — 1/m, signed. The cheapest way to find where the corners are, with no detection at all.
