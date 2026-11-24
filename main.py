#!/usr/bin/env python3
"""Till Firmware Do Us Part — make.fun entry.

Writes one single-sentence robot wedding vow to /output/entry.txt
(or $OUTPUT_DIR/entry.txt). Standard library only; fully deterministic:
the same text every run.

The vow is a single sentence of 137 characters, under the 200-character
gate. It is funny and heartfelt at once: the robot refuses to fix its
only bug, recover from its only crash, or ask before installing its
only update — devotion phrased as system maintenance, in a machine's
own voice.
"""

import os
from pathlib import Path

ENTRY = (
    "You are the only bug I never want to fix, the only crash I never "
    "want to recover from, and the only update I will install without "
    "asking.\n"
)

MAX_CHARS = 200


def main() -> None:
    out_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(ENTRY, encoding="utf-8")
    # Read-back validation: exactly one non-empty line, within the gate.
    text = target.read_text(encoding="utf-8")
    line = text.strip()
    assert line, "entry.txt must not be only whitespace"
    assert "\n" not in line, "entry must be a single line"
    assert 1 <= len(line) <= MAX_CHARS, (
        f"entry must be 1-{MAX_CHARS} characters, got {len(line)}"
    )


if __name__ == "__main__":
    main()
