import argparse
import csv
import os
from icrawler.builtin import BingImageCrawler


class PathsIterator:
    """
    Итератор по путям к файлам из CSV-аннотации.
    """
    def __init__(self, csv_path: str):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Файл аннотации не найден: {csv_path}")

        with open(csv_path, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            self.paths = [(row[0], row[1]) for row in reader if len(row) >= 2]
            self.index = 0

    def __iter__(self):
        return self

    def __next__(self) -> tuple[str, str]:
        if self.index < len(self.paths):
            path_tuple = self.paths[self.index]
            self.index += 1
            return path_tuple
        raise StopIteration


def parse_args():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description="Скачивание изображений monkey с помощью icrawler и создание аннотации"
    )
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


def download_monkey_images(img_dir: str, max_num: int):
    """Скачивание изображений monkey через BingImageCrawler (icrawler)"""
    crawler = BingImageCrawler(
        downloader_threads=4,
        storage={'root_dir': img_dir}
    )
    crawler.crawl(keyword="monkey", max_num=max_num)


def create_annotation(img_dir: str, csv_path: str):
    """Создаёт CSV с абсолютными и относительными путями к изображениям"""
    if not os.path.exists(img_dir):
        raise FileNotFoundError(f"Папка с изображениями не найдена: {img_dir}")

    image_files = [
        f for f in os.listdir(img_dir)
        if os.path.isfile(os.path.join(img_dir, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
    ]

    if not image_files:
        print("Предупреждение: изображения не найдены в папке.")
        return

    data = [["Абсолютный путь", "Относительный путь"]]
    for filename in sorted(image_files):
        abs_path = os.path.abspath(os.path.join(img_dir, filename))
        rel_path = os.path.join(img_dir, filename)
        data.append([abs_path, rel_path])

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    print(f"Аннотация создана: {csv_path} ({len(image_files)} изображений)")


def main():
    try:
        img_dir, csv_path, max_num = parse_args()
        os.makedirs(img_dir, exist_ok=True)
        print(f"Скачиваем до {max_num} изображений 'monkey' в папку: {img_dir}")
        download_monkey_images(img_dir, max_num)
        print("Создаём аннотацию")
        create_annotation(img_dir, csv_path)
        print(f"Изображения сохранены в: {os.path.abspath(img_dir)}")
        print(f"Аннотация сохранена в: {os.path.abspath(csv_path)}")
        print("\n")
        print("Работа итератора PathsIterator")
        print(" ")
        while True:
            try:
                user_input = input("\nВведите количество записей для вывода (или Enter для 5): ").strip()
                if user_input == "":
                    n = 5
                else:
                    n = int(user_input)
                    if n <= 0:
                        print("Пожалуйста, введите положительное число.")
                        continue
                break
            except ValueError:
                print("Ошибка: введите целое положительное число.")
        print(f"\nПервые {n} записей через итератор:")
        print(" ")
        iterator = PathsIterator(csv_path)
        count = 0
        for abs_path, rel_path in iterator:
            if count >= n:
                break
            print(f"Абсолютный:   {abs_path}")
            print(f"Относительный: {rel_path}")
            print("  ")
            count += 1

        if count == 0:
            print("(Нет записей, аннотация пуста)")
            
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
