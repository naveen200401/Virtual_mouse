import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np
import subprocess
import threading
from collections import deque

# --- ULTRA-OPTIMIZED Configuration ---
FRAME_SKIP = 3
SMOOTHENING_FACTOR = 0.65  # Fine-tuned EMA
SHOW_DEBUG_INFO = False
ENABLE_MULTITHREADING = True  # NEW: Thread-based capture

# Camera settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30
CAMERA_BUFFER_SIZE = 1  # NEW: Minimal buffer

# Click thresholds (squared for faster comparison)
LEFT_CLICK_DIST_SQ = 1600  # 40^2
RIGHT_CLICK_DIST_SQ = 1600  # 40^2
CLICK_COOLDOWN = 0.3

# Scroll parameters
THUMBS_UP_REL_Y = 0.08
THUMB_STRAIGHT = 0.1
FINGER_BENT = 0.05
INITIAL_SCROLL_SENS = 15
CONTINUOUS_SCROLL_SENS = 8
CONTINUOUS_SCROLL_HOLD = 1.5
SCROLL_COOLDOWN = 0.5

# Volume control
VOLUME_DIST_THRESHOLD = 5
VOLUME_SENSITIVITY = 0.5
VOLUME_SMOOTH = 0.6

# PyAutoGUI fail-safe
pyautogui.FAILSAFE = False

# --- NEW: Threaded Video Capture Class ---
class ThreadedCamera:
    """Separate thread for frame capture to eliminate blocking"""
    def __init__(self, src=0, width=640, height=480, fps=30, buffer_size=1):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)  # NEW: Minimize buffer
        
        self.ret = False
        self.frame = None
        self.stopped = False
        self.lock = threading.Lock()
        
    def start(self):
        """Start the frame capture thread"""
        threading.Thread(target=self._update, daemon=True).start()
        return self
        
    def _update(self):
        """Continuously read frames in separate thread"""
        while not self.stopped:
            ret, frame = self.cap.read()
            with self.lock:
                self.ret = ret
                self.frame = frame
                
    def read(self):
        """Get the latest frame"""
        with self.lock:
            return self.ret, self.frame.copy() if self.frame is not None else None
            
    def stop(self):
        """Stop the capture thread"""
        self.stopped = True
        self.cap.release()

# --- MediaPipe Setup (Optimized) ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=0,  # Fastest model
    min_detection_confidence=0.3,  # Lower for better responsiveness
    min_tracking_confidence=0.3
)
mp_draw = mp.solutions.drawing_utils

# --- Video Capture Setup ---
if ENABLE_MULTITHREADING:
    cap = ThreadedCamera(0, CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_FPS, CAMERA_BUFFER_SIZE).start()
    time.sleep(1.0)  # Allow camera to warm up
else:
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, CAMERA_BUFFER_SIZE)

screen_width, screen_height = pyautogui.size()

# --- Volume Control Functions ---
volume_available = False
current_volume = 50

def get_macos_volume():
    try:
        cmd = "osascript -e 'get output volume of (get volume settings)'"
        output = subprocess.check_output(cmd, shell=True, text=True).strip()
        return int(output)
    except:
        return 50

def set_macos_volume(vol):
    global current_volume
    vol = max(0, min(100, int(vol)))
    try:
        cmd = f"osascript -e 'set volume output volume {vol}'"
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        current_volume = vol
    except:
        pass

# Initialize volume
try:
    current_volume = get_macos_volume()
    volume_available = True
    print(f"Volume Control: Enabled ({current_volume}%)")
except:
    print("Volume Control: Disabled")

# --- NEW: Optimized Distance Function ---
def dist_sq(p1, p2):
    """Squared distance - faster than sqrt"""
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

# --- NEW: Fast EMA ---
def ema(current, previous, alpha):
    """Exponential moving average"""
    return alpha * current + (1 - alpha) * previous

# --- NEW: Landmark Cache Structure ---
class HandData:
    """Efficient hand data storage"""
    __slots__ = ['thumb_tip', 'thumb_mcp', 'index_tip', 'index_mcp', 
                 'middle_tip', 'middle_mcp', 'ring_tip', 'ring_mcp',
                 'pinky_tip', 'pinky_mcp', 'wrist', 'handedness']
    
    def __init__(self, landmarks, w, h, handedness):
        # Extract only needed landmarks (avoids loop)
        lm = landmarks.landmark
        self.thumb_tip = (int(lm[4].x * w), int(lm[4].y * h), lm[4].y)
        self.thumb_mcp = (int(lm[2].x * w), int(lm[2].y * h), lm[2].y)
        self.index_tip = (int(lm[8].x * w), int(lm[8].y * h), lm[8].y)
        self.index_mcp = (int(lm[5].x * w), int(lm[5].y * h), lm[5].y)
        self.middle_tip = (int(lm[12].x * w), int(lm[12].y * h), lm[12].y)
        self.middle_mcp = (int(lm[9].x * w), int(lm[9].y * h), lm[9].y)
        self.ring_tip = (int(lm[16].x * w), int(lm[16].y * h), lm[16].y)
        self.ring_mcp = (int(lm[13].x * w), int(lm[13].y * h), lm[13].y)
        self.pinky_tip = (int(lm[20].x * w), int(lm[20].y * h), lm[20].y)
        self.pinky_mcp = (int(lm[17].x * w), int(lm[17].y * h), lm[17].y)
        self.wrist = (int(lm[0].x * w), int(lm[0].y * h))
        self.handedness = handedness

# --- State Variables ---
prev_mouse_x, prev_mouse_y = 0, 0
last_left_click = 0
last_right_click = 0
frame_count = 0

# Scroll states
scroll_state = {
    "Left": {"active": False, "start": 0.0, "last": 0.0, "scrolled": False, "dir": -1},
    "Right": {"active": False, "start": 0.0, "last": 0.0, "scrolled": False, "dir": 1}
}

# Volume state
volume_active = False
smooth_hand_dist = 0

print(f"Screen: {screen_width}x{screen_height}")
print(f"Threading: {'Enabled' if ENABLE_MULTITHREADING else 'Disabled'}")
print("Press 'q' to quit\n")

# --- Main Loop ---
try:
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            continue
            
        frame = cv2.flip(frame, 1)
        frame_count += 1
        
        # Frame skipping
        if frame_count % FRAME_SKIP != 0:
            cv2.imshow('Virtual Mouse', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue
        
        # Process frame
        h, w = frame.shape[:2]
        current_time = time.time()
        
        # Convert to RGB (make non-writable for performance)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        results = hands.process(rgb)
        
        # Parse hands
        hands_data = []
        if results.multi_hand_landmarks:
            for idx, hand_lm in enumerate(results.multi_hand_landmarks):
                handedness = results.multi_handedness[idx].classification[0].label
                hands_data.append(HandData(hand_lm, w, h, handedness))
                
                if SHOW_DEBUG_INFO:
                    mp_draw.draw_landmarks(frame, hand_lm, mp_hands.HAND_CONNECTIONS)
        
        # Find pointer hand and check for two-hand volume
        pointer_hand = None
        left_wrist = None
        right_wrist = None
        
        for hand in hands_data:
            if hand.handedness == "Left":
                left_wrist = hand.wrist
            else:
                right_wrist = hand.wrist
            
            # Prefer right hand for pointer
            if pointer_hand is None or hand.handedness == "Right":
                pointer_hand = hand
        
        # Two-hand volume control
        if left_wrist and right_wrist and volume_available:
            dist = np.sqrt((left_wrist[0] - right_wrist[0])**2 + (left_wrist[1] - right_wrist[1])**2)
            
            if not volume_active:
                volume_active = True
                smooth_hand_dist = dist
            else:
                smooth_hand_dist = ema(dist, smooth_hand_dist, VOLUME_SMOOTH)
                delta = dist - smooth_hand_dist
                
                if abs(delta) > VOLUME_DIST_THRESHOLD:
                    new_vol = current_volume + delta * VOLUME_SENSITIVITY
                    set_macos_volume(new_vol)
            
            if SHOW_DEBUG_INFO:
                cv2.line(frame, left_wrist, right_wrist, (0, 255, 0), 2)
        else:
            volume_active = False
        
        # Scroll detection
        if not volume_active:
            for hand in hands_data:
                # Check thumbs-up gesture
                is_thumbs_up = (
                    (hand.thumb_tip[2] - hand.index_mcp[2]) < THUMBS_UP_REL_Y and
                    (hand.thumb_tip[2] - hand.thumb_mcp[2]) < THUMB_STRAIGHT and
                    (hand.index_tip[2] - hand.index_mcp[2]) > FINGER_BENT and
                    (hand.middle_tip[2] - hand.middle_mcp[2]) > FINGER_BENT and
                    (hand.ring_tip[2] - hand.ring_mcp[2]) > FINGER_BENT and
                    (hand.pinky_tip[2] - hand.pinky_mcp[2]) > FINGER_BENT
                )
                
                state = scroll_state[hand.handedness]
                
                if is_thumbs_up:
                    if not state["active"]:
                        state["active"] = True
                        state["start"] = current_time
                        
                        if not state["scrolled"] and (current_time - state["last"]) > SCROLL_COOLDOWN:
                            pyautogui.scroll(INITIAL_SCROLL_SENS * state["dir"])
                            state["last"] = current_time
                            state["scrolled"] = True
                    else:
                        hold_time = current_time - state["start"]
                        if hold_time >= CONTINUOUS_SCROLL_HOLD and \
                           (current_time - state["last"]) > SCROLL_COOLDOWN:
                            pyautogui.scroll(CONTINUOUS_SCROLL_SENS * state["dir"])
                            state["last"] = current_time
                else:
                    if state["active"]:
                        state["active"] = False
                        state["scrolled"] = False
        
        # Pointer and clicks
        if pointer_hand and not volume_active:
            # Map cursor
            mouse_x = np.interp(pointer_hand.index_tip[0], [50, w-50], [0, screen_width])
            mouse_y = np.interp(pointer_hand.index_tip[1], [50, h-50], [0, screen_height])
            
            # EMA smoothing
            curr_x = ema(mouse_x, prev_mouse_x, SMOOTHENING_FACTOR)
            curr_y = ema(mouse_y, prev_mouse_y, SMOOTHENING_FACTOR)
            
            pyautogui.moveTo(curr_x, curr_y)
            prev_mouse_x, prev_mouse_y = curr_x, curr_y
            
            # Left click (index + thumb)
            if dist_sq(pointer_hand.index_tip, pointer_hand.thumb_tip) < LEFT_CLICK_DIST_SQ:
                if current_time - last_left_click > CLICK_COOLDOWN:
                    pyautogui.click(button='left')
                    last_left_click = current_time
            
            # Right click (middle + thumb)
            if dist_sq(pointer_hand.middle_tip, pointer_hand.thumb_tip) < RIGHT_CLICK_DIST_SQ:
                if current_time - last_right_click > CLICK_COOLDOWN:
                    pyautogui.click(button='right')
                    last_right_click = current_time
        
        # Display
        cv2.imshow('Virtual Mouse', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nStopped by user")

finally:
    # Cleanup
    if ENABLE_MULTITHREADING:
        cap.stop()
    else:
        cap.release()
    cv2.destroyAllWindows()
    print("Virtual Mouse Stopped")
