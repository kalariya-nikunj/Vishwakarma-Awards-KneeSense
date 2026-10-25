# Recording data dictionary

Status: schema inspected against `software/kneesense_ble_logger.py` and `firmware/Firmware_thigh_shank/Firmware_thigh_shank.ino`. Their field order and scale agree. Verify the firmware actually flashed for each recorded session; physical accuracy, sensor configuration, and alignment have not been established by this source inspection.

One CSV row represents one received BLE notification from one node. Rows from two devices may be interleaved; they are not synchronized pairs.

| CSV column | Meaning | Unit / type | Verification needed |
| --- | --- | --- | --- |
| `host_time_s` | Host monotonic time at notification handling, relative to recording start | seconds, float | Includes reception/scheduling delay; not sensor sample time |
| `device` | Logger-assigned node name | `KS_THIGH` or `KS_SHANK` | Confirm physical placement and device identity |
| `device_t_ms` | Timestamp transmitted by that node | milliseconds, unsigned 32-bit integer | Confirm clock origin, rollover handling, drift, and reset behavior |
| `ax_ms2`, `ay_ms2`, `az_ms2` | Decoded acceleration components | nominal m/s², float | Logger divides packet integers by 100; confirm firmware scale, axes, calibration, and gravity handling |
| `gx_dps`, `gy_dps`, `gz_dps` | Decoded angular-velocity components | nominal degrees/second, float | Logger divides packet integers by 100; confirm firmware scale, axes, and calibration |
| `accel_mag_ms2` | `sqrt(ax_ms2² + ay_ms2² + az_ms2²)` | nominal m/s², float | Derived from decoded acceleration; not knee angle |

The logger expects little-endian `<I6h` packets: one unsigned 32-bit timestamp and six signed 16-bit components, totaling 16 bytes. It rejects other packet lengths. The firmware uses a packed structure in the same field order, multiplies sensor values by 100, rounds them, and saturates to signed 16-bit limits before transmission; byte order depends on the target board. It uses `millis()` for device timestamps and targets a 20,000-microsecond sample interval (50 Hz), which is not a measured delivered rate. Acceleration includes gravity; gyroscope readings have a stationary startup bias subtracted. Independent node timestamps must not be assumed to share a clock.

## Complete for the actual recording format

- Firmware file/version for each node: [fill in]
- Logger file/version and Python/package versions: [fill in]
- Sensor model, ranges, nominal sample rate: [fill in]
- Actual CSV header and any added/changed columns: [fill in]
- Axis orientation, mounting position, and calibration: [fill in]
- Missing/malformed packet policy and disconnect handling: [fill in]
- Synchronization method, if any: [fill in]
- Raw file paths and session record path: [fill in]

Record unknown values explicitly as `unknown`; do not substitute assumed specifications. Retain original raw recordings and document transformations separately.
