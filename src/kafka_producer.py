import json
import time

def emulate_kafka_producer(df, topic_name='payment_events', logger=None):
    """Simulates sending payment events to a Kafka topic and returns the events."""
    logger.info(f"Simulating Kafka Message Production for Topic: {topic_name}")

    events = []
    df_copy = df.copy()
    df_copy['payment_date'] = df_copy['payment_date'].astype(str)

    for _, row in df_copy.iterrows():
        message = row.to_dict()
        events.append(message)
        # Just for console visualisation
        # print(f"Producing message: {json.dumps(message)}")
        time.sleep(0.01)  # Simulates a small delay

    logger.info(f"{len(events)} events produced for topic '{topic_name}'.")
    return events
