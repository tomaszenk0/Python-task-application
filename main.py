from pathlib import Path
import os
folder=Path("zadanie_3_logi")
empty_file=Path("zadanie_3_logi/raport_bledow.txt")
empty_file.touch(exist_ok=True)
for root, dirs, files in os.walk(folder):
    for file in files:
        if files == 'raport_bledow.txt':
            continue
        path = Path(root) / file
        context = path.read_text(encoding='utf-8').splitlines()

        for number, line in enumerate(context, start=1):
            if 'ERROR' in line:
                with open('zadanie_3_logi/raport_bledow.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{file}|{number}|{line}\n")




