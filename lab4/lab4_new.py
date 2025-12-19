import argparse
import pandas as pd
import os
import cv2
import numpy as np

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv_path", default="annotation.csv", type=str)
    args = parser.parse_args()
    return args.csv_path

def calculate_mean_brightness(image, channel_idx):
    if image is None:
        return np.nan
    return image[:, :, channel_idx].mean()

def main():
    annotation_path = parse_arguments()
    df = pd.read_csv(annotation_path)

    # Вычисляем среднюю яркость по всем трём каналам
    red_means = []
    green_means = []
    blue_means = []

    for rel_path in df["Относительный путь"]:
        image = cv2.imread(rel_path)
        if image is None:
            red_means.append(np.nan)
            green_means.append(np.nan)
            blue_means.append(np.nan)
            continue
        blue_means.append(calculate_mean_brightness(image, 0))  # B
        green_means.append(calculate_mean_brightness(image, 1))  # G
        red_means.append(calculate_mean_brightness(image, 2))    # R

    df["Средняя яркость (red)"] = red_means
    df["Средняя яркость (green)"] = green_means
    df["Средняя яркость (blue)"] = blue_means

    print("DataFrame с добавленными колонками средней яркости:")
    print(df.head(10))

if __name__ == "__main__":
    main()
