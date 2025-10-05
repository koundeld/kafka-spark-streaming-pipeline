import json,time,random

from kafka import KafkaProducer
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers = "localhost:9092",
    value_serializer = lambda v: json.dumps(v).encode("utf-8"),
    key_serializer = lambda k: k.encode("utf-8")
)

topic = "taxi-rides-topic"

pickup_boroughs = ["Pune", "Mumbai", "Pimpri"]
drop_boroughs = ["Satara", "Nashik", "Raigad"]

while True:
    #driver_id as key
    driver_id = f"driver_{random.randint(1, 100)}"
    #generate mock event
    event = {
        "driver_id": driver_id,                          # include key inside event too
        "event_time": datetime.now().isoformat(),
        "pickup_borough": random.choice(pickup_boroughs),
        "drop_borough": random.choice(drop_boroughs),
        "trip_distance": round(random.uniform(100, 300), 2),  # 1–20 km
        "passenger_count": random.randint(1, 4),          # 1–4 passengers
        "fare_amount": round(random.uniform(500, 1000), 2),   # $5–$50
        "payment_type": random.choice(["Cash", "Card"])
    }

#send event on topic
    producer.send(topic, key = driver_id, value = event)
    print(f"Produced event: {event}")

    time.sleep(10)