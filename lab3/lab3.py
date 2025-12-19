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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True, help="Путь к изображению")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print("Файл не найден")
        sys.exit(1)

    image = load_image(args.input)
    get_dimensions(image)

    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Исходное изображение")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
