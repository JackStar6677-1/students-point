#!/usr/bin/env python
"""
Script para eliminar emojis de archivos
"""
import re
from pathlib import Path

def remove_emojis(text):
    """Elimina todos los emojis del texto"""
    # Patrón para emojis Unicode
    emoji_pattern = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251" 
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)

def process_file(filepath):
    """Procesa un archivo eliminando emojis"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = remove_emojis(content)
        
        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    except Exception as e:
        print(f"Error procesando {filepath}: {e}")
        return False

def main():
    base_dir = Path(__file__).resolve().parents[3]
    
    # Procesar archivos .md, .py, .js
    patterns = ['**/*.md', '**/*.py', '**/*.js']
    modified = 0
    
    for pattern in patterns:
        files = list(base_dir.glob(pattern))
        for filepath in files:
            if any(x in str(filepath) for x in ['node_modules', '.git', '__pycache__', 'remove_emojis.py']):
                continue
            if process_file(filepath):
                print(f"Procesado: {filepath.relative_to(base_dir)}")
                modified += 1
    
    print(f"\nTotal archivos modificados: {modified}")

if __name__ == '__main__':
    main()

