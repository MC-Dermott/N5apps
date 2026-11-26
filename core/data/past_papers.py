"""Real SQA past paper questions for "Past Paper Questions" mode.

Each question is its own PDF on Google Drive (anyone with the link can view): the question pages, then the marking
instructions, then the paper's formulae list (National 5) or data booklet (Higher, only where needed). past_papers.json
records where each one is and which topics it tests; rebuild it with tools/build_past_paper_index.py.
"""
import json
from pathlib import Path

_INDEX = json.loads((Path(__file__).parent / "past_papers.json").read_text())


def get_past_paper_units(qualification):
    return list(_INDEX["topics"].get(qualification, {}))


def get_past_paper_topics(qualification, unit):
    return list(_INDEX["topics"].get(qualification, {}).get(unit, {}))


def get_past_paper_entries(qualification, unit, topic):
    """Questions testing this topic, each with the parts that do ("" for the whole question)."""
    found = _INDEX["topics"].get(qualification, {}).get(unit, {}).get(topic, [])
    return [{**_INDEX["questions"][e["id"]], **e} for e in found]
