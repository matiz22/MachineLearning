import csv


def read_csv(filename: str) -> list[list[str]]:
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        return [row for row in csv_reader]
