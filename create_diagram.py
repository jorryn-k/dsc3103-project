
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

Path("docs").mkdir(exist_ok=True)

fig, ax = plt.subplots(figsize=(11, 4.5))
ax.set_xlim(0, 11)
ax.set_ylim(0, 5)
ax.axis("off")

components = [
    ("Producer", "Generates price events", 0.4),
    ("Broker", "JSONL event log", 3.1),
    ("Consumer", "Validates, deduplicates,\nprocesses windows", 5.8),
    ("Sink", "Window counts and\nmean prices", 8.5),
]

for title, description, x in components:
    rect = FancyBboxPatch(
        (x, 2.0), 2.1, 1.1,
        boxstyle="round,pad=0.12",
        linewidth=1.5,
        edgecolor="black",
        facecolor="white"
    )
    ax.add_patch(rect)
    ax.text(x + 1.05, 2.7, title,
            ha="center", va="center",
            fontsize=12, fontweight="bold")
    ax.text(x + 1.05, 2.3, description,
            ha="center", va="center", fontsize=9)

for x in [2.5, 5.2, 7.9]:
    ax.add_patch(FancyArrowPatch(
        (x, 2.55), (x + 0.55, 2.55),
        arrowstyle="->", mutation_scale=18,
        linewidth=1.5, color="black"
    ))

ax.text(6.85, 1.25,
        "Late events -> late_events.jsonl",
        ha="center", fontsize=10)

ax.text(6.85, 0.8,
        "Duplicate events -> duplicate_events.jsonl",
        ha="center", fontsize=10)

ax.set_title(
    "Lab 09: Streaming Data Architecture",
    fontsize=15, fontweight="bold", pad=15
)

plt.savefig(
    "docs/stream_architecture.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()
print("Diagram saved to docs/stream_architecture.png")
