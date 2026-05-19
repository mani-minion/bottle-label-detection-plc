# Bottle Label Detection using PLC & Vision Sensor

> Capstone Project — Department of Robotics and Automation  
> Sri Ramakrishna Engineering College, Coimbatore | Anna University, 2022

---

## Overview

An automated industrial quality inspection system that detects **faulty or missing bottle labels** on a moving conveyor belt using a **SIEMENS PLC**, **Banner Q3X laser contrast sensor**, and **SCADA monitoring** — without human intervention.

The system uses PLC ladder logic to coordinate proximity switches, a vision sensor, and a pneumatic ejector to automatically identify and remove defective bottles from the production line.

---

## System Architecture

```
Conveyor Belt
     │
     ▼
[Proximity Switch 1] ── Detects bottle arrival → triggers scan
     │
     ▼
[Banner Q3X Laser Contrast Sensor] ── Scans label presence/absence
     │
     ├── Label PRESENT  → Plunger OFF → bottle continues ──► [Proximity Switch 2 counts good bottles]
     │
     └── Label ABSENT   → Plunger ON  → bottle ejected   ──► Faulty bottle removed
     │
     ▼
[SIEMENS PLC] ── Ladder Diagram program coordinates all logic
     │
     ▼
[SCADA Interface] ── Real-time monitoring and data logging
```

---

## Hardware Components

| Component | Specification | Purpose |
|-----------|--------------|---------|
| SIEMENS S7-1200 PLC | 24V DC, DI/DO modules | Main control logic |
| Banner Q3X Laser Contrast Sensor | Range: 50mm, Speed: 250μs | Label detection |
| Proximity Switch (×2) | Inductive, NPN | Bottle counting & triggering |
| Pneumatic Plunger / Ejector | 24V solenoid actuated | Faulty bottle removal |
| Conveyor Belt Motor | AC motor with VFD | Belt movement control |
| SCADA System | WinCC / TIA Portal | Monitoring & visualization |

---

## PLC Ladder Diagram Logic

```
Network 1: Bottle Detection Trigger
─────────────────────────────────────────────────────────────────
  [PS1]──────────────────────────────────────────( SCAN_TRIGGER )
  Proximity Switch 1 energizes the scan trigger coil

Network 2: Label Check & Ejector Control  
─────────────────────────────────────────────────────────────────
  [SCAN_TRIGGER]──[/Q3X_LABEL_OK]────────────────( EJECTOR_ON )
  If scan triggered AND label NOT detected → activate ejector

Network 3: Good Bottle Counter
─────────────────────────────────────────────────────────────────
  [PS2]──────────────────────────────────────────( GOOD_COUNT++ )
  Proximity Switch 2 increments good bottle counter

Network 4: Ejector Auto-Reset Timer
─────────────────────────────────────────────────────────────────
  [EJECTOR_ON]──[TON T1, PT:500ms]───────────────( EJECTOR_OFF )
  Ejector stays on for 500ms then resets automatically

Network 5: Production Counter Display (SCADA)
─────────────────────────────────────────────────────────────────
  GOOD_COUNT and REJECT_COUNT → SCADA HMI tags for visualization
```

---

## Sensor Details — Banner Q3X Laser Contrast Sensor

The **Q3X** uses laser contrast detection (not standard diffuse mode) to reliably distinguish between:
- **Label present** → high contrast reading → output ON (good bottle)
- **Label absent** → low contrast reading → output OFF (faulty bottle)

Key advantages:
- Fixed background suppression up to 60mm — ignores the shiny metal conveyor rail
- High-speed detection: 250 μs response time → up to 2,000 events/second
- IP67/IP68/IP69K rated — suitable for wash-down environments
- Simple 2-button tactile setup with 3-digit intensity display

---

## SCADA Monitoring Tags

| Tag Name | Data Type | Description |
|----------|-----------|-------------|
| `GOOD_BOTTLE_COUNT` | INT | Total good bottles passed |
| `REJECT_COUNT` | INT | Total faulty bottles ejected |
| `EJECTOR_STATUS` | BOOL | Current ejector state (ON/OFF) |
| `CONVEYOR_RUNNING` | BOOL | Conveyor motor status |
| `SENSOR_INTENSITY` | INT | Q3X real-time intensity value |
| `PRODUCTION_RATE` | REAL | Bottles per minute |

---

## Results

| Parameter | Result |
|-----------|--------|
| Detection accuracy | ~99% (no false triggers from conveyor rail) |
| Cycle time per bottle | < 1 second |
| Sensor response time | 250 μs |
| System cost | Low (PLC + sensor vs. full vision system) |

---

## Key Concepts Demonstrated

- **PLC Programming** — Ladder diagram with timers, counters, coils, contacts
- **Industrial Sensor Integration** — Laser contrast sensor with fixed background suppression
- **SCADA** — Real-time supervisory control and data acquisition
- **Automation Logic** — Sequential control without human intervention
- **Industrial Communication** — PLC I/O mapping and HMI tag configuration

---

## Tools & Technologies

- SIEMENS TIA Portal (PLC programming + SCADA/WinCC)
- Ladder Diagram (IEC 61131-3)
- Banner Q3X Laser Contrast Sensor
- SCADA / HMI visualization

---

## References

- Banner Engineering — Q3X Laser Contrast Sensor Datasheet
- SIEMENS S7-1200 PLC System Manual
- IEC 61131-3: Programming Languages for PLCs
