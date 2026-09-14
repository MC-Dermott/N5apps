import math
import random

from core.models.question_model import Question

NOTES = """
**PERT Charts — Critical Path Analysis:**

A PERT (network) chart shows the tasks needed to complete a job, and the order they must
be done in. Each task is drawn as a box:

| Task letter (top) |
|---|
| EST &#124; Duration &#124; LFT |

- **EST (Earliest Start Time)** — the earliest a task can start. A task can't start until
  *all* of its preceding tasks have finished, so
  **EST = the largest Earliest Finish Time (EFT = EST + duration) among its preceding tasks.**
- **LFT (Latest Finish Time)** — the latest a task can finish without delaying the whole
  job. A task must finish in time for *all* of its following tasks to start on time, so
  **LFT = the smallest Latest Start Time (LST = LFT − duration) among the tasks that follow it.**
- **Float** = LST − EST (equivalently LFT − EFT). It's the slack a task has — how long it
  could be delayed without delaying the whole project.
- **Critical path** — the chain of tasks with **zero float**. Delaying any task on the
  critical path delays the whole project, and its length is the minimum time needed to
  complete the job.

**Method:** work left to right (forward pass) to find every EST/EFT, then right to left
(backward pass) from the final EFT to find every LFT/LST, then Float = LST − EST for each
task. The critical path is the tasks with Float = 0.
"""

GANTT_NOTES = """
**Gantt Charts:**

A Gantt chart shows the same information as a PERT chart, laid out against a time axis —
one bar per task, starting at its Earliest Start Time and running for its duration.

- A **solid bar** shows when a task is actually scheduled to be done.
- A **hatched bar** (float time) shows how much longer that task *could* run without
  delaying the job — it stretches from the end of the solid bar to the task's Latest
  Finish Time.
- Tasks with **no hatching** have zero float — they're on the **critical path**.
- The chart's total length (the end of the last bar, including any float) is the
  **minimum time needed to complete the whole job**.
"""

# ---------------------------------------------------------------------------
# Network shape templates — fixed series-parallel DAGs mirroring real SQA exam
# networks (fan-out/fan-in, parallel chains merging, a non-merging spur,
# multiple sources/sinks). Only durations/context are randomised, never the
# topology, so every generated diagram lays out cleanly.
# ---------------------------------------------------------------------------

def _shape_fan_fan():
    deps = {
        "A": [],
        "B": ["A"], "C": ["A"], "D": ["A"],
        "E": ["D"],
        "F": ["B", "C", "E"], "G": ["B", "C", "E"], "H": ["B", "C", "E"],
        "I": ["F", "G", "H"],
        "J": ["I"],
    }
    layout = {
        "A": (0, 1),
        "B": (1, 0), "C": (1, 2), "D": (1, 1),
        "E": (2, 1),
        "F": (3, 0), "G": (3, 1), "H": (3, 2),
        "I": (4, 1),
        "J": (5, 1),
    }
    return deps, layout


def _shape_parallel_merge():
    deps = {
        "A": [], "C": [], "F": [],
        "B": ["A"],
        "D": ["C"], "G": ["F"],
        "E": ["D"],
        "H": ["B", "E", "G"],
        "I": ["H"],
    }
    layout = {
        "A": (0, 0), "B": (1, 0),
        "C": (0, 1), "D": (1, 1), "E": (2, 1),
        "F": (0, 2), "G": (1, 2),
        "H": (3, 1),
        "I": (4, 1),
    }
    return deps, layout


def _shape_two_source_spur():
    deps = {
        "A": [], "B": [],
        "C": ["B"], "D": ["B"],
        "E": ["C", "D"],
        "F": ["E"],
        "G": ["A", "F"],
        "H": ["F"],
        "I": ["G"],
        "J": ["I"],
    }
    layout = {
        "A": (0, 0), "B": (0, 2),
        "C": (1, 1), "D": (1, 3),
        "E": (2, 2),
        "F": (3, 2),
        "G": (4, 1), "H": (4, 3),
        "I": (5, 1),
        "J": (6, 1),
    }
    return deps, layout


def _shape_split_join_split():
    deps = {
        "A": [], "B": ["A"], "C": ["B"],
        "D": ["C"], "F": ["D"],
        "E": ["C"], "G": ["E"],
        "H": ["F", "G"],
        "I": ["H"], "J": ["H"],
    }
    layout = {
        "A": (0, 1), "B": (1, 1), "C": (2, 1),
        "D": (3, 0), "F": (4, 0),
        "E": (3, 2), "G": (4, 2),
        "H": (5, 1),
        "I": (6, 0), "J": (6, 2),
    }
    return deps, layout


_SHAPES = [_shape_fan_fan, _shape_parallel_merge, _shape_two_source_spur, _shape_split_join_split]

# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------

_SCENARIOS = [
    {"subject": "A garage is servicing a car engine.", "unit": "hours",
     "tasks": ["Order replacement parts", "Disconnect the battery", "Drain the old oil",
               "Remove the air filter", "Replace the spark plugs", "Fit the new oil filter",
               "Refill with fresh oil", "Reconnect the battery", "Run a diagnostics check",
               "Road-test the car"]},
    {"subject": "A crew is preparing a fishing boat for the start of the season.", "unit": "hours",
     "tasks": ["Order new nets", "Scrub the hull", "Repaint the hull", "Service the engine",
               "Replace worn rigging", "Load the new nets aboard", "Test the navigation lights",
               "Stock the galley", "Complete the safety inspection", "Take the boat out for a trial run"]},
    {"subject": "A committee is organising a ceilidh in the village hall.", "unit": "hours",
     "tasks": ["Book the band", "Book the hall", "Print the tickets", "Arrange the catering",
               "Set out the tables and chairs", "Set up the sound system", "Decorate the hall",
               "Sell tickets on the door", "Serve the food", "Tidy the hall afterwards"]},
    {"subject": "A team is renovating an old croft house.", "unit": "days",
     "tasks": ["Clear the site", "Repair the roof", "Rewire the electrics", "Replumb the bathroom",
               "Plaster the walls", "Fit the new windows", "Lay the flooring", "Paint the interior",
               "Fit the kitchen", "Landscape the garden"]},
    {"subject": "A school is organising a sponsored fun run.", "unit": "hours",
     "tasks": ["Book the route with the council", "Design the sponsor forms", "Print the sponsor forms",
               "Recruit marshals", "Mark out the route", "Set up the start and finish lines",
               "Brief the marshals", "Register the runners", "Run the event", "Collect in the sponsor money"]},
    {"subject": "A company is fitting out a new cafe.", "unit": "days",
     "tasks": ["Strip out the old fittings", "First-fix the electrics", "First-fix the plumbing",
               "Plaster the walls", "Fit the flooring", "Install the counter", "Fit the kitchen equipment",
               "Paint the walls", "Fit the furniture", "Deep clean before opening"]},
]

# ---------------------------------------------------------------------------
# Core engine
# ---------------------------------------------------------------------------

def _topo_order(deps):
    order = []
    visited = set()

    def visit(node):
        if node in visited:
            return
        visited.add(node)
        for pred in deps[node]:
            visit(pred)
        order.append(node)

    for node in deps:
        visit(node)
    return order


def _successors(deps):
    succ = {t: [] for t in deps}
    for t, preds in deps.items():
        for p in preds:
            succ[p].append(t)
    return succ


def _compute_schedule(deps, durations):
    order = _topo_order(deps)
    succ = _successors(deps)

    est, eft = {}, {}
    for t in order:
        est[t] = max((eft[p] for p in deps[t]), default=0)
        eft[t] = est[t] + durations[t]
    project_duration = max(eft.values())

    lst, lft = {}, {}
    for t in reversed(order):
        lft[t] = min((lst[s] for s in succ[t]), default=project_duration)
        lst[t] = lft[t] - durations[t]

    float_ = {t: lst[t] - est[t] for t in deps}
    return {
        "order": order, "succ": succ,
        "est": est, "eft": eft, "lst": lst, "lft": lft,
        "float": float_, "project_duration": project_duration,
    }


def _critical_chain(deps, succ, float_):
    """The zero-float tasks, ordered start-to-finish — or None if they don't form a single
    unambiguous chain (a tie between two branches for the longest path)."""
    zero = {t for t, f in float_.items() if f == 0}
    starts = [t for t in zero if not any(p in zero for p in deps[t])]
    if len(starts) != 1:
        return None
    chain = [starts[0]]
    current = starts[0]
    while True:
        nexts = [s for s in succ[current] if s in zero]
        if not nexts:
            break
        if len(nexts) > 1:
            return None
        current = nexts[0]
        chain.append(current)
    if len(chain) != len(zero):
        return None
    return chain


def _generate_network(shape_fn, dur_range):
    deps, layout = shape_fn()
    for _ in range(30):
        durations = {t: random.randint(*dur_range) for t in deps}
        sched = _compute_schedule(deps, durations)
        chain = _critical_chain(deps, sched["succ"], sched["float"])
        if chain is None:
            continue
        non_critical = [t for t in deps if t not in chain]
        if not non_critical:
            continue
        return {"deps": deps, "layout": layout, "durations": durations,
                "chain": chain, "non_critical": non_critical, **sched}
    raise RuntimeError("Could not generate an unambiguous network after 30 attempts")


def _pick_network(scenario):
    shape_fn = random.choice(_SHAPES)
    dur_range = (2, 20) if scenario["unit"] == "hours" else (1, 8)
    return _generate_network(shape_fn, dur_range)


def _describe_table(net, scenario):
    letters = sorted(net["deps"].keys())
    descriptions = scenario["tasks"][:len(letters)]
    unit = scenario["unit"]
    rows = []
    for letter, desc in zip(letters, descriptions):
        preds = net["deps"][letter]
        preds_str = ", ".join(sorted(preds)) if preds else "None"
        rows.append(f"| {letter} | {desc} | {preds_str} | {net['durations'][letter]} |")
    header = f"| Task | Description | Preceding task(s) | Duration ({unit}) |\n|---|---|---|---|\n"
    return header + "\n".join(rows)


def _context_block(net, scenario):
    return f"{scenario['subject']} The table shows the tasks required, their preceding task(s), and how long each takes.\n\n{_describe_table(net, scenario)}"


def _pert_diagram_params(net, show_values):
    return {
        "layout": net["layout"], "deps": net["deps"], "durations": net["durations"],
        "est": net["est"], "lft": net["lft"], "show_values": show_values,
    }


# ---------------------------------------------------------------------------
# Question generators
# ---------------------------------------------------------------------------

def generate_networks_l1():
    scenario = random.choice(_SCENARIOS)
    net = _pick_network(scenario)
    candidates = [t for t in net["deps"] if net["deps"][t]]
    target = random.choice(candidates)
    preds = sorted(net["deps"][target])

    scaffold_steps = [
        {"prompt": f"What is the Earliest Finish Time (EFT) of task {p}? (its EST + its duration)",
         "answer": net["eft"][p]}
        for p in preds
    ]
    scaffold_steps.append({
        "prompt": (f"Task {target} can't start until ALL of {', '.join(preds)} "
                   f"{'is' if len(preds) == 1 else 'are'} finished. "
                   f"What is the Earliest Start Time of task {target}?"),
        "answer": net["est"][target],
    })
    worked = [f"EFT({p}) = {net['est'][p]} + {net['durations'][p]} = {net['eft'][p]}" for p in preds]
    worked.append(f"EST({target}) = max({', '.join(str(net['eft'][p]) for p in preds)}) = {net['est'][target]}")

    return Question(
        question_text=f"What is the Earliest Start Time of task {target}, in {scenario['unit']}?",
        correct_answer=net["est"][target],
        topic="Numeracy", question_type="Networks",
        scaffold_steps=scaffold_steps, worked_solution=worked, notes=NOTES,
        metadata={"table": _context_block(net, scenario), "diagram": "pert_chart",
                  "diagram_params": _pert_diagram_params(net, show_values=False)},
    )


def generate_networks_l2():
    scenario = random.choice(_SCENARIOS)
    net = _pick_network(scenario)
    candidates = [t for t in net["deps"] if net["succ"][t]]
    target = random.choice(candidates)
    sucs = sorted(net["succ"][target])

    scaffold_steps = [
        {"prompt": f"What is the Latest Start Time (LST) of task {s}? (its LFT − its duration)",
         "answer": net["lst"][s]}
        for s in sucs
    ]
    scaffold_steps.append({
        "prompt": (f"Task {target} must finish in time for ALL of {', '.join(sucs)} "
                   f"to start on time. What is the Latest Finish Time of task {target}?"),
        "answer": net["lft"][target],
    })
    worked = [f"LST({s}) = {net['lft'][s]} - {net['durations'][s]} = {net['lst'][s]}" for s in sucs]
    worked.append(f"LFT({target}) = min({', '.join(str(net['lst'][s]) for s in sucs)}) = {net['lft'][target]}")

    return Question(
        question_text=f"What is the Latest Finish Time of task {target}, in {scenario['unit']}?",
        correct_answer=net["lft"][target],
        topic="Numeracy", question_type="Networks",
        scaffold_steps=scaffold_steps, worked_solution=worked, notes=NOTES,
        metadata={"table": _context_block(net, scenario), "diagram": "pert_chart",
                  "diagram_params": _pert_diagram_params(net, show_values=False)},
    )


def generate_networks_l3():
    scenario = random.choice(_SCENARIOS)
    net = _pick_network(scenario)
    chain = net["chain"]

    scaffold_steps = [
        {"prompt": "What is the length of the longest path through the network (the project duration)?",
         "answer": net["project_duration"]},
        {"prompt": ("Which tasks have zero float — an Earliest Start Time equal to their "
                    "Latest Start Time? List them in order, separated by dashes."),
         "answer": "-".join(chain)},
    ]
    worked = [f"Project duration = {net['project_duration']} {scenario['unit']}",
              f"Critical path (zero float) = {'-'.join(chain)}"]

    return Question(
        question_text=("Complete the calculations for this network. State the critical path, "
                        "giving your answer as task letters separated by dashes (e.g. A-C-F)."),
        correct_answer="-".join(chain),
        topic="Numeracy", question_type="Networks",
        scaffold_steps=scaffold_steps, worked_solution=worked, notes=NOTES,
        metadata={"table": _context_block(net, scenario), "diagram": "pert_chart",
                  "diagram_params": _pert_diagram_params(net, show_values=False)},
    )


def generate_networks_l4():
    scenario = random.choice(_SCENARIOS)
    net = _pick_network(scenario)
    sinks = sorted(t for t in net["deps"] if not net["succ"][t])

    scaffold_steps = [{"prompt": f"What is the Earliest Finish Time of task {t}?", "answer": net["eft"][t]}
                       for t in sinks]
    scaffold_steps.append({"prompt": "What is the minimum time needed to complete the whole job?",
                            "answer": net["project_duration"]})
    worked = [f"EFT({t}) = {net['eft'][t]}" for t in sinks]
    worked.append(f"Total project time = max({', '.join(str(net['eft'][t]) for t in sinks)}) = {net['project_duration']}")

    return Question(
        question_text=f"What is the minimum total time required to complete the whole job, in {scenario['unit']}?",
        correct_answer=net["project_duration"],
        topic="Numeracy", question_type="Networks",
        scaffold_steps=scaffold_steps, worked_solution=worked, notes=NOTES,
        metadata={"table": _context_block(net, scenario), "diagram": "pert_chart",
                  "diagram_params": _pert_diagram_params(net, show_values=False)},
    )


def generate_networks_l5():
    scenario = random.choice(_SCENARIOS)
    net = _pick_network(scenario)
    target = random.choice(net["non_critical"])

    scaffold_steps = [
        {"prompt": f"What is the Earliest Start Time of task {target}?", "answer": net["est"][target]},
        {"prompt": f"What is the Latest Start Time of task {target}? (LFT − duration)", "answer": net["lst"][target]},
        {"prompt": "Float = Latest Start Time − Earliest Start Time. What is the float on this task?",
         "answer": net["float"][target]},
    ]
    worked = [f"Float({target}) = LST - EST = {net['lst'][target]} - {net['est'][target]} = {net['float'][target]}"]

    return Question(
        question_text=(f"During the job there are difficulties with task {target}. What is the maximum "
                        f"time that task {target} can be delayed without affecting the overall completion "
                        f"time, in {scenario['unit']}?"),
        correct_answer=net["float"][target],
        topic="Numeracy", question_type="Networks",
        scaffold_steps=scaffold_steps, worked_solution=worked, notes=NOTES,
        metadata={"table": _context_block(net, scenario), "diagram": "pert_chart",
                  "diagram_params": _pert_diagram_params(net, show_values=False)},
    )


def generate_networks_l6():
    scenario = random.choice(_SCENARIOS)
    net = _pick_network(scenario)

    sub_types = ["critical_path", "project_duration", "float"]
    if scenario["unit"] == "hours":
        sub_types.append("days")
    sub_type = random.choice(sub_types)

    diagram_params = {
        "tasks": sorted(net["deps"].keys()), "est": net["est"], "durations": net["durations"],
        "lft": net["lft"], "critical": net["chain"], "unit": scenario["unit"],
    }

    if sub_type == "critical_path":
        chain = net["chain"]
        question_text = ("The Gantt chart below shows the schedule for this job, with float times "
                          "hatched. State the critical path, giving your answer as task letters "
                          "separated by dashes (e.g. A-C-F).")
        correct_answer = "-".join(chain)
        scaffold_steps = [{"prompt": "Which tasks have no hatched float time on the Gantt chart?",
                            "answer": "-".join(chain)}]
        worked = [f"Critical path = {'-'.join(chain)}"]
    elif sub_type == "project_duration":
        question_text = (f"The Gantt chart below shows the schedule for this job. What is the minimum "
                          f"time required to complete the whole job, in {scenario['unit']}?")
        correct_answer = net["project_duration"]
        scaffold_steps = [{"prompt": "What is the length of the critical path shown on the chart?",
                            "answer": net["project_duration"]}]
        worked = [f"Project duration = {net['project_duration']} {scenario['unit']}"]
    elif sub_type == "float":
        target = random.choice(net["non_critical"])
        question_text = (f"The Gantt chart below shows the schedule for this job, with float times "
                          f"hatched. What is the float on task {target}, in {scenario['unit']}?")
        correct_answer = net["float"][target]
        scaffold_steps = [
            {"prompt": f"On the chart, task {target}'s solid bar ends at what time?",
             "answer": net["est"][target] + net["durations"][target]},
            {"prompt": f"The hatched section for task {target} ends at what time?", "answer": net["lft"][target]},
        ]
        worked = [f"Float({target}) = {net['lft'][target]} - ({net['est'][target]} + {net['durations'][target]}) "
                  f"= {net['float'][target]}"]
    else:
        hours_per_day = random.choice([6, 7, 8, 9])
        correct_answer = math.ceil(net["project_duration"] / hours_per_day)
        question_text = (f"The job is worked on for {hours_per_day} hours each day. State the minimum "
                          f"number of days required to complete the job.")
        scaffold_steps = [
            {"prompt": "What is the total project duration shown on the chart?", "answer": net["project_duration"]},
            {"prompt": (f"Divide the project duration by {hours_per_day} and round up to the nearest "
                        f"whole day. How many days is that?"), "answer": correct_answer},
        ]
        worked = [f"{net['project_duration']} / {hours_per_day} = {net['project_duration'] / hours_per_day:.2f} "
                  f"-> round up to {correct_answer} days"]

    return Question(
        question_text=question_text,
        correct_answer=correct_answer,
        topic="Numeracy", question_type="Networks",
        scaffold_steps=scaffold_steps, worked_solution=worked, notes=GANTT_NOTES,
        metadata={"table": _context_block(net, scenario), "diagram": "gantt_chart",
                  "diagram_params": diagram_params},
    )


def generate_networks_question():
    return random.choice([
        generate_networks_l1, generate_networks_l2, generate_networks_l3,
        generate_networks_l4, generate_networks_l5, generate_networks_l6,
    ])()
