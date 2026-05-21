---
title: "Bestsellers by Women Authors"
date: 2026-05-06
description: "Explore 16,000+ bestselling books by female authors with interactive tiles"
---

{{< rawhtml >}}
<style>
    .max-w-prose:has(> .bookshelf-body) {
        max-width: 100%;
    }

    .bookshelf-body {
        font-family: sans-serif;
        display: flex;
        justify-content: center;
        align-items: flex-start;
        padding: 20px;
        /* width: 80vw;
        position: relative;
        left: calc(-40vw + 50%); */
    }

    .bookshelf-container-wrapper {
        display: flex;
        width: 100%;
        max-width: 1200px;
        gap: 20px;
    }

    .bookshelf-container {
        flex: 3;
        display: flex;
        flex-direction: column;
        gap: 50px; /* Increased gap to simulate shelves being further apart */
    }

    .shelf-box {
        height: 200px;
        width: 100%;
        display: flex;
        flex-direction: column;
        /* background: blue; */
    }

    .shelf {
        background-color: #846358;
        height: 20px;
        padding: 10px;
        border-radius: 5px;
        border-top: 7px solid #a18072;
    }

    .book-container {
        height: 180px;
        display: flex;
        align-items: flex-end;
        justify-content: space-around;
    }

    .book {
        background-color: #a78bfa;
        width: 100px;
        height: 160px;
        border-radius: 2px;
        position: relative;
        padding: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    .book .title {
        text-align: center;
        font-weight: bold;
        font-size: 12px;
        user-select: none;
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 3;
        overflow: hidden;
        background: #fafafa;
        padding: 4px;
        border-radius: 5px;
    }

    .book hr {
        margin-top: 5px;
        margin-bottom: 5px;
        margin-right: 10px;
        margin-left: 10px;
        border: 1px solid #4b4b4b;
    }
    .book .author {
        font-size: 12px;
        text-align: center;
        user-select: none;
    }

    .controls-container {
        flex: 1;
        padding: 20px;
        background-color: #fff;
        border-radius: 5px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        position: relative;
    }

    .filter-title {
        margin-top: 0px;
        margin-bottom: 10px;
    }

    .filters {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-bottom: 20px;
    }

    .filter-group {
        display: flex;
        flex-direction: column;
    }

    #draw-button {
        width: 100%;
        padding: 10px;
        background-color: #e53935;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }

    #draw-button:hover {
        background-color: #c62828;
    }

    #gender-filter {
        padding: 10px;
        border-radius: 5px;
    }

    .badges-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-bottom: 20px;
    }

    .badges-group {
        display: flex;
        flex-direction: column;
        gap: 8px;
        position: relative;
    }

    .badges-group-label {
        font-size: 12px;
        font-weight: 600;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .badges-list {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        min-height: 28px;
        align-content: flex-start;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #a78bfa;
        color: white;
        padding: 2px 9px;
        border-radius: 5px;
        font-size: 14px;
        white-space: nowrap;
    }

    .badge-delete {
        cursor: pointer;
        font-size: 16px;
        line-height: 1;
        opacity: 0.8;
        transition: opacity 0.2s;
    }

    .badge-delete:hover {
        opacity: 1;
    }

    .add-filter-container {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-bottom: 20px;
    }

    .add-filter-btn {
        width: fit-content;
        padding: 6px 6px;
        background-color: #f5f5f5;
        border: 2px solid #ddd;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
        transition: all 0.2s;
        text-align: left;
    }

    .add-filter-btn:hover {
        border-color: #a78bfa;
        background-color: #fafafa;
    }

    .rating-buttons {
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
    }

    .rating-btn {
        padding: 6px 6px;
        background-color: #f5f5f5;
        border: 2px solid #ddd;
        border-radius: 5px;
        cursor: pointer;
        font-size: 13px;
        transition: all 0.2s;
    }

    .rating-btn:hover {
        border-color: #a78bfa;
        background-color: #fafafa;
    }

    .rating-btn.active {
        background-color: #a78bfa;
        color: white;
        border-color: #a78bfa;
    }

    .language-buttons {
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
    }

    .language-btn {
        padding: 6px 6px;
        background-color: #f5f5f5;
        border: 2px solid #ddd;
        border-radius: 5px;
        cursor: pointer;
        font-size: 13px;
        transition: all 0.2s;
    }

    .language-btn:hover {
        border-color: #a78bfa;
        background-color: #fafafa;
    }

    .language-btn.active {
        background-color: #a78bfa;
        color: white;
        border-color: #a78bfa;
    }

    .filter-dropdown {
        position: absolute;
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        min-width: 150px;
        max-height: 300px;
        overflow-y: auto;
    }

    .filter-dropdown-item {
        padding: 10px 15px;
        cursor: pointer;
        transition: background-color 0.2s;
        border-bottom: 1px solid #f0f0f0;
    }

    .filter-dropdown-item:last-child {
        border-bottom: none;
    }

    .filter-dropdown-item:hover {
        background-color: #f9f9f9;
    }

    .filter-dropdown-item.selected {
        background-color: #e8f5e9;
        font-weight: 500;
    }

    .filters-content {
        position: relative;
    }

    .book-tooltip {
        position: fixed;
        display: none;
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        font-size: 12px;
        z-index: 100;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        width: 200px;
        pointer-events: none;
    }

    .book-tooltip.visible {
        display: block;
    }

    .tooltip-title {
        font-weight: 600;
        margin-bottom: 6px;
        color: #333;
    }

    .tooltip-item {
        margin-bottom: 6px;
        font-size: 11px;
    }

    .tooltip-label {
        font-weight: 500;
        color: #666;
        font-size: 10px;
        text-transform: uppercase;
    }

    .tooltip-value {
        color: #333;
        margin-top: 2px;
    }

    .tooltip-rating {
        font-weight: 600;
        color: #ff9800;
    }

    .tooltip-genre {
        display: inline-block;
        background-color: #e8e8e8;
        padding: 2px 6px;
        border-radius: 2px;
        margin-right: 4px;
        margin-bottom: 3px;
        font-size: 10px;
    }

    .modal-overlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0,0,0,0.5);
        z-index: 1000;
    }

    .modal-overlay.visible {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .modal-content {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        padding: 24px;
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        position: relative;
    }

    .modal-close {
        position: absolute;
        top: 0px;
        right: 16px;
        background: none;
        border: none;
        font-size: 24px;
        cursor: pointer;
        color: #666;
    }

    .modal-close:hover {
        color: #333;
    }

    .modal-title {
        font-weight: 700;
        font-size: 20px;
        margin-bottom: 12px;
        color: #333;
    }

    .modal-field {
        margin-bottom: 16px;
    }

    .modal-field:last-child {
        margin-bottom: 0;
    }

    .modal-label {
        font-weight: 600;
        color: #666;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    .modal-value {
        color: #333;
    }

    .modal-rating {
        font-weight: 600;
        color: #ff9800;
        font-size: 16px;
    }

    .modal-description {
        line-height: 1.6;
        color: #444;
    }

    .modal-genre {
        display: inline-block;
        background-color: #a78bfa;
        color: white;
        padding: 4px 10px;
        border-radius: 3px;
        margin-right: 6px;
        margin-bottom: 6px;
        font-size: 12px;
    }
</style>

<div class="bookshelf-body">
    <div class="bookshelf-container-wrapper">
        <div class="bookshelf-container">
            <div class="shelf-box">
                <div class="book-container"></div>
                <div class="shelf"></div>
            </div>
            <div class="shelf-box">
                <div class="book-container"></div>
                <div class="shelf"></div>
            </div>
            <div class="shelf-box">
                <div class="book-container"></div>
                <div class="shelf"></div>
            </div>
        </div>
        <div class="controls-container">
            <h2 class="filter-title">Filters</h2>
            <div id="badges-container" class="badges-container">
                <div class="badges-group">
                    <div class="badges-group-label">Rating ⭐</div>
                    <div class="rating-buttons">
                        <button class="rating-btn" data-rating="0">All</button>
                        <button class="rating-btn" data-rating="3">3+</button>
                        <button class="rating-btn" data-rating="3.5">3.5+</button>
                        <button class="rating-btn" data-rating="4">4+</button>
                        <button class="rating-btn" data-rating="4.5">4.5+</button>
                    </div>
                </div>
                <div class="badges-group">
                    <div class="badges-group-label">Language</div>
                    <div class="badges-list" id="language-badges"></div>
                    <button id="add-language-btn" class="add-filter-btn">+ Select language</button>
                    <div id="language-dropdown" class="filter-dropdown" style="display: none;"></div>
                </div>
            </div>
            <button id="draw-button">Draw new books!</button>
        </div>
    </div>
</div>

<div id="book-tooltip" class="book-tooltip"></div>

<div id="modal-overlay" class="modal-overlay">
    <div class="modal-content">
        <button class="modal-close">×</button>
        <div id="modal-body"></div>
    </div>
</div>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
    const bookContainers = document.querySelectorAll('.book-container');
    const drawButton = document.getElementById('draw-button');
    const modal = document.getElementById('modal-overlay');
    const modalClose = document.querySelector('.modal-close');
    const tooltip = document.getElementById('book-tooltip');
    const addLanguageBtn = document.getElementById('add-language-btn');
    const languageDropdown = document.getElementById('language-dropdown');

    let booksData = [];
    let selectedFilters = { rating: 0, languages: [] };
    let availableLanguages = [];

    // Load data
    d3.csv('/data/bookshelf2.csv').then(data => {
        booksData = data;

        // Extract available languages only for female authors
        availableLanguages = [...new Set(
            booksData
                .filter(d => d.gender === 'w')
                .map(d => d.language)
                .filter(l => l)
        )].sort();

        setupRatingButtons();
        setupLanguageDropdown();
        drawBooks();
    }).catch(error => {
        console.error('Error loading the CSV file:', error);
    });

    function getRandomBooks(filteredData, count) {
        const shuffled = filteredData.sort(() => 0.5 - Math.random());
        return shuffled.slice(0, count);
    }

    function renderBook(bookData) {
        const bookElement = document.createElement('div');
        bookElement.classList.add('book');

        const title = document.createElement('div');
        title.classList.add('title');
        title.textContent = bookData.title;

        const separator = document.createElement('hr');

        const author = document.createElement('div');
        author.classList.add('author');
        author.textContent = bookData.author;

        bookElement.appendChild(title);
        bookElement.appendChild(separator);
        bookElement.appendChild(author);

        const colors = ['#dcd6fd', '#a78bfa', '#c4b5fd'];
        bookElement.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        bookElement.style.height = `${140 + (Math.random() * 25)}px`;
        bookElement.style.width = `${100 + (Math.random() * 20)}px`;

        // Add hover listeners for tooltip
        bookElement.addEventListener('mouseenter', (e) => showBookTooltip(bookData, e));
        bookElement.addEventListener('mouseleave', hideBookTooltip);

        // Add click listener for modal
        bookElement.addEventListener('click', () => showBookModal(bookData));
        bookElement.style.cursor = 'pointer';

        return bookElement;
    }

    function showBookTooltip(bookData, event) {
        let genresArray = [];

        if (bookData.genres) {
            try {
                const jsonString = bookData.genres.replace(/'/g, '"');
                genresArray = JSON.parse(jsonString);
            } catch (e) {
                genresArray = [];
            }
        }

        tooltip.innerHTML = `
            <div class="tooltip-title">${bookData.title}</div>
            <div class="tooltip-item">
                <div class="tooltip-label">Author</div>
                <div class="tooltip-value">${bookData.author}</div>
            </div>
            <div class="tooltip-item">
                <div class="tooltip-label">Rating</div>
                <div class="tooltip-value tooltip-rating">⭐ ${bookData.rating}</div>
            </div>
            <div class="tooltip-item">
                <div class="tooltip-label">Genres</div>
                <div class="tooltip-value">
                    ${genresArray.map(g => `<span class="tooltip-genre">${g}</span>`).join('')}
                </div>
            </div>
        `;

        // Position tooltip near the book
        const mouseX = event.clientX;
        const mouseY = event.clientY;
        tooltip.style.left = (mouseX + 10) + 'px';
        tooltip.style.top = (mouseY + 10) + 'px';
        tooltip.classList.add('visible');
    }

    function hideBookTooltip() {
        tooltip.classList.remove('visible');
    }

    function showBookModal(bookData) {
        let genresArray = [];

        if (bookData.genres) {
            try {
                const jsonString = bookData.genres.replace(/'/g, '"');
                genresArray = JSON.parse(jsonString);
            } catch (e) {
                genresArray = [];
            }
        }

        const modalBody = document.getElementById('modal-body');
        modalBody.innerHTML = `
            <div class="modal-title">${bookData.title}</div>
            <div class="modal-field">
                <div class="modal-label">Author</div>
                <div class="modal-value">${bookData.author}</div>
            </div>
            <div class="modal-field">
                <div class="modal-label">Rating</div>
                <div class="modal-value modal-rating">⭐ ${bookData.rating}</div>
            </div>
            <div class="modal-field">
                <div class="modal-label">Language</div>
                <div class="modal-value">${bookData.language}</div>
            </div>
            <div class="modal-field">
                <div class="modal-label">Genres</div>
                <div class="modal-value">
                    ${genresArray.map(g => `<span class="modal-genre">${g}</span>`).join('')}
                </div>
            </div>
            <div class="modal-field">
                <div class="modal-label">Description</div>
                <div class="modal-value modal-description">${bookData.description || 'No description available'}</div>
            </div>
        `;

        modal.classList.add('visible');
    }

    function closeModal() {
        modal.classList.remove('visible');
    }

    function drawBooks() {
        const oldBooks = document.querySelectorAll('.book');
        const animationPromises = [];

        // Animate out old books
        oldBooks.forEach(book => {
            const promise = new Promise(resolve => {
                book.style.transition = 'transform 0.5s ease-in';
                book.style.transform = 'translateY(1000px)';
                book.addEventListener('transitionend', () => {
                    book.remove();
                    resolve();
                }, { once: true });
            });
            animationPromises.push(promise);
        });

        Promise.all(animationPromises).then(() => {
            bookContainers.forEach(container => container.innerHTML = '');

            let filteredData = booksData;

            // Hardcoded: filter by female authors
            filteredData = filteredData.filter(d => d.gender === 'w');

            // Filter by minimum rating
            if (selectedFilters.rating > 0) {
                filteredData = filteredData.filter(d => {
                    const rating = parseFloat(d.rating);
                    return rating >= selectedFilters.rating;
                });
            }

            // Filter by language
            if (selectedFilters.languages.length > 0) {
                filteredData = filteredData.filter(d => selectedFilters.languages.includes(d.language));
            }

            const randomBooks = getRandomBooks(filteredData, 15);

            randomBooks.forEach((book, index) => {
                const shelfIndex = Math.floor(index / 5);
                const bookElement = renderBook(book);

                bookElement.style.transform = 'translateY(-1000px)';
                bookElement.style.transition = 'transform 0.8s ease-out';

                if (bookContainers[shelfIndex]) {
                    bookContainers[shelfIndex].appendChild(bookElement);
                }

                setTimeout(() => {
                    bookElement.style.transform = 'translateY(0)';
                }, 50 * index);
            });
        });
    }

    // Event listeners

    // Rating buttons
    function setupRatingButtons() {
        document.querySelectorAll('.rating-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const rating = parseFloat(btn.dataset.rating);
                selectedFilters.rating = rating;

                // Update active button
                document.querySelectorAll('.rating-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                drawBooks();
            });
        });

        // Set initial active button (All Ratings)
        document.querySelector('[data-rating="0"]').classList.add('active');
    }

    // Language badge rendering and filtering
    function renderLanguageBadges() {
        const languageBadgesContainer = document.getElementById('language-badges');
        languageBadgesContainer.innerHTML = '';

        console.log(2);
        if (selectedFilters.languages.length === 0) {
            const badge = document.createElement('div');
            badge.classList.add('badge');
            badge.innerHTML = `All languages`;
            languageBadgesContainer.appendChild(badge);
        }

        selectedFilters.languages.forEach(language => {
            const badge = document.createElement('div');
            badge.classList.add('badge');
            badge.innerHTML = `${language}<span class="badge-delete">×</span>`;
            badge.querySelector('.badge-delete').addEventListener('click', () => removeLanguageFilter(language));
            languageBadgesContainer.appendChild(badge);
        });
    }

    function addLanguageFilter(language) {
        if (!selectedFilters.languages.includes(language)) {
            selectedFilters.languages.push(language);
            renderLanguageBadges();
            drawBooks();
        }
        languageDropdown.style.display = 'none';
    }

    function removeLanguageFilter(language) {
        selectedFilters.languages = selectedFilters.languages.filter(l => l !== language);
        renderLanguageBadges();
        drawBooks();
    }

    function toggleLanguageDropdown() {
        if (languageDropdown.style.display === 'none') {
            languageDropdown.style.display = 'block';
        } else {
            languageDropdown.style.display = 'none';
        }
    }

    function setupLanguageDropdown() {
        // Populate dropdown with available languages
        availableLanguages.forEach(language => {
            const item = document.createElement('div');
            item.classList.add('filter-dropdown-item');
            item.textContent = language;
            item.addEventListener('click', () => addLanguageFilter(language));
            languageDropdown.appendChild(item);
        });
    }

    // Modal close button
    modalClose.addEventListener('click', closeModal);

    // Close modal when clicking outside the modal content
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Language button toggle
    addLanguageBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleLanguageDropdown();
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', () => {
        languageDropdown.style.display = 'none';
    });

    drawButton.addEventListener('click', drawBooks);
    renderLanguageBadges();
});
</script>
{{< /rawhtml >}}