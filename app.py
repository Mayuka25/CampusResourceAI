from flask import Flask, render_template, request, jsonify
from database import (
    initialize_database,
    get_all_facilities,
    get_all_bookings,
    add_booking,
    is_facility_available
)
from allocator import get_recommendation
from datetime import datetime, date

app = Flask(__name__)

initialize_database()


# Campus operating window used for utilization analytics.
# 08:00-18:00 = 10 resource-hours available per facility per day.
OPERATING_HOURS_PER_DAY = 10


def calculate_duration(start_time, end_time):
    try:
        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")
        duration = (end - start).total_seconds() / 3600
        return max(duration, 0)
    except Exception:
        return 0


@app.route("/")
def home():
    facilities = get_all_facilities()
    bookings = get_all_bookings()

    total = len(facilities)

    used_facilities = len(
        set(booking["facility_name"] for booking in bookings)
    )

    available = max(total - used_facilities, 0)

    return render_template(
        "index.html",
        facilities=facilities,
        bookings=bookings,
        total=total,
        available=available,
        booked=used_facilities
    )


@app.route("/allocate")
def allocate_page():
    facilities = get_all_facilities()
    return render_template(
        "allocate.html",
        facilities=facilities
    )


@app.route("/analytics")
def analytics():
    facilities = get_all_facilities()
    bookings = get_all_bookings()

    return render_template(
        "analytics.html",
        facilities=facilities,
        bookings=bookings
    )


@app.route("/api/facilities")
def api_facilities():
    facilities = get_all_facilities()

    data = []

    for facility in facilities:
        data.append({
            "id": facility["id"],
            "name": facility["name"],
            "type": facility["facility_type"],
            "facility_type": facility["facility_type"],
            "capacity": facility["capacity"],
            "projector": bool(facility["projector"]),
            "ac": bool(facility["ac"])
        })

    return jsonify(data)


@app.route("/api/bookings")
def api_bookings():
    bookings = get_all_bookings()

    data = []

    for booking in bookings:
        event_name = booking["event_name"] or "Campus Event"
        facility_name = booking["facility_name"]

        data.append({
            "id": booking["id"],

            # Keep both names for compatibility with existing frontend code.
            "facility": facility_name,
            "facility_name": facility_name,

            "facility_type": booking["facility_type"],
            "capacity": booking["capacity"],
            "date": booking["date"],
            "start_time": booking["start_time"],
            "end_time": booking["end_time"],

            "event": event_name,
            "event_name": event_name,

            "duration": calculate_duration(
                booking["start_time"],
                booking["end_time"]
            )
        })

    return jsonify(data)


@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json() or {}

    try:
        students = int(data.get("students", 0))
    except Exception:
        students = 0

    facility_type = data.get(
        "facility_type",
        "Classroom"
    )

    date_value = data.get(
        "date",
        datetime.now().strftime("%Y-%m-%d")
    )

    start_time = data.get(
        "start_time",
        "09:00"
    )

    end_time = data.get(
        "end_time",
        "10:00"
    )

    needs_projector = bool(
        data.get("projector", False)
    )

    needs_ac = bool(
        data.get("ac", False)
    )

    if students <= 0:
        return jsonify({
            "success": False,
            "message": "Please enter a valid student count."
        }), 400

    if not date_value or not start_time or not end_time:
        return jsonify({
            "success": False,
            "message": "Please provide date and time."
        }), 400

    if start_time >= end_time:
        return jsonify({
            "success": False,
            "message": "End time must be later than start time."
        }), 400

    result = get_recommendation(
        students=students,
        facility_type=facility_type,
        date=date_value,
        start_time=start_time,
        end_time=end_time,
        needs_projector=needs_projector,
        needs_ac=needs_ac
    )

    return jsonify(result)


@app.route("/api/book", methods=["POST"])
def book_facility():
    data = request.get_json() or {}

    try:
        facility_id = int(data.get("facility_id"))
    except Exception:
        return jsonify({
            "success": False,
            "message": "Invalid facility."
        }), 400

    date_value = data.get("date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    event_name = str(
        data.get("event_name") or "Campus Event"
    ).strip()

    if not event_name:
        event_name = "Campus Event"

    if not all([date_value, start_time, end_time]):
        return jsonify({
            "success": False,
            "message": "Missing booking information."
        }), 400

    if start_time >= end_time:
        return jsonify({
            "success": False,
            "message": "End time must be later than start time."
        }), 400

    facilities = get_all_facilities()

    facility = None

    for item in facilities:
        if item["id"] == facility_id:
            facility = item
            break

    if facility is None:
        return jsonify({
            "success": False,
            "message": "Facility not found."
        }), 404

    # Final conflict check before writing to SQLite.
    if not is_facility_available(
        facility_id,
        date_value,
        start_time,
        end_time
    ):
        return jsonify({
            "success": False,
            "conflict": True,
            "message": (
                f"{facility['name']} is already booked "
                "during the selected time."
            ),
            "suggestion": (
                "Try another time slot or "
                "choose an alternative facility."
            )
        }), 409

    add_booking(
        facility_id,
        date_value,
        start_time,
        end_time,
        event_name
    )

    return jsonify({
        "success": True,
        "message": (
            f"{facility['name']} allocated successfully!"
        ),
        "booking": {
            "facility": facility["name"],
            "facility_name": facility["name"],
            "facility_type": facility["facility_type"],
            "capacity": facility["capacity"],
            "date": date_value,
            "start_time": start_time,
            "end_time": end_time,
            "event": event_name,
            "event_name": event_name,
            "duration": calculate_duration(
                start_time,
                end_time
            )
        }
    })


@app.route("/api/check-availability", methods=["POST"])
def check_availability():
    data = request.get_json() or {}

    try:
        facility_id = int(data.get("facility_id"))
    except Exception:
        return jsonify({
            "available": False,
            "message": "Invalid facility."
        }), 400

    date_value = data.get("date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    if not all([date_value, start_time, end_time]):
        return jsonify({
            "available": False,
            "message": "Missing date or time."
        }), 400

    available = is_facility_available(
        facility_id,
        date_value,
        start_time,
        end_time
    )

    return jsonify({
        "available": available,
        "message": (
            "Facility is available."
            if available
            else
            "Facility is already booked for this time."
        )
    })


@app.route("/api/stats")
def stats():
    facilities = get_all_facilities()
    bookings = get_all_bookings()

    total_facilities = len(facilities)
    total_bookings = len(bookings)

    total_capacity = sum(
        facility["capacity"]
        for facility in facilities
    )

    average_capacity = (
        round(
            total_capacity / total_facilities,
            1
        )
        if total_facilities
        else 0
    )

    # -------------------------------------------------
    # Facility-wise booking and utilization calculation
    # -------------------------------------------------

    usage = {}

    for facility in facilities:
        usage[facility["name"]] = {
            "name": facility["name"],
            "facility_type": facility["facility_type"],
            "capacity": facility["capacity"],
            "bookings": 0,
            "booked_hours": 0.0,
            "utilization": 0.0,
            "used_dates": set()
        }

    for booking in bookings:
        name = booking["facility_name"]

        if name not in usage:
            continue

        duration = calculate_duration(
            booking["start_time"],
            booking["end_time"]
        )

        usage[name]["bookings"] += 1
        usage[name]["booked_hours"] += duration
        usage[name]["used_dates"].add(booking["date"])

    # Utilization = booked hours / available operating hours.
    # Each day contributes 10 available operating hours.
    for item in usage.values():
        available_hours = (
            len(item["used_dates"]) * OPERATING_HOURS_PER_DAY
        )

        if available_hours > 0:
            item["utilization"] = round(
                min(
                    (item["booked_hours"] / available_hours) * 100,
                    100
                ),
                1
            )
        else:
            item["utilization"] = 0.0

        item["booked_hours"] = round(
            item["booked_hours"],
            2
        )

        # Sets are not JSON serializable and aren't needed by frontend.
        item.pop("used_dates", None)

    facility_usage = list(usage.values())

    # Highest usage is based on actual booked hours.
    most_used = None

    if facility_usage:
        most_used = max(
            facility_usage,
            key=lambda x: (
                x["booked_hours"],
                x["bookings"]
            )
        )

    # Least used among facilities that have at least one booking.
    used_items = [
        item for item in facility_usage
        if item["bookings"] > 0
    ]

    least_used = None

    if used_items:
        least_used = min(
            used_items,
            key=lambda x: x["booked_hours"]
        )

    used_facilities = len(
        [
            item for item in facility_usage
            if item["bookings"] > 0
        ]
    )

    resource_coverage = (
        round(
            (used_facilities / total_facilities) * 100,
            1
        )
        if total_facilities
        else 0
    )

    # Demand by facility type.
    type_demand = {}

    for booking in bookings:
        facility_type = booking["facility_type"]

        type_demand[facility_type] = (
            type_demand.get(facility_type, 0) + 1
        )

    total_hours = 0

    for booking in bookings:
        total_hours += calculate_duration(
            booking["start_time"],
            booking["end_time"]
        )

    time_demand = {}

    for booking in bookings:
        hour = booking["start_time"][:2]
        label = hour + ":00"

        time_demand[label] = (
            time_demand.get(label, 0) + 1
        )

    # -------------------------------------------------
    # Administrator insights
    # -------------------------------------------------

    # Facilities with less than 30% utilization.
    under_utilized = [
        item for item in facility_usage
        if item["utilization"] < 30
    ]

    # High demand = at least 2 allocations OR 70%+ utilization.
    high_demand = [
        item for item in facility_usage
        if item["bookings"] >= 2
        or item["utilization"] >= 70
    ]

    return jsonify({
        "total_facilities": total_facilities,
        "total_bookings": total_bookings,
        "average_capacity": average_capacity,

        "most_used": most_used,
        "least_used": least_used,

        "facility_usage": facility_usage,

        "used_facilities": used_facilities,
        "resource_coverage": resource_coverage,

        "type_demand": type_demand,

        "total_hours": round(total_hours, 2),
        "time_demand": time_demand,

        "under_utilized": under_utilized,
        "high_demand": high_demand,

        "operating_hours_per_day": OPERATING_HOURS_PER_DAY
    })


if __name__ == "__main__":

    print("=" * 60)
    print("      SMART CAMPUS RESOURCE ALLOCATION SYSTEM")
    print("=" * 60)
    print("AI Allocation Engine : ACTIVE")
    print("SQLite Database      : ACTIVE")
    print("Conflict Detection   : ACTIVE")
    print("Analytics Engine     : ACTIVE")
    print("Utilization Reports  : ACTIVE")
    print("-" * 60)
    print("Open: http://127.0.0.1:5000")
    print("=" * 60)

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
