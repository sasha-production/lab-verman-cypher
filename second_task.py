import random
import os


class VernamWithEquivalentKeys:
    def __init__(self):
        self.key_length = 10  # Длина ключа по умолчанию

    def generate_random_key(self, length=None):
        """Генерация случайного ключа заданной длины"""
        if length is None:
            length = self.key_length
        return random.randint(10 ** (length - 1), 10 ** length - 1)


    def create_equivalent_key(self, original_key: int, parameter):
        """
        Создание равнозначного ключа
        Формат: [M][S][S_Length][p] где M = original_key × (S + p), S = сумма цифр original_key
        """
        S = sum(int(n) for n in str(original_key))
        M = original_key * (S + parameter)

        length_s = len(str(S))

        # Формируем элемент группы: [M][S][S_Length][p]
        equivalent_key = int(f"{M}{S}{length_s}{parameter}")
        return equivalent_key

    def extract_original_key(self, equivalent_key):
        """Извлечение исходного ключа из равнозначного ключа"""
        key_str = str(equivalent_key)
        # Параметр - первая цифра
        parameter = int(key_str[-1])
        # значение без параметра
        key_str = key_str[:-1]

        # S_length
        S_length = int(key_str[-1])
        # значение без длины суммы
        key_str = key_str[:-1]
        # S
        S = int(key_str[-S_length:])
        # значение без суммы
        # M - оставшаяся средняя часть
        M = int(key_str[:-S_length])

        # Восстанавливаем исходный ключ
        original_key = M // (S + parameter)

        return original_key, parameter

    def generate_key_group(self, original_key=None, group_size=10):
        """Генерация группы равнозначных ключей"""
        if original_key is None:
            original_key = self.generate_random_key()

        key_group = []
        for i in range(group_size):
            # Параметры от 1 до 9
            # parameter = random.randint(1, 9)
            equivalent_key = self.create_equivalent_key(original_key, i)
            key_group.append(equivalent_key)

        return key_group, original_key

    def save_key_group(self, key_group, filename="key_group.txt"):
        """Сохранение группы ключей в файл"""
        with open(filename, 'w', encoding='utf-8') as f:
            for i, key in enumerate(key_group, 1):
                f.write(f"Ключ {i}: {key}\n")
        return filename

    def load_key_group(self, filename="key_group.txt"):
        """Загрузка группы ключей из файла"""
        key_group = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    key = int(line.split(':')[1].strip())
                    key_group.append(key)
        return key_group

    def text_to_binary(self, text):
        """Преобразование текста в бинарную строку"""
        return ''.join(format(ord(char), '08b') for char in text)

    def binary_to_text(self, binary_str):
        """Преобразование бинарной строки в текст"""
        text = ''
        for i in range(0, len(binary_str), 8):
            byte = binary_str[i:i + 8]
            text += chr(int(byte, 2))
        return text

    def generate_gamma(self, key, length):
        """Генерация гаммы из ключа для шифрования"""
        key_str = str(key)
        gamma = ''
        while len(gamma) < length:
            gamma += key_str
        return gamma[:length]

    def vernam_encrypt(self, plaintext, key):
        """Шифрование методом Вернама (однократное гаммирование)"""
        binary_text = self.text_to_binary(plaintext)
        # print(f"binary text - {binary_text}")
        gamma = self.generate_gamma(key, len(binary_text))
        # print(f"gamma - {gamma}")

        # Побитовое XOR
        encrypted_binary = ''.join(
            str(int(text_bit) ^ int(gamma_bit))
            for text_bit, gamma_bit in zip(binary_text, gamma)
        )

        return encrypted_binary

    def vernam_decrypt(self, encrypted_binary, key):
        """Дешифрование методом Вернама"""
        gamma = self.generate_gamma(key, len(encrypted_binary))
        # print(encrypted_binary, gamma, sep='****')
        # Побитовое XOR (аналогично шифрованию)
        decrypted_binary = ''.join(
            str(int(enc_bit) ^ int(gamma_bit))
            for enc_bit, gamma_bit in zip(encrypted_binary, gamma)
        )

        return self.binary_to_text(decrypted_binary)


def main():
    app = VernamWithEquivalentKeys()

    while True:
        print("\n" + "=" * 50)
        print("Шифрование методом Вернама с равнозначными ключами")
        print("=" * 50)
        print("1. Сгенерировать группу ключей")
        print("2. Зашифровать сообщение")
        print("3. Расшифровать сообщение")
        print("4. Показать информацию о ключах")
        print("5. Выход")

        choice = input("\nВыберите действие: ")

        if choice == '1':
            # Генерация группы ключей
            length = int(input("Длина исходного ключа (по умолчанию 10): ") or 10)
            original_key = app.generate_random_key(length)
            key_group, original_key = app.generate_key_group(original_key)

            filename = app.save_key_group(key_group)
            print(f"\nГруппа из {len(key_group)} ключей сохранена в файл: {filename}")
            print(f"Исходный ключ: {original_key}")

            # Показываем информацию о ключах
            print("\nСгенерированные ключи:")
            for i, key in enumerate(key_group, 1):
                original, param = app.extract_original_key(key)
                print(f"Ключ {i}: {key} (параметр: {param}, исходный: {original})")

        elif choice == '2':
            # Шифрование
            if not os.path.exists("key_group.txt"):
                print("Сначала сгенерируйте группу ключей!")
                continue

            key_group = app.load_key_group()
            print(f"\nЗагружено {len(key_group)} ключей")

            # Выбор ключа
            key_choice = input("Выберите ключ (1-10) или 'r' для случайного: ")
            if key_choice.lower() == 'r':
                key = random.choice(key_group)
                key_index = key_group.index(key) + 1
            else:
                key_index = int(key_choice)
                key = key_group[key_index - 1]

            original_key, parameter = app.extract_original_key(key)
            print(f"Выбран ключ {key_index}: {key}")
            print(f"Параметр: {parameter}, Исходный ключ: {original_key}")

            plaintext = input("\nВведите сообщение для шифрования: ")
            encrypted = app.vernam_encrypt(plaintext, key)

            print(f"\nЗашифрованное сообщение (бинарный вид):")
            print(encrypted)

            # Сохраняем зашифрованное сообщение
            with open("encrypted.txt", 'w', encoding='utf-8') as f:
                f.write(encrypted)
            print("Зашифрованное сообщение сохранено в encrypted.txt")

        elif choice == '3':
            # Дешифрование
            if not os.path.exists("key_group.txt"):
                print("Сначала сгенерируйте группу ключей!")
                continue

            key_group = app.load_key_group()

            # Выбор ключа
            key_choice = input("Выберите ключ для дешифрования (1-10): ")
            key_index = int(key_choice)
            key = key_group[key_index - 1]

            original_key, parameter = app.extract_original_key(key)
            print(f"Выбран ключ {key_index}: {key}")
            print(f"Параметр: {parameter}, Исходный ключ: {original_key}")

            # Загрузка зашифрованного сообщения
            try:
                with open("encrypted.txt", 'r', encoding='utf-8') as f:
                    encrypted = f.read().strip()

                decrypted = app.vernam_decrypt(encrypted, key)
                print(f"\nРасшифрованное сообщение: {decrypted}")

            except FileNotFoundError:
                print("Файл encrypted.txt не найден! Сначала зашифруйте сообщение.")

        elif choice == '4':
            # Информация о ключах
            if not os.path.exists("key_group.txt"):
                print("Сначала сгенерируйте группу ключей!")
                continue

            key_group = app.load_key_group()
            print(f"\nГруппа ключей ({len(key_group)} ключей):")
            print("-" * 60)
            for i, key in enumerate(key_group, 1):
                original, param = app.extract_original_key(key)
                print(f"Ключ {i:2d}: {key:15d} | Параметр: {param} | Исходный: {original}")

        elif choice == '5':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    main()