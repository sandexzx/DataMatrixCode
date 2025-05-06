def main():
    try:
        # Определяем путь к Excel файлу
        CONFIG['EXCEL_FILE'] = find_excel_file()
        console.print(f"[bold green]Найден Excel файл: {CONFIG['EXCEL_FILE']}")
        
        # Запрашиваем размер страницы
        size_choice = console.input("[bold yellow]Выберите размер страницы (1 - 15x15 см, 2 - 15x15 мм): ")
        CONFIG['PDF']['USE_MM'] = size_choice == '2'
        
        # Запрашиваем текст для подписи
        label = console.input("[bold yellow]Введите текст для подписи под кодом (например, 06.25/255): ")
        
        # Шаг 1: Извлекаем коды из Excel
        codes = extract_codes_from_excel()
        
        # В режиме отладки ограничиваем количество кодов
        if CONFIG['DEBUG']['ENABLED']:
            codes = codes[:CONFIG['DEBUG']['MAX_PAGES']]
            console.print(f"[bold yellow]Режим отладки: будет сгенерировано {len(codes)} страниц")
        
        # Шаг 2: Генерируем PDF с кодами
        if codes:
            create_pdf_with_codes(codes, label)
            console.print("\n[bold green]Процесс успешно завершен!")
        else:
            console.print("[bold red]Коды не были извлечены. Генерация PDF невозможна.")
    except Exception as e:
        console.print(f"[bold red]Ошибка: {e}")

def find_excel_file():
    # Implementation of find_excel_file function
    pass

def extract_codes_from_excel():
    # Implementation of extract_codes_from_excel function
    pass

def create_pdf_with_codes(codes, label):
    # Implementation of create_pdf_with_codes function
    pass 