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
        border-radius: 5px;
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
    }
    .book .author {
        font-size: 12px;
        margin-top: 5px;
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
        padding: 8px 8px;
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
                    <div class="badges-group-label">Gender</div>
                    <div class="badges-list" id="gender-badges"></div>
                    <button id="add-gender-btn" class="add-filter-btn">+ Add Gender</button>
                </div>
            </div>
            <div id="gender-dropdown" class="filter-dropdown" style="display: none;"></div>
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
    const addGenderBtn = document.getElementById('add-gender-btn');
    const genderDropdown = document.getElementById('gender-dropdown');
    const drawButton = document.getElementById('draw-button');
    const modal = document.getElementById('modal-overlay');
    const modalClose = document.querySelector('.modal-close');
    const tooltip = document.getElementById('book-tooltip');

    let booksData = [];
    let selectedFilters = { gender: [] };
    let availableFilters = { gender: [] };

    // Load data
    d3.csv('/data/bookshelf2.csv').then(data => {
        booksData = data;
        console.log(booksData);
        populateAvailableFilters();
        setupDropdowns();
        drawBooks();
    }).catch(error => {
        console.error('Error loading the CSV file:', error);
    });

    function populateAvailableFilters() {
        availableFilters.gender = [...new Set(booksData.flatMap(d => d.gender ? d.gender.split(';').map(g => g.trim()) : []).filter(g => g))];
    }

    function getGenderLabel(gender) {
        return gender === 'm' ? 'Male' : (gender === 'w' ? 'Female' : 'Other');
    }

    function setupDropdowns() {
        // Gender dropdown
        availableFilters.gender.forEach(gender => {
            const item = document.createElement('div');
            item.classList.add('filter-dropdown-item');
            item.textContent = getGenderLabel(gender);
            item.dataset.value = gender;
            item.dataset.type = 'gender';
            item.addEventListener('click', () => addFilter('gender', gender, getGenderLabel(gender)));
            genderDropdown.appendChild(item);
        });
    }

    function toggleDropdown(dropdown, btn) {
        if (dropdown.style.display === 'none') {
            dropdown.style.display = 'block';

            // Position dropdown below button relative to controls-container
            const btnRect = btn.getBoundingClientRect();
            const containerRect = document.querySelector('.controls-container').getBoundingClientRect();
            dropdown.style.top = (btnRect.bottom - containerRect.top + 5) + 'px';
            dropdown.style.left = (btnRect.left - containerRect.left) + 'px';
        } else {
            dropdown.style.display = 'none';
        }
    }

    function addFilter(type, value, label) {
        if (!selectedFilters[type].includes(value)) {
            selectedFilters[type].push(value);
            renderBadges();
            drawBooks();
        }
        // Hide dropdown
        genderDropdown.style.display = 'none';
    }

    function removeFilter(type, value) {
        selectedFilters[type] = selectedFilters[type].filter(v => v !== value);
        renderBadges();
        drawBooks();
    }

    function renderBadges() {
        const genderBadgesContainer = document.getElementById('gender-badges');
        genderBadgesContainer.innerHTML = '';

        if (selectedFilters.gender.length == 0) {
            const badge = document.createElement('div');
            badge.classList.add('badge');
            badge.innerHTML = `All genders`;
            genderBadgesContainer.appendChild(badge);
        }

        selectedFilters.gender.forEach(gender => {
            const badge = document.createElement('div');
            badge.classList.add('badge');
            const label = getGenderLabel(gender);
            badge.innerHTML = `${label}<span class="badge-delete">×</span>`;
            badge.querySelector('.badge-delete').addEventListener('click', () => removeFilter('gender', gender));
            genderBadgesContainer.appendChild(badge);
        });
    }

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

        const author = document.createElement('div');
        author.classList.add('author');
        author.textContent = bookData.author;

        bookElement.appendChild(title);
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
            if (selectedFilters.gender.length > 0) {
                filteredData = filteredData.filter(d => d.gender && selectedFilters.gender.some(g => d.gender.includes(g)));
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
    addGenderBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleDropdown(genderDropdown, addGenderBtn);
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', () => {
        genderDropdown.style.display = 'none';
    });

    // Modal close button
    modalClose.addEventListener('click', closeModal);

    // Close modal when clicking outside the modal content
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });

    drawButton.addEventListener('click', drawBooks);
    renderBadges();
});
</script>
{{< /rawhtml >}}