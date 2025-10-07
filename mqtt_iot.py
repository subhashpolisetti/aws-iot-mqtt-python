from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
import argparse, os, sys, time, json

def find_root_ca():
    for c in ("AmazonRootCA1.pem", "root-CA.crt", "AmazonRootCA1.crt", "/etc/ssl/cert.pem"):
        if os.path.exists(c):
            return c
    return None

def must_exist(path, label):
    if not os.path.exists(path):
        print(f"ERROR: {label} not found at: {path}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="AWS IoT Core MQTT (mTLS) client")
    parser.add_argument("--endpoint", required=True, help="AWS IoT data endpoint (xxxx-ats.iot.<region>.amazonaws.com)")
    parser.add_argument("--cert", required=True, help="Device certificate path (*.pem/.crt)")
    parser.add_argument("--key", required=True, help="Device private key path (*.key)")
    parser.add_argument("--root-ca", default=None, help="Root CA path (auto-detected if omitted)")
    parser.add_argument("--client-id", default=f"iot-mqtt-device-{int(time.time())}", help="MQTT client ID")
    parser.add_argument("--topic", default="class/demo/topic", help="Topic to use")
    parser.add_argument("--keepalive", type=int, default=30, help="Keep-alive seconds")
    parser.add_argument("--listen-secs", type=int, default=20, help="Seconds to listen after publish")
    parser.add_argument("--trace", action="store_true", help="Enable TRACE logs")
    args = parser.parse_args()

    root_ca = args.root_ca or find_root_ca()
    if not root_ca:
        print("ERROR: Root CA not found. Place 'AmazonRootCA1.pem' or 'root-CA.crt' in this folder,")
        print("or pass --root-ca /path/to/AmazonRootCA1.pem")
        sys.exit(1)

    must_exist(args.cert, "Certificate")
    must_exist(args.key,  "Private key")
    must_exist(root_ca,   "Root CA")


    io.init_logging(io.LogLevel.Trace if args.trace else io.LogLevel.Info, "stderr")


    event_loop_group = io.EventLoopGroup(1)
    host_resolver    = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)


    mqtt_conn = mqtt_connection_builder.mtls_from_path(
        endpoint=args.endpoint,
        cert_filepath=args.cert,
        pri_key_filepath=args.key,
        ca_filepath=root_ca,
        client_bootstrap=client_bootstrap,
        client_id=args.client_id,
        clean_session=False,
        keep_alive_secs=args.keepalive,
    )

    print(f"Connecting to {args.endpoint} as {args.client_id} ...")
    mqtt_conn.connect().result()
    print("Connected.")

    def on_msg(topic, payload, dup, qos, retain, **kwargs):
        try:
            body = payload.decode()
        except Exception:
            body = str(payload)
        print(f"[MSG] {topic} -> {body}")


    subscribe_future, _ = mqtt_conn.subscribe(
        topic=args.topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_msg
    )
    subscribe_future.result()
    print(f"Subscribed to {args.topic}")


    message = {"msg": "hello from device", "ts": int(time.time())}
    mqtt_conn.publish(topic=args.topic, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published:", message)

    print(f"Listening for {args.listen_secs}s... (publish in console to '{args.topic}' to see messages here)")
    time.sleep(args.listen_secs)

    mqtt_conn.disconnect().result()
    print("Disconnected.")

if __name__ == "__main__":
    main()
