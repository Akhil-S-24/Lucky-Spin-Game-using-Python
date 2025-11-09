import tkinter as tk
import random
import math

# -------------------------------
# 🎯 LUCKY SPIN GAME WITH WIN MARKER
# -------------------------------
root = tk.Tk()
root.title("🎯 Lucky Spin Game (with Win Marker)")
root.geometry("440x580")
root.config(bg="#1e1e2f")


sectors = [
    ("🎁 100", 100),
    ("🎉 Try Again", 0),
    ("💎 500", 500),
    ("💰 1000", 1000),
    ("😞 0", 0),
    ("⭐ Bonus 200", 200)
]

sector_count = len(sectors)
sector_angle = 360 / sector_count
colors = ["#ff595e", "#ffca3a", "#8ac926", "#1982c4", "#6a4c93", "#ff924c"]

score = 0
current_angle = 0.0 


title_label = tk.Label(root, text="🎡 LUCKY SPIN 🎡", font=("Helvetica", 22, "bold"),
                       bg="#1e1e2f", fg="#00ffcc")
title_label.pack(pady=12)

canvas_size = 360
canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="#2b2b3d", highlightthickness=0)
canvas.pack()


def draw_marker():
    cx = canvas_size // 2
    pointer = canvas.create_polygon(
        cx - 15, 10,   # left point
        cx + 15, 10,   # right point
        cx, 35,        # bottom point
        fill="white", outline="#00ffcc", width=2, tags="marker"
    )
    canvas.create_text(cx, 50, text="⬇ WIN HERE ⬇", fill="#00ffcc", font=("Arial", 10, "bold"), tags="marker")


result_label = tk.Label(root, text="Press SPIN to Start!", font=("Helvetica", 16, "bold"),
                        bg="#1e1e2f", fg="white")
result_label.pack(pady=15)

score_label = tk.Label(root, text=f"Your Score: {score}", font=("Helvetica", 14),
                       bg="#1e1e2f", fg="#00ffcc")
score_label.pack()


def draw_wheel(angle_deg):
    canvas.delete("wheel")
    cx, cy = canvas_size // 2, canvas_size // 2
    r_outer = canvas_size // 2 - 10
    r_inner = 70

    for i, (label, pts) in enumerate(sectors):
        start = angle_deg + i * sector_angle
        canvas.create_arc(10, 10, canvas_size - 10, canvas_size - 10,
                          start=start, extent=sector_angle,
                          fill=colors[i % len(colors)], outline="black", tags="wheel")

  
    canvas.create_oval(cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner,
                       fill="#222", outline="#00ffcc", width=3, tags="wheel")
    canvas.create_text(cx, cy, text="SPIN", font=("Arial", 12, "bold"), fill="white", tags="wheel")

  
  
    for i, (label, pts) in enumerate(sectors):
        mid_angle = math.radians(angle_deg + i * sector_angle + sector_angle / 2 - 90)
        text_r = (r_outer + r_inner) / 2
        tx = cx + text_r * math.cos(mid_angle)
        ty = cy + text_r * math.sin(mid_angle)
        canvas.create_text(tx, ty, text=label, font=("Arial", 10, "bold"), tags="wheel")



def sector_at_top(final_angle_deg):
    pointer_deg = 90  # 12 o’clock
    for i in range(sector_count):
        center_angle = (final_angle_deg + i * sector_angle + sector_angle / 2) % 360
        diff = (center_angle - pointer_deg + 540) % 360 - 180
        if abs(diff) <= sector_angle / 2:
            return i
    return 0



def spin_animation(start_angle, total_rotation, duration_ms=4200):
    frames = max(1, duration_ms // 20)
    def frame_func(frame):
        t = frame / frames
        ease = 1 - (1 - t) ** 3  # ease-out cubic
        angle = start_angle + total_rotation * ease
        draw_wheel(angle)
        draw_marker()
        if frame < frames:
            root.after(20, lambda: frame_func(frame + 1))
        else:
            final_angle = (start_angle + total_rotation) % 360
            idx = sector_at_top(final_angle)
            label, pts = sectors[idx]
            apply_result(label, pts)
            spin_button.config(state="normal")
    frame_func(0)

def apply_result(label, points):
    global score
    score += points
    result_label.config(
        text=f"🎉 You got: {label}   (+{points} pts)" if points else f"😞 You got: {label}"
    )
    score_label.config(text=f"Your Score: {score}")


def spin_wheel():
    spin_button.config(state="disabled")
    global current_angle
    target_idx = random.randrange(sector_count)
    sector_center = target_idx * sector_angle + sector_angle / 2
    desired_final_angle = (90 - sector_center) % 360
    current_mod = current_angle % 360
    needed = (desired_final_angle - current_mod) % 360
    total_rotation = random.randint(5, 7) * 360 + needed
    spin_animation(current_angle, total_rotation, duration_ms=random.randint(3800, 5000))
    current_angle += total_rotation


def reset_game():
    global score, current_angle
    score = 0
    current_angle = 0.0
    result_label.config(text="Press SPIN to Start!", fg="white")
    score_label.config(text=f"Your Score: {score}")
    draw_wheel(current_angle)
    draw_marker()


btn_frame = tk.Frame(root, bg="#1e1e2f")
btn_frame.pack(pady=14)

spin_button = tk.Button(btn_frame, text="🎯 SPIN", font=("Helvetica", 16, "bold"),
                        bg="#00ffcc", fg="black", width=12, command=spin_wheel)
spin_button.grid(row=0, column=0, padx=8, pady=4)

reset_button = tk.Button(btn_frame, text="🔁 RESET", font=("Helvetica", 12),
                         bg="#444", fg="white", width=12, command=reset_game)
reset_button.grid(row=0, column=1, padx=8, pady=4)

exit_button = tk.Button(root, text="❌ EXIT", font=("Helvetica", 12),
                        bg="#ff4d4d", fg="white", width=28, command=root.destroy)
exit_button.pack(pady=8)


draw_wheel(current_angle)
draw_marker()

root.mainloop()
