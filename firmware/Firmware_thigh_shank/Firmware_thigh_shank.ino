
#include <Wire.h>
#include <math.h>
#include <stdint.h>
#include "LSM6DS3.h"
#include <ArduinoBLE.h>

// CHANGE THIS LINE FOR THE SECOND BOARD:
// Board 1: "KS_THIGH"
// Board 2: "KS_SHANK"
#define DEVICE_NAME "KS_THIGH"

LSM6DS3 imu(I2C_MODE, 0x6A);

const char* SERVICE_UUID =
    "8f2a0001-6d6f-4b6c-a12a-9b9f3c6e0001";

const char* DATA_UUID =
    "8f2a0002-6d6f-4b6c-a12a-9b9f3c6e0001";

BLEService imuService(SERVICE_UUID);

BLECharacteristic imuData(
    DATA_UUID,
    BLERead | BLENotify,
    16,
    true
);

const uint32_t SAMPLE_INTERVAL_US = 20000; // Target: 50 Hz
const int CAL_SAMPLES = 300;

float biasX = 0;
float biasY = 0;
float biasZ = 0;

uint32_t lastSampleUs = 0;

struct __attribute__((packed)) ImuPacket {
  uint32_t t_ms;
  int16_t ax_cms2;
  int16_t ay_cms2;
  int16_t az_cms2;
  int16_t gx_cdeg;
  int16_t gy_cdeg;
  int16_t gz_cdeg;
};

int16_t toInt16(float value) {
  long v = lroundf(value);

  if (v > 32767) v = 32767;
  if (v < -32768) v = -32768;

  return (int16_t)v;
}

void setup() {
  Serial.begin(115200);

  // Do not wait indefinitely for USB: the board may be battery-powered.
  uint32_t waitStart = millis();
  while (!Serial && millis() - waitStart < 3000) {
    delay(10);
  }

  if (imu.begin() != 0) {
    Serial.println("ERROR: IMU initialization failed.");
    while (true) {
      delay(1000);
    }
  }

  // Keep the board motionless throughout calibration.
  delay(1000);

  for (int i = 0; i < CAL_SAMPLES; i++) {
    biasX += imu.readFloatGyroX();
    biasY += imu.readFloatGyroY();
    biasZ += imu.readFloatGyroZ();
    delay(5);
  }

  biasX /= CAL_SAMPLES;
  biasY /= CAL_SAMPLES;
  biasZ /= CAL_SAMPLES;

  Serial.print("Device: ");
  Serial.println(DEVICE_NAME);
  Serial.print("Gyro bias X: ");
  Serial.println(biasX, 4);
  Serial.print("Gyro bias Y: ");
  Serial.println(biasY, 4);
  Serial.print("Gyro bias Z: ");
  Serial.println(biasZ, 4);

  if (!BLE.begin()) {
    Serial.println("ERROR: BLE initialization failed.");
    while (true) {
      delay(1000);
    }
  }

  BLE.setLocalName(DEVICE_NAME);
  BLE.setDeviceName(DEVICE_NAME);
  BLE.setAdvertisedService(imuService);

  imuService.addCharacteristic(imuData);
  BLE.addService(imuService);

  ImuPacket zeroPacket = {};
  imuData.writeValue(
      (const uint8_t*)&zeroPacket,
      sizeof(zeroPacket)
  );

  BLE.advertise();

  Serial.println("BLE advertising started.");
  lastSampleUs = micros();
}

void loop() {
  BLE.poll();

  uint32_t nowUs = micros();

  if ((uint32_t)(nowUs - lastSampleUs)
      < SAMPLE_INTERVAL_US) {
    return;
  }

  lastSampleUs = nowUs;

  const float G = 9.80665f;

  // Seeed LSM6DS3 library:
  // acceleration readings in g; gyro readings in deg/s.
  float ax = imu.readFloatAccelX() * G;
  float ay = imu.readFloatAccelY() * G;
  float az = imu.readFloatAccelZ() * G;

  float gx = imu.readFloatGyroX() - biasX;
  float gy = imu.readFloatGyroY() - biasY;
  float gz = imu.readFloatGyroZ() - biasZ;

  ImuPacket packet;

  packet.t_ms = millis();

  // Acceleration: hundredths of m/s^2.
  packet.ax_cms2 = toInt16(ax * 100.0f);
  packet.ay_cms2 = toInt16(ay * 100.0f);
  packet.az_cms2 = toInt16(az * 100.0f);

  // Gyroscope: hundredths of degrees/second.
  packet.gx_cdeg = toInt16(gx * 100.0f);
  packet.gy_cdeg = toInt16(gy * 100.0f);
  packet.gz_cdeg = toInt16(gz * 100.0f);

  imuData.writeValue(
      (const uint8_t*)&packet,
      sizeof(packet)
  );
}
