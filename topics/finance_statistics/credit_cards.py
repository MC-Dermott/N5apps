"""Higher Finance — Credit Cards.

Mirrors Credit_Cards_Worksheet.docx (Higher Apps/Worksheets/Finance). Convention from 2025 Q11: interest is
added at the end of the month (balance × (1 + annual)^(1/12)), THEN the minimum payment — 5% of the balance
or £5, whichever is higher — is made on the 1st. Traps: paying before adding interest (Candidate B), dividing
the annual rate by 12, ignoring the £5 floor, forgetting a balance-transfer fee.
"""
import random

from core.models.question_model import Question

TOPIC = "Finance"
QTYPE = "Credit Cards"
_NAMES = ["Freddie", "Eilidh", "Callum", "Mhairi", "Fiona", "Iona", "Ruaridh", "Kenny", "Seonag", "Donald"]

NOTES = """
**Credit cards**

1. **Interest first:** balance at the end of the month = balance × (1 + annual rate)^(1/12)
2. **Then the payment** on the 1st: minimum payment = 5% of that balance **or £5, whichever is higher**
3. Balance after the payment = end-of-month balance − payment

**Example:** Freddie's card has an annual effective rate of 29.9%. After his payment on 1 March his balance was £823.19
and he does not use the card in March. Calculate his balance on 1 April after the minimum payment.

- Monthly rate = 1.299^(1/12) − 1 = 2.205%
- Balance on 31 March = 823.19 × 1.299^(1/12) = £841.33
- Minimum payment = 5% of £841.33 = £42.07 (more than £5)
- Balance on 1 April = 841.33 − 42.07 = **£799.26**

⚠ Don't take off the payment before adding the interest (2025 marking instructions). A reason to pay the full
balance: to avoid interest / building up debt — "avoids going into debt" is **not** accepted.
"""


def _m(a):
    return (1 + a) ** (1 / 12) - 1


def _month(bal, i):
    it = round(bal * i + 1e-9, 2); b = round(bal + it, 2)
    pay = min(b, max(round(0.05 * b + 1e-9, 2), 5.0))
    return it, b, pay, round(b - pay, 2)


def generate_credit_cards_l1():
    """One month: interest, then the minimum payment (styled on 2025 Q11(a))."""
    name = random.choice(_NAMES); a = round(random.uniform(18.9, 34.9), 1)
    bal = round(random.uniform(150, 2500), 2); i = _m(a / 100)
    it, b, pay, after = _month(bal, i)
    q = (f"{name}'s credit card has an annual effective rate of interest of {a}%. Interest is added at the end of each month, "
         f"and the minimum payment (5% of the balance or £5, whichever is higher) is made on the 1st.\n\nAfter the last payment "
         f"the balance was £{bal:,.2f}, and the card is not used this month. Calculate the balance after the next minimum payment.")
    return Question(question_text=q, correct_answer=after, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Monthly effective rate, as a percentage (3 d.p.)", "answer": round(i * 100, 3)},
                                    {"prompt": "Balance at the end of the month, after interest (£)", "answer": b},
                                    {"prompt": "Minimum payment (£)", "answer": pay}],
                    worked_solution=[f"Monthly rate = {1 + a / 100:.3f}^(1/12) − 1 = {i * 100:.3f}%",
                                     f"End of month: {bal:,.2f} × {1 + a / 100:.3f}^(1/12) = £{b:,.2f}",
                                     f"Minimum payment = 5% of £{b:,.2f} = £{pay:,.2f}", f"Balance = £{after:,.2f}"],
                    notes=NOTES)


def generate_credit_cards_l2():
    """Three months of minimum payments."""
    name = random.choice(_NAMES); a = round(random.uniform(18.9, 29.9), 1)
    start = float(random.randrange(300, 2001, 10)); i = _m(a / 100)
    bal, lines, steps = start, [], []
    for k in range(3):
        it, b, pay, bal = _month(bal, i)
        lines.append(f"Month {k + 1}: interest £{it:.2f}, payment £{pay:.2f}, balance £{bal:,.2f}")
        steps.append({"prompt": f"Balance after payment {k + 1} (£)", "answer": bal})
    q = (f"{name} owes £{start:,.2f} on a credit card with an annual effective rate of interest of {a}%. Interest is added at "
         f"the end of each month, then {name} pays only the minimum (5% of the balance or £5, whichever is higher). The card "
         f"is not used.\n\nCalculate the balance after the third payment.")
    return Question(question_text=q, correct_answer=bal, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps[:2], worked_solution=[f"Monthly rate = {i * 100:.3f}%"] + lines, notes=NOTES)


def generate_credit_cards_l3():
    """The minimum payment, including the £5 floor."""
    bal = random.choice([round(random.uniform(20, 99.99), 2), round(random.uniform(100, 3000), 2)])
    pay = max(round(0.05 * bal + 1e-9, 2), 5.0)
    q = (f"A credit card's minimum payment is 5% of the balance or £5, whichever is higher.\n\n"
         f"Calculate the minimum payment on a balance of £{bal:,.2f}.")
    return Question(question_text=q, correct_answer=pay, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "5% of the balance (£)", "answer": round(0.05 * bal, 2)}],
                    worked_solution=[f"5% of £{bal:,.2f} = £{0.05 * bal:,.2f}",
                                     f"Minimum payment = £{pay:,.2f}" + (" (5% is less than £5, so £5)" if pay == 5 else "")],
                    notes=NOTES)


def generate_credit_cards_l4():
    """Comparing a monthly rate with an annual rate: annual rate of the monthly card."""
    mp = random.choice([1.4, 1.6, 1.8, 1.9, 2.1, 2.3, 2.5]); a = round(random.uniform(18.9, 32.9), 1)
    ann = ((1 + mp / 100) ** 12 - 1) * 100
    q = (f"Card A charges an annual effective rate of {a}%. Card B charges {mp}% per month.\n\n"
         f"Calculate the annual effective rate of Card B, as a percentage to 2 decimal places.")
    return Question(question_text=q, correct_answer=round(ann, 2), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Annual multiplier for Card B, (1 + monthly rate)^12 (5 d.p.)", "answer": round((1 + mp / 100) ** 12, 5)}],
                    worked_solution=[f"{1 + mp / 100:g}^12 − 1 = {ann:.2f}% per year",
                                     f"Card {'A' if a < ann else 'B'} is cheaper ({min(a, ann):.2f}% < {max(a, ann):.2f}%)"],
                    notes=NOTES)


def generate_credit_cards_l5():
    """Balance transfer: saving over the offer period (ignoring payments)."""
    bal = random.randrange(1000, 5001, 100); a = round(random.uniform(19.9, 29.9), 1)
    months = random.choice([12, 15, 18, 24]); fee = random.choice([2.5, 2.9, 3.0, 3.5])
    interest = bal * (1 + a / 100) ** (months / 12) - bal; f = bal * fee / 100
    q = (f"£{bal:,} is owed on a card with an annual effective rate of {a}%. Another card offers 0% interest for {months} months "
         f"on a balance transfer, with a {fee}% transfer fee.\n\nCalculate the saving over the {months} months (ignoring payments).")
    return Question(question_text=q, correct_answer=round(interest - f, 2), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": f"Interest on the original card over {months} months (£)", "answer": round(interest, 2)},
                                    {"prompt": "Transfer fee (£)", "answer": round(f, 2)}],
                    worked_solution=[f"Interest = {bal:,} × {1 + a / 100:.3f}^({months}/12) − {bal:,} = £{interest:,.2f}",
                                     f"Fee = {fee}% of {bal:,} = £{f:,.2f}", f"Saving = £{interest - f:,.2f}"],
                    notes=NOTES)


def generate_credit_cards_question():
    return random.choice([generate_credit_cards_l1, generate_credit_cards_l2, generate_credit_cards_l3,
                          generate_credit_cards_l4, generate_credit_cards_l5])()
