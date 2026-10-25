# KneeSense — Vishwakarma Awards Prototype

KneeSense is an experimental knee-motion sensing project being prepared for the Vishwakarma Awards. The current development workflow uses two sensor nodes, identified by the test logger as `KS_THIGH` and `KS_SHANK`, to collect accelerometer and gyroscope readings over Bluetooth Low Energy (BLE). Python is used to record readings and generate signal plots.

## Prototype status

This repository contains sensor firmware, a Python BLE logger, three CSV recordings with matching PNG graphs, SolidWorks models, and a KiCad project with custom libraries, fabrication exports, and historical backups. A finished report and documented reference-measurement evaluation are still pending.

The supplied files were copied from the local project folder with their original filenames and contents preserved. Recordings and graphs demonstrate the available acquisition artifacts; they do not establish measurement accuracy or clinical performance. Firmware compilation, CAD assembly resolution, and PCB manufacturability have not been verified during this import.

Knee-angle estimation, sensor alignment/calibration, synchronization between nodes, and comparison against a reference measurement remain to be documented and evaluated. No validated knee-angle accuracy, osteoarthritis (OA) detection, diagnosis, or treatment performance is claimed. Signal plots alone do not establish these capabilities.

## Repository layout

| Path | Intended contents |
| --- | --- |
| `firmware/` | Sensor-node source, board details, build/flash instructions |
| `software/` | Python BLE logger |
| `data/raw/` | Original recordings, preserved without manual edits |
| `results/graphs/` | Derived plots linked to source recordings |
| `hardware/KiCad/` | Schematics, PCB layouts, libraries, fabrication exports |
| `mechanical/CAD/` | Editable models and exported mechanical parts |
| `media/photos/` | Link to externally hosted prototype photos |
| `media/videos/` | Link to externally hosted demonstrations and recordings |
| `docs/report/` | Brief project report and supporting notes |

## Project files and demonstration media

- [Sensor firmware](firmware/Firmware_thigh_shank/Firmware_thigh_shank.ino): set `DEVICE_NAME` to `KS_THIGH` for one board and `KS_SHANK` for the other. The source includes ArduinoBLE and LSM6DS3 libraries, a target 50 Hz sampling interval, and stationary gyroscope bias calibration at startup. Board package and tested library versions still need recording.
- [Python BLE logger](software/kneesense_ble_logger.py): receives acceleration and angular velocity from both nodes, writes CSV, and plots four signal panels. It does not calculate knee angle or classify OA.
- [Raw recordings](data/raw/) and [matching graphs](results/graphs/): match files by their unchanged `kneesense_YYYYMMDD_HHMMSS` basename. Run conditions and participant/movement details remain to be documented.
- [KiCad project](hardware/KiCad/Prototype_KneeSense_V1/): preserves the supplied project tree and relative library/model references. See [hardware import notes](hardware/KiCad/README.md) before using fabrication files.
- [SolidWorks models](mechanical/CAD/3D-Models/): `Assem2.SLDASM`, `bottom plate_V5.SLDPRT`, and `casing_V4.SLDPRT`; assembly references have not been opened/verified.
- [Photos and videos on Google Drive](https://drive.google.com/drive/folders/1JCOzSr-7obGCgrjGczuZRWfTyBF06cKV?usp=sharing): supplied by the project owner and hosted externally to avoid storing large media in Git history. Folder contents and viewer access were not verified during import. Check access in a signed-out browser before sharing with judges. No Drive permissions were changed.

The original `Untitled-1.txt` file remains in `media/videos/`. The Drive folder is the intended location for demonstration media.

## Python setup

`requirements.txt` lists the logger's external dependencies. Use Python 3.10 or newer for the syntax used in the supplied script. Package versions are intentionally unpinned until the tested acquisition environment is recorded.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python software/kneesense_ble_logger.py
```

Run from the repository root with both correctly configured sensor nodes nearby and Bluetooth enabled. The unchanged logger records for 60 seconds and saves new CSV/PNG files to `kneesense_output/` relative to the working directory. After recording, copy CSVs to `data/raw/` and PNGs to `results/graphs/`, preserving filenames and documenting the session. The logger is not executed automatically by this repository.

## Adding evidence

1. Record board, sensor, firmware, and tested software versions for the supplied source.
2. Preserve original filenames and raw data; use a session record to link recordings, plots, and videos.
3. Complete [the data dictionary](docs/DATA_DICTIONARY.md) against the actual firmware and logger.
4. Follow [the recording instructions](docs/RECORDING_INSTRUCTIONS.md) and copy [the session template](docs/SESSION_TEMPLATE.md) for each run.
5. Write the brief report using [the report outline](docs/report/REPORT_TEMPLATE.md), separating observed behavior from planned work.

Only include material suitable for sharing. Record participant codes rather than personal identifiers in session notes; confirm permission before adding identifiable participant media.

Keep original recordings and design revisions available when adding or updating evidence.
