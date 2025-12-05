import matplotlib
# Thiết lập backend để đảm bảo hiển thị
matplotlib.use('Qt5Agg') 

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec

# --- I. NHẬP THÔNG SỐ BAN ĐẦU ---

# Vòng lặp nhập H_initial (Độ cao ban đầu)
while True:
    try:
        h_input = input("Nhập Độ cao ban đầu H (mét, ví dụ: 20.0): ")
        H_initial = float(h_input)
        if H_initial <= 0:
            print("LỖI: Độ cao phải là một giá trị dương. Vui lòng nhập lại.")
            continue
        break
    except ValueError:
        print("LỖI: Giá trị nhập vào không hợp lệ. Vui lòng nhập số (ví dụ: 20.0).")

# Vòng lặp nhập DeltaT (Chênh lệch thời gian chạm đất)
while True:
    try:
        deltaT_input = input("Nhập Chênh lệch thời gian chạm đất Delta T (giây, ví dụ: 2.0): ")
        DeltaT = float(deltaT_input)
        if DeltaT < 0:
            print("LỖI: Chênh lệch thời gian không được âm. Vui lòng nhập lại.")
            continue
        break
    except ValueError:
        print("LỖI: Giá trị nhập vào không hợp lệ. Vui lòng nhập số (ví dụ: 2.0).")

G_ACCEL = 10.0      # Gia tốc trọng trường (giá trị cố định)

# --- II. NHẬP TÙY CHỌN ĐỒ THỊ MỚI ---

while True:
    plot_mode_input = input("Chọn chế độ Quỹ đạo bên trái ('2D' hoặc '3D'): ").upper()
    if plot_mode_input in ['2D', '3D']:
        plot_mode = plot_mode_input
        break
    else:
        print("LỖI: Vui lòng chỉ nhập '2D' hoặc '3D'.")
        
# Thiết lập vị trí X cố định cho chế độ 3D (Xuất phát cùng một chỗ)
if plot_mode == '3D':
    X_CONSTANT_A = 0.0 
    X_CONSTANT_B = 0.0  
    print(f"-> Đã chọn chế độ 3D. Cả hai vật xuất phát tại X={X_CONSTANT_A}m.")


# --- III. GIẢI PHÁP SYMBOLIC & TÍNH TOÁN ---

sp.var('t H G t_A t_B v_0 C1 C2')
a = -G
v = sp.integrate(a, t) + C1 
y_general = sp.integrate(v, t) + C2 

# Vật A (Ném lên)
C2_A_sol = sp.solve(sp.Eq(y_general.subs(t, 0), H), C2)[0] 
C1_A_sol = sp.solve(sp.Eq(v.subs(t, 0), v_0), C1)[0] 
y_A_sym = y_general.subs({C1: C1_A_sol, C2: C2_A_sol}) 

# Vật B (Rơi tự do)
C2_B_sol = H 
C1_B_sol = 0 
y_B_sym_check = y_general.subs({C1: C1_B_sol, C2: C2_B_sol}) 

# Tính toán kết quả
t_B_sym = sp.solve(sp.Eq(y_B_sym_check.subs(t, t_B), 0), t_B)[1]
t_B_val = t_B_sym.subs({H: H_initial, G: G_ACCEL})
t_B_num = float(t_B_val) 

t_A_num = t_B_num + DeltaT 
v_0_sym = sp.solve(sp.Eq(y_A_sym.subs(t, t_A), 0), v_0)[0]
v_0_num = float(v_0_sym.subs({H: H_initial, G: G_ACCEL, t_A: t_A_num})) 

print(f"\n--- KẾT QUẢ TÍNH TOÁN ---")
print(f"Thời gian rơi B (t_B): {t_B_num:.2f} s")
print(f"Thời gian chạm đất A (t_A): {t_A_num:.2f} s")
print(f"Vận tốc ném lên (v_0): {v_0_num:.2f} m/s\n")


# --- IV. TRỰC QUAN HÓA ĐỘNG KÉP ---

# 1. Chuyển biểu thức symbolic sang hàm numpy
y_A_func = sp.lambdify((t, sp.Symbol('v_0'), H, G), y_A_sym, 'numpy')
y_B_func = sp.lambdify((t, H, G), y_B_sym_check, 'numpy') 

# 2. Tạo dữ liệu thời gian
t_final = t_A_num 
time_steps = 100 # TỐI ƯU HÓA: Giảm số bước thời gian để tăng độ mượt
t_data = np.linspace(0, t_final, time_steps) 

# Tính toán Y và X data
y_data = y_A_func(t_data, v_0_num, H_initial, G_ACCEL)
y_peak = np.max(y_data) 

if plot_mode == '3D':
    x_data_A = X_CONSTANT_A * np.ones_like(t_data)
    x_data_B = X_CONSTANT_B * np.ones_like(t_data)
    x_max = float(np.max([X_CONSTANT_A, X_CONSTANT_B])) 
else:
    x_max = 0 

# --- 3. THIẾT LẬP SUBPLOTS ---
from matplotlib.gridspec import GridSpec
# Tăng kích thước Figure và điều chỉnh GridSpec để có chỗ cho Legend
fig = plt.figure(figsize=(16, 8)) 
fig.suptitle(f'Mô Phỏng Chuyển Động Ném Thẳng Đứng: H={H_initial}m, ΔT={DeltaT}s', fontsize=16, fontweight='bold')

# Tỷ lệ 1 (Quỹ đạo) : 1 (Đồ thị Y-T) : 0.4 (Legend)
gs = GridSpec(1, 3, width_ratios=[1, 1, 0.4]) 
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
ax_legend = fig.add_subplot(gs[2])
ax_legend.set_axis_off() 

# --- Cấu hình AXES bên phải (Đồ thị y-t, ax2) ---
ax2.set_xlim(0, t_final * 1.1)
ax2.set_ylim(0, y_peak * 1.05) 
ax2.set_xlabel("Thời gian t (giây)")
ax2.set_ylabel("Độ cao y (mét)")
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.set_title(f"Đồ Thị Vị trí theo Thời gian (y-t)\n($v_0$={v_0_num:.2f} m/s)", fontsize=12)

# Khởi tạo các đường và điểm cho AX2 (y-t)
ground_line_yt = ax2.axhline(0, color='k', linestyle='-', linewidth=1.5, zorder=0) 
trail_A_yt, = ax2.plot([], [], linestyle='-', color='red', alpha=0.5)
head_A_yt, = ax2.plot([], [], 'o', color='red', markersize=8)
trail_B_yt, = ax2.plot([], [], linestyle='--', color='blue', alpha=0.5)
head_B_yt, = ax2.plot([], [], '^', color='blue', markersize=8)

# --- Cấu hình AXES bên trái (Quỹ đạo, ax1) ---
if plot_mode == '3D':
    ax1.set_visible(False) 
    ax1 = fig.add_subplot(gs[0], projection='3d')
    
    ax1.set_xlim(-1.0, 1.0) 
    ax1.set_ylim(-1.0, 1.0) 
    ax1.set_zlim(0, y_peak * 1.05)
    
    ax1.set_xlabel('Vị trí X (m)')
    ax1.set_ylabel('Trục Phụ Z')
    ax1.set_zlabel('Độ cao Y (m)')
    ax1.view_init(elev=20, azim=45) 
    
    y_data_B_full = y_B_func(t_data, H_initial, G_ACCEL)
    
    ax1.plot(x_data_A, np.zeros_like(x_data_A), y_data, linestyle=':', color='red', alpha=0.5, label='Quỹ đạo A (3D)')
    ax1.plot(x_data_B, np.zeros_like(x_data_B), y_data_B_full, linestyle=':', color='blue', alpha=0.5, label='Quỹ đạo B (3D)')
    
    head_A_qd, = ax1.plot([x_data_A[0]], [0], [y_data[0]], 'o', color='red', markersize=8)
    head_B_qd, = ax1.plot([x_data_B[0]], [0], [H_initial], '^', color='blue', markersize=8)
    
    trail_A_qd, = ax1.plot([], [], [], linestyle='-', color='red', alpha=0.5)
    trail_B_qd, = ax1.plot([], [], [], linestyle='--', color='blue', alpha=0.5)
    
    time_text_qd = ax1.text(-0.9, 0.9, y_peak * 1.03, 'Thời gian: 0.00 s', color='black', fontsize=10)
    
else:
    # THIẾT LẬP 2D
    ax1.set_xlim(-0.5, 0.5) 
    ax1.set_ylim(0, y_peak * 1.05)
    ax1.set_xlabel(' ')
    ax1.set_ylabel('Độ cao Y (m)')
    ax1.tick_params(axis='x', labelbottom=False) 
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    ax1.plot([0, 0], [0, y_peak], linestyle=':', color='gray', alpha=0.5)
    ax1.axhline(H_initial, color='gray', linestyle='-.', alpha=0.7)
    
    head_A_qd, = ax1.plot([0], [y_data[0]], 'o', color='red', markersize=8)
    head_B_qd, = ax1.plot([0], [H_initial], '^', color='blue', markersize=8)

    trail_A_qd, = ax1.plot([], [], linestyle='-', color='red', alpha=0.1)
    trail_B_qd, = ax1.plot([], [], linestyle='--', color='blue', alpha=0.1)
    
    time_text_qd = ax1.text(0.05, 0.95, 'Thời gian: 0.00 s', transform=ax1.transAxes) 

ax1.set_title(f'Quỹ Đạo Chuyển Động ({plot_mode})', fontsize=12)


# --- 4. CẬP NHẬT LEGEND (CHÚ THÍCH) ---
hit_A_handle, = ax2.plot([], [], 'o', color='red', markersize=8) 
hit_B_handle, = ax2.plot([], [], 's', color='blue', markersize=8)
final_handles = [trail_A_yt, hit_A_handle, trail_B_yt, hit_B_handle, ground_line_yt]
final_labels = [
    f'Vật A (Ném lên, $v_0$={v_0_num:.2f}m/s)',
    f'A chạm đất ({t_A_num:.2f}s)',
    f'Vật B (Rơi tự do, $v_0$=0m/s)',
    f'B chạm đất ({t_B_num:.2f}s)',
    'Mặt đất ($y=0m$)'
]

ax_legend.legend(final_handles, final_labels, 
                 loc='center left', 
                 bbox_to_anchor=(0, 0.5), 
                 fontsize=10, 
                 frameon=False) 

# --- 5. Hàm khởi tạo ---
t_A_list, y_A_list = [], []
t_B_list, y_B_list = [], []
x_A_list_qd, y_A_list_qd = [], []
x_B_list_qd, y_B_list_qd = [], []

def init():
    # Reset y-t
    trail_A_yt.set_data([], []); head_A_yt.set_data([], [])
    trail_B_yt.set_data([], []); head_B_yt.set_data([], [])
    
    # Reset Quỹ đạo
    if plot_mode == '3D':
        trail_A_qd.set_data_3d([], [], [])
        trail_B_qd.set_data_3d([], [], [])
        head_A_qd.set_data_3d([], [], [])
        head_B_qd.set_data_3d([], [], [])
    else:
        trail_A_qd.set_data([], []); head_A_qd.set_data([], [])
        trail_B_qd.set_data([], []); head_B_qd.set_data([], [])

    # Reset lists
    t_A_list.clear(); y_A_list.clear()
    t_B_list.clear(); y_B_list.clear()
    x_A_list_qd.clear(); y_A_list_qd.clear()
    x_B_list_qd.clear(); y_B_list_qd.clear()
    
    time_text_qd.set_text('Thời gian: 0.00 s')
    
    return (trail_A_yt, head_A_yt, trail_B_yt, head_B_yt, 
            trail_A_qd, head_A_qd, trail_B_qd, head_B_qd, time_text_qd)

# --- 6. Hàm cập nhật Animation (UPDATE) ---
def update(frame):
    current_t = t_data[frame]

    # Tính vị trí Vật A
    y_A_current = y_A_func(current_t, v_0_num, H_initial, G_ACCEL)
    
    # --- Cập nhật Vật A ---
    if y_A_current >= 0 and current_t <= t_A_num:
        # 1. Cập nhật Y-T
        t_A_list.append(current_t); y_A_list.append(y_A_current)
        trail_A_yt.set_data(t_A_list, y_A_list)
        head_A_yt.set_data([current_t], [y_A_current]) 
        
        # 2. Cập nhật Quỹ đạo
        if plot_mode == '3D':
            x_A_current = x_data_A[frame]
            x_A_list_qd.append(x_A_current); y_A_list_qd.append(y_A_current)
            
            trail_A_qd.set_data_3d(x_A_list_qd, np.zeros_like(x_A_list_qd), y_A_list_qd)
            head_A_qd.set_data_3d([x_A_current], [0], [y_A_current])
        else:
            x_A_list_qd.append(0); y_A_list_qd.append(y_A_current)
            trail_A_qd.set_data([0] * len(y_A_list_qd), y_A_list_qd)
            head_A_qd.set_data([0], [y_A_current])
            
    else: # Dừng ở điểm chạm đất
        head_A_yt.set_data([t_A_num], [0])
        if plot_mode == '3D':
            head_A_qd.set_data_3d([x_data_A[-1]], [0], [0])
        else:
            head_A_qd.set_data([0], [0])
            

    # Tính vị trí Vật B
    y_B_current = y_B_func(current_t, H_initial, G_ACCEL)

    # --- Cập nhật Vật B ---
    if y_B_current >= 0 and current_t <= t_B_num:
        # 1. Cập nhật Y-T
        t_B_list.append(current_t); y_B_list.append(y_B_current)
        trail_B_yt.set_data(t_B_list, y_B_list)
        head_B_yt.set_data([current_t], [y_B_current]) 
        
        # 2. Cập nhật Quỹ đạo
        if plot_mode == '3D':
            x_B_current = x_data_B[frame]
            x_B_list_qd.append(x_B_current); y_B_list_qd.append(y_B_current)
            
            trail_B_qd.set_data_3d(x_B_list_qd, np.zeros_like(x_B_list_qd), y_B_list_qd)
            head_B_qd.set_data_3d([x_B_current], [0], [y_B_current])
        else:
            x_B_list_qd.append(0); y_B_list_qd.append(y_B_current)
            trail_B_qd.set_data([0] * len(y_B_list_qd), y_B_list_qd)
            head_B_qd.set_data([0], [y_B_current])
            
    else: # Dừng ở điểm chạm đất
        head_B_yt.set_data([t_B_num], [0])
        if plot_mode == '3D':
            head_B_qd.set_data_3d([x_data_B[0]], [0], [0])
        else:
            head_B_qd.set_data([0], [0])
            
    # Cập nhật thời gian
    time_text_qd.set_text(f'Thời gian: {current_t:.2f} s')
    
    return (trail_A_yt, head_A_yt, trail_B_yt, head_B_yt, 
            trail_A_qd, head_A_qd, trail_B_qd, head_B_qd, time_text_qd)


# --- 7. Chạy Animation ---
ani = FuncAnimation(
    fig, 
    update, 
    frames=len(t_data), 
    # TỐI ƯU HÓA: Giữ interval tối ưu để khớp thời gian thực với frame đã giảm
    interval=t_final * 1000 / len(t_data), 
    blit=False, 
    init_func=init, 
    repeat=False
)

# LỆNH LÀM CỬA SỔ HIỆN RA Ở CHẾ ĐỘ PHÓNG TO TỐI ĐA
try:
    fig.canvas.manager.window.showMaximized()
except Exception:
    pass

plt.show()

# LỆNH DỪNG (Giữ cửa sổ mở)
input("--- Đồ thị đã hiện. Nhấn Enter để thoát chương trình... ---")