import time
import random
from db import get_connection

print("🚀 Payment Worker Started")

MAX_RETRIES = 3

while True:

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT event_id, ride_id, retry_count
        FROM events
        WHERE event_type = 'payment_requested'
        AND status = 'pending'
        ORDER BY event_id
        LIMIT 1
    """)

    event = cur.fetchone()

    if event:

        event_id, ride_id, retry_count = event

        print(f"💳 Processing payment for Ride {ride_id}")

        try:

            # Simulate random payment failure
            if random.choice([True, False]):
                raise Exception("Payment gateway timeout")

            time.sleep(5)

            cur.execute("""
                UPDATE rides
                SET status = 'paid'
                WHERE ride_id = %s
            """, (ride_id,))

            cur.execute("""
                UPDATE events
                SET status = 'processed'
                WHERE event_id = %s
            """, (event_id,))

            conn.commit()

            print(f"✅ Payment completed for Ride {ride_id}")

        except Exception as e:

            print(f"❌ Payment failed for Ride {ride_id}: {e}")

            retry_count += 1

            if retry_count >= MAX_RETRIES:

                cur.execute("""
                    UPDATE events
                    SET status = 'failed',
                        retry_count = %s
                    WHERE event_id = %s
                """, (retry_count, event_id))

                print(f"☠️ Event moved to FAILED state")

            else:

                cur.execute("""
                    UPDATE events
                    SET retry_count = %s
                    WHERE event_id = %s
                """, (retry_count, event_id))

                print(f"🔁 Retry count updated to {retry_count}")

            conn.commit()

    cur.close()
    conn.close()

    time.sleep(2)
