import os
import re

def fix_html_content(content):
    # Assets (src and href)
    content = re.sub(r'(src|href|poster)="(\.\./)?assets/', r'\1="/assets/', content)
    
    # Internal Page Links
    # Root pages
    pages = ["index.html", "about.html", "services.html", "products.html", "contact.html"]
    for page in pages:
        # Match "page.html" or "../page.html"
        content = re.sub(r'href="(\.\./)?' + re.escape(page) + r'"', f'href="/{page}"', content)
    
    # Home link href="./" or href="../"
    content = re.sub(r'href="\.\.?/"', 'href="/"', content)
    
    # Specific folder fixes
    # href="services/page.html" -> href="/service-list/page.html"
    # href="../services/page.html" -> href="/service-list/page.html"
    content = re.sub(r'href="(\.\./)?services/', 'href="/service-list/', content)
    
    # href="products/page.html" -> href="/products-list/page.html"
    # href="../products/page.html" -> href="/products-list/page.html"
    content = re.sub(r'href="(\.\./)?products/', 'href="/products-list/', content)
    
    # Ensure all href="/service-list/..." and href="/products-list/..." are absolute
    # (The above regex already does it, but let's be double sure)
    
    # Fix any existing partial absolute paths that might be mixed
    # e.g. href="/services/..." -> href="/service-list/..."
    content = content.replace('href="/services/', 'href="/service-list/')
    content = content.replace('href="/products/', 'href="/products-list/')
    
    return content

root_dir = "e:\\Durgesh work\\papery"
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            print(f"Processing {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = fix_html_content(content)
            
            if content != new_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Fixed {file_path}")
