with open("numbers.txt", "w", encoding="utf-8") as file:
    for i in range(1, 1_000_001):
        file.write(f"{i}\n")

print("Готово!")
print("Создан файл numbers.txt с 1 000 000 чисел.")