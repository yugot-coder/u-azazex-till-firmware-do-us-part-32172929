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
    raw = text.encode("utf-8")
    # The file must end with exactly one trailing newline — no more, no less.
    assert text.endswith("\n"), "entry.txt must end with a newline"
    assert not text.endswith("\n\n"), "entry.txt must not end with blank lines"
    line = text[:-1]
    assert "\n" not in line and "\r" not in line, "entry must be a single line"
    # No leading/trailing whitespace, tabs, or control characters on the line.
    assert line == line.strip(), "entry line must not have leading/trailing whitespace"
    assert not any(ord(ch) < 0x20 for ch in line), (
        "entry line must not contain control characters"
    )
    assert line, "entry.txt must not be only whitespace"
    assert 1 <= len(line) <= MAX_CHARS, (
        f"entry must be 1-{MAX_CHARS} characters, got {len(line)}"
    )
    # Byte length (1-200 bytes) tracks the character gate for this ASCII text.
    assert 1 <= len(raw) - 1 <= MAX_CHARS, (
        f"entry must be 1-{MAX_CHARS} bytes, got {len(raw) - 1}"
    )
    assert line == ENTRY.rstrip("\n"), "entry.txt content differs from ENTRY"


if __name__ == "__main__":
    main()
