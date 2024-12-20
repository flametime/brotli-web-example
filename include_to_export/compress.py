import brotli
import os

def compress_file(input_path):
    if not os.path.exists(input_path):
        print(f"Файл {input_path} не найден")
        return
        
    with open(input_path, 'rb') as input_file:
        data = input_file.read()
        compressed = brotli.compress(data, quality=11)
        
    output_path = input_path + '.br'
    with open(output_path, 'wb') as output_file:
        output_file.write(compressed)
    print(f"Создан сжатый файл: {output_path}")
    
# Сжимаем оба файла
compress_file('index.wasm')
compress_file('index.pck')