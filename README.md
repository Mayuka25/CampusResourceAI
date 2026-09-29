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

```text
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
```

---

## 🤖 AI Allocation Engine

The allocation engine uses a weighted scoring system with a maximum score of **100**.

| Criterion | Weight |
|---|---:|
| Capacity Fit | 30 |
| Projector Requirement | 15 |
| AC Requirement | 15 |
| Facility Type | 20 |
| Utilization Efficiency | 20 |
| **Total** | **100** |

### How It Works

The system first removes facilities that fail mandatory requirements.

For example:

```text
Requested Students → 55
Facility Type → Classroom
Projector → Required
AC → Required
Time → 2:00 PM – 3:00 PM
```

The system then:

1. Checks facility availability.
2. Detects overlapping bookings.
3. Removes facilities with insufficient capacity.
4. Removes facilities without required equipment.
5. Calculates a score for feasible facilities.
6. Selects the highest-scoring facility.
7. Provides alternative recommendations.

---

## 🔴 Conflict Detection & Automatic Rerouting

CampusResourceAI prevents double booking by checking existing bookings before allocating a facility.

If a requested facility is already occupied:

```text
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
```

The conflicting facility is automatically excluded from the candidate pool, and the system searches for another feasible resource.

This allows the system to maintain conflict-free facility allocation.

---

## ✨ Key Features

### 🧠 Intelligent Facility Allocation

Automatically identifies the most suitable facility based on multiple requirements instead of selecting a room randomly.

### 🔒 Conflict Prevention

Prevents overlapping bookings and double allocation of the same facility.

### 🔄 Automatic Alternative Recommendation

If the requested facility is unavailable, the system automatically searches for suitable alternatives.

### 📊 Utilization Analytics

Provides administrators with facility usage information and resource-demand insights.

### 📄 PDF Utilization Reports

Administrators can generate a structured PDF report containing resource utilization and allocation history.

### ⚡ Real-Time Availability Checking

Checks existing bookings before confirming a new allocation.

### 🏢 Multiple Facility Types

Supports:

- Classrooms
- Laboratories
- Seminar Halls
- Sports Facilities

### 📱 Interactive Dashboard

Provides a centralized interface for monitoring facilities, allocations, and utilization.

---

## 📊 Admin Analytics

The analytics dashboard provides:

- Total facilities
- Total allocations
- Resource coverage
- Total resource hours
- Facility-wise utilization
- Most-used facility
- Under-utilized facilities
- High-demand facilities
- Allocation history
- Resource distribution
- Current bookings
- Upcoming bookings
- Completed bookings

The administrator can also generate a **Resource Utilization Report in PDF format**.

---

## 🛠️ Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap
- Chart.js

### Backend

- Python
- Flask

### Database

- SQLite

### AI / Optimization

- Constraint-based filtering
- Weighted multi-factor scoring
- Availability checking
- Utilization analysis

### Deployment

- Render
- Gunicorn

---

## 📁 Project Structure

```text
CampusResourceAI/
│
├── app.py
├── allocator.py
├── database.py
├── campus.db
├── requirements.txt
│
└── templates/
    ├── index.html
    ├── allocate.html
    └── analytics.html
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Mayuka25/CampusResourceAI.git
```

### 2. Open the project directory

```bash
cd CampusResourceAI
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in browser

```text
http://127.0.0.1:5000
```

---

## 🗄️ Database

The application uses SQLite to manage campus resources and bookings.

### Facilities Table

Stores:

- Facility name
- Facility type
- Capacity
- Projector availability
- AC availability

### Bookings Table

Stores:

- Facility
- Date
- Start time
- End time
- Event name

The system checks time overlap before confirming a booking.

---

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Dashboard |
| `/allocate` | GET | Resource allocation page |
| `/analytics` | GET | Analytics dashboard |
| `/api/facilities` | GET | Get all facilities |
| `/api/bookings` | GET | Get booking records |
| `/api/recommend` | POST | Get AI facility recommendation |
| `/api/book` | POST | Create booking |
| `/api/check-availability` | POST | Check facility availability |
| `/api/stats` | GET | Get utilization statistics |

---

## 🧪 Example Use Case

### AI & IoT Workshop

A faculty member wants to conduct an AI & IoT workshop.

```text
Students       : 55
Facility Type  : Classroom
Projector      : Required
AC             : Required
Time           : 2:00 PM – 3:00 PM
```

CampusResourceAI evaluates the available facilities.

Facilities that:

- Are already booked
- Have insufficient capacity
- Do not have a projector
- Do not have AC

are automatically excluded.

The remaining feasible facilities are scored using the AI allocation engine.

The highest-scoring facility is recommended.

If the selected facility becomes unavailable, the system detects the conflict and recommends another suitable facility.

---

## 📈 Impact

CampusResourceAI can help educational institutions:

- Reduce manual scheduling effort
- Prevent resource conflicts
- Improve facility utilization
- Reduce under-utilization
- Handle high-demand facilities
- Improve administrative decision-making
- Support data-driven campus planning

---

## 🔮 Future Scope

The system can be extended with:

- Machine learning-based demand prediction
- Automatic timetable integration
- Student and faculty authentication
- Email and notification alerts
- IoT-based real-time occupancy detection
- Dynamic room allocation
- Energy-aware facility selection
- Predictive maintenance
- Mobile application
- Integration with existing college ERP systems

---

## 🏆 Hackathon Value

CampusResourceAI demonstrates how AI and optimization can be applied to a real-world campus management problem.

Instead of simply displaying available rooms, the system:

**Understands → Filters → Scores → Allocates → Monitors → Reports**

This creates an intelligent resource management workflow for campus administrators.

---

## 👥 Team

**Team Name:** byte quenns  
**Team ID:** TEAM-07

### Project

**CampusResourceAI — Intelligent Resource Allocation System for Campus Facilities**

---

## 📜 License

This project was developed as a hackathon prototype for demonstrating intelligent campus resource allocation and optimization.
