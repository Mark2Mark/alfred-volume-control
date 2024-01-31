#! /usr/local/bin/python3
import os
import sys
import subprocess
import json


def execute(cmd):
    result = subprocess.getstatusoutput(cmd)
    return result[1]


def get_volume():
    return execute("""osascript -e 'output volume of (get volume settings)'""")


def get_muted():
    return execute("""osascript -e 'output muted of (get volume settings)'""")


def set_volume(vol):
    subprocess.run(["osascript", "-e", "set volume output volume {}".format(vol)])


def set_muted(muted):
    subprocess.run(["osascript", "-e", 'set volume output muted "{}"'.format(muted)])


def get_volume_summary():
    if get_muted() == "true":
        return "Muted, original volume: " + get_volume() + "%"
    else:
        return "Current volume: " + get_volume() + "%"


def parse_volume(s, default=10):
    try:
        return int(s)
    except:
        return default


def process_query(q):
    results = []
    if len(q) == 0:
        results.append(
            {
                "attributes": {"arg": "", "valid": "false"},
                "title": get_volume_summary(),
                "subtitle": "",
            }
        )
    op = q[0].lower() if len(q) > 0 else ""

    if op == "":
        results.append(
            {
                "attributes": {"arg": "", "valid": "false"},
                "title": "Set Volume to ...",
                "subtitle": "vol ${num}",
            }
        )
    else:
        try:
            new = int(op)
        except ValueError:
            new = -1
        if new >= 0:
            set_volume(new)
            results.append(
                {
                    "attributes": {"arg": str(new), "autocomplete": ""},
                    "title": "Set Volume: {}%".format(new),
                    "subtitle": "vol ${num}",
                }
            )
        elif "up".startswith(op):
            val = parse_volume(q[1], 10) if len(q) >= 2 else 10
            set_volume(int(get_volume()) + val)
            results.append(
                {
                    "attributes": {"arg": "", "valid": "false"},
                    "title": "Volume up by {}%".format(val),
                    "subtitle": "vol up ${num}",
                    "subtitleCmd": "Hold cmd to double the increment.",
                }
            )
        elif "down".startswith(op):
            val = parse_volume(q[1], 10) if len(q) >= 2 else 10
            set_volume(int(get_volume()) - val)
            results.append(
                {
                    "attributes": {"arg": "", "valid": "false"},
                    "title": "Volume down by {}%".format(val),
                    "subtitle": "vol down ${num}",
                    "subtitleCmd": "Hold cmd to double the decrement.",
                }
            )
        elif "low".startswith(op):
            set_volume(25)
            results.append(
                {
                    "attributes": {"arg": "", "valid": "false"},
                    "title": "Low Volume: 25%",
                    "subtitle": "vol low",
                }
            )
        elif "mid".startswith(op):
            set_volume(50)
            results.append(
                {
                    "attributes": {"arg": "", "valid": "false"},
                    "title": "Middle Volume: 50%",
                    "subtitle": "vol mid",
                }
            )
        elif "high".startswith(op):
            set_volume(75)
            results.append(
                {
                    "attributes": {"arg": "", "valid": "false"},
                    "title": "High Volume: 75%",
                    "subtitle": "vol high",
                }
            )

    if len(q) > 0:
        results.append(
            {
                "attributes": {"arg": "", "valid": "false"},
                "title": get_volume_summary(),
                "subtitle": "",
            }
        )

        alfred_output = {"items": results}
        sys.stdout.write(json.dumps(alfred_output))  # or use `print`


if __name__ == "__main__":
    process_query(sys.argv[1:])
