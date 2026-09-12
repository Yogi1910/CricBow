document.addEventListener("DOMContentLoaded", function () {
    const readMoreButtons = document.querySelectorAll('.read-more-button');

    readMoreButtons.forEach(button => {
        button.addEventListener("click", () => {
            const articleContainer = button.closest('.article-container');
            const articleContent = articleContainer.querySelector('.article-content');
            const articleExcerpt = articleContent.querySelector('.article-excerpt');
            const articleFull = articleContent.querySelector('.article-full');

            articleContent.classList.toggle('expanded');
            if (articleContent.classList.contains('expanded')) {
                button.textContent = 'Read Less';
                articleExcerpt.style.display = 'none';
                articleFull.style.display = 'block';
            } else {
                button.textContent = 'Read More';
                articleExcerpt.style.display = 'block';
                articleFull.style.display = 'none';
            }
        });
    });

    const excerpts = document.querySelectorAll('.article-excerpt p');
    const maxExcerptLines = 2; // Set the maximum number of lines for the excerpt

    excerpts.forEach(excerpt => {
        const lines = excerpt.textContent.trim().split('\n').filter(line => line.trim() !== '');
        excerpt.innerHTML = lines.slice(0, maxExcerptLines).join('\n');
    });
});
