
import sys
import json
import time
import threading
from datetime import datetime, timezone

import paho.mqtt.client as mqtt


YOUR_NAME = "claude"                                  
BROKER    = "broker.hivemq.com"
PORT      = 1883
TOPIC     = f"warehouse/sensor/{YOUR_NAME}/temp"
DEVICE_ID = "warehouse-sensor-01"
UNIT      = "C"


ALERT_THRESHOLD = 26



def make_client(client_id):
    """paho-mqtt 2.0 requires a CallbackAPIVersion; 1.x does not.
    This builds a client that works under either installed version."""
    try:
        return mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,   # paho-mqtt >= 2.0
            client_id=client_id,
        )
    except (AttributeError, TypeError):
        return mqtt.Client(client_id=client_id)  # paho-mqtt 1.x



def on_connect(client, userdata, *args):
    """Fires when the subscriber connects to the broker."""
    print(f"[SUBSCRIBER] Connected to {BROKER}:{PORT}")
    client.subscribe(TOPIC)
    print(f"[SUBSCRIBER] Subscribed to '{TOPIC}' - waiting for data...\n")


def on_message(client, userdata, msg):
    """Fires every time a message arrives on the subscribed topic."""
    received_at = datetime.now(timezone.utc).strftime("%H:%M:%S")
    try:
        data = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        print(f"[SUBSCRIBER] Received non-JSON payload: {msg.payload!r}")
        return

    value = data.get("value")
    unit  = data.get("unit", "")
    dev   = data.get("device_id", "?")

   
    if isinstance(value, (int, float)) and value >= ALERT_THRESHOLD:
        status = "🔥 ALERT - elevated temperature!"
    else:
        status = "✅ NORMAL"

    print(f"[SUBSCRIBER] {received_at} | topic={msg.topic}")
    print(f"             {dev}: {value}{unit}  ->  {status}")
    print(f"             raw JSON: {json.dumps(data)}\n")


def run_subscriber(stop_event=None):
    client = make_client(f"monitoring-system-{YOUR_NAME}")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=60)

    if stop_event is None:

        client.loop_forever()
    else:

        client.loop_start()
        stop_event.wait()
        client.loop_stop()
        client.disconnect()



def build_payload(value):
    """Construct the JSON telemetry message required by Part 2."""
    return {
        "device_id": DEVICE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "value":     value,
        "unit":      UNIT,
    }


def run_publisher():
    client = make_client(f"device-{YOUR_NAME}")
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()
    time.sleep(1)  
    print(f"[PUBLISHER] Connected. Publishing telemetry to '{TOPIC}'\n")

 
    normal_band   = [21, 22, 23, 24, 25]
    elevated_band = [26, 27, 28, 29, 30]

    print("[PUBLISHER] --- Normal range (21-25 C) ---")
    for v in normal_band:
        payload = build_payload(v)
        client.publish(TOPIC, json.dumps(payload), qos=1)
        print(f"[PUBLISHER] Published value={v}{UNIT}")
        time.sleep(1)

    print("\n[PUBLISHER] --- Elevated range (26-30 C) ---")
    for v in elevated_band:
        payload = build_payload(v)
        client.publish(TOPIC, json.dumps(payload), qos=1)
        print(f"[PUBLISHER] Published value={v}{UNIT}")
        time.sleep(1)

    time.sleep(1)
    client.loop_stop()
    client.disconnect()
    print("\n[PUBLISHER] Done. All 10 messages sent.")



def run_demo():
    print("=" * 60)
    print("  Lab 9 - MQTT Telemetry Demo (subscriber + publisher)")
    print("=" * 60 + "\n")

    stop_event = threading.Event()
    sub_thread = threading.Thread(target=run_subscriber, args=(stop_event,))
    sub_thread.start()

    time.sleep(2)   
    run_publisher()

    time.sleep(2)   
    stop_event.set()
    sub_thread.join()
    print("\nDemo complete.")


# ----------------------------------------------------------------------
if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "demo"

    if mode in ("sub", "subscribe", "subscriber"):
        try:
            run_subscriber()
        except KeyboardInterrupt:
            print("\n[SUBSCRIBER] Stopped.")
    elif mode in ("pub", "publish", "publisher"):
        run_publisher()
    else:
        run_demo()
