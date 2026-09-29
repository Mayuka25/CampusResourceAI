from database import (
    get_connection,
    initialize_database,
    is_facility_available
)


def calculate_score(
    facility,
    students,
    needs_projector,
    needs_ac,
    preferred_type=None
):
    """
    Weighted scoring system for intelligent facility allocation.

    Maximum score = 100
    """

    score = 0
    reasons = []

    capacity = facility["capacity"]

    # 1. Capacity fit - 30 points
    if capacity >= students:
        unused_capacity = capacity - students

        if unused_capacity <= 10:
            score += 30
            reasons.append("Excellent capacity fit")
        elif unused_capacity <= 25:
            score += 25
            reasons.append("Good capacity fit")
        else:
            score += 20
            reasons.append("Sufficient capacity")
    else:
        return 0, ["Capacity insufficient"]

    # 2. Projector requirement - 15 points
    if needs_projector:
        if facility["projector"]:
            score += 15
            reasons.append("Projector available")
        else:
            return 0, ["Projector required but unavailable"]
    else:
        score += 15

    # 3. AC requirement - 15 points
    if needs_ac:
        if facility["ac"]:
            score += 15
            reasons.append("AC available")
        else:
            return 0, ["AC required but unavailable"]
    else:
        score += 15

    # 4. Facility type preference - 20 points
    if preferred_type:
        if facility["facility_type"].lower() == preferred_type.lower():
            score += 20
            reasons.append("Preferred facility type matched")
        else:
            score += 10
            reasons.append("Alternative facility type")
    else:
        score += 20

    # 5. Utilization efficiency - 20 points
    utilization_ratio = students / capacity

    if utilization_ratio >= 0.75:
        score += 20
        reasons.append("High utilization efficiency")
    elif utilization_ratio >= 0.50:
        score += 16
        reasons.append("Good utilization efficiency")
    elif utilization_ratio >= 0.30:
        score += 10
        reasons.append("Moderate utilization")
    else:
        score += 5
        reasons.append("Low utilization")

    return score, reasons


def find_best_facilities(
    students,
    facility_type,
    date,
    start_time,
    end_time,
    needs_projector=False,
    needs_ac=False
):
    """
    Finds and ranks suitable facilities.
    """

    initialize_database()

    conn = get_connection()

    facilities = conn.execute("""
        SELECT *
        FROM facilities
        ORDER BY name
    """).fetchall()

    conn.close()

    results = []
    rejected = []

    for facility in facilities:

        # Check availability
        available = is_facility_available(
            facility["id"],
            date,
            start_time,
            end_time
        )

        if not available:
            rejected.append({
                "name": facility["name"],
                "reason": "Already booked during selected time"
            })
            continue

        score, reasons = calculate_score(
            facility,
            students,
            needs_projector,
            needs_ac,
            facility_type
        )

        if score > 0:

            results.append({
                "id": facility["id"],
                "name": facility["name"],
                "facility_type": facility["facility_type"],
                "capacity": facility["capacity"],
                "projector": bool(facility["projector"]),
                "ac": bool(facility["ac"]),
                "score": score,
                "reasons": reasons
            })

        else:

            rejected.append({
                "name": facility["name"],
                "reason": ", ".join(reasons)
            })

    # Highest score first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results, rejected


def get_recommendation(
    students,
    facility_type,
    date,
    start_time,
    end_time,
    needs_projector=False,
    needs_ac=False
):
    """
    Returns the best recommendation and alternatives.
    """

    results, rejected = find_best_facilities(
        students=students,
        facility_type=facility_type,
        date=date,
        start_time=start_time,
        end_time=end_time,
        needs_projector=needs_projector,
        needs_ac=needs_ac
    )

    if not results:
        return {
            "success": False,
            "message": "No suitable facility found.",
            "recommendation": None,
            "alternatives": [],
            "rejected": rejected
        }

    best = results[0]

    return {
        "success": True,
        "message": "Best facility successfully recommended.",
        "recommendation": best,
        "alternatives": results[1:5],
        "rejected": rejected
    }


def print_recommendation(data):
    """
    Console demonstration for testing.
    """

    print("\n")
    print("=" * 55)
    print("       AI CAMPUS RESOURCE ALLOCATION")
    print("=" * 55)

    if not data["success"]:
        print("\n❌", data["message"])
        return

    best = data["recommendation"]

    print("\n🏆 RECOMMENDED FACILITY")
    print("-" * 55)
    print("Facility      :", best["name"])
    print("Type          :", best["facility_type"])
    print("Capacity      :", best["capacity"])
    print("Projector     :", "Yes" if best["projector"] else "No")
    print("AC            :", "Yes" if best["ac"] else "No")
    print("Match Score   :", f'{best["score"]}%')

    print("\nWHY THIS FACILITY?")
    for reason in best["reasons"]:
        print("✓", reason)

    if data["alternatives"]:

        print("\n🔄 ALTERNATIVE FACILITIES")
        print("-" * 55)

        for i, facility in enumerate(data["alternatives"], 1):
            print(
                f"{i}. {facility['name']} "
                f"→ {facility['score']}% match"
            )

    if data["rejected"]:

        print("\n⚠️ FILTERED FACILITIES")
        print("-" * 55)

        for item in data["rejected"]:
            print(
                f"• {item['name']} → {item['reason']}"
            )

    print("\n" + "=" * 55)


if __name__ == "__main__":

    initialize_database()

    # Demo request
    result = get_recommendation(
        students=55,
        facility_type="Classroom",
        date="2026-09-29",
        start_time="14:00",
        end_time="15:00",
        needs_projector=True,
        needs_ac=True
    )

    print_recommendation(result)