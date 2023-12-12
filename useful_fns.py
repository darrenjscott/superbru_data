import csv


def dict_to_csv(save_path, list_dicts):
    with open(save_path, 'w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=list(list_dicts[0].keys()))
        writer.writeheader()
        writer.writerows(list_dicts)
