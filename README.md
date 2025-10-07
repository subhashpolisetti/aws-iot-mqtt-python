# 🛰️ AWS IoT Core MQTT Client (mTLS)

A lightweight Python client for connecting to **AWS IoT Core** using **mutual TLS (mTLS)** authentication.  
This tool demonstrates secure MQTT publish/subscribe communication using the official **AWS IoT Device SDK for Python (V2)**.

---

## Features

- ✅ Secure connection using **mutual TLS (X.509 certificates)**  
- ✅ Automatic **Root CA detection** (no need to specify manually)  
- ✅ Simple **publish/subscribe** demo  
- ✅ Configurable **topic**, **client ID**, and **keep-alive interval**  
- ✅ Optional **TRACE logging** for debugging network events  

---

## Requirements

- Python 3.7 or higher  
- AWS IoT Device SDK v2 for Python  

Install dependencies:
```bash
pip install awscrt awsiot
```

---

##  Setup

### 1. Generate AWS IoT Device Certificates
If you haven’t already, create and download certificates via the AWS IoT Console or CLI:
- Device certificate (`*.pem.crt`)
- Private key (`*.private.key`)
- Amazon Root CA (`AmazonRootCA1.pem`)

Attach an **IoT policy** that allows publish/subscribe on the desired topic.

---

### 2. Prepare Your Files
Place the following in your working directory:
```
device-cert.pem.crt
private-key.pem.key
AmazonRootCA1.pem
mqtt_client.py
```

---

### 3. Run the Client

```bash
python mqtt_client.py   --endpoint <your-iot-endpoint>   --cert device-cert.pem.crt   --key private-key.pem.key   --topic class/demo/topic
```

Example:
```bash
python mqtt_client.py   --endpoint a1b2c3d4e5f6-ats.iot.us-east-1.amazonaws.com   --cert ./device-cert.pem.crt   --key ./private-key.pem.key   --trace
```

---

##  Command-Line Options

| Flag | Description | Default |
|------|--------------|----------|
| `--endpoint` | AWS IoT Core endpoint (e.g. `xxxx-ats.iot.us-east-1.amazonaws.com`) | **Required** |
| `--cert` | Path to device certificate | **Required** |
| `--key` | Path to private key | **Required** |
| `--root-ca` | Path to root CA (auto-detected if omitted) | Auto |
| `--client-id` | MQTT client ID | `iot-mqtt-device-<timestamp>` |
| `--topic` | MQTT topic to publish/subscribe | `class/demo/topic` |
| `--keepalive` | Keep-alive interval (seconds) | 30 |
| `--listen-secs` | Time to listen after publishing | 20 |
| `--trace` | Enable detailed TRACE logging | Off |

---

##  Example Output

```
Connecting to a1b2c3d4e5f6-ats.iot.us-east-1.amazonaws.com as iot-mqtt-device-1728212023 ...
Connected.
Subscribed to class/demo/topic
Published: {'msg': 'hello from device', 'ts': 1728212023}
Listening for 20s... (publish in console to 'class/demo/topic' to see messages here)
[MSG] class/demo/topic -> {"msg":"hello from device","ts":1728212023}
Disconnected.
```

---

##  How It Works

1. **Establish Connection**  
   Creates a secure MQTT connection over TLS using the provided certs and keys.

2. **Subscribe to Topic**  
   Subscribes to a given topic and prints incoming messages.

3. **Publish Message**  
   Sends a JSON-formatted message containing a timestamp.

4. **Listen & Disconnect**  
   Listens for incoming messages for a defined period, then gracefully disconnects.

---


## Resources

- [AWS IoT Core Documentation](https://docs.aws.amazon.com/iot/)
- [AWS IoT Device SDK for Python (V2)](https://github.com/aws/aws-iot-device-sdk-python-v2)
- [AWS IoT Core MQTT Test Client](https://docs.aws.amazon.com/iot/latest/developerguide/view-mqtt-client.html)
