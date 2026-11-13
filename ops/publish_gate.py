#!/usr/bin/env python3
"""Random-afternoon-slot gate for ops/publish_daily.sh (rule: one journal post a day, random time in the afternoon, never in the same hour as yesterday).

launchd calls this every 15 minutes (12:00-18:45 KST). It keeps ~/.ipe/queue/claimball/slot.json:
  {"date","time","prev_date","prev_time","published"}   # time = HH:MM KST, drawn from 12:00-17:59
A new KST day draws a new slot (hour != yesterday's hour; yesterday's values move to prev_*). From the slot on, while published is false, the gate runs
publish_daily.sh; when that run really published (or today's post was already out) published becomes true. SKIP / QUEUE_EMPTY / failure keep it false: the
next 15-minute tick retries.
Test hooks: CLAIMBALL_SLOT_FILE, CLAIMBALL_PUBLISH_CMD (default "bash <ops>/publish_daily.sh"), CLAIMBALL_NOW ("YYYY-MM-DD HH:MM"), CLAIMBALL_SEED.
"""
import json
import os
import random
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

KST = timezone(timedelta(hours=9))
SLOT_FILE = Path(os.environ.get("CLAIMBALL_SLOT_FILE", str(Path.home() / ".ipe/queue/claimball/slot.json")))
HERE = Path(__file__).resolve().parent
FIRST_HOUR, LAST_HOUR = 12, 17   # slot is drawn in 12:00..17:59


def now_kst():
    s = os.environ.get("CLAIMBALL_NOW")
    return datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=KST) if s else datetime.now(KST)


def draw_time(prev_time, rng):
    """Random HH:MM in 12:00-17:59 whose hour differs from prev_time's hour (if any)."""
    prev_hour = int(prev_time.split(":")[0]) if prev_time else None
    hours = [h for h in range(FIRST_HOUR, LAST_HOUR + 1) if h != prev_hour]
    return "%02d:%02d" % (rng.choice(hours), rng.randrange(60))


def load():
    try:
        return json.loads(SLOT_FILE.read_text())
    except (OSError, ValueError):
        return {}


def save(st):
    SLOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = SLOT_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(st, indent=1) + "\n")
    tmp.replace(SLOT_FILE)


def roll(st, today, rng):
    """Return the state for `today`: unchanged if already today's, else a freshly drawn slot with yesterday's values in prev_*."""
    if st.get("date") == today:
        return st
    return {"date": today, "time": draw_time(st.get("time"), rng), "prev_date": st.get("date"), "prev_time": st.get("time"), "published": False}


def run_publish():
    cmd = os.environ.get("CLAIMBALL_PUBLISH_CMD") or "bash %s/publish_daily.sh" % HERE
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    sys.stdout.write(out)
    return r.returncode == 0 and "SKIP" not in out and "QUEUE_EMPTY" not in out


def main():
    now = now_kst()
    today, hm = now.strftime("%Y-%m-%d"), now.strftime("%H:%M")
    seed = os.environ.get("CLAIMBALL_SEED")
    rng = random.Random(int(seed)) if seed else random.Random()
    st = roll(load(), today, rng)
    if st.get("published"):
        save(st)
        print("[%s KST] gate: today's post already published (slot %s)" % (hm, st["time"]))
        return 0
    if hm < st["time"]:
        save(st)
        print("[%s KST] gate: waiting for slot %s" % (hm, st["time"]))
        return 0
    print("[%s KST] gate: slot %s reached — running publish_daily" % (hm, st["time"]))
    st["published"] = run_publish()
    save(st)
    print("[%s KST] gate: published=%s" % (hm, str(st["published"]).lower()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
