document.addEventListener("DOMContentLoaded", function () {
    const placeholder = document.getElementById("topbar-placeholder");
    if (!placeholder) return;

    const rootPath = placeholder.getAttribute("data-root-path") || "./";
    
    // Determine the path to the component file
    // If rootPath is "./", fetch("components/topbar.html") works
    // If rootPath is "../", fetch("../components/topbar.html") works
    fetch(rootPath + "components/topbar.html")
        .then(response => {
            if (!response.ok) throw new Error("Topbar not found");
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

            // 3. Fix href="contact.html" -> href="{rootPath}contact.html"
            // We only have one explicit internal link in the provided HTML: contact.html
            // But strict adherence says we check if there are others. 
            // In the provided HTML, only contact.html is an internal link.
            content = content.replace(/href="contact\.html"/g, `href="${rootPath}contact.html"`);

            // Inject
            placeholder.innerHTML = content;
            
        })
        .catch(err => console.error("Error loading topbar:", err));
});
