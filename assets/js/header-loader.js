document.addEventListener("DOMContentLoaded", function () {
    const placeholder = document.getElementById("header-placeholder");
    if (!placeholder) return;

    const rootPath = placeholder.getAttribute("data-root-path") || "./";
    
    fetch(rootPath + "components/header.html")
        .then(response => {
            if (!response.ok) throw new Error("Header not found");
            return response.text();
        })
        .then(html => {
            // Adjust paths
            let content = html;

            // 1. Fix src="assets/..." -> src="{rootPath}assets/..."
            content = content.replace(/src="assets\//g, `src="${rootPath}assets/`);

            // 2. Fix href="./" -> href="{rootPath}"
            // Note: Replace exactly href="./"
            content = content.replace(/href="\.\/"/g, `href="${rootPath}"`);

            // 3. Fix href="page.html" -> href="{rootPath}page.html"
            // List of known pages in the header
            const pages = [
                "about.html", "services.html", "blog.html", "projects.html", "contact.html", 
                "index.html", "index-video.html", "index-slider.html", 
                "service-single.html", "blog-single.html", "project-single.html", 
                "team.html", "team-single.html", "pricing.html", "testimonial.html", 
                "image-gallery.html", "video-gallery.html", "faqs.html", "404.html"
            ];
            
            pages.forEach(page => {
                 const re = new RegExp(`href="${page}"`, "g");
                 content = content.replace(re, `href="${rootPath}${page}"`);
            });

            // Inject
            placeholder.innerHTML = content;
            
            // Re-initialize SlickNav (Mobile Menu)
            // The original logic is: $('#menu').slicknav({...});
            // We need to check if jQuery and Slicknav are available
            if (window.jQuery && window.jQuery.fn.slicknav) {
                window.jQuery('#menu').slicknav({
                    label: '',
                    prependTo: '.responsive-menu'
                });
            }
            
            // Re-initialize Sticky Header logic if necessary
            // The original logic binds to window scroll, but it sets size on resize.
            // It relies on 'header.main-header' existing.
            // Since we just injected it, we might need to manually trigger a 'resize' or 'scroll' event 
            // to ensure accurate heights are calculated immediately.
            
            setTimeout(() => {
                window.dispatchEvent(new Event('resize'));
            }, 100);

        })
        .catch(err => console.error("Error loading header:", err));
});
