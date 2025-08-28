#!/usr/bin/env python3
"""
rose_draw.py — Animate drawing a rose curve and show progress.

Run:
  python rose_draw.py                 # default 7-petal animation
  python rose_draw.py --k 5 --a 1.5   # 5 petals, larger
  python rose_draw.py --speed 1.5      # faster animation
  python rose_draw.py --save out.gif   # also save animation to a GIF

Notes:
- If k is odd -> k petals; if k is even -> 2k petals.
- Requires: numpy, matplotlib, pillow (only if saving GIF).
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate_rose(k: int = 7, a: float = 1.0, points: int = 3000, speed: float = 1.0, save: str | None = None):
    # Prepare data
    theta = np.linspace(0, 2*np.pi, points)
    r = a * np.cos(k * theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Figure
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.set_xlim(-a-0.1, a+0.1)
    ax.set_ylim(-a-0.1, a+0.1)
    ax.axis('off')

    # Draw partial line that grows
    (line,) = ax.plot([], [], linewidth=3)
    pct_text = ax.text(0.02, 0.96, "0%", transform=ax.transAxes, fontsize=12, ha="left", va="top")

    # Background faint full path (optional guide)
    ax.plot(x, y, alpha=0.08)

    # Number of frames (speed scales how many points we reveal each frame)
    base_frames = 240  # looks smooth; ~8s at 30fps
    frames = max(60, int(base_frames / max(0.1, speed)))
    idx_per_frame = max(1, len(x) // frames)

    def init():
        line.set_data([], [])
        pct_text.set_text("0%")
        return (line, pct_text)

    def update(frame):
        i = min(len(x), (frame + 1) * idx_per_frame)
        line.set_data(x[:i], y[:i])
        pct = int(100 * i / len(x))
        pct_text.set_text(f"{pct}%")
        fig.canvas.manager.set_window_title(f"Rose Drawing — {pct}%")
        return (line, pct_text)

    anim = FuncAnimation(fig, update, frames=frames, init_func=init, interval=33, blit=True, repeat=False)

    if save:
        try:
            # Try to save as GIF using Pillow writer
            anim.save(save, writer="pillow", fps=30)
            print(f"Saved animation to {save}")
        except Exception as e:
            print("Could not save GIF:", e)

    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Animate drawing a rose curve with progress.")
    parser.add_argument("--k", type=int, default=7, help="Rose parameter k (odd=k petals, even=2k petals). Default: 7")
    parser.add_argument("--a", type=float, default=1.0, help="Scale (size) of the rose. Default: 1.0")
    parser.add_argument("--speed", type=float, default=1.0, help="Speed multiplier (>1 faster, <1 slower). Default: 1.0")
    parser.add_argument("--points", type=int, default=3000, help="Number of points along the curve. Default: 3000")
    parser.add_argument("--save", type=str, default=None, help="Optional path to save a GIF of the animation (e.g., out.gif)")
    args = parser.parse_args()

    animate_rose(k=args.k, a=args.a, points=args.points, speed=args.speed, save=args.save)

if __name__ == "__main__":
    main()
