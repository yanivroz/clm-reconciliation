import json
import os
import sys
import time

import requests
from kafka import KafkaProducer

# API_SERVER = "http://nginx-deployment.default.svc.cluster.local:8080/clm/api/clusters/adc/all/params?all=True"
# KAFKA_HOST = "kafka.kafka.svc.cluster.local:9092"
# KAFKA_TOPIC = "my_favorite_topic"

API_SERVER = os.getenv('API_SERVER')
KAFKA_HOST = os.getenv('KAFKA_HOST')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')

if API_SERVER is None or KAFKA_HOST is None or KAFKA_TOPIC is None:
    sys.exit(f"Missing environment variable: API_SERVER={API_SERVER}, KAFKA_HOST={KAFKA_HOST}, KAFKA_TOPIC={KAFKA_TOPIC}")

start = time.time()

producer = KafkaProducer(bootstrap_servers=KAFKA_HOST, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

count = 0
for cluster in requests.get(API_SERVER, timeout=5).json():
    msg = {
        "type": "cluster",
        "tenant": cluster["tenant"],
        "id": cluster["id"]
    }
    producer.send(KAFKA_TOPIC, msg)
    count += 1
producer.flush()
end = time.time()
print(f"Total triggers sent: {count} (took {end-start:.3f} seconds)")
