import pandas as pd
import os
from pylibdmtx.pylibdmtx import encode
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import warnings

def extract_codes_from_excel():
    """Извлекает коды из Excel файла"""
    print("Извлечение кодов из Excel файла...")
    
    # Отключаем предупреждения при чтении Excel
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # Читаем Excel файл
        df = pd.read_excel(
            'src/file-181f58e4-fa35-446d-9ebb-e75dcd0c726d.xlsx',
            skiprows=1,
            dtype=str,  # Читаем все колонки как строки
            na_filter=False,  # Не интерпретируем пустые ячейки как NaN
            engine='openpyxl'  # Явно указываем движок
        )

    # Получаем первую колонку и очищаем данные
    codes = df.iloc[:, 0].astype(str).str.strip()
    
    # Выводим общее количество кодов
    print(f"Найдено кодов: {len(codes)}")
    
    return codes.tolist()

def generate_datamatrix(code):
    """Генерирует Data Matrix код и возвращает его как PIL Image"""
    # Кодируем данные в Data Matrix код
    encoded = encode(code.encode('utf-8'))
    
    # Конвертируем в PIL Image
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    
    # Увеличиваем размер изображения
    img = img.resize((encoded.width * 5, encoded.height * 5), Image.Resampling.NEAREST)
    
    return img

def create_pdf_with_codes(codes, label, output_filename='datamatrix_codes.pdf'):
    """Создает PDF файл с Data Matrix кодами на отдельных страницах"""
    # Создаем размер страницы 15x15 см
    page_size = (15 * cm, 15 * cm)
    
    # Создаем PDF canvas с пользовательским размером страницы
    c = canvas.Canvas(output_filename, pagesize=page_size)
    width, height = page_size
    
    # Вычисляем центральную позицию
    center_x = width / 2
    center_y = height / 2
    box_size = 14 * cm  # Немного меньше страницы, чтобы был отступ
    
    total_codes = len(codes)
    print("\nНачинаем генерацию PDF...")
    
    for index, code in enumerate(codes, 1):
        try:
            # Генерируем Data Matrix изображение
            img = generate_datamatrix(code)
            
            # Сохраняем изображение во временный файл
            temp_filename = f'temp_{hash(code)}.png'
            img.save(temp_filename)
            
            # Вычисляем позицию изображения для центрирования
            img_width, img_height = img.size
            scale = min(box_size / img_width, box_size / img_height)
            scaled_width = img_width * scale
            scaled_height = img_height * scale
            
            x = center_x - scaled_width / 2
            y = center_y - scaled_height / 2
            
            # Рисуем изображение
            c.drawImage(temp_filename, x, y, width=scaled_width, height=scaled_height)
            
            # Добавляем текст под кодом
            text_y = y - 0.2 * cm  # Уменьшаем отступ от кода до текста
            c.setFont("Helvetica", 30)  # Уменьшаем размер шрифта
            text_width = c.stringWidth(label, "Helvetica", 30)
            c.drawString(center_x - text_width/2, text_y, label)
            
            # Удаляем временный файл
            os.remove(temp_filename)
            
            # Добавляем новую страницу
            c.showPage()
            
            # Показываем прогресс
            progress = (index / total_codes) * 100
            print(f"\rПрогресс: {progress:.1f}% ({index}/{total_codes} кодов)", end="")
            
        except Exception as e:
            print(f"\nОшибка при генерации кода {code}: {str(e)}")
    
    # Сохраняем PDF
    c.save()
    print(f"\n\nPDF файл успешно создан: {output_filename}")

def main():
    # Запрашиваем текст для подписи
    label = input("Введите текст для подписи под кодом (например, 06.25/255): ")
    
    # Шаг 1: Извлекаем коды из Excel
    codes = extract_codes_from_excel()
    
    # Шаг 2: Генерируем PDF с кодами
    if codes:
        create_pdf_with_codes(codes, label)
        print("\nПроцесс успешно завершен!")
    else:
        print("Коды не были извлечены. Генерация PDF невозможна.")

if __name__ == "__main__":
    main() 