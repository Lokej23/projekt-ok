import argparse
import os
from typing import List, Optional

import matplotlib.pyplot as plt

from tsp_utils import eprint, loadJson


def _compute_cap(times: List[float], statuses: List[str], user_cap: Optional[float]) -> Optional[float]:
    if user_cap is not None:
        return max(user_cap, 0.0)

    non_sat_times = [t for t, s in zip(times, statuses) if s != "SATISFIED"]
    non_sat_times = [t for t in non_sat_times if isinstance(t, (int, float))]

    if not non_sat_times:
        return None

    return max(non_sat_times) * 1.1


def plot_mzn_summary(json_file: str, output_path: str, cap_satisfied: Optional[float]) -> None:
    if not os.path.exists(json_file):
        eprint(f"Błąd: Nie znaleziono pliku {json_file}")
        return

    data = loadJson(json_file)
    data.sort(key=lambda x: x.get("n", 0))

    ns = [d.get("n", 0) for d in data]
    times = [d.get("minizinc", {}).get("time", 0.0) for d in data]
    statuses = [d.get("minizinc", {}).get("status", "UNKNOWN") for d in data]

    cap = _compute_cap(times, statuses, cap_satisfied)

    colors = []
    plot_times = []
    clipped = []
    for t, status in zip(times, statuses):
        is_satisfied = status == "SATISFIED"
        colors.append("red" if is_satisfied else "steelblue")

        if is_satisfied and cap is not None:
            plot_times.append(min(t, cap))
            clipped.append(t > cap)
        else:
            plot_times.append(t)
            clipped.append(False)

    plt.style.use("seaborn-v0_8-whitegrid")
    plt.figure(figsize=(10, 6))
    bars = plt.bar(ns, plot_times, color=colors)

    ax = plt.gca()
    max_height = max(plot_times) if plot_times else 0.0
    offset = max(0.02 * max_height, 0.1)

    for bar, is_clipped in zip(bars, clipped):
        if is_clipped:
            bar.set_hatch("//")
            bar.set_edgecolor("black")

    for bar, original_time in zip(bars, times):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + offset,
            f"{original_time:.3f}s",
            ha="center",
            va="bottom",
            fontsize=8,
            rotation=0,
        )

    plt.xlabel("Liczba miast (n)")
    plt.ylabel("Czas wykonania [s]")

    if ns:
        tick_start = min(ns)
        tick_end = max(ns)
        plt.xticks(range(tick_start, tick_end + 1, 2))
    title = "MiniZinc: czas wykonania"
    plt.title(title)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    eprint(f"Wygenerowano wykres: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wykres wyników MiniZinc z oznaczeniem SATISFIED")
    parser.add_argument("-d", "--data", required=True, help="Plik JSON z wynikami zbiorczymi")
    parser.add_argument("-o", "--output", default="data/tmp_mzn_plot.png", help="Ścieżka wyjściowa wykresu")
    parser.add_argument(
        "--cap-satisfied",
        type=float,
        default=None,
        help="Ręczny limit przycięcia słupków SATISFIED (sekundy). Domyślnie auto.",
    )
    args = parser.parse_args()

    plot_mzn_summary(args.data, args.output, args.cap_satisfied)
