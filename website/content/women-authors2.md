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

    .book-info-box {
        display: none;
        margin-top: 15px;
        padding: 12px;
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 5px;
        font-size: 13px;
        line-height: 1.4;
    }

    .book-info-box.visible {
        display: block;
    }

    .book-info-title {
        font-weight: 600;
        margin-bottom: 8px;
        color: #333;
    }

    .book-info-item {
        margin-bottom: 8px;
    }

    .book-info-item:last-child {
        margin-bottom: 0;
    }

    .book-info-label {
        font-weight: 500;
        color: #666;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }

    .book-info-value {
        color: #333;
        margin-top: 3px;
    }

    .book-info-rating {
        font-weight: 600;
        color: #ff9800;
    }

    .book-genre {
        display: inline-block;
        background-color: #e8e8e8;
        padding: 3px 8px;
        border-radius: 3px;
        margin-right: 5px;
        margin-bottom: 5px;
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
                <div class="badges-group">
                    <div class="badges-group-label">Origin</div>
                    <div class="badges-list" id="origin-badges"></div>
                    <button id="add-origin-btn" class="add-filter-btn">+ Add Origin</button>
                </div>
            </div>
            <div id="gender-dropdown" class="filter-dropdown" style="display: none;"></div>
            <div id="origin-dropdown" class="filter-dropdown" style="display: none;"></div>
            <button id="draw-button">Draw new books!</button>
            <div id="book-info-box" class="book-info-box"></div>
        </div>
    </div>
</div>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
    const bookContainers = document.querySelectorAll('.book-container');
    const addGenderBtn = document.getElementById('add-gender-btn');
    const addOriginBtn = document.getElementById('add-origin-btn');
    const genderDropdown = document.getElementById('gender-dropdown');
    const originDropdown = document.getElementById('origin-dropdown');
    const drawButton = document.getElementById('draw-button');

    let booksData = [];
    let selectedFilters = { gender: [], origin: [] };
    let availableFilters = { gender: [], origin: [] };

    // Load data
    d3.csv('/data/bookshelf.csv').then(data => {
        booksData = data;
        populateAvailableFilters();
        setupDropdowns();
        drawBooks();
    }).catch(error => {
        console.error('Error loading the CSV file:', error);
    });

    function populateAvailableFilters() {
        availableFilters.gender = [...new Set(booksData.flatMap(d => d.gender ? d.gender.split(';').map(g => g.trim()) : []).filter(g => g))];
        availableFilters.origin = [...new Set(booksData.flatMap(d => d.nationality ? d.nationality.split(';').map(n => n.trim()) : []).filter(n => n))];
        availableFilters.origin.sort();
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

        // Origin dropdown
        availableFilters.origin.forEach(origin => {
            const item = document.createElement('div');
            item.classList.add('filter-dropdown-item');
            item.textContent = origin;
            item.dataset.value = origin;
            item.dataset.type = 'origin';
            item.addEventListener('click', () => addFilter('origin', origin, origin));
            originDropdown.appendChild(item);
        });
    }

    function toggleDropdown(dropdown, btn) {
        if (dropdown.style.display === 'none') {
            // Hide other dropdown
            const otherDropdown = dropdown === genderDropdown ? originDropdown : genderDropdown;
            otherDropdown.style.display = 'none';

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
        const dropdown = type === 'gender' ? genderDropdown : originDropdown;
        dropdown.style.display = 'none';
    }

    function removeFilter(type, value) {
        selectedFilters[type] = selectedFilters[type].filter(v => v !== value);
        renderBadges();
        drawBooks();
    }

    function renderBadges() {
        const genderBadgesContainer = document.getElementById('gender-badges');
        const originBadgesContainer = document.getElementById('origin-badges');

        genderBadgesContainer.innerHTML = '';
        originBadgesContainer.innerHTML = '';

        if (selectedFilters.gender.length == 0) {
            const badge = document.createElement('div');
            badge.classList.add('badge');
            const label = "All genders";
            badge.innerHTML = `${label}`;
            genderBadgesContainer.appendChild(badge);
        }

        if (selectedFilters.origin.length == 0) {
            const badge = document.createElement('div');
            badge.classList.add('badge');
            const label = "All origins";
            badge.innerHTML = `${label}`;
            originBadgesContainer.appendChild(badge);
        }

        selectedFilters.gender.forEach(gender => {
            const badge = document.createElement('div');
            badge.classList.add('badge');
            const label = getGenderLabel(gender);
            badge.innerHTML = `${label}<span class="badge-delete">×</span>`;
            badge.querySelector('.badge-delete').addEventListener('click', () => removeFilter('gender', gender));
            genderBadgesContainer.appendChild(badge);
        });

        selectedFilters.origin.forEach(origin => {
            const badge = document.createElement('div');
            badge.classList.add('badge');
            badge.innerHTML = `${origin}<span class="badge-delete">×</span>`;
            badge.querySelector('.badge-delete').addEventListener('click', () => removeFilter('origin', origin));
            originBadgesContainer.appendChild(badge);
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

        // Add hover listeners
        bookElement.addEventListener('mouseenter', () => showBookInfo(bookData));
        bookElement.addEventListener('mouseleave', hideBookInfo);

        return bookElement;
    }

    function showBookInfo(bookData) {
        const infoBox = document.getElementById('book-info-box');
        let genresArray = [];

        if (bookData.genres) {
            try {
                // Convert Python list string to valid JSON (single quotes -> double quotes)
                const jsonString = bookData.genres.replace(/'/g, '"');
                genresArray = JSON.parse(jsonString);
            } catch (e) {
                genresArray = [];
            }
        }

        infoBox.innerHTML = `
            <div class="book-info-title">${bookData.title}</div>
            <div class="book-info-item">
                <div class="book-info-label">Author</div>
                <div class="book-info-value">${bookData.author}</div>
            </div>
            <div class="book-info-item">
                <div class="book-info-label">Rating</div>
                <div class="book-info-value book-info-rating">⭐ ${bookData.rating}</div>
            </div>
            <div class="book-info-item">
                <div class="book-info-label">Genres</div>
                <div class="book-info-value">
                    ${genresArray.map(g => `<span class="book-genre">${g}</span>`).join('')}
                </div>
            </div>
        `;
        infoBox.classList.add('visible');
    }

    function hideBookInfo() {
        const infoBox = document.getElementById('book-info-box');
        infoBox.classList.remove('visible');
        infoBox.innerHTML = '';
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
            if (selectedFilters.origin.length > 0) {
                filteredData = filteredData.filter(d => d.nationality && selectedFilters.origin.some(o => d.nationality.includes(o)));
            }
            console.log(booksData);

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

    addOriginBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleDropdown(originDropdown, addOriginBtn);
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', () => {
        genderDropdown.style.display = 'none';
        originDropdown.style.display = 'none';
    });

    drawButton.addEventListener('click', drawBooks);
    renderBadges();
});
</script>
{{< /rawhtml >}}