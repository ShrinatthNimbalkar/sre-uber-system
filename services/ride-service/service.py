# service.py

from repository import create_ride, get_ride, update_status, create_event
from event import emit_event
from kafka_producer import publish_payment_requested

ALLOWED_TRANSITIONS = {
    "requested": ["assigned", "cancelled"],
    "assigned": ["in_progress", "cancelled"],
    "in_progress": ["completed"],
    "completed": ["paid"],
    "paid": []
}


def create_ride_service(data):
    ride_id = create_ride(
        data["user_id"],
        data["pickup"],
        data["drop"]
    )

    return {
        "ride_id": ride_id,
        "status": "requested"
    }


def get_ride_service(ride_id):
    result = get_ride(ride_id)

    if not result:
        return None

    return {
        "ride_id": result[0],
        "status": result[1]
    }


def update_ride_status(ride_id, new_status):

    ride = get_ride(ride_id)

    if not ride:
        return {"error": "Ride not found"}, 404

    current_status = ride[1]

    if new_status not in ALLOWED_TRANSITIONS.get(current_status, []):
        return {
            "error": f"Invalid transition from {current_status} to {new_status}"
        }, 400

    # Update ride status
    update_status(ride_id, new_status)

    # Create async payment event
    if new_status == "completed":
        create_event(ride_id, "payment_requested")
        publish_payment_requested(ride_id)

    # Emit internal event
    emit_event(
        event_type="ride_status_changed",
        ride_id=ride_id,
        old_status=current_status,
        new_status=new_status
    )

    return {
        "ride_id": ride_id,
        "old_status": current_status,
        "new_status": new_status
    }, 200
