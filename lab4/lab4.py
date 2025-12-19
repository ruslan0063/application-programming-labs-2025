import argparse
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description="Лабораторная №4: Анализ яркости каналов")
    parser.add_argument("-c", "--csv_path", default="annotation.csv", type=str,
                        help="Путь к файлу аннотации из Lab2")
    parser.add_argument("-d", "--dtfr_path", default="dataframe.csv", type=str,
                        help="Путь для сохранения DataFrame")
    parser.add_argument("-g", "--grph_path", default="histogram.jpg", type=str,
                        help="Путь для сохранения гистограммы")
    parser.add_argument("-s", "--channel", default="red", type=str,
                        choices=["red", "green", "blue"],
                        help="Канал для анализа и построения диапазонов (red, green или blue)")
    args = parser.parse_args()
    return args.csv_path, args.dtfr_path, args.grph_path, args.channel


def calculate_mean_brightness(image: np.ndarray, channel_idx: int) -> float:
    """Вычисляет среднюю яркость по указанному каналу (0=B, 1=G, 2=R)"""
    if image is None:
        return np.nan
    # OpenCV использует BGR
    channel = image[:, :, channel_idx]
    return channel.mean()


def get_brightness_range(mean_value: float, bins: list = None) -> str:
    """Определяет диапазон яркости (например, '0-50', '51-100' и т.д.)"""
    if bins is None:
        bins = [0, 50, 100, 150, 200, 256]
    for i in range(len(bins) - 1):
        if bins[i] <= mean_value < bins[i + 1]:
            return f"{int(bins[i])}-{int(bins[i + 1] - 1)}"
    return f"{int(bins[-1])}+"


def create_dataframe(annotation_path: str, channel: str) -> pd.DataFrame:
    """Создаёт DataFrame с путями и диапазоном средней яркости по каналу"""
    df = pd.read_csv(annotation_path)

    # Словарь соответствия названия канала и индекса в BGR
    channel_map = {"red": 2, "green": 1, "blue": 0}
    channel_idx = channel_map[channel]

    mean_brightnesses = []
    ranges = []

    for rel_path in df["Относительный путь"]:
        image = cv2.imread(rel_path)
        mean_val = calculate_mean_brightness(image, channel_idx)
        mean_brightnesses.append(mean_val)
        ranges.append(get_brightness_range(mean_val))

    df["Средняя яркость"] = mean_brightnesses
    df[f"Диапазон яркости ({channel})"] = ranges

    return df


def plot_histogram(df: pd.DataFrame, channel: str, save_path: str):
    """Строит гистограмму распределения файлов по диапазонам яркости"""
    range_column = f"Диапазон яркости ({channel})"
    counts = df[range_column].value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title(f"Распределение изображений по диапазонам средней яркости канала '{channel}'")
    plt.xlabel("Диапазон средней яркости")
    plt.ylabel("Количество изображений")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()


def main():
    try:
        annotation_path, dataframe_path, graph_path, channel = parse_arguments()

        if not os.path.exists(annotation_path):
            print(f"Ошибка: файл аннотации не найден: {annotation_path}")
            return

        print(f"Загружаем аннотацию из: {annotation_path}")
        print(f"Анализируемый канал: {channel}")

        df = create_dataframe(annotation_path, channel)

        # Сортировка и фильтрация (пример демонстрации)
        sorted_df = df.sort_values("Средняя яркость", ignore_index=True)
        print("\nDataFrame отсортирован по средней яркости:")
        print(sorted_df.head(10))

        # Сохранение DataFrame
        sorted_df.to_csv(dataframe_path, index=False)
        print(f"\nDataFrame сохранён в: {dataframe_path}")

        # Построение и сохранение гистограммы
        plot_histogram(sorted_df, channel, graph_path)
        print(f"Гистограмма сохранена в: {graph_path}")

    except Exception as exc:
        print(f"Возникла ошибка: {exc}")


if __name__ == "__main__":
    main()
