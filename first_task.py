from typing import List, Optional


def get_message_hex(message: str) -> list[str]:
    """
    Функция получает строку и переводит каждый символ в hex формат
    :param message: строка (в кириллице)
    :return: li[str],где li[i] = hex(message[i])
    """
    message_hex = []
    for c in message:
        c_ord = ord(c) - ord('А') + 192 if ord(c) > 200 else ord(c)  ## для кириллицы
        c_encoded = hex(c_ord)[2:].upper()
        message_hex.append(c_encoded)
    return message_hex


# def hex_to_message(ciphertext: list[str]):
#     for i in range(len(ciphertext)):
#         ciphertext[i] = chr(int(ciphertext[i], 16))
#     return ciphertext


def xor_algorithm(key: list[str], source_message: list[str]):
    """
    Функция криптоалгоритма (поэлементный xor)
    :param key: Гамма (список в формате hex) или шифротекст
    :param source_message: list(str) в hex формате
    :return: Шифротекст (шифробит = A XOR B)
    """
    res = []
    if len(key) != len(source_message):
        return 'length are not equal'

    for i in range(len(key)):
        key_symbol = key[i]
        key_symbol_int = int(key_symbol, 16)
        message_symbol = source_message[i]
        message_symbol_int = int(message_symbol, 16)
        cipher_smb = key_symbol_int ^ message_symbol_int  ## в формате '0xdd'
        cipher_smb_without_0x = hex(cipher_smb)[2:].upper()
        res.append(cipher_smb_without_0x if len(cipher_smb_without_0x) > 1 else '0' + cipher_smb_without_0x)
    return res


if __name__ == "__main__":
    center_key = '05 0C 17 7F 0E 4E 37 D2 94 10 09 2E 22 57 FF C8 0B B2 70 54'.split()
    center_message = 'Штирлиц - Вы Герой!!'
    center_message_hex = get_message_hex(center_message)
    ciphertext = xor_algorithm(center_key, center_message_hex)
    print(f"{ciphertext} - шифротекст при известном ключе и сообщении \"{center_message}\"")
    expected_message = 'СНовымГодом, друзья!'
    expected_message_hex = get_message_hex(expected_message)
    expected_key = xor_algorithm(ciphertext, expected_message_hex)
    print(f"{expected_key} - ключ по известному шифротексту и ожидаемому сообщению \"{expected_message}\"")
