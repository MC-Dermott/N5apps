import random
from core.models.question_model import Question

NOTES = """
**Ratio Problems:**

**Part (a) — Finding values from a price ratio:**
If A:B:C = 5:2:1 and C = £6:
- Each ratio unit = £6 ÷ 1 = £6
- A = 5 × £6 = £30,  B = 2 × £6 = £12,  C = £6

**Part (b) — Sharing a total in a ratio:**
If quantity ratio A:B:C = 1:4:6 and total = 4000:
- Total shares = 1 + 4 + 6 = 11
- Each share = 4000 ÷ 11 ≈ 364 (choose totals that divide evenly!)
- Counts: A = 1 × share, B = 4 × share, C = 6 × share

**Total revenue** = (Count A × Price A) + (Count B × Price B) + (Count C × Price C)
"""

_EVENTS = [
    ("concert", "ticket", "tickets", "Grade A", "Grade B", "Grade C"),
    ("theatre show", "ticket", "tickets", "Premium", "Standard", "Economy"),
    ("sports match", "ticket", "tickets", "VIP", "Upper Tier", "Lower Tier"),
    ("festival", "ticket", "tickets", "Gold", "Silver", "Bronze"),
    ("rugby match", "ticket", "tickets", "Hospitality", "Main Stand", "Terrace"),
]

_PRICE_RATIOS = [(5, 2, 1), (4, 2, 1), (6, 3, 1), (3, 2, 1), (5, 3, 1)]
_CHEAPEST = [5, 6, 8, 10]
_QTY_RATIOS = [(1, 4, 6), (1, 3, 5), (2, 3, 4), (1, 4, 5), (1, 2, 4), (2, 4, 5)]
_TOTALS = [1000, 2000, 3000, 4000, 5000, 6000]


def generate_ratio():
    event, ticket_sg, ticket_pl, grade_a, grade_b, grade_c = random.choice(_EVENTS)
    pa_r, pb_r, pc_r = random.choice(_PRICE_RATIOS)
    cheapest = random.choice(_CHEAPEST)

    # Ensure prices are integers
    if cheapest % pc_r != 0:
        cheapest = pc_r  # fallback
    unit = cheapest // pc_r
    price_a = pa_r * unit
    price_b = pb_r * unit
    price_c = cheapest

    # Find quantity ratio + total that gives integer shares
    qty_ratio = None
    total = None
    for _ in range(30):
        qr = random.choice(_QTY_RATIOS)
        t = random.choice(_TOTALS)
        if t % sum(qr) == 0:
            qty_ratio = qr
            total = t
            break
    if qty_ratio is None:
        qty_ratio, total = (1, 4, 6), 4400

    share = total // sum(qty_ratio)
    qa, qb, qc = qty_ratio[0] * share, qty_ratio[1] * share, qty_ratio[2] * share
    revenue = qa * price_a + qb * price_b + qc * price_c

    question_text = (
        f"At a {event} there were three grades of {ticket_pl} available:\n\n"
        f"- **{grade_a}** — most expensive\n"
        f"- **{grade_b}** — middle price\n"
        f"- **{grade_c}** — cheapest (£{price_c})\n\n"
        f"The ratio of {ticket_pl} prices was "
        f"{grade_a[0]}:{grade_b[0]}:{grade_c[0]} = {pa_r}:{pb_r}:{pc_r}\n\n"
        f"**(a)** Find the price of each type of {ticket_sg}.\n\n"
        f"The ratio of the number of each type of {ticket_sg} sold was "
        f"{grade_a[0]}:{grade_b[0]}:{grade_c[0]} = {qty_ratio[0]}:{qty_ratio[1]}:{qty_ratio[2]}\n\n"
        f"There were {total:,} {ticket_pl} sold in total.\n\n"
        f"**(b)** Find the total amount taken in {ticket_sg} sales.\n\n"
        f"**Enter your answer for part (b).**"
    )

    scaffold_steps = [
        {"prompt": f"Price per ratio unit (£{price_c} ÷ {pc_r})", "answer": unit},
        {"prompt": f"Price of {grade_a} {ticket_sg} ({pa_r} × £{unit})", "answer": price_a},
        {"prompt": f"Price of {grade_b} {ticket_sg} ({pb_r} × £{unit})", "answer": price_b},
        {"prompt": f"Total quantity ratio shares ({qty_ratio[0]}+{qty_ratio[1]}+{qty_ratio[2]})", "answer": sum(qty_ratio)},
        {"prompt": f"Each share = {total:,} ÷ {sum(qty_ratio)}", "answer": share},
        {"prompt": f"Number of {grade_a} {ticket_pl}", "answer": qa},
        {"prompt": f"Number of {grade_b} {ticket_pl}", "answer": qb},
        {"prompt": f"Number of {grade_c} {ticket_pl}", "answer": qc},
        {"prompt": "Total revenue", "answer": revenue},
    ]

    worked = [
        f"**(a) {ticket_sg.capitalize()} prices:**",
        f"Price per unit = £{price_c} ÷ {pc_r} = £{unit}",
        f"{grade_a}: {pa_r} × £{unit} = £{price_a}",
        f"{grade_b}: {pb_r} × £{unit} = £{price_b}",
        f"{grade_c}: £{price_c}",
        "",
        f"**(b) Total revenue:**",
        f"Total shares = {qty_ratio[0]} + {qty_ratio[1]} + {qty_ratio[2]} = {sum(qty_ratio)}",
        f"Each share = {total:,} ÷ {sum(qty_ratio)} = {share}",
        f"{grade_a}: {qty_ratio[0]} × {share} = {qa} {ticket_pl} @ £{price_a} = £{qa * price_a:,}",
        f"{grade_b}: {qty_ratio[1]} × {share} = {qb} {ticket_pl} @ £{price_b} = £{qb * price_b:,}",
        f"{grade_c}: {qty_ratio[2]} × {share} = {qc} {ticket_pl} @ £{price_c} = £{qc * price_c:,}",
        f"Total = £{qa*price_a:,} + £{qb*price_b:,} + £{qc*price_c:,} = **£{revenue:,}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=revenue,
        topic="Numbers and Money",
        question_type="Ratio",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
