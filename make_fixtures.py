import subprocess
import sys
import os


fixtures_dir = os.path.join('catalog', 'fixtures')
os.makedirs(fixtures_dir, exist_ok=True)

commands = [
    ['catalog.Category', 'category_data.json'],
    ['catalog.Product', 'product_data.json']
]

for model, filename in commands:
    print(f'Создаю фикстуру для {model}...')
    cmd = [sys.executable, 'manage.py', 'dumpdata', model, '--indent', '2']

    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

    if result.returncode != 0:
        print(f'Ошибка при дампе {model}:', result.stderr)
        continue

    filepath = os.path.join(fixtures_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result.stdout)

    print(f'Файл сохранён: {filepath}')

print('Готово!')
