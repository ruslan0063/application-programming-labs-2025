import cv2
import matplotlib.pyplot as plt
import argparse
import os
import sys

def load_image(image_path: str):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Ошибка: не удалось загрузить '{image_path}'")
        sys.exit(1)
    print(f"Изображение загружено: {image_path}")
    return image

def get_dimensions(image):
    h, w = image.shape[:2]
    channels = image.shape[2] if len(image.shape) == 3 else 1
    print(f"Размер: {w}x{h}, каналы: {channels}")
def swap_channels(image, mode='RGB'):
    if len(image.shape) != 3 or image.shape[2] != 3:
        print("Изображение не цветное — каналы не меняем")
        return image.copy()

    orders = {
        'RGB': [2, 1, 0],  # BGR -> RGB
        'RBG': [2, 0, 1],
        'GRB': [1, 2, 0],
        'GBR': [1, 0, 2],
        'BRG': [0, 2, 1],
        'BGR': [0, 1, 2],  # без изменений
    }
    indices = orders.get(mode, [2, 1, 0])
    return image[:, :, indices]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--mode", "-m", default="RGB",
                        choices=['RGB', 'RBG', 'GRB', 'GBR', 'BRG', 'BGR'])
    args = parser.parse_args()

    if not os.path.exists(args.input):
        sys.exit(1)

    image = load_image(args.input)
    get_dimensions(image)

    result = swap_channels(image, args.mode)
    print(f"Каналы изменены: BGR → {args.mode}")

    # Отображение до/после
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    ax[0].set_title("Исходное")
    ax[1].imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    ax[1].set_title(f"После ({args.mode})")
    for a in ax:
        a.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
