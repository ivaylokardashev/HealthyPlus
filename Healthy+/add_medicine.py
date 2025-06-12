from database import QRDatabase  # или каквото е името на твоя файл с класа

def main():
    db = QRDatabase()

    print("Въвеждане на нов продукт в базата данни.")
    qrcode = input("Въведи QR код (уникален ключ): ")
    name = input("Въведи име на продукта: ")
    ingredients = input("Въведи съставки: ")

    db.add_item(qrcode, name, ingredients)
    print("Данните са добавени успешно!")

if __name__ == "__main__":
    main()
