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
                        help="Канал для анализа (red, green или blue)")
    args = parser.parse_args()
    return args.csv_path, args.dtfr_path, args.grph_path, args.channel


def calculate_mean_brightness(image: np.ndarray, channel_idx: int) -> float:
    """Вычисляет среднюю яркость по указанному каналу (0=B, 1=G, 2=R)"""
    if image is None:
        return np.nan
    channel = image[:, :, channel_idx]
    return channel.mean()


def get_brightness_range(mean_value: float) -> str:
    """Определяет диапазон яркости"""
    if pd.isna(mean_value):
        return "Ошибка загрузки"

    bins = [0, 50, 100, 150, 200, 256]
    for i in range(len(bins) - 1):
        if bins[i] <= mean_value < bins[i + 1]:
            return f"{int(bins[i])}-{int(bins[i + 1] - 1)}"
    return "201-255"


def create_dataframe(annotation_path: str, channel: str) -> pd.DataFrame:
    """Создаёт DataFrame с путями и диапазоном средней яркости по каналу"""
    df = pd.read_csv(annotation_path)

    channel_map = {"red": 2, "green": 1, "blue": 0}
    channel_idx = channel_map[channel]

    mean_brightnesses = []
    ranges = []

    # Используем абсолютный путь
    for abs_path in df["Абсолютный путь"]:
        image = cv2.imread(abs_path)
        mean_val = calculate_mean_brightness(image, channel_idx)
        mean_brightnesses.append(mean_val)
        ranges.append(get_brightness_range(mean_val))

    df["Средняя яркость"] = mean_brightnesses
    df[f"Диапазон яркости ({channel})"] = ranges

    return df


def plot_histogram(df: pd.DataFrame, channel: str, save_path: str):
    """Строит гистограмму распределения файлов по диапазонам яркости"""
    range_column = f"Диапазон яркости ({channel})"
    clean_data = df[df[range_column] != "Ошибка загрузки"]
    counts = clean_data[range_column].value_counts().sort_index()

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

        # Сортировка по средней яркости
        sorted_df = df.sort_values("Средняя яркость", ignore_index=True, na_position='last')

        # вывод количества строк
        print("\n")
        print("ОТСОРТИРОВАННЫЙ DATAFRAME")
        print(" ")
        while True:
            try:
                user_input = input("\nСколько строк вывести? (Enter — 10, 'all' — все): ").strip()
                if user_input == "" or user_input.lower() == "all":
                    n = len(sorted_df) if user_input.lower() == "all" else 10
                else:
                    n = int(user_input)
                    if n <= 0:
                        print("Введите положительное число.")
                        continue
                break
            except ValueError:
                print("Ошибка: введите число или 'all'.")

        print(f"\nПервые {n} строк отсортированного DataFrame:")
        print(sorted_df.head(n) if n < len(sorted_df) else sorted_df)

        # Сохранение DataFrame
        sorted_df.to_csv(dataframe_path, index=False)
        print(f"\nDataFrame сохранён в: {dataframe_path}")

        # Гистограмма
        plot_histogram(sorted_df, channel, graph_path)
        print(f"Гистограмма сохранена в: {graph_path}")
        print("Все работает без ошибок")
    except Exception as exc:
        print(f"Возникла ошибка: {exc}")


if __name__ == "__main__":
    main()
