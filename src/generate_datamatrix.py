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
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from rich.panel import Panel
from rich import print as rprint
from rich.style import Style
from rich.text import Text
import glob

def find_excel_file():
    """Находит единственный Excel файл в текущей директории"""
    excel_files = glob.glob('*.xlsx')
    if len(excel_files) == 0:
        raise FileNotFoundError("Excel файл не найден в текущей директории")
    if len(excel_files) > 1:
        raise ValueError(f"Найдено несколько Excel файлов: {', '.join(excel_files)}. Оставьте только один файл.")
    return excel_files[0]

# Конфигурация
CONFIG = {
    # Путь к Excel файлу будет определен динамически
    'EXCEL_FILE': None,  # Будет установлено при запуске
    
    # Настройки PDF
    'PDF': {
        'PAGE_SIZE': (15 * cm, 15 * cm),  # Размер страницы
        'OUTPUT_FILENAME': 'datamatrix_codes.pdf',
        'BOX_SIZE': 14 * cm,  # Размер области для кода
        'TEXT_OFFSET': 0.2 * cm,  # Отступ текста от кода
        'FONT_SIZE': 30,  # Размер шрифта для подписи
        'FONT_NAME': 'Helvetica'
    },
    
    # Настройки DataMatrix
    'DATAMATRIX': {
        'SCALE_FACTOR': 5  # Множитель для увеличения размера кода
    }
}

# Инициализируем консоль rich
console = Console()

def extract_codes_from_excel():
    """Извлекает коды из Excel файла"""
    with console.status("[bold green]Извлечение кодов из Excel файла..."):
        # Отключаем предупреждения при чтении Excel
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Читаем Excel файл
            df = pd.read_excel(
                CONFIG['EXCEL_FILE'],
                skiprows=1,
                dtype=str,  # Читаем все колонки как строки
                na_filter=False,  # Не интерпретируем пустые ячейки как NaN
                engine='openpyxl'  # Явно указываем движок
            )

        # Получаем первую колонку и очищаем данные
        codes = df.iloc[:, 0].astype(str).str.strip()
        
        # Выводим общее количество кодов
        console.print(Panel(f"[bold green]Найдено кодов: {len(codes)}", title="Результат"))
        
        return codes.tolist()

def generate_datamatrix(code):
    """Генерирует Data Matrix код и возвращает его как PIL Image"""
    # Кодируем данные в Data Matrix код
    encoded = encode(code.encode('utf-8'))
    
    # Конвертируем в PIL Image
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    
    # Увеличиваем размер изображения
    img = img.resize((encoded.width * CONFIG['DATAMATRIX']['SCALE_FACTOR'], encoded.height * CONFIG['DATAMATRIX']['SCALE_FACTOR']), Image.Resampling.NEAREST)
    
    return img

def create_pdf_with_codes(codes, label, output_filename=CONFIG['PDF']['OUTPUT_FILENAME']):
    """Создает PDF файл с Data Matrix кодами на отдельных страницах"""
    # Создаем размер страницы
    page_size = CONFIG['PDF']['PAGE_SIZE']
    
    # Создаем PDF canvas с пользовательским размером страницы
    c = canvas.Canvas(output_filename, pagesize=page_size)
    width, height = page_size
    
    # Вычисляем центральную позицию
    center_x = width / 2
    center_y = height / 2
    box_size = CONFIG['PDF']['BOX_SIZE']  # Немного меньше страницы, чтобы был отступ
    
    total_codes = len(codes)
    console.print("\n[bold blue]Начинаем генерацию PDF...")
    
    # Создаем стилизованный прогресс
    progress_style = Style(color="cyan", bold=True)
    counter_style = Style(color="yellow", bold=True)
    
    with Progress(
        SpinnerColumn(style=progress_style),
        TextColumn("[progress.description]{task.description}", style=progress_style),
        BarColumn(complete_style=progress_style, finished_style="green"),
        TextColumn(
            "[progress.percentage]{task.percentage:>3.0f}%",
            style=progress_style
        ),
        TextColumn(
            "[progress.completed]{task.completed}/{task.total}",
            style=counter_style
        ),
        TimeRemainingColumn(),
        console=console,
        expand=True
    ) as progress:
        task = progress.add_task(
            "[cyan]Генерация кодов...",
            total=total_codes
        )
        
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
                text_y = y - CONFIG['PDF']['TEXT_OFFSET']
                c.setFont(CONFIG['PDF']['FONT_NAME'], CONFIG['PDF']['FONT_SIZE'])
                text_width = c.stringWidth(label, CONFIG['PDF']['FONT_NAME'], CONFIG['PDF']['FONT_SIZE'])
                c.drawString(center_x - text_width/2, text_y, label)
                
                # Удаляем временный файл
                os.remove(temp_filename)
                
                # Добавляем новую страницу
                c.showPage()
                
                # Обновляем прогресс
                progress.update(task, advance=1)
                
            except Exception as e:
                console.print(f"[bold red]Ошибка при генерации кода {code}: {str(e)}")
    
    # Сохраняем PDF
    c.save()
    console.print(Panel(
        f"[bold green]PDF файл успешно создан: {output_filename}",
        title="[bold green]Успех",
        border_style="green"
    ))

def main():
    try:
        # Определяем путь к Excel файлу
        CONFIG['EXCEL_FILE'] = find_excel_file()
        console.print(f"[bold green]Найден Excel файл: {CONFIG['EXCEL_FILE']}")
        
        # Запрашиваем текст для подписи
        label = console.input("[bold yellow]Введите текст для подписи под кодом (например, 06.25/255): ")
        
        # Шаг 1: Извлекаем коды из Excel
        codes = extract_codes_from_excel()
        
        # Шаг 2: Генерируем PDF с кодами
        if codes:
            create_pdf_with_codes(codes, label)
            console.print("\n[bold green]Процесс успешно завершен!")
        else:
            console.print("[bold red]Коды не были извлечены. Генерация PDF невозможна.")
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[bold red]Ошибка: {str(e)}")
    except Exception as e:
        console.print(f"[bold red]Произошла непредвиденная ошибка: {str(e)}")

if __name__ == "__main__":
    main() 