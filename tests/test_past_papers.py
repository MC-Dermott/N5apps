"""Checks the past paper index. Run: venv/bin/python tests/test_past_papers.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.data.past_papers import get_past_paper_units, get_past_paper_topics, get_past_paper_entries
from core.engine.question_factory import QUAL_REGISTRY

ids = set()
for qualification in ("National 5", "Higher"):
    assert get_past_paper_units(qualification)
    for unit in get_past_paper_units(qualification):
        assert unit in QUAL_REGISTRY[qualification], unit
        for topic in get_past_paper_topics(qualification, unit):
            entries = get_past_paper_entries(qualification, unit, topic)
            assert entries, topic
            assert len({e["id"] for e in entries}) == len(entries), topic
            for e in entries:
                assert e["drive_id"] and not e["drive_id"].startswith("local"), e
                assert e["question_pages"] >= 1 and e["marking_pages"] >= 1, e
                ids.add(e["id"])
for qualification in ("National 4", "N5 Numeracy"):
    assert get_past_paper_units(qualification) == []
print(f"OK: {len(ids)} questions reachable")
