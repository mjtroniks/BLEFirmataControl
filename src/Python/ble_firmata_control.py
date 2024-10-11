import asyncio
from bleak import BleakScanner, BleakClient

# UUIDs for the BLE characteristics
SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
CHARACTERISTIC_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

# Target device name
TARGET_NAME = "FIRMATA"

async def connect_and_blink():
    print("Scanning for devices...")
    devices = await BleakScanner.discover()

    target_device = None
    for device in devices:
        print(f"Device: {device.name}, Address: {device.address}")
        if device.name == TARGET_NAME:
            target_device = device
            print(f"Found target device: {device.name}, Address: {device.address}")
            break

    if target_device is None:
        print("Target device not found.")
        return

    async with BleakClient(target_device.address) as client:
        print(f"Attempting to connect to {target_device.name} at {target_device.address}")

        # Wait for the Java program confirmation
        input("Did you run the Java program? Press Enter to continue once Java is ready.")

        if client.is_connected:
            print("Connected to Arduino.")
            services = await client.get_services()
            for service in services:
                print(f"Service: {service.uuid}")
                for char in service.characteristics:
                    print(f"  Characteristic: {char.uuid}, Properties: {char.properties}")

            try:
                while True:
                    command = input("Enter command from Java (type 'BLINK' to blink LED): ")
                    if command == "BLINK":
                        await client.write_gatt_char(CHARACTERISTIC_UUID, b'\x01')  # Sending command to Arduino
                        print("Successfully wrote to the characteristic.")
            except Exception as e:
                print(f"Failed to write to characteristic: {e}")
        else:
            print("Failed to connect to the device.")

loop = asyncio.get_event_loop()
loop.run_until_complete(connect_and_blink())
