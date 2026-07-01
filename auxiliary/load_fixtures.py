import sys
import os
import django
from pathlib import Path
from django.core.management import call_command

base_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(base_dir))
os.chdir(base_dir)

from auxiliary.constants import FIXTURES_DICT

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_22.settings')
django.setup()

FIXTURES_DIR = base_dir / 'fixtures'
os.makedirs(FIXTURES_DIR, exist_ok=True)

for key, value in FIXTURES_DICT.items():
    file_path = os.path.join(FIXTURES_DIR, key)
    if not os.path.exists(file_path):
        print(f'Файл {key} не найден, пропускаю.')
        continue
    print(f'Загружаю {key}...')
    call_command('loaddata', file_path)
