import cv2

path = "/home/shrirag10/llm_astar_sim/20_ by_ 20_orthogonalmaze.png"
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)


if img is None:
    raise FileNotFoundError(f"Could not load image: {path}")
else: 
    print("Image loaded successfully.")