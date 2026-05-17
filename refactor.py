import os
import re

src_dir = r'src/views'

for filename in os.listdir(src_dir):
    if filename.endswith('.vue'):
        filepath = os.path.join(src_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if "fetch('/api/" in content or "fetch(`/api/" in content:
            if "import { API_BASE_URL }" not in content:
                content = re.sub(r'<script setup>', "<script setup>\nimport { API_BASE_URL } from '../api/config.js';", content, count=1)
            
            # Replace fetch(`/api/...`) -> fetch(`${API_BASE_URL}/api/...`)
            content = content.replace("fetch(`/api/", "fetch(`${API_BASE_URL}/api/")
            
            # Replace fetch('/api/...') -> fetch(`${API_BASE_URL}/api/...`)
            content = re.sub(r"fetch\('/api/(.*?)'\)", r"fetch(`${API_BASE_URL}/api/\1`)", content)
            
            # Replace fetch('/api/...', { ... }) -> fetch(`${API_BASE_URL}/api/...`, { ... })
            content = re.sub(r"fetch\('/api/(.*?)',\s*\{", r"fetch(`${API_BASE_URL}/api/\1`, {", content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

print("Refactoring complete.")
