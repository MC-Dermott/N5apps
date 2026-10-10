"""Turn an 'App assignments' CSV exported from the assessment tracker into assignment groups.

The CSV (export_app_assignments.py) has one row per pupil per app item: username, qualification,
unit, question_type, tracker_topic, topic_pct. Pupils whose focus items are identical share one
assignment, so a class of 30 becomes a handful of assignments rather than 30."""
import csv
import io

REQUIRED = ["username", "qualification", "unit", "question_type", "tracker_topic"]


def parse(csv_bytes, registry):
    """Returns (groups, problems). groups: [{items, topics, usernames}] ; problems: [str]."""
    reader = csv.DictReader(io.StringIO(csv_bytes.decode("utf-8-sig")))
    missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
    if missing:
        return [], [f"Not an App assignments export — missing column(s): {', '.join(missing)}."]
    problems, per_user, topics = [], {}, {}
    for row in reader:
        user = (row["username"] or "").strip()
        item = (row["qualification"], row["unit"], row["question_type"])
        if not user:
            continue
        if item[2] not in registry.get(item[0], {}).get(item[1], {}):
            problems.append(f"{item[1]} / {item[2]} ({item[0]}) is not in the app — skipped.")
            continue
        items = per_user.setdefault(user, [])
        if item not in items:
            items.append(item)
        topics.setdefault(user, [])
        if row["tracker_topic"] not in topics[user]:
            topics[user].append(row["tracker_topic"])
    grouped = {}
    for user, items in per_user.items():
        g = grouped.setdefault(tuple(sorted(items)), dict(
            items=[dict(qualification=q, topic=u, question_type=t) for q, u, t in items],
            topics=topics[user], usernames=[]))
        g["usernames"].append(user)
    groups = sorted(grouped.values(), key=lambda g: (-len(g["usernames"]), g["topics"]))
    return groups, sorted(set(problems))


def title_for(base, group):
    shown = ", ".join(group["topics"][:3]) + ("…" if len(group["topics"]) > 3 else "")
    return f"{base}: {shown}"
