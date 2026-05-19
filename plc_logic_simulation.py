"""
plc_logic_simulation.py
──────────────────────────────────────────────────────────────────────────────
Software simulation of the SIEMENS PLC ladder logic for the Bottle Label
Detection system. Simulates the conveyor belt, proximity switches, Q3X sensor,
and ejector plunger using Python — useful for logic validation before
deploying to real PLC hardware.
──────────────────────────────────────────────────────────────────────────────
"""

import random
import time

# ── PLC Memory (coils and counters) ──────────────────────────────────────────
class PLCMemory:
    def __init__(self):
        # Inputs
        self.PS1              = False   # Proximity Switch 1 (bottle arrived)
        self.PS2              = False   # Proximity Switch 2 (bottle passed exit)
        self.Q3X_LABEL_OK     = False   # Q3X sensor: True = label present

        # Outputs / Coils
        self.SCAN_TRIGGER     = False
        self.EJECTOR_ON       = False

        # Counters
        self.GOOD_COUNT       = 0
        self.REJECT_COUNT     = 0
        self.TOTAL_COUNT      = 0

        # Timer
        self.ejector_timer    = 0.0
        self.EJECTOR_PULSE_MS = 0.5     # 500ms ejector pulse

# ── Ladder Logic Networks ─────────────────────────────────────────────────────
def run_ladder_scan(plc: PLCMemory):
    """One PLC scan cycle — executes all ladder networks in order."""

    # Network 1: Bottle detection trigger
    plc.SCAN_TRIGGER = plc.PS1

    # Network 2: Label check → ejector
    if plc.SCAN_TRIGGER and not plc.Q3X_LABEL_OK:
        plc.EJECTOR_ON = True
        plc.ejector_timer = time.time()
        plc.REJECT_COUNT += 1

    # Network 3: Good bottle counter (proximity switch 2)
    if plc.PS2 and not plc.EJECTOR_ON:
        plc.GOOD_COUNT += 1

    # Network 4: Ejector auto-reset timer (500ms)
    if plc.EJECTOR_ON:
        if (time.time() - plc.ejector_timer) >= plc.EJECTOR_PULSE_MS:
            plc.EJECTOR_ON = False

    plc.TOTAL_COUNT = plc.GOOD_COUNT + plc.REJECT_COUNT

# ── Simulate Conveyor Belt ────────────────────────────────────────────────────
def simulate_bottle(plc: PLCMemory, bottle_id: int, faulty_rate: float = 0.15):
    """Simulate one bottle passing through the system."""

    # Bottle arrives at PS1
    plc.PS1 = True
    plc.Q3X_LABEL_OK = random.random() > faulty_rate   # 15% chance of faulty

    has_label = plc.Q3X_LABEL_OK
    run_ladder_scan(plc)

    status = "✅ GOOD   " if has_label else "❌ FAULTY "
    ejector = "EJECTOR ON" if plc.EJECTOR_ON else "          "

    print(f"  Bottle #{bottle_id:03d}  |  Label: {'YES' if has_label else 'NO '}  |  {status}  |  {ejector}  "
          f"|  Good: {plc.GOOD_COUNT:3d}  Rejected: {plc.REJECT_COUNT:3d}")

    time.sleep(0.03)  # simulate conveyor belt timing

    # Bottle passes PS2 (if not ejected)
    plc.PS2 = has_label
    run_ladder_scan(plc)

    # Reset inputs for next bottle
    plc.PS1 = False
    plc.PS2 = False

    time.sleep(0.02)

# ── SCADA Display ─────────────────────────────────────────────────────────────
def scada_display(plc: PLCMemory, duration_sec: float):
    efficiency = (plc.GOOD_COUNT / plc.TOTAL_COUNT * 100) if plc.TOTAL_COUNT > 0 else 0
    rate = plc.TOTAL_COUNT / duration_sec * 60 if duration_sec > 0 else 0

    print("\n" + "═" * 60)
    print("  SCADA PRODUCTION REPORT")
    print("═" * 60)
    print(f"  Total Bottles Processed : {plc.TOTAL_COUNT}")
    print(f"  Good Bottles            : {plc.GOOD_COUNT}")
    print(f"  Rejected (No Label)     : {plc.REJECT_COUNT}")
    print(f"  Line Efficiency         : {efficiency:.1f}%")
    print(f"  Production Rate         : {rate:.0f} bottles/min")
    print("═" * 60)

# ── Main Simulation ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    NUM_BOTTLES  = 50
    FAULTY_RATE  = 0.15   # 15% of bottles will have missing labels

    plc = PLCMemory()

    print("═" * 60)
    print("  BOTTLE LABEL DETECTION — PLC SIMULATION")
    print("  SIEMENS S7-1200 | Banner Q3X Sensor | SCADA")
    print("═" * 60)
    print(f"  Simulating {NUM_BOTTLES} bottles  |  Faulty rate: {FAULTY_RATE*100:.0f}%\n")
    print(f"  {'Bottle':<12} {'Label':<8} {'Status':<12} {'Ejector':<12} {'Good':>6} {'Rejected':>9}")
    print("  " + "─" * 56)

    start = time.time()
    for i in range(1, NUM_BOTTLES + 1):
        simulate_bottle(plc, i, FAULTY_RATE)

    duration = time.time() - start
    scada_display(plc, duration)
