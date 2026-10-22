# training_parsing_yap

Учебные парсеры данных о Python и пример argparse. Нужен Python 3.14.

В каталоге проекта создайте и активируйте окружение.

Windows PowerShell:
```powershell
py -3.14 -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux/macOS:
```bash
python3.14 -m venv venv
source venv/bin/activate
```

Установка и запуск:
```text
python -m pip install -r requirements.txt
python arg_parsing.py Stepan --murzik
python whats_new.py
python latest_versions.py
python download.py
```

Парсерам нужен интернет. Архив документации сохраняется в downloads.
