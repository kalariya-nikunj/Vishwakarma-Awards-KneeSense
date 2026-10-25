# Recording instructions

This is a procedure template. The logger is not yet included in this repository; complete its run command and verify configuration before recording.

## Before recording

1. Add/review firmware and logger source. Record board/sensor models, firmware versions, Python version, and installed package versions in a copy of `SESSION_TEMPLATE.md`.
2. Check node identity and placement (`KS_THIGH`, `KS_SHANK` in the separate test logger), power, mounting orientation, and calibration procedure. Record any unknown details.
3. Check the actual BLE characteristic, packet layout, duration, and output directory in the logger. The separate test script uses a 60-second duration and writes into `kneesense_output/` relative to the working directory; do not assume a newly added script has the same settings.
4. Use a unique run identifier and confirm output files will not overwrite an earlier run. Record the command and working directory. Close other applications connected to the sensors.

## During recording

1. Run the reviewed logger: `[insert actual command]`.
2. Wait for both devices to connect and follow the logger's startup/countdown messages. Record the movement protocol, start/end cues, repetitions, and any interruptions.
3. If a video is made, record how its timeline relates to the sensor recording. A shared visible cue can document alignment, but does not itself synchronize the two sensor clocks.
4. Save console packet counts, malformed-packet count, and errors. Keep partial/failed sessions and label them accordingly.

## After recording

1. Keep raw CSVs unchanged. Add copies to `data/raw/` with their original filenames; leave the original test files where they are. Preserve source files when deriving any cleaned data.
2. Add graph copies to `results/graphs/` and videos/photos to the matching `media/` folders. Record exact source-to-output links in the session record.
3. Confirm both device identifiers appear, inspect timestamp continuity, and note missing data, uneven sampling, and disconnects. Distinguish host reception time from device time.
4. Label graph axes and units, record processing steps, and describe only observations supported by that run. A successful BLE stream or plot is not evidence of validated knee-angle or OA performance.
5. Complete the session record and link it from the report. Review files before committing or sharing.
