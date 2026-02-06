import os

folder = 'products-list'
for f in os.listdir(folder):
    if f.endswith('.html'):
        path = os.path.join(folder, f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        new_content = content.replace('href="/services.html">products</a>', 'href="/products.html">products</a>')
        
        if content != new_content:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Fixed breadcrumb in {f}")
