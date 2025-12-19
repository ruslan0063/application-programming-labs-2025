import os
import csv
from typing import List


class ImageIterator:
    """
    Итератор по путям к файлам изображений.
    Поддерживает два источника:
    - Папку с изображениями (рекурсивно ищет во всех подпапках)
    - CSV-файл аннотации (берёт абсолютные пути из первой колонки)
    """
    def __init__(self, path: str) -> None:
        self.path = path
        self.data: List[str] = []
        self.index: int = 0

        if not os.path.exists(path):
            raise FileNotFoundError(f"Путь не найден: {path}")

        if path.lower().endswith(".csv"):
            self._load_from_csv(path)
        else:
            if not os.path.isdir(path):
                raise ValueError(f"Путь должен быть папкой или CSV-файлом: {path}")
            self._load_from_folder(path)

    def _load_from_folder(self, folder_path: str) -> None:
        """Рекурсивно собирает все изображения из папки и подпапок"""
        supported_extensions = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff")
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(supported_extensions):
                    full_path = os.path.join(root, file)
                    self.data.append(full_path)

    def _load_from_csv(self, csv_path: str) -> None:
        """Читает абсолютные пути из первой колонки CSV (как в Lab2)"""
        with open(csv_path, newline='', encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            next(reader, None)  # пропускаем заголовок
            for row in reader:
                if row:  # если строка не пустая
                    # Берём первый элемент — абсолютный путь
                    self.data.append(row[0].strip())

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self) -> str:
        if self.index >= len(self.data):
            raise StopIteration
        current_path = self.data[self.index]
        self.index += 1
        return current_path

    def __len__(self) -> int:
        return len(self.data)
