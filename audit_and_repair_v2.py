import os
import re

root_dir = "e:\\Durgesh work\\papery"

# List of all HTML files to know which links are internal
all_html_files = []
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            rel_path = os.path.relpath(os.path.join(root, file), root_dir).replace("\\", "/")
            all_html_files.append(rel_path)

def fix_html_content(file_rel_path, content):
    # 1. Fix data-root-path
    content = re.sub(r'data-root-path="[^"]*"', 'data-root-path="/"', content)
    
    # 2. Fix assets to absolute root
    content = re.sub(r'(src|href|poster)="(\.\./)*assets/', r'\1="/assets/', content)
    
    # 3. Fix internal links to absolute root
    # We'll look for href="something.html" or href="../something.html"
    # and if it corresponds to a file we know, we make it absolute.
    
    def link_replacer(match):
        prefix = match.group(1) # href="
        link = match.group(2)   # ../../about.html
        suffix = match.group(3) # "
        
        # If it's already absolute or external, don't touch
        if link.startswith("/") or link.startswith("http") or link.startswith("mailto") or link.startswith("tel") or link.startswith("#"):
            return match.group(0)
        
        # Calculate what this relative link would be from the current file
        file_dir = os.path.dirname(file_rel_path)
        # Handle cases like "about.html" or "../about.html"
        # We'll just check if it matches any of our known files
        
        # First, try to resolve it
        potential_path = os.path.normpath(os.path.join(file_dir, link)).replace("\\", "/")
        if potential_path in all_html_files:
            return f'{prefix}/{potential_path}{suffix}'
        
        # If not found, check if it's a known root page link without prefix
        root_pages = ["index.html", "about.html", "services.html", "products.html", "contact.html"]
        for rp in root_pages:
            if link == rp:
                return f'{prefix}/{rp}{suffix}'
        
        # Special case for folder-based links if any
        if link == "./" or link == "../":
            return f'{prefix}/{suffix}'
            
        return match.group(0)

    content = re.sub(r'(href=")([^"]+\.html|[^"]*/|[^"]*\.\.?/)(")', link_replacer, content)

    # 4. Fix specific broken paths found in audit
    content = content.replace('href="/services/', 'href="/service-list/')
    content = content.replace('href="/products/', 'href="/products-list/')
    
    # 5. Point missing pages to # (if they are in the navbar or somewhere)
    missing_pages = ["blog.html", "projects.html", "faqs.html", "404.html", "project-single.html", "service-single.html"]
    for mp in missing_pages:
        # If it's an absolute link to a missing page, point to #
        # Use word boundaries to avoid matching sub-parts
        content = re.sub(r'href="/' + re.escape(mp) + r'"', 'href="#"', content)
        # Also relative ones
        content = re.sub(r'href="' + re.escape(mp) + r'"', 'href="#"', content)

    return content

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, root_dir).replace("\\", "/")
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = fix_html_content(rel_path, content)
            
            if content != new_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Fixed {rel_path}")
