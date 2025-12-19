import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import sys


def load_image(image_path: str) -> np.ndarray:
    """Загрузка изображения"""
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Ошибка: не удалось загрузить изображение '{image_path}'")
            return None
        print(f"Изображение загружено: {image_path}")
        return image
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")
        return None


def get_dimensions(image: np.ndarray) -> tuple:
    """Получение размеров изображения"""
    if len(image.shape) == 3:
        height, width, channels = image.shape
        print(f"Размер изображения: {width}x{height}, каналы: {channels}")
        return height, width, channels
    else:
        height, width = image.shape
        print(f"Размер изображения: {width}x{height}, каналы: 1 (grayscale)")
        return height, width, 1


def swap_channels(image: np.ndarray, swap_mode: str = 'RGB') -> np.ndarray:
    """
    Поменять местами цветовые каналы изображения.
    """
    if len(image.shape) != 3 or image.shape[2] != 3:
        print("Изображение не имеет 3 цветовых канала. Возвращаем исходное.")
        return image.copy()

    
    # BGR в OpenCV: 0 = B, 1 = G, 2 = R
    channel_order = {
        'RGB': [2, 1, 0],  
        'RBG': [2, 0, 1],  
        'GRB': [1, 2, 0],  
        'GBR': [1, 0, 2],  
        'BRG': [0, 2, 1], 
        'BGR': [0, 1, 2],  
    }

    if swap_mode not in channel_order:
        print(f"Неизвестный режим '{swap_mode}'. Используется режим RGB.")
        swap_mode = 'RGB'

    indices = channel_order[swap_mode]
    swapped = image[:, :, indices]

    print(f"Каналы изменены: BGR -> {swap_mode}")
    return swapped


def display_result(original: np.ndarray, result: np.ndarray, swap_mode: str) -> None:
    """Отображение оригинального и результирующего изображений"""
    # Конвертируем в RGB для matplotlib
    def to_rgb(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if len(img.shape) == 3 and img.shape[2] == 3 else img

    original_rgb = to_rgb(original)
    result_rgb = to_rgb(result)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    axes[0].imshow(original_rgb)
    axes[0].set_title('Исходное изображение')
    axes[0].axis('off')

    axes[1].imshow(result_rgb)
    axes[1].set_title(f'После замены каналов ({swap_mode})')
    axes[1].axis('off')

    plt.suptitle('Сравнение до и после замены цветовых каналов', fontsize=14)
    plt.tight_layout()
    plt.show()


def save_image(output_path: str, image: np.ndarray, swap_mode: str) -> None:
    """Сохранение изображения"""
    try:
        # Добавляем расширение, если нет
        if not output_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            output_path += '.jpg'
            print(f"Добавлено расширение .jpg: {output_path}")

        # Если изображение в RGB — конвертируем обратно в BGR для OpenCV
        if swap_mode != 'BGR':
            save_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        else:
            save_img = image

        cv2.imwrite(output_path, save_img)
        print(f"Изображение сохранено: {output_path}")

    except Exception as e:
        print(f"Ошибка при сохранении изображения: {e}")


def main():
    parser = argparse.ArgumentParser(description="Программа для замены цветовых каналов изображения")
    parser.add_argument("--input", "-i", required=True, type=str, help="Путь к исходному изображению")
    parser.add_argument("--output", "-o", default="result_image.jpg", type=str, help="Путь для сохранения результата")
    parser.add_argument("--mode", "-m", default="RGB", type=str,
                        choices=['RGB', 'RBG', 'GRB', 'GBR', 'BRG', 'BGR'],
                        help="Режим замены цветовых каналов")
    args = parser.parse_args()
    if not os.path.exists(args.input):
        print(f"Ошибка: файл '{args.input}' не найден")
        sys.exit(1)
    print(" ")
    print("Лобораторная №2")
    print(" ")
    print(f"Исходный файл: {args.input}")
    print(f"Выходной файл: {args.output}")
    print(f"Режим замены: {args.mode}")
    print("  ")
    original_image = load_image(args.input)
    if original_image is None:
        sys.exit(1)
    get_dimensions(original_image)
    print("\nВыполняется замена цветовых каналов")
    result_image = swap_channels(original_image, args.mode)
    save_image(args.output, result_image, args.mode)
    display_result(original_image, result_image, args.mode)
    print(" ")
    print("Все работает без ошибок")
    print(" " )


if __name__ == "__main__":
    main()
