import sqlite3

DATABASE = "campus.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Facilities table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            facility_type TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            projector INTEGER DEFAULT 0,
            ac INTEGER DEFAULT 0
        )
    """)

    # Bookings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facility_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            event_name TEXT,
            FOREIGN KEY (facility_id) REFERENCES facilities(id)
        )
    """)

    # Check whether facilities already exist
    cursor.execute("SELECT COUNT(*) FROM facilities")
    count = cursor.fetchone()[0]

    # Add sample campus facilities
    if count == 0:
        facilities = [
            ("C201", "Classroom", 40, 1, 1),
            ("C202", "Classroom", 50, 1, 1),
            ("C204", "Classroom", 60, 1, 1),
            ("C206", "Classroom", 70, 1, 1),
            ("C301", "Classroom", 80, 1, 0),
            ("LAB1", "Laboratory", 30, 1, 1),
            ("LAB2", "Laboratory", 50, 1, 1),
            ("LAB3", "Laboratory", 60, 1, 1),
            ("Seminar Hall A", "Seminar Hall", 120, 1, 1),
            ("Seminar Hall B", "Seminar Hall", 80, 1, 1),
            ("Sports Hall", "Sports", 100, 0, 0)
        ]

        cursor.executemany("""
            INSERT INTO facilities
            (name, facility_type, capacity, projector, ac)
            VALUES (?, ?, ?, ?, ?)
        """, facilities)

    conn.commit()
    conn.close()


def get_all_facilities():
    conn = get_connection()
    facilities = conn.execute(
        "SELECT * FROM facilities ORDER BY name"
    ).fetchall()
    conn.close()
    return facilities


def get_all_bookings():
    conn = get_connection()

    bookings = conn.execute("""
        SELECT
            bookings.*,
            facilities.name AS facility_name,
            facilities.facility_type,
            facilities.capacity
        FROM bookings
        JOIN facilities
        ON bookings.facility_id = facilities.id
        ORDER BY bookings.date, bookings.start_time
    """).fetchall()

    conn.close()
    return bookings


def add_booking(facility_id, date, start_time, end_time, event_name):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO bookings
        (facility_id, date, start_time, end_time, event_name)
        VALUES (?, ?, ?, ?, ?)
    """, (
        facility_id,
        date,
        start_time,
        end_time,
        event_name
    ))

    conn.commit()
    conn.close()


def is_facility_available(facility_id, date, start_time, end_time):
    conn = get_connection()

    booking = conn.execute("""
        SELECT id
        FROM bookings
        WHERE facility_id = ?
        AND date = ?
        AND start_time < ?
        AND end_time > ?
    """, (
        facility_id,
        date,
        end_time,
        start_time
    )).fetchone()

    conn.close()

    return booking is None


if __name__ == "__main__":
    initialize_database()
    print("===================================")
    print(" CAMPUS RESOURCE DATABASE READY")
    print("===================================")
    print("Database : campus.db")
    print("Facilities: 11")
    print("Status   : SUCCESS")