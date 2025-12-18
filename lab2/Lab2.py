import argparse
import csv
import os
from icrawler.builtin import BingImageCrawler


def parse_args():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description="Скачивание изображений monkey с помощью icrawler и создание аннотации")
    parser.add_argument("-i", "--img_dir", default="imgs", type=str,
                        help="Папка для сохранения изображений (по умолчанию: imgs)")
    parser.add_argument("-c", "--csv_path", default="annotation.csv", type=str,
                        help="Путь к файлу аннотации CSV (по умолчанию: annotation.csv)")
    parser.add_argument("-n", "--img_max_num", default=100, type=int,
                        help="Количество изображений (50-1000, по умолчанию: 100)")
    args = parser.parse_args()
    
    if not (50 <= args.img_max_num <= 1000):
        parser.error("Количество изображений должно быть от 50 до 1000")
    
    return args.img_dir, args.csv_path, args.img_max_num


def main():
    try:
        img_dir, csv_path, max_num = parse_args()
        os.makedirs(img_dir, exist_ok=True)
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
