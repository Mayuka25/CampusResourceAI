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
