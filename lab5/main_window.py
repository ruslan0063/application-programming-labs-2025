import os
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# Импортируем итератор
from iterator import ImageIterator


class PhotoViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_iter = None
        self.current_pos = 0

        self.setWindowTitle("Просмотрщик датасета — Лабораторная №5")
        self.resize(900, 700)

        # Центральный виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Кнопки выбора источника
        top_buttons = QVBoxLayout()
        self.btn_select_folder = QPushButton("Открыть папку с изображениями")
        self.btn_select_folder.clicked.connect(self.open_folder)
        top_buttons.addWidget(self.btn_select_folder)

        self.btn_select_csv = QPushButton("Открыть файл аннотации (CSV)")
        self.btn_select_csv.clicked.connect(self.open_annotation)
        top_buttons.addWidget(self.btn_select_csv)

        layout.addLayout(top_buttons)

        # Информация о текущем изображении
        self.status_label = QLabel("Выберите источник данных")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Метка для изображения
        self.photo_label = QLabel()
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setStyleSheet("border: 3px solid gray;")
        self.photo_label.setText("Здесь будет изображение")
        layout.addWidget(self.photo_label)

        # Кнопки навигации
        nav_layout = QVBoxLayout()
        self.btn_back = QPushButton("<- Предыдущее")
        self.btn_back.clicked.connect(self.show_previous)
        self.btn_back.setEnabled(False)
        nav_layout.addWidget(self.btn_back)

        self.btn_forward = QPushButton("Следующее ->")
        self.btn_forward.clicked.connect(self.show_next)
        self.btn_forward.setEnabled(False)
        nav_layout.addWidget(self.btn_forward)

        layout.addLayout(nav_layout)

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с изображениями")
        if folder:
            self.load_dataset(folder)

    def open_annotation(self):
        file, _ = QFileDialog.getOpenFileName(self, "Выберите CSV-аннотацию", "", "CSV (*.csv)")
        if file:
            self.load_dataset(file)

    def load_dataset(self, source_path):
        try:
            self.image_iter = ImageIterator(source_path)
            if len(self.image_iter) == 0:
                QMessageBox.warning(self, "Внимание", "Изображения не найдены")
                return

            self.current_pos = 0
            self.btn_back.setEnabled(True)
            self.btn_forward.setEnabled(True)
            self.display_current_photo()

        except Exception as error:
            QMessageBox.critical(self, "Ошибка", str(error))

    def display_current_photo(self):
        if not self.image_iter:
            return

        try:
            img_path = self.image_iter.data[self.current_pos]
            pixmap = QPixmap(img_path)

            if pixmap.isNull():
                self.photo_label.setText("Не удалось загрузить изображение")
            else:
                # Масштабируем с сохранением пропорций
                scaled_pixmap = pixmap.scaled(
                    self.photo_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.photo_label.setPixmap(scaled_pixmap)

            # Обновляем статус
            total = len(self.image_iter)
            filename = os.path.basename(img_path)
            self.status_label.setText(f"{self.current_pos + 1} из {total} — {filename}")

        except Exception as error:
            self.photo_label.setText(f"Ошибка: {error}")

    def show_next(self):
        if self.current_pos < len(self.image_iter) - 1:
            self.current_pos += 1
            self.display_current_photo()
        else:
            QMessageBox.information(self, "Конец", "Это последнее изображение")

    def show_previous(self):
        if self.current_pos > 0:
            self.current_pos -= 1
            self.display_current_photo()
        else:
            QMessageBox.information(self, "Начало", "Это первое изображение")

    def resizeEvent(self, event):
        """Автоматическое масштабирование при изменении размера окна"""
        super().resizeEvent(event)
        if self.image_iter:
            self.display_current_photo()


def main():
    app = QApplication(sys.argv)
    viewer = PhotoViewer()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
