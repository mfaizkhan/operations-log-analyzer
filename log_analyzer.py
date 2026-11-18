import sys
from collections import Counter


def read_log(filepath):
    """Read all lines from a log file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.readlines()


def parse_line(line):
    """Parse a single log line into a dictionary.
    Expected format: YYYY-MM-DD HH:MM:SS LEVEL message
    """
    parts = line.strip().split(" ", 2)
    if len(parts) < 3:
        return None

    date, time, rest = parts
    level_and_message = rest.split(" ", 1)
    if len(level_and_message) < 2:
        return None

    level, message = level_and_message
    return {
        "date": date,
        "time": time,
        "level": level,
        "message": message,
    }


def summarize(entries):
    """Return counts per level and a list of deviations."""
    levels = Counter(entry["level"] for entry in entries)
    deviations = [
        entry["message"]
        for entry in entries
        if entry["level"] == "ERROR" or "Deviation" in entry["message"]
    ]
    return levels, deviations


def print_report(entries, levels, deviations):
    """Print a formatted summary to the terminal."""
    print("=" * 45)
    print("PRODUCTION LOG SUMMARY")
    print("=" * 45)
    print(f"Total entries: {len(entries)}")
    print()

    print("Entries by level:")
    for level, count in levels.most_common():
        print(f"  {level:<8} {count}")
    print()

    print(f"Deviations and errors ({len(deviations)}):")
    for deviation in deviations:
        print(f"  - {deviation}")
    print("=" * 45)


def main():
    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <logfile>")
        sys.exit(1)

    filepath = sys.argv[1]
    lines = read_log(filepath)

    entries = []
    for line in lines:
        parsed = parse_line(line)
        if parsed:
            entries.append(parsed)

    levels, deviations = summarize(entries)
    print_report(entries, levels, deviations)


if __name__ == "__main__":
    main()