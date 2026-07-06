import cv2
import numpy as np

# --- Input array ---
np.random.seed(42)
rows = 12
cols = 24
array = np.random.randint(0, 2, size=(rows, cols))

# --- Canvas ---
W, H = 900, 900
img = np.zeros((H, W, 3), dtype=np.uint8)
img[:] = (40, 40, 40)

cx, cy = W // 2, H // 2
f = 600
cam_dist = 5.5

def project(x, y, z):
    rx = x
    ry = z
    rz = cam_dist - y
    if rz <= 0.01:
        return None
    px = int(cx + f * rx / rz)
    py = int(cy - f * ry / rz)
    return (px, py)

def draw_curve(points_3d, color, thickness=1):
    pts = [project(*p) for p in points_3d]
    pts = [p for p in pts if p is not None]
    for i in range(len(pts) - 1):
        cv2.line(img, pts[i], pts[i+1], color, thickness)

def fill_quad(t0, t1, z0, z1, color, border_color=None):
    steps = 10
    thetas = np.linspace(t0, t1, steps)
    overlay = img.copy()
    for i in range(len(thetas) - 1):
        pts_3d = [
            (r * np.cos(thetas[i]),   r * np.sin(thetas[i]),   z0),
            (r * np.cos(thetas[i+1]), r * np.sin(thetas[i+1]), z0),
            (r * np.cos(thetas[i+1]), r * np.sin(thetas[i+1]), z1),
            (r * np.cos(thetas[i]),   r * np.sin(thetas[i]),   z1),
        ]
        proj = [project(*p) for p in pts_3d]
        if any(p is None for p in proj):
            continue
        pts_np = np.array(proj, dtype=np.int32)
        cv2.fillPoly(overlay, [pts_np], color)
    cv2.addWeighted(overlay, 0.85, img, 0.15, 0, img)

    if border_color:
        n = 20
        rt = np.linspace(t0, t1, n)
        rz = np.linspace(z0, z1, n)
        draw_curve([(r*np.cos(t), r*np.sin(t), z0) for t in rt], border_color, 1)
        draw_curve([(r*np.cos(t), r*np.sin(t), z1) for t in rt], border_color, 1)
        draw_curve([(r*np.cos(t0), r*np.sin(t0), z) for z in rz], border_color, 1)
        draw_curve([(r*np.cos(t1), r*np.sin(t1), z) for z in rz], border_color, 1)

# --- Cylinder parameters ---
r       = 1.0
cyl_h   = 3.5
z_start = -cyl_h / 2
z_end   =  cyl_h / 2

thetas = np.linspace(0, 2 * np.pi, cols + 1)
zs     = np.linspace(z_start, z_end, rows + 1)

# --- Cylinder shading ---
for t in np.linspace(0, 2 * np.pi, 60):
    x, y = r * np.cos(t), r * np.sin(t)
    p1 = project(x, y, z_start)
    p2 = project(x, y, z_end)
    if p1 and p2:
        light = int(30 + 40 * abs(np.cos(t)))
        cv2.line(img, p1, p2, (light, light, light), 1)

# Top and bottom circles
for z_val in [z_start, z_end]:
    pts = [(r*np.cos(t), r*np.sin(t), z_val)
           for t in np.linspace(0, 2*np.pi, 120)]
    draw_curve(pts, (100, 100, 100), 2)

# --- Draw squares ---
for row in range(rows):
    for col in range(cols):
        t0 = thetas[col]
        t1 = thetas[col + 1]
        z0 = zs[row]
        z1 = zs[row + 1]

        t_mid = (t0 + t1) / 2
        y_mid = r * np.sin(t_mid)
        if y_mid > 0.15:   # facing away from camera (behind cylinder)
            continue

        val = array[row, col]
        if val == 0:
            fill_color   = (220, 220, 220)
            border_color = (80, 80, 80)
        else:
            fill_color   = (20, 20, 20)
            border_color = (120, 120, 120)

        fill_quad(t0, t1, z0, z1, fill_color, border_color)

# Redraw circles on top
for z_val in [z_start, z_end]:
    pts = [(r*np.cos(t), r*np.sin(t), z_val)
           for t in np.linspace(0, 2*np.pi, 120)]
    draw_curve(pts, (160, 160, 160), 2)

# --- Legend & info ---
cv2.putText(img, "0 = White  |  1 = Black", (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (200, 200, 200), 2)
cv2.putText(img, f"Array: {rows} rings x {cols} squares", (30, 90),
            cv2.FONT_HERSHEY_SIMPLEX, 0.65, (160, 160, 160), 1)
cv2.putText(img, "OpenCV only", (30, H - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (120, 120, 120), 1)

cv2.imwrite('cylinder_rings_opencv-3.png', img)
print("Saved!")