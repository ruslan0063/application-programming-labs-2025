import argparse
import datetime

# Парсим аргументы командной строки
def parse_args():
    parser = argparse.ArgumentParser(description='Скачать картинки обезьян')
    
    parser.add_argument('-t', '--total', type=int, required=True,
                       help='Сколько картинок (от 50 до 1000)')
    parser.add_argument('-o', '--output', default='monkey_images',
                       help='Куда сохранять')
    parser.add_argument('-a', '--annotation', default='annotation.csv',
                       help='Файл для списка картинок')
    parser.add_argument('-y', '--year', type=int,
                       default=datetime.datetime.now().year,
                       help='Какого года картинки')
    
    return parser.parse_args()

# Проверяем, что аргументы правильные
def check_args(args):
    if not 50 <= args.total <= 1000:
        raise ValueError(f"Нужно от 50 до 1000, а не {args.total}")
    
    now = datetime.datetime.now().year
    if not 2000 <= args.year <= now:
        raise ValueError(f"Год должен быть от 2000 до {now}")
    
    return args

# Главная функция
def main():
    args = parse_args()
    
    try:
        check_args(args)
        print(f"Скачаем {args.total} картинок обезьян {args.year} года")
        print(f"Сохраним в папку: {args.output}")
        print(f"Список файлов: {args.annotation}")
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
