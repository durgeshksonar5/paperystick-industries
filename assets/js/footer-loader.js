document.addEventListener("DOMContentLoaded", function () {
  const placeholder = document.getElementById("footer-placeholder");
  if (!placeholder) return;

  const rootPath = placeholder.getAttribute("data-root-path") || "./";

  fetch(rootPath + "components/footer.html")
    .then((response) => {
      if (!response.ok) throw new Error("Footer not found");
      return response.text();
    })
    .then((html) => {
      // Adjust paths
      let content = html;

      // 1. Fix src="assets/..." -> src="{rootPath}assets/..."
      content = content.replace(/src="assets\//g, `src="${rootPath}assets/`);

      // 2. Fix href="./" -> href="{rootPath}"
      content = content.replace(/href="\.\/"/g, `href="${rootPath}"`);

      // 3. Fix href="page.html" -> href="{rootPath}page.html"
      const pages = [
        "about.html",
        "services.html",
        "blog.html",
        "projects.html",
        "products.html",
        "contact.html",
        "index.html",
        "index-video.html",
        "index-slider.html",
        "service-single.html",
        "blog-single.html",
        "project-single.html",
        "team.html",
        "team-single.html",
        "pricing.html",
        "testimonial.html",
        "image-gallery.html",
        "video-gallery.html",
        "faqs.html",
        "404.html",
      ];

      pages.forEach((page) => {
        // specific regex to replace exact matches or matches with query params/anchors if needed,
        // but usually just href="page.html" is what we want.
        // We use "g" to replace all occurrences.
        const re = new RegExp(`href="${page}"`, "g");
        content = content.replace(re, `href="${rootPath}${page}"`);
      });

      // Inject
      placeholder.innerHTML = content;

      // Initialize Scroll Up Button
      const scrollUp = document.getElementById("scroll-up");
      if (scrollUp) {
        window.addEventListener("scroll", () => {
          if (window.scrollY > 300) {
            scrollUp.classList.add("show");
          } else {
            scrollUp.classList.remove("show");
          }
        });

        scrollUp.addEventListener("click", () => {
          window.scrollTo({
            top: 0,
            behavior: "smooth",
          });
        });
      }
    })
    .catch((err) => console.error("Error loading footer:", err));
});
