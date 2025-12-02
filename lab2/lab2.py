import os
import argparse
import datetime
from icrawler.builtin import BingImageCrawler

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

# Скачивание изображений обезьян с Bing
def download_images(total, year, folder):
    os.makedirs(folder, exist_ok=True)
    print(f"паппка: {os.path.abspath(folder)}")
    print(f"ищем: monkey {year}")
    print(f"скачиваем {total} картинок")
    
    crawler = BingImageCrawler(storage={'root_dir': folder})
    crawler.crawl(keyword=f"monkey {year}", max_num=total)
    
    print("Скачано!")

# Главная функция программы
def main():
    args = parse_args()
    
    try:
        check_args(args)
        
        print("=" * 40)
        print("СКАЧИВАЕМ КАРТИНКИ ОБЕЗЬЯН")
        print("=" * 40)
        
        download_images(args.total, args.year, args.output)
        
        print("\n Картинки скачаны!")
        
    except Exception as e:
        print(f"\n Ошибка: {e}")

if __name__ == "__main__":
    main()
