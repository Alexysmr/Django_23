
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

FIXTURES_DIR = base_dir/'fixtures'
os.makedirs(FIXTURES_DIR, exist_ok=True)

for key, value in FIXTURES_DICT.items():
    print(f'Создаю фикстуру {key}...')
    with open(os.path.join(FIXTURES_DIR, key), 'w', encoding='utf-8') as f:
        call_command(
            'dumpdata',
            *value,
            '--exclude', 'contenttypes',
            '--indent', '2',
            stdout=f
        )

print('Фикстуры созданы в папке fixtures/')