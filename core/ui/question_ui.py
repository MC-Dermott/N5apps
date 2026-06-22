import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def _build_duration_str(h, m):
    h, m = int(h), int(m)
    h_word = f"{h} hour{'s' if h != 1 else ''}"
    m_word = f"{m} minute{'s' if m != 1 else ''}"
    if h == 0:
        return m_word
    if m == 0:
        return h_word
    return f"{h_word} {m_word}"


def _render_duration_input(qid, suffix):
    col_h, col_hlbl, col_m, col_mlbl = st.columns([1.2, 0.5, 1.2, 0.5])
    with col_h:
        h = st.number_input("Hours", min_value=0, value=0, step=1,
                             label_visibility="collapsed", key=f"dur_h_{qid}_{suffix}")
    with col_hlbl:
        st.write("")
        st.markdown("hrs")
    with col_m:
        m = st.number_input("Minutes", min_value=0, max_value=59, value=0, step=1,
                             label_visibility="collapsed", key=f"dur_m_{qid}_{suffix}")
    with col_mlbl:
        st.write("")
        st.markdown("mins")
    return _build_duration_str(h, m)


def render_question(question, suffix="default"):
    if question.metadata.get("table"):
        st.markdown(question.metadata["table"])
    st.subheader(question.question_text)

    if question.metadata.get("diagram") == "two_triangle":
        _render_two_triangle_diagram(
            question.metadata["diagram_params"],
            question.metadata.get("unit", "m"),
        )
    elif question.metadata.get("diagram") == "isosceles_height":
        _render_isosceles_diagram(
            question.metadata["diagram_params"],
            question.metadata.get("unit", "m"),
        )
    elif question.metadata.get("diagram") == "sphere":
        _render_sphere_diagram(
            question.metadata["diagram_params"],
            question.metadata.get("unit", "cm"),
        )
    elif question.metadata.get("diagram") == "cone":
        _render_cone_diagram(
            question.metadata["diagram_params"],
            question.metadata.get("unit", "cm"),
        )
    elif question.metadata.get("diagram") == "cylinder":
        _render_cylinder_diagram(
            question.metadata["diagram_params"],
            question.metadata.get("unit", "cm"),
        )
    elif question.metadata.get("diagram") == "bar_chart":
        _render_bar_chart(question.metadata["diagram_params"])
    elif question.metadata.get("diagram") == "pie_chart":
        _render_pie_chart(question.metadata["diagram_params"])
    elif question.metadata.get("diagram") == "blood_pressure":
        _render_blood_pressure(question.metadata["diagram_params"])
    elif question.metadata.get("diagram") == "ni_bands":
        _render_ni_band_diagram(question.metadata["diagram_params"])

    if question.metadata.get("answer_type") == "duration":
        return _render_duration_input(question.qid, suffix)
    return st.text_input("Your answer", key=f"ans_{question.qid}_{suffix}")


def _render_two_triangle_diagram(p, unit):
    BD, DC, AD, AB, AC = p["BD"], p["DC"], p["AD"], p["AB"], p["AC"]
    find_ac = p["find_ac"]

    B = np.array([0.0, 0.0])
    D = np.array([float(BD), 0.0])
    C = np.array([float(BD + DC), 0.0])
    A = np.array([float(BD), float(AD)])

    total_base = BD + DC
    fig_w = 7
    fig_h = max(3.5, min(6.5, fig_w * AD / total_base * 1.1))
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    # Outer triangle
    tri = plt.Polygon([B, A, C], fill=False, edgecolor="#2c3e50", linewidth=2.5)
    ax.add_patch(tri)

    # Altitude (dashed)
    ax.plot([D[0], A[0]], [D[1], A[1]], color="#666", linestyle="--", linewidth=1.5, zorder=2)

    # Right-angle square at D (between altitude and BC, toward C)
    sq = min(total_base, AD) * 0.055
    rect = patches.Rectangle(
        (BD, 0), sq, sq, fill=False, edgecolor="#666", linewidth=1.2, zorder=3
    )
    ax.add_patch(rect)

    # Height label (h) beside the dashed line
    pad = min(total_base, AD) * 0.09
    ax.text(D[0] + pad * 0.9, AD / 2, "h", fontsize=11, ha="left", va="center", color="#666", style="italic")

    # Label helpers
    base_kw = dict(fontsize=11, ha="center", va="center",
                   bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))
    unk_kw = dict(fontsize=13, ha="center", va="center", color="crimson", fontweight="bold",
                  bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))

    off = min(total_base, AD) * 0.13

    # BD label — below baseline
    ax.text((B[0] + D[0]) / 2, -off * 0.65, f"{BD} {unit}", **base_kw)

    # DC label — below baseline
    ax.text((D[0] + C[0]) / 2, -off * 0.65, f"{DC} {unit}", **base_kw)

    # AB label — outside the triangle, left of AB
    mid_AB = (A + B) / 2
    # Perpendicular to AB pointing left (outside): rotate BA direction 90° CCW
    n_AB = np.array([-float(AD), float(BD)])
    n_AB = n_AB / np.linalg.norm(n_AB) * off
    if find_ac:
        ax.text(mid_AB[0] + n_AB[0], mid_AB[1] + n_AB[1], f"{AB} {unit}", **base_kw)
    else:
        ax.text(mid_AB[0] + n_AB[0], mid_AB[1] + n_AB[1], "?", **unk_kw)

    # AC label — outside the triangle, right of AC
    mid_AC = (A + C) / 2
    # Perpendicular to AC pointing right (outside): left perp of A→C direction
    n_AC = np.array([float(AD), float(DC)])
    n_AC = n_AC / np.linalg.norm(n_AC) * off
    if find_ac:
        ax.text(mid_AC[0] + n_AC[0], mid_AC[1] + n_AC[1], "?", **unk_kw)
    else:
        ax.text(mid_AC[0] + n_AC[0], mid_AC[1] + n_AC[1], f"{AC} {unit}", **base_kw)

    ax.set_aspect("equal")
    ax.autoscale_view()
    xl, yl = ax.get_xlim(), ax.get_ylim()
    margin = min(total_base, AD) * 0.35
    ax.set_xlim(xl[0] - margin, xl[1] + margin)
    ax.set_ylim(yl[0] - margin, yl[1] + margin)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)


def _render_isosceles_diagram(p, unit):
    h, half_base, s = p["h"], p["half_base"], p["s"]
    base = 2 * half_base

    left  = np.array([0.0, 0.0])
    right = np.array([float(base), 0.0])
    mid   = np.array([float(half_base), 0.0])
    apex  = np.array([float(half_base), float(h)])

    fig_w = 7
    fig_h = max(3.5, min(6.5, fig_w * h / base * 1.2))
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    # Triangle outline
    tri = plt.Polygon([left, apex, right], fill=False, edgecolor="#2c3e50", linewidth=2.5)
    ax.add_patch(tri)

    # Height (dashed)
    ax.plot([mid[0], apex[0]], [mid[1], apex[1]], color="#666", linestyle="--", linewidth=1.5, zorder=2)

    # Right-angle square at midpoint of base (toward right)
    sq = min(base, h) * 0.055
    rect = patches.Rectangle(
        (half_base, 0), sq, sq, fill=False, edgecolor="#666", linewidth=1.2, zorder=3
    )
    ax.add_patch(rect)

    off = min(base, h) * 0.13

    base_kw = dict(fontsize=11, ha="center", va="center",
                   bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))
    unk_kw  = dict(fontsize=13, ha="center", va="center", color="crimson", fontweight="bold",
                   bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))

    # Left half-base label
    ax.text(half_base / 2, -off * 0.65, f"{half_base} {unit}", **base_kw)
    # Right half-base label
    ax.text(half_base + half_base / 2, -off * 0.65, f"{half_base} {unit}", **base_kw)

    # Left sloping side — perpendicular offset pointing upper-left (outside)
    mid_L = (left + apex) / 2
    n_L = np.array([-float(h), float(half_base)])
    n_L = n_L / np.linalg.norm(n_L) * off
    ax.text(mid_L[0] + n_L[0], mid_L[1] + n_L[1], f"{s} {unit}", **base_kw)

    # Right sloping side — perpendicular offset pointing upper-right (outside)
    mid_R = (right + apex) / 2
    n_R = np.array([float(h), float(half_base)])
    n_R = n_R / np.linalg.norm(n_R) * off
    ax.text(mid_R[0] + n_R[0], mid_R[1] + n_R[1], f"{s} {unit}", **base_kw)

    # Height label "?" beside the dashed line
    ax.text(half_base + off * 0.8, h / 2, "?", **unk_kw)

    ax.set_aspect("equal")
    ax.autoscale_view()
    xl, yl = ax.get_xlim(), ax.get_ylim()
    margin = min(base, h) * 0.35
    ax.set_xlim(xl[0] - margin, xl[1] + margin)
    ax.set_ylim(yl[0] - margin, yl[1] + margin)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)


def _render_sphere_diagram(p, unit):
    r = p["r"]
    use_diam = p["use_diam"]
    d = p.get("d")

    fig, ax = plt.subplots(figsize=(4, 4))

    # Outer circle
    ax.add_patch(plt.Circle((0, 0), r, fill=False, edgecolor="#2c3e50", linewidth=2.5))

    # Equatorial ellipse: dashed back arc, solid front arc
    ax.add_patch(patches.Arc((0, 0), 2 * r, 0.6 * r,
                              theta1=0, theta2=180,
                              edgecolor="#999", linewidth=1.2, linestyle="--"))
    ax.add_patch(patches.Arc((0, 0), 2 * r, 0.6 * r,
                              theta1=180, theta2=360,
                              edgecolor="#666", linewidth=1.5))

    lbl_kw = dict(fontsize=11, ha="center", va="center",
                  bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))

    if use_diam:
        ax.annotate("", xy=(r, 0), xytext=(-r, 0),
                    arrowprops=dict(arrowstyle="<->", color="#2c3e50", lw=1.5))
        ax.text(0, r * 0.22, f"{d} {unit}", **lbl_kw)
    else:
        ax.plot([0, r], [0, 0], color="#2c3e50", linewidth=1.8)
        ax.plot(0, 0, "o", color="#2c3e50", markersize=4)
        ax.text(r / 2, r * 0.18, f"{r:g} {unit}", **lbl_kw)

    margin = r * 0.35
    ax.set_xlim(-r - margin, r + margin)
    ax.set_ylim(-r - margin, r + margin)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)


def _render_cone_diagram(p, unit):
    r = p["r"]
    h = p["h"]
    use_diam = p["use_diam"]
    d = p.get("d")

    # Normalised visual coordinates so the cone always looks proportional
    vr, vh, ey = 1.0, 2.0, 0.28

    fig, ax = plt.subplots(figsize=(4, 4.5))

    # Base ellipse: dashed back arc, solid front arc
    ax.add_patch(patches.Arc((0, 0), 2 * vr, 2 * ey,
                              theta1=0, theta2=180,
                              edgecolor="#999", linewidth=1.2, linestyle="--"))
    ax.add_patch(patches.Arc((0, 0), 2 * vr, 2 * ey,
                              theta1=180, theta2=360,
                              edgecolor="#2c3e50", linewidth=2))

    # Sloping sides
    ax.plot([-vr, 0], [0, vh], color="#2c3e50", linewidth=2.5, zorder=3)
    ax.plot([vr, 0], [0, vh], color="#2c3e50", linewidth=2.5, zorder=3)

    # Height dashed line
    ax.plot([0, 0], [0, vh], color="#666", linestyle="--", linewidth=1.5, zorder=2)

    # Right-angle square at base of height
    sq = 0.1
    ax.add_patch(patches.Rectangle((0, 0), sq, sq, fill=False,
                                    edgecolor="#666", linewidth=1.2, zorder=4))

    lbl_kw = dict(fontsize=11, ha="center", va="center",
                  bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))

    ax.text(0.22, vh / 2, f"h = {h:g} {unit}", ha="left", va="center", fontsize=11,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))

    if use_diam:
        ax.annotate("", xy=(vr, -ey * 1.6), xytext=(-vr, -ey * 1.6),
                    arrowprops=dict(arrowstyle="<->", color="#2c3e50", lw=1.5))
        ax.text(0, -ey * 3.0, f"d = {d:g} {unit}", **lbl_kw)
    else:
        ax.plot([0, vr], [-ey * 0.4, -ey * 0.4], color="#2c3e50", linewidth=1.8)
        ax.plot(0, 0, "o", color="#2c3e50", markersize=3)
        ax.text(vr / 2, -ey * 1.6, f"r = {r:g} {unit}", **lbl_kw)

    ax.set_xlim(-vr * 1.7, vr * 2.1)
    ax.set_ylim(-ey * 5, vh * 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)


def _render_cylinder_diagram(p, unit):
    r = p["r"]
    h = p["h"]
    use_diam = p["use_diam"]
    d = p.get("d")

    # Normalised visual coordinates
    vr, vh, ey = 1.0, 2.5, 0.3

    fig, ax = plt.subplots(figsize=(4, 5))

    # Bottom ellipse (full solid — entirely visible)
    ax.add_patch(patches.Ellipse((0, 0), 2 * vr, 2 * ey, fill=False,
                                  edgecolor="#2c3e50", linewidth=2))

    # Top ellipse: dashed back arc, solid front arc
    ax.add_patch(patches.Arc((0, vh), 2 * vr, 2 * ey,
                              theta1=0, theta2=180,
                              edgecolor="#999", linewidth=1.2, linestyle="--"))
    ax.add_patch(patches.Arc((0, vh), 2 * vr, 2 * ey,
                              theta1=180, theta2=360,
                              edgecolor="#2c3e50", linewidth=2))

    # Side lines
    ax.plot([-vr, -vr], [0, vh], color="#2c3e50", linewidth=2.5, zorder=3)
    ax.plot([vr, vr], [0, vh], color="#2c3e50", linewidth=2.5, zorder=3)

    lbl_kw = dict(fontsize=11, ha="center", va="center",
                  bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))

    # Height double-headed arrow on the right
    hx = vr * 1.5
    ax.annotate("", xy=(hx, vh), xytext=(hx, 0),
                arrowprops=dict(arrowstyle="<->", color="#555", lw=1.2))
    ax.text(hx + 0.2, vh / 2, f"h = {h:g} {unit}", ha="left", va="center", fontsize=11)

    # Radius / diameter label on top face
    if use_diam:
        ax.annotate("", xy=(vr, vh + ey * 1.3), xytext=(-vr, vh + ey * 1.3),
                    arrowprops=dict(arrowstyle="<->", color="#2c3e50", lw=1.5))
        ax.text(0, vh + ey * 2.6, f"d = {d:g} {unit}", **lbl_kw)
    else:
        ax.plot([0, vr], [vh + ey * 0.2, vh + ey * 0.2], color="#2c3e50", linewidth=1.8)
        ax.plot(0, vh, "o", color="#2c3e50", markersize=3)
        ax.text(vr / 2, vh + ey * 1.6, f"r = {r:g} {unit}", **lbl_kw)

    ax.set_xlim(-vr * 1.5, vr * 3.2)
    ax.set_ylim(-ey * 2.5, vh + ey * 4.5)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)


def _render_bar_chart(p):
    categories = p["categories"]
    g1 = p["group1_data"]
    g2 = p["group2_data"]
    g1_name = p["group1_name"]
    g2_name = p["group2_name"]

    x = np.arange(len(categories))
    width = 0.38

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - width / 2, g1, width, label=g1_name, color="#2c3e50")
    ax.bar(x + width / 2, g2, width, label=g2_name, color="#95a5a6")

    max_val = max(max(g1), max(g2))
    ax.set_ylim(0, max_val + 5)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_xlabel(p.get("x_label", "Category"), fontsize=11)
    ax.set_ylabel(p.get("y_label", "Frequency"), fontsize=11)
    ax.set_title(p.get("title", "Bar Chart"), fontsize=13, fontweight="bold")
    ax.legend(loc="upper right")
    ax.yaxis.set_major_locator(plt.MultipleLocator(5))
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)


def _render_pie_chart(p):
    categories = p["categories"]
    angles = p["angles"]
    ref_cat = p["ref_cat"]
    ref_count = p["ref_count"]
    ask_cat = p["ask_cat"]

    colors = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6", "#1abc9c"][:len(categories)]

    fig, ax = plt.subplots(figsize=(7, 5))
    wedges, _ = ax.pie(
        angles,
        labels=categories,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )

    for wedge, angle in zip(wedges, angles):
        theta = np.radians((wedge.theta1 + wedge.theta2) / 2)
        r = 0.6
        ax.text(r * np.cos(theta), r * np.sin(theta), f"{angle}°",
                ha="center", va="center", fontsize=10, fontweight="bold", color="white")

    ax.set_title(
        f"Given: {ref_count} people chose {ref_cat}   |   Find: how many chose {ask_cat}",
        fontsize=10, pad=12,
    )
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)


def _render_blood_pressure(p):
    systolic = p["systolic"]
    diastolic = p["diastolic"]

    fig, ax = plt.subplots(figsize=(6, 6))

    # Red background (high blood pressure — whole chart)
    ax.add_patch(patches.Rectangle((40, 70), 60, 120, facecolor="#e74c3c", alpha=0.6, zorder=1))

    # Pre-high (yellow): diastolic 80–90, systolic 120–140
    ax.add_patch(patches.Rectangle((80, 120), 10, 20, facecolor="#f39c12", alpha=0.9, zorder=2))
    ax.text(85, 130, "Pre-high\nblood\npressure", ha="center", va="center",
            fontsize=7, zorder=5, color="black")

    # Ideal (green): diastolic 60–80, systolic 90–120
    ax.add_patch(patches.Rectangle((60, 90), 20, 30, facecolor="#27ae60", alpha=0.9, zorder=2))
    ax.text(70, 105, "Ideal\nblood\npressure", ha="center", va="center",
            fontsize=7, zorder=5, color="white")

    # Low (purple): diastolic 40–60, systolic 70–90
    ax.add_patch(patches.Rectangle((40, 70), 20, 20, facecolor="#8e44ad", alpha=0.9, zorder=2))
    ax.text(50, 80, "Low", ha="center", va="center", fontsize=8, zorder=5, color="white")

    ax.text(90, 170, "High blood pressure", ha="center", va="center",
            fontsize=9, color="white", zorder=5, fontweight="bold")

    # Mark the reading
    ax.plot(diastolic, systolic, "ko", markersize=10, zorder=10)
    ax.plot(diastolic, systolic, "wo", markersize=5, zorder=11)
    ax.axhline(systolic, color="black", linestyle="--", linewidth=0.8, alpha=0.5, zorder=6)
    ax.axvline(diastolic, color="black", linestyle="--", linewidth=0.8, alpha=0.5, zorder=6)

    ax.set_xlim(40, 100)
    ax.set_ylim(70, 190)
    ax.set_xlabel("Diastolic", fontsize=12)
    ax.set_ylabel("Systolic", fontsize=12)
    ax.set_title("Blood Pressure Chart", fontsize=13, fontweight="bold")
    ax.xaxis.set_major_locator(plt.MultipleLocator(10))
    ax.yaxis.set_major_locator(plt.MultipleLocator(10))
    ax.grid(True, linestyle="--", alpha=0.3, zorder=0)

    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)


def _render_ni_band_diagram(p):
    income = p["income"]
    PT = 12_570
    UEL = 50_270

    vis_max = max(income * 1.12, UEL * 1.35)

    color_low = "#888780"
    color_mid = "#378ADD"
    color_top = "#E24B4A"

    bar_l, bar_r = 0.0, 0.5
    bar_w = bar_r - bar_l

    fig, ax = plt.subplots(figsize=(5.5, 5))

    # Background bar (unfilled portion)
    ax.add_patch(patches.Rectangle(
        (bar_l, 0), bar_w, vis_max,
        facecolor="#f5f5f5", edgecolor="#ccc", linewidth=1, zorder=1
    ))

    # Fill each band up to income level
    ax.add_patch(patches.Rectangle(
        (bar_l, 0), bar_w, min(income, PT),
        facecolor=color_low, edgecolor="none", zorder=2
    ))
    if income > PT:
        ax.add_patch(patches.Rectangle(
            (bar_l, PT), bar_w, min(income, UEL) - PT,
            facecolor=color_mid, edgecolor="none", zorder=2
        ))
    if income > UEL:
        ax.add_patch(patches.Rectangle(
            (bar_l, UEL), bar_w, income - UEL,
            facecolor=color_top, edgecolor="none", zorder=2
        ))

    # Dashed threshold lines
    for thresh in (PT, UEL):
        ax.plot([bar_l, bar_r], [thresh, thresh],
                color="#222", linestyle="--", linewidth=1.5, zorder=3)

    # Income marker line
    ax.plot([bar_l, bar_r], [income, income],
            color="#111", linewidth=2.5, zorder=4)

    # £ labels to the left of the bar
    min_gap = vis_max * 0.035
    for val in (PT, UEL):
        ax.text(-0.04, val, f"£{val:,}",
                ha="right", va="center", fontsize=8.5, color="#444")
    if not any(abs(income - v) < min_gap for v in (PT, UEL)):
        ax.text(-0.04, income, f"£{income:,}",
                ha="right", va="center", fontsize=9, fontweight="bold", color="#111")

    # Band labels (coloured square marker + rate + range) to the right
    lbl_x = bar_r + 0.12
    offset = vis_max * 0.045
    for y_c, color, rate, rng in [
        ((UEL + vis_max) / 2, color_top, "2%",  "above £50,270"),
        ((PT + UEL) / 2,      color_mid, "12%", "£12,570–£50,270"),
        (PT / 2,              color_low, "0%",  "first £12,570"),
    ]:
        ax.plot(lbl_x, y_c, "s", color=color, markersize=10, zorder=5,
                markeredgecolor="none")
        ax.text(lbl_x + 0.08, y_c + offset * 0.3,
                rate, ha="left", va="center", fontsize=12, fontweight="bold", color="#111")
        ax.text(lbl_x + 0.08, y_c - offset * 0.7,
                rng, ha="left", va="center", fontsize=9, color="#555")

    ax.set_xlim(-0.35, 1.7)
    ax.set_ylim(-vis_max * 0.04, vis_max * 1.04)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)
