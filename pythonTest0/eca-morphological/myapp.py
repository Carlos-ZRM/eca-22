import cv2
import numpy as np

# --- Input array ---
np.random.seed(42)
rows = 12
cols = 24
array = np.random.randint(0, 2, size=(rows, cols))

# ============================================================
#  CAMERA CONTROLS  ← change these
# ============================================================
AZIMUTH     =  45.0   # horizontal rotation around cylinder (degrees)
ELEVATION   =  30.0   # vertical tilt / inclination (degrees)
CAM_DIST    =  5.5    # distance from cylinder
FOCAL       =  600    # zoom / focal length
# ============================================================

# --- Canvas ---
W, H = 900, 900
img = np.zeros((H, W, 3), dtype=np.uint8)
img[:] = (40, 40, 40)

cx, cy = W // 2, H // 2

az  = np.radians(AZIMUTH)
el  = np.radians(ELEVATION)

# Camera position in 3D
cam_x = CAM_DIST * np.cos(el) * np.sin(az)
cam_y = CAM_DIST * np.cos(el) * np.cos(az)
cam_z = CAM_DIST * np.sin(el)

# Build camera axes
fwd = np.array([-cam_x, -cam_y, -cam_z])
fwd /= np.linalg.norm(fwd)
world_up = np.array([0, 0, 1])
right = np.cross(fwd, world_up)
right_n = np.linalg.norm(right)
if right_n < 1e-6:
    world_up = np.array([0, 1, 0])
    right = np.cross(fwd, world_up)
right /= np.linalg.norm(right)
up = np.cross(right, fwd)
up /= np.linalg.norm(up)

def project(x, y, z):
    dx = x - cam_x
    dy = y - cam_y
    dz = z - cam_z
    depth = -(dx*fwd[0] + dy*fwd[1] + dz*fwd[2])
    if depth <= 0.01:
        return None
    rx =  dx*right[0] + dy*right[1] + dz*right[2]
    ry =  dx*up[0]    + dy*up[1]    + dz*up[2]
    px = int(cx + FOCAL * rx / depth)
    py = int(cy - FOCAL * ry / depth)
    return (px, py)

def is_facing_camera(t_mid):
    """Check if surface normal points toward camera."""
    nx = np.cos(t_mid)
    ny = np.sin(t_mid)
    to_cam_x = cam_x - r * nx
    to_cam_y = cam_y - r * ny
    dot = nx * to_cam_x + ny * to_cam_y
    return dot > 0

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
            (r*np.cos(thetas[i]),   r*np.sin(thetas[i]),   z0),
            (r*np.cos(thetas[i+1]), r*np.sin(thetas[i+1]), z0),
            (r*np.cos(thetas[i+1]), r*np.sin(thetas[i+1]), z1),
            (r*np.cos(thetas[i]),   r*np.sin(thetas[i]),   z1),
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
for t in np.linspace(0, 2 * np.pi, 80):
    x, y = r * np.cos(t), r * np.sin(t)
    p1 = project(x, y, z_start)
    p2 = project(x, y, z_end)
    if p1 and p2:
        light = int(25 + 50 * max(0, np.cos(t - az)))
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
        if not is_facing_camera(t_mid):
            continue

        val = array[row, col]
        if val == 0:
            fill_color   = (220, 220, 220)
            border_color = (80, 80, 80)
        else:
            fill_color   = (20, 20, 20)
            border_color = (130, 130, 130)

        fill_quad(t0, t1, z0, z1, fill_color, border_color)

# Redraw circles on top
for z_val in [z_start, z_end]:
    pts = [(r*np.cos(t), r*np.sin(t), z_val)
           for t in np.linspace(0, 2*np.pi, 120)]
    draw_curve(pts, (160, 160, 160), 2)

# --- HUD ---
cv2.putText(img, f"Azimuth: {AZIMUTH:.0f} deg  |  Elevation: {ELEVATION:.0f} deg", (30, 45),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
cv2.putText(img, "0 = White   1 = Black", (30, 85),
            cv2.FONT_HERSHEY_SIMPLEX, 0.65, (160, 160, 160), 1)
cv2.putText(img, f"Array: {rows} rings x {cols} squares", (30, 120),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (130, 130, 130), 1)

cv2.imwrite('cylinder_rings_opencv.png', img)
print("Saved!")