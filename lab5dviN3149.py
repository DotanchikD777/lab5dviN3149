import sys
import os
import random
import struct
from datetime import datetime

# Функция для генерации случайной строки формата даты или времени
def generate_random_date_time():
    if random.choice([True, False]):
        # Генерация времени в формате чч.мм.сс
        return "{:02d}.{:02d}.{:02d}".format(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
    else:
        # Генерация даты в формате дд.мм.гггг
        return "{:02d}.{:02d}.{:04d}".format(random.randint(1, 31), random.randint(1, 12), random.randint(1000, 9999))

# Функция для записи данных в бинарный файл
def write_to_file(filename, n, io_array, ls_array):
    with open(filename, "wb") as file:
        # Запись n
        file.write(struct.pack("i", n))

        # Запись области i, o
        for io in io_array:
            file.write(struct.pack("ii", io[0], io[1]))

        # Запись пустой области в 100 байт
        file.write(b'\x00' * 100)

        # Запись области k, s
        for ls in ls_array:
            file.write(struct.pack("i", ls[0]))
            file.write(ls[1].encode())

def print_data(n, io_array, ls_array):
    for i in range(n):
        index, offset = io_array[i]
        length, string = ls_array[i]
        print(f"Строка [{index}], по адресу: (0x{offset:08x}) = {string}")

# Основная функция программы
def main():
    name = sys.argv[0]
    args = sys.argv[1:]
    
    if not args:
        print(f"Используйте: {name} [-n <количество_строк>] <имя_файла> || {name} -v")
        sys.exit(1)

    if args[0] == "-v":
        print("\tДенис Ильчук Витальевич, гр. N3149\n\tВариант: 8-5\n")
        sys.exit(0)

    if args[0] == "-n":
        if len(args) != 3:
            print(f"Используйте: {name} -n <количество_строк> <имя_файла>")
            sys.exit(1)
        try:
            n = int(args[1])
        except ValueError:
            print("Количество строк, должно быть целым числом")
            sys.exit(1)
        if n <= 0:
            print("Количество строк, должно быть натуральным числом")
            sys.exit(1)
        filename = args[2]
    else:
        if len(args) != 1:
            print(f"Используйте: {name} <имя_файла>")
            sys.exit(1)
        filename = args[0]
        n = random.randint(10, 1000)

    io_array = []
    ls_array = []

    current_offset = 0

    for i in range(n):
        random_string = generate_random_date_time()
        string_length = len(random_string)
        
        ls_array.append((string_length, random_string))
        io_array.append((i, current_offset))
        
        current_offset += struct.calcsize("i") + string_length
    print_data(n, io_array, ls_array)
    write_to_file(filename, n, io_array, ls_array)

if __name__ == "__main__":
    main()
