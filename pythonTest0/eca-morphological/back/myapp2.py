import cv2
import numpy as np

# --- Canvas ---
W, H = 800, 800
img = np.zeros((H, W, 3), dtype=np.uint8)
img[:] = (30, 30, 30)  # dark background

# --- Camera / projection settings ---
cx, cy = W // 2, H // 2   # image center
f = 600                    # focal length (zoom)
cam_dist = 5               # camera distance from cylinder axis

def project(x, y, z):
    """Simple perspective projection (camera on +Y axis looking at origin)"""
    # Rotate scene: camera is at (0, cam_dist, 0) looking at origin
    rx = x
    ry = z
    rz = cam_dist - y   # depth
    if rz <= 0:
        return None
    px = int(cx + f * rx / rz)
    py = int(cy - f * ry / rz)
    return (px, py)

def draw_curve(points_3d, color, thickness=2):
    pts = [project(*p) for p in points_3d]
    pts = [p for p in pts if p is not None]
    for i in range(len(pts) - 1):
        cv2.line(img, pts[i], pts[i+1], color, thickness)

def fill_quad_surface(theta_range, z_range, color, alpha=0.5):
    """Fill rectangle on cylinder surface using filled polygons strip by strip"""
    overlay = img.copy()
    steps = 40
    thetas = np.linspace(theta_range[0], theta_range[1], steps)
    zs = np.linspace(z_range[0], z_range[1], steps)
    for i in range(len(thetas) - 1):
        for j in range(len(zs) - 1):
            pts_3d = [
                (r * np.cos(thetas[i]),   r * np.sin(thetas[i]),   zs[j]),
                (r * np.cos(thetas[i+1]), r * np.sin(thetas[i+1]), zs[j]),
                (r * np.cos(thetas[i+1]), r * np.sin(thetas[i+1]), zs[j+1]),
                (r * np.cos(thetas[i]),   r * np.sin(thetas[i]),   zs[j+1]),
            ]
            proj = [project(*p) for p in pts_3d]
            if any(p is None for p in proj):
                continue
            pts_np = np.array(proj, dtype=np.int32)
            cv2.fillPoly(overlay, [pts_np], color)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

# --- Cylinder parameters ---
r = 1.0
h = 3.0
n = 80

# Draw cylinder surface as vertical lines
for t in np.linspace(0, 2 * np.pi, 40):
    x, y = r * np.cos(t), r * np.sin(t)
    p1 = project(x, y, -h/2)
    p2 = project(x, y,  h/2)
    if p1 and p2:
        # Shade based on angle (lighting simulation)
        light = int(60 + 80 * abs(np.cos(t)))
        cv2.line(img, p1, p2, (light, light, light), 1)

# Draw top and bottom ellipses
for z_val in [-h/2, h/2]:
    pts = [(r * np.cos(t), r * np.sin(t), z_val)
           for t in np.linspace(0, 2*np.pi, 100)]
    draw_curve(pts, (150, 150, 150), 2)

# --- Rectangle 1: RED (front, visible side) ---
t1, t2 = np.radians(-70), np.radians(70)
z1, z2 = -0.8, 0.8
fill_quad_surface((t1, t2), (z1, z2), (0, 0, 200), alpha=0.65)

# Border edges
n_pts = 60
rt = np.linspace(t1, t2, n_pts)
rz = np.linspace(z1, z2, n_pts)
draw_curve([(r*np.cos(t), r*np.sin(t), z1) for t in rt], (0, 0, 255), 3)  # bottom
draw_curve([(r*np.cos(t), r*np.sin(t), z2) for t in rt], (0, 0, 255), 3)  # top
draw_curve([(r*np.cos(t1), r*np.sin(t1), z) for z in rz], (0, 0, 255), 3) # left
draw_curve([(r*np.cos(t2), r*np.sin(t2), z) for z in rz], (0, 0, 255), 3) # right

# --- Rectangle 2: GREEN (side, partial visibility) ---
t3, t4 = np.radians(100), np.radians(200)
z3, z4 = -1.0, 0.2
fill_quad_surface((t3, t4), (z3, z4), (0, 150, 0), alpha=0.55)

rt2 = np.linspace(t3, t4, n_pts)
rz2 = np.linspace(z3, z4, n_pts)
draw_curve([(r*np.cos(t), r*np.sin(t), z3) for t in rt2], (0, 255, 0), 3)
draw_curve([(r*np.cos(t), r*np.sin(t), z4) for t in rt2], (0, 255, 0), 3)
draw_curve([(r*np.cos(t3), r*np.sin(t3), z) for z in rz2], (0, 255, 0), 3)
draw_curve([(r*np.cos(t4), r*np.sin(t4), z) for z in rz2], (0, 255, 0), 3)

# --- Labels ---
cv2.putText(img, "Rectangle 1 (Red)", (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (80, 80, 255), 2)
cv2.putText(img, "Rectangle 2 (Green)", (30, 90),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (80, 255, 80), 2)
cv2.putText(img, "OpenCV only - Cylinder Surface", (30, H - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)

cv2.imwrite('cylinder2_opencv.png', img)
print("Done!")