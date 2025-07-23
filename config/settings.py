# Video source default (overridden by GUI or CLI)
CAMERA_SOURCE = 0  # 0 for webcam, or path/RTSP URL

# Motion detection parameters
def default_params():

    return {
        'sensitivity': 0.5,    # 0.0 (high) → 1.0 (low)
        'cooldown': 10,        # seconds between captures
        'buffer_size': 5,      # number of past frames to retain
        'min_area_ratio': 0.15 # area ratio threshold
    }