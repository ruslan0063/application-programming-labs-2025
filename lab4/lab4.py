import argparse
import pandas as pd
import os

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv_path", default="annotation.csv", type=str)
    args = parser.parse_args()
    return args.csv_path

def main():
    annotation_path = parse_arguments()
    if not os.path.exists(annotation_path):
        print("Файл аннотации не найден")
        return

    df = pd.read_csv(annotation_path)
    print("DataFrame из аннотации Lab2:")
    print(df.head(10))  # показываем первые 10 строк

    print("\nНазвания колонок:")
    print(df.columns.tolist())

if __name__ == "__main__":
    main()
