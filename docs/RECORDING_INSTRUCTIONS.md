# Recording instructions

Use `software/kneesense_ble_logger.py` with the matching sensor firmware. The existing CSVs and PNGs are imported artifacts; their full recording conditions remain unknown. Complete a session note for future recordings.

## Before recording

1. Review firmware and logger source. Record board/sensor models, firmware versions, Python version, and installed package versions in a copy of `SESSION_TEMPLATE.md`. Use Python 3.10+ and install the root `requirements.txt`.
2. Check node identity and placement (`KS_THIGH`, `KS_SHANK`), power, mounting orientation, and calibration procedure. Set `DEVICE_NAME` appropriately before flashing each node. Keep each board stationary during its startup gyroscope bias calibration. Record any unknown details.
3. Check the BLE characteristic, packet layout, duration, and output directory in the logger. The supplied script uses a 60-second duration and writes into `kneesense_output/` relative to the working directory.
4. Use a unique run identifier and confirm output files will not overwrite an earlier run. Record the command and working directory. Close other applications connected to the sensors.

## During recording

1. From the repository root, run `python software/kneesense_ble_logger.py` after powering the nodes and enabling Bluetooth.
2. Wait for both devices to connect and follow the logger's startup/countdown messages. Record the movement protocol, start/end cues, repetitions, and any interruptions.
3. If a video is made, record how its timeline relates to the sensor recording. A shared visible cue can document alignment, but does not itself synchronize the two sensor clocks.
4. Save console packet counts, malformed-packet count, and errors. Keep partial/failed sessions and label them accordingly.

## After recording

1. Keep raw CSVs unchanged. Add copies to `data/raw/` with their original filenames; leave the original test files where they are. Preserve source files when deriving any cleaned data.
2. Add graph copies to `results/graphs/`. Keep large videos/photos in the linked Google Drive folder and record their exact Drive links in the session record. The repository's `media/` documentation links to that folder.
3. Confirm both device identifiers appear, inspect timestamp continuity, and note missing data, uneven sampling, and disconnects. Distinguish host reception time from device time.
4. Label graph axes and units, record processing steps, and describe only observations supported by that run. A successful BLE stream or plot is not evidence of validated knee-angle or OA performance.
5. Complete the session record and link it from the report. Review files before committing or sharing.
