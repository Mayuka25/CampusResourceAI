# 🏫 CampusResourceAI
### Intelligent Resource Allocation System for Campus Facilities

> **Hackathon Project — PS-03 | Smart Campus / AI & Optimization**

CampusResourceAI is an AI-powered web application that intelligently allocates campus facilities such as classrooms, laboratories, seminar halls, and sports facilities based on availability, capacity, equipment requirements, facility type, and utilization efficiency.

The system prevents double-booking, detects scheduling conflicts, automatically recommends alternatives, and provides utilization analytics for administrators.

---

## 🚀 Live Demo

🌐 **Live Application:**  
https://campusresourceai.onrender.com

💻 **GitHub Repository:**  
https://github.com/Mayuka25/CampusResourceAI

---

## 🎯 Problem Statement

Educational institutions manage multiple shared resources such as:

- Classrooms
- Laboratories
- Seminar halls
- Sports facilities
- Projector-enabled rooms
- Air-conditioned facilities

Manual allocation of these resources can lead to:

- Double booking
- Scheduling conflicts
- Poor utilization of facilities
- Overcrowding
- Under-utilized rooms
- Difficulty finding suitable alternatives
- Time-consuming administrative work

CampusResourceAI addresses these challenges through intelligent, constraint-based facility allocation.

---

## 💡 Solution

CampusResourceAI uses a **constraint-based AI allocation engine** to automatically identify and rank suitable facilities for an event.

The system first applies **hard constraints** such as:

- Facility availability
- Capacity requirement
- Projector requirement
- AC requirement
- Scheduling conflicts

After filtering unavailable or unsuitable facilities, the AI engine ranks the remaining facilities using a weighted scoring model.

### Allocation Flow


Event Request
      ↓
Hard Constraint Filtering
      ↓
Availability & Conflict Check
      ↓
Capacity & Equipment Validation
      ↓
AI Weighted Scoring
      ↓
Best Facility Selection
      ↓
Alternative Recommendations
      ↓
Booking & Analytics


🤖 AI Allocation Engine

The allocation engine uses a weighted scoring system with a maximum score of 100
| Criterion              |  Weight |
| ---------------------- | ------: |
| Capacity Fit           |      30 |
| Projector Requirement  |      15 |
| AC Requirement         |      15 |
| Facility Type          |      20 |
| Utilization Efficiency |      20 |
| **Total**              | **100** |

Why this approach?

Instead of randomly selecting an available facility, the system evaluates multiple factors and selects the most suitable resource.

For example:

Student Requirement → 55
Facility Type → Classroom
Projector → Required
AC → Required
Time → 2:00 PM – 3:00 PM

        ↓

Check Availability
        ↓
Remove Conflicting Facilities
        ↓
Evaluate Capacity & Equipment
        ↓
Calculate AI Score
        ↓
Recommend Best Facility

🔴 Conflict Detection & Automatic Rerouting

CampusResourceAI prevents double booking by checking existing bookings before allocating a facility.

If a requested facility is already occupied:
Requested Facility
       ↓
Already Booked?
       ↓
     YES
       ↓
🚨 CONFLICT DETECTED
       ↓
Remove from Candidate Pool
       ↓
🤖 AI REROUTING
       ↓
Find Best Available Alternative

The system therefore maintains conflict-free resource allocation.

📊 Admin Analytics

The analytics dashboard provides administrators with information such as:

Total facilities
Total allocations
Resource coverage
Total resource hours
Facility-wise utilization
Most-used facilities
Under-utilized facilities
High-demand facilities
Allocation history
Resource distribution
Current and upcoming bookings

The system can also generate a PDF Resource Utilization Report for administrative use.

✨ Key Features
🧠 Intelligent Allocation

Automatically selects the most suitable facility using weighted constraint-based scoring.

🔒 Conflict Prevention

Prevents overlapping bookings and double allocation of facilities.

🔄 Automatic Alternatives

If a facility is unavailable, the system recommends suitable alternatives automatically.

📈 Utilization Analytics

Tracks facility usage and identifies utilization patterns.

📄 PDF Reports

Administrators can generate a structured resource utilization report.

⚡ Real-Time Availability

Facility availability is checked against existing bookings before allocation.

🏢 Multi-Resource Support

Supports classrooms, laboratories, seminar halls, and sports facilities.

📱 Interactive Dashboard

Provides a centralized interface for resource monitoring and allocation.

🛠️ Technology Stack
Frontend
HTML5
CSS3
JavaScript
Bootstrap
Chart.js
Backend
Python
Flask
Database
SQLite
AI / Optimization
Constraint-based filtering
Weighted scoring algorithm
Resource utilization analysis
Deployment
Render
Gunicorn


