
import asyncio
import csv
import math
import struct
import time
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
from bleak import BleakClient, BleakScanner

THIGH_NAME = "KS_THIGH"
SHANK_NAME = "KS_SHANK"

DATA_UUID = "8f2a0002-6d6f-4b6c-a12a-9b9f3c6e0001"

RECORD_SECONDS = 60

# Rows contain:
# uint32 timestamp + six int16 values = 16 bytes.
PACKET_FORMAT = "<I6h"
PACKET_SIZE = struct.calcsize(PACKET_FORMAT)

OUTPUT_DIR = Path("kneesense_output")
OUTPUT_DIR.mkdir(exist_ok=True)

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_path = OUTPUT_DIR / f"kneesense_{run_id}.csv"
plot_path = OUTPUT_DIR / f"kneesense_{run_id}.png"

records = {
    THIGH_NAME: [],
    SHANK_NAME: [],
}

start_time = None
csv_writer = None
csv_file = None
bad_packets = 0


def make_handler(device_name):
    def handle_notification(sender, data):
        global bad_packets

        if len(data) != PACKET_SIZE:
            bad_packets += 1
            return

        t_ms, ax, ay, az, gx, gy, gz = struct.unpack(
            PACKET_FORMAT, bytes(data)
        )

        host_time = time.monotonic() - start_time

        # Firmware scales both accelerometer and gyro values by 100.
        ax, ay, az = ax / 100.0, ay / 100.0, az / 100.0
        gx, gy, gz = gx / 100.0, gy / 100.0, gz / 100.0

        accel_mag = math.sqrt(ax*ax + ay*ay + az*az)

        row = {
            "host_time_s": host_time,
            "device": device_name,
            "device_t_ms": t_ms,
            "ax_ms2": ax,
            "ay_ms2": ay,
            "az_ms2": az,
            "gx_dps": gx,
            "gy_dps": gy,
            "gz_dps": gz,
            "accel_mag_ms2": accel_mag,
        }

        records[device_name].append(row)

        csv_writer.writerow(row)
        csv_file.flush()

    return handle_notification


async def main():
    global start_time, csv_writer, csv_file

    print("Scanning for KneeSense sensors...")
    print("Turn on both XIAO modules and keep them nearby.")

    devices = await BleakScanner.discover(timeout=10)

    found = {}
    for device in devices:
        if device.name in (THIGH_NAME, SHANK_NAME):
            found[device.name] = device

    for device in devices:
        print(f"Found: {device.name or 'Unnamed'} | {device.address}")

    missing = [
        name for name in (THIGH_NAME, SHANK_NAME)
        if name not in found
    ]

    if missing:
        print("\nMissing devices:", ", ".join(missing))
        print("Check power, firmware, BLE and device names.")
        return

    columns = [
        "host_time_s", "device", "device_t_ms",
        "ax_ms2", "ay_ms2", "az_ms2",
        "gx_dps", "gy_dps", "gz_dps",
        "accel_mag_ms2",
    ]

    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            csv_file = f
            csv_writer = csv.DictWriter(f, fieldnames=columns)
            csv_writer.writeheader()

            print("\nConnecting to both devices...")

            async with (
                BleakClient(found[THIGH_NAME]) as thigh,
                BleakClient(found[SHANK_NAME]) as shank
            ):
                print("Connected to both sensors.")
                print(f"Recording for {RECORD_SECONDS} seconds.")
                print("Start your movement only after the countdown.")

                await asyncio.sleep(3)
                start_time = time.monotonic()

                await thigh.start_notify(
                    DATA_UUID, make_handler(THIGH_NAME)
                )
                await shank.start_notify(
                    DATA_UUID, make_handler(SHANK_NAME)
                )

                try:
                    await asyncio.sleep(RECORD_SECONDS)
                finally:
                    await thigh.stop_notify(DATA_UUID)
                    await shank.stop_notify(DATA_UUID)

    except Exception as exc:
        print("\nBluetooth recording failed:", repr(exc))
        print("Check that no other app is connected to the sensors.")
        return

    print("\nRecording finished.")
    print("Thigh packets:", len(records[THIGH_NAME]))
    print("Shank packets:", len(records[SHANK_NAME]))
    print("Malformed packets:", bad_packets)
    print("CSV saved to:", csv_path)

    if not records[THIGH_NAME] or not records[SHANK_NAME]:
        print("At least one sensor produced no usable packets.")
        return

    # Four graphs: accelerometer and gyroscope for each sensor.
    fig, axes = plt.subplots(4, 1, figsize=(13, 11), sharex=True)

    configs = [
        (THIGH_NAME, "Acceleration (m/s²)", ["ax_ms2", "ay_ms2", "az_ms2"]),
        (THIGH_NAME, "Angular velocity (deg/s)", ["gx_dps", "gy_dps", "gz_dps"]),
        (SHANK_NAME, "Acceleration (m/s²)", ["ax_ms2", "ay_ms2", "az_ms2"]),
        (SHANK_NAME, "Angular velocity (deg/s)", ["gx_dps", "gy_dps", "gz_dps"]),
    ]

    labels = {
        "ax_ms2": "X", "ay_ms2": "Y", "az_ms2": "Z",
        "gx_dps": "X", "gy_dps": "Y", "gz_dps": "Z",
    }

    for ax, (device_name, title, fields) in zip(axes, configs):
        data = records[device_name]

        for field in fields:
            ax.plot(
                [r["host_time_s"] for r in data],
                [r[field] for r in data],
                label=labels[field],
                linewidth=0.8,
            )

        ax.set_title(f"{device_name} — {title}")
        ax.set_ylabel(title)
        ax.grid(True, alpha=0.3)
        ax.legend(loc="upper right")

    axes[-1].set_xlabel("Laptop receive time since recording start (s)")

    fig.suptitle("KneeSense dual-IMU recording")
    fig.tight_layout()
    fig.savefig(plot_path, dpi=180)
    print("Graph saved to:", plot_path)

    plt.show()


if __name__ == "__main__":
    asyncio.run(main())
