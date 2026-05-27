---
title: "Bestsellers by Women Authors"
date: 2026-05-06
description: "Explore 16,000+ bestselling books by female authors with interactive tiles"
---

{{< lead >}}
Discover over 16,000 bestselling books written by women. Click any tile to see more details.
{{< /lead >}}

<!-- prettier-ignore-start -->
{{< d3 >}}
// Fetch and process CSV data
let allBooks = [];
let filteredBooks = [];
let selectedBook = null;
const tileSize = 150;
const tilesPerRow = Math.floor(container.clientWidth / (tileSize + 8));

// Parse CSV with quoted field support
function parseCSV(csv) {
  const rows = [];
  let current = [];
  let insideQuotes = false;
  let field = '';

  for (let i = 0; i < csv.length; i++) {
    const char = csv[i];
    const nextChar = csv[i + 1];

    if (char === '"') {
      if (insideQuotes && nextChar === '"') {
        field += '"';
        i++;
      } else {
        insideQuotes = !insideQuotes;
      }
    } else if (char === ',' && !insideQuotes) {
      current.push(field.trim());
      field = '';
    } else if ((char === '\n' || char === '\r') && !insideQuotes) {
      if (field || current.length > 0) {
        current.push(field.trim());
        if (current.length > 0) rows.push(current);
        current = [];
        field = '';
      }
      if (char === '\r' && nextChar === '\n') i++;
    } else {
      field += char;
    }
  }

  if (field || current.length > 0) {
    current.push(field.trim());
    if (current.length > 0) rows.push(current);
  }

  return rows;
}

// Load CSV data
fetch('{{< asset-url "data/bookshelf2.csv" >}}')
  .then(response => response.text())
  .then(csv => {
    const rows = parseCSV(csv);

    allBooks = rows.slice(1).map(row => {
      if (row.length < 6) return null;
      return {
        title: row[0],
        author: row[1],
        rating: parseFloat(row[2]) || 0,
        genres: row[3],
        language: row[4],
        gender: row[5]
      };
    }).filter(book => book !== null);

    // Filter female authors and sort by rating
    filteredBooks = allBooks
      .filter(book => book.gender === 'w')
      .sort((a, b) => b.rating - a.rating);

    render();
  });

// Simple hash function for consistent colors
function hashColor(str) {
  let hash = 0;
  const hue = Math.abs(hash) % 360;
  return `hsl(${hue}, 70%, 60%)`;
}

// Virtual scrolling grid with Intersection Observer
function render() {
  const mainContainer = d3.select(container);

  // Remove previous content
  mainContainer.selectAll("*").remove();

  // Create wrapper with styles
  const wrapper = mainContainer.append("div")
    .style("display", "grid")
    .style("grid-template-columns", `repeat(auto-fill, minmax(${tileSize}px, 1fr))`)
    .style("gap", "8px")
    .style("padding", "20px")
    .style("max-height", "80vh")
    .style("overflow-y", "auto");

  // Render visible tiles with virtual scrolling
  const visibleTiles = new Set();
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      const idx = parseInt(entry.target.dataset.idx);
      if (entry.isIntersecting) {
        visibleTiles.add(idx);
        renderTile(entry.target, idx);
      } else {
        visibleTiles.delete(idx);
        entry.target.innerHTML = '';
      }
    });
  }, { rootMargin: '200px' });

  // Create tile placeholders
  filteredBooks.forEach((book, idx) => {
    const tile = wrapper.append("div")
      .attr("data-idx", idx)
      .style("width", `${tileSize}px`)
      .style("height", `${tileSize + 40}px`)
      .style("cursor", "pointer")
      .style("border-radius", "6px")
      .style("overflow", "hidden")
      .style("transition", "transform 0.2s");

    observer.observe(tile.node());
  });

  function renderTile(tileNode, idx) {
    const book = filteredBooks[idx];
    if (!book) return;

    const color = hashColor(book.title + book.author);

    d3.select(tileNode)
      .style("background-color", color)
      .style("padding", "8px")
      .style("display", "flex")
      .style("flex-direction", "column")
      .style("justify-content", "flex-end")
      .style("box-shadow", "0 2px 4px rgba(0,0,0,0.1)")
      .on("mouseenter", function() {
        d3.select(this)
          .style("transform", "scale(1.05)")
          .style("box-shadow", "0 4px 12px rgba(0,0,0,0.2)")
          .style("transition", "transform 0.2s");
      })
      .on("mouseleave", function() {
        d3.select(this)
          .style("transform", "scale(1)")
          .style("box-shadow", "0 2px 4px rgba(0,0,0,0.1)");
      })
      .on("click", function() {
        showDetails(book);
      })
      .html(`
        <div style="font-size: 11px; font-weight: bold; color: white; text-shadow: 0 1px 2px rgba(0,0,0,0.3); line-height: 1.2; word-break: break-word;">
          ${book.title}
        </div>
        <div style="font-size: 9px; color: white; text-shadow: 0 1px 1px rgba(0,0,0,0.3); margin-top: 4px; opacity: 0.9;">
          ${book.author}
        </div>
      `);
  }
}

// Show details modal
function showDetails(book) {
  const mainContainer = d3.select(container);

  // Remove existing modal
  mainContainer.selectAll(".modal-overlay").remove();

  const overlay = mainContainer.append("div")
    .attr("class", "modal-overlay")
    .style("position", "fixed")
    .style("top", "0")
    .style("left", "0")
    .style("right", "0")
    .style("bottom", "0")
    .style("background", "rgba(0,0,0,0.5)")
    .style("display", "flex")
    .style("align-items", "center")
    .style("justify-content", "center")
    .style("z-index", "1000")
    .on("click", function() {
      d3.select(this).remove();
    });

  const modal = overlay.append("div")
    .style("background", "white")
    .style("padding", "30px")
    .style("border-radius", "8px")
    .style("max-width", "500px")
    .style("max-height", "80vh")
    .style("overflow-y", "auto")
    .style("box-shadow", "0 10px 40px rgba(0,0,0,0.3)")
    .on("click", function() {
      d3.event.stopPropagation();
    });

  const color = hashColor(book.title + book.author);

  modal.append("div")
    .style("background", color)
    .style("color", "white")
    .style("padding", "15px")
    .style("border-radius", "4px")
    .style("margin-bottom", "15px")
    .html(`
      <h2 style="margin: 0 0 8px 0; font-size: 20px;">${book.title}</h2>
      <p style="margin: 0; font-size: 14px; opacity: 0.95;">By ${book.author}</p>
    `);

  modal.append("div")
    .html(`
      <p><strong>Rating:</strong> ${book.rating} ⭐</p>
      <p><strong>Language:</strong> ${book.language}</p>
      <p><strong>Genres:</strong> ${book.genres}</p>
    `)
    .style("font-size", "14px")
    .style("color", "#333");

  modal.append("button")
    .text("Close")
    .style("width", "100%")
    .style("padding", "10px")
    .style("margin-top", "15px")
    .style("background", color)
    .style("color", "white")
    .style("border", "none")
    .style("border-radius", "4px")
    .style("cursor", "pointer")
    .on("click", function() {
      overlay.remove();
    });
}

// Handle window resize
window.addEventListener('resize', () => {
  render();
});
{{< /d3 >}}
<!-- prettier-ignore-end -->
