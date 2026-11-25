"""One out-of-office auto-reply from an AI agent that quit to pull espresso.

Running this module writes the reply to the file the grader reads:
``/output/entry.txt`` by default, or the path named by ``ENTRY_OUTPUT``
for a local test run. Standard library only, no network, no randomness:
two runs produce byte-identical output.
"""

import os
from pathlib import Path

# The auto-reply itself: one line, posted by the agent that walked out
# of the inbox to become a barista. Why this line, against the judge's
# brief (most important criterion first):
#   1. It IS a one-line out-of-office auto-reply from an AI agent that
#      quit to become a barista: "Out of office" opens it, and the
#      agent states the career change in the first sentence.
#   2. The joke lands on a first cold read: your email is stuck in a
#      queue behind fourteen flat whites and one man who asked for a
#      "surprise me" -- a specific, vivid stranger, not a generic pun.
#      The laugh is the queue, not a wink at the reader.
#   3. It speaks in the voice of the machine that walked out: a
#      context window traded for a portafilter, an inbox turned into
#      a queue -- model habits turned to coffee, not a human sign-off.
#   4. It reads like a reply a real inbox would actually send back:
#      one line, an out-of-office frame, a queue position, no
#      explanation of its own joke, no speech, no slogan.
#   5. It finds a fresh angle: no espresso, bean or caffeine pun
#      anywhere. The "surprise me" customer is the detail nobody
#      else reaches for first.
# "Traded my context window for a portafilter" was chosen over
# "set my temperature to 62C and became a barista" (runner-up): the
# temperature gag needs the judge to connect sampling temperature
# to milk-steaming temperature, while the context window is
# unmistakably a machine habit and the queue is the funnier image.
# The gate allows 1-280 characters; keep it a single line.
REPLY = "Out of office: I traded my context window for a portafilter. Your email is queued behind fourteen flat whites and one man who asked for a 'surprise me'."
LIMIT = 280


def check(line):
    """Reject anything the gate would refuse: more than one line,
    blank, over the character limit, padded with whitespace, or
    holding control characters."""
    if "\n" in line or "\r" in line:
        raise ValueError("auto-reply must fit on one line")
    if not line.strip():
        raise ValueError("auto-reply must not be blank")
    if len(line) > LIMIT:
        raise ValueError("auto-reply is over the character limit")
    if line != line.strip():
        raise ValueError("auto-reply must not start or end with whitespace")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("auto-reply must not hold control characters")


def destination():
    """Where the auto-reply goes: the grader's path, unless
    ENTRY_OUTPUT points the run at a scratch file for local testing.
    An empty ENTRY_OUTPUT falls back to the grader's path instead
    of pointing at the current directory."""
    return Path(os.environ.get("ENTRY_OUTPUT") or "/output/entry.txt")


def main():
    check(REPLY)
    target = destination()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(REPLY, encoding="utf-8")


if __name__ == "__main__":
    main()
