---
title: "Languages"
date: 2026-04-13
description: "Guide to D3.js usage in Congo"
layout: "simple"
---
{{< rawhtml >}}
<div class="waffle-page">
  <style>
    .waffle-page {
      --text: #1f2937;
      --muted: #6b7280;
      --border: rgba(31, 41, 55, 0.12);
      --shadow: 0 20px 60px rgba(30, 41, 59, 0.12);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--text);
    }

    .waffle-shell {
      max-width: 1180px;
      margin: 0 auto;
      border: 1px solid var(--border);
      border-radius: 24px;
      box-shadow: var(--shadow);
      padding: 24px;
      backdrop-filter: blur(10px);
    }

    .waffle-layout {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 280px;
      gap: 24px;
      align-items: start;
    }

    .waffle-chart-card {
      min-width: 0;
    }

    #waffle-chart {
      width: 100%;
      overflow: hidden;
    }

    .waffle-note {
      margin-top: 14px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
    }

    .waffle-legend {
      background: rgba(255, 255, 255, 0.68);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 16px;
    }

    .waffle-legend h2 {
      margin: 0 0 10px;
      font-size: 0.95rem;
      letter-spacing: 0.02em;
    }

    .waffle-legend-list {
      display: grid;
      margin: 0;
      padding: 0;
      list-style: none;
      max-height: 620px;
      overflow: auto;
    }

    .waffle-legend-item {
      display: grid;
      grid-template-columns: 14px minmax(0, 1fr);
      gap: 10px;
      align-items: start;
      font-size: 13px;
      line-height: 1.35;
    }

    .waffle-swatch {
      width: 14px;
      height: 14px;
      border-radius: 4px;
      margin-top: 2px;
      box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.08);
    }

    .waffle-legend-name {
      font-weight: 700;
      color: #111827;
    }

    .waffle-legend-detail {
      display: block;
      color: var(--muted);
      font-size: 12px;
      margin-top: 2px;
    }

    @media (max-width: 920px) {
      .waffle-layout {
        grid-template-columns: 1fr;
      }

      .waffle-legend {
        order: 2;
      }
    }
  </style>

  <section class="waffle-shell">
    <div class="waffle-layout">
      <div class="waffle-chart-card">
        <div id="waffle-chart"></div>
      </div>
      <aside class="waffle-legend" id="waffle-legend">
        <h2>Legend</h2>
        <ul class="waffle-legend-list" id="waffle-legend-list"></ul>
      </aside>
    </div>
  </section>
</div>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
  const topN = 20;
  const gridSize = 20;
  const cellCount = gridSize * gridSize;
  const gap = 3;
  const cellSize = 20;
  const svgWidth = gridSize * cellSize + (gridSize - 1) * gap;
  const svgHeight = svgWidth;

  const palette = d3.schemeTableau10
    .concat(d3.schemeSet3)
    .concat(['#7b8b8e', '#d97d54', '#82a7e0', '#b49ad9', '#74a57f', '#d4a373']);

  d3.csv('{{< asset-url "data/language_counts.csv" >}}', d => ({
    language: d.language || 'Unknown',
    num_books: +d.num_books || 0,
  })).then(raw => {
    const totals = d3.rollups(
      raw,
      values => d3.sum(values, d => d.num_books),
      d => d.language,
    )
      .map(([language, num_books]) => ({ language, num_books }))
      .sort((a, b) => d3.descending(a.num_books, b.num_books));

    const topLanguages = totals.slice(0, topN);
    const remainder = totals.slice(topN);
    const otherBooks = d3.sum(remainder, d => d.num_books);
    const categories = otherBooks > 0
      ? topLanguages.concat([{ language: 'Other', num_books: otherBooks }])
      : topLanguages;

    const totalBooks = d3.sum(categories, d => d.num_books);

    const assigned = categories.map(category => {
      const exact = (category.num_books / totalBooks) * cellCount;
      return {
        ...category,
        exact,
        cells: Math.floor(exact),
        remainder: exact - Math.floor(exact),
        share: category.num_books / totalBooks,
      };
    });

    let allocated = d3.sum(assigned, d => d.cells);
    const byRemainder = [...assigned].sort((a, b) => d3.descending(a.remainder, b.remainder));
    let extra = cellCount - allocated;
    let cursor = 0;
    while (extra > 0 && byRemainder.length > 0) {
      byRemainder[cursor % byRemainder.length].cells += 1;
      extra -= 1;
      cursor += 1;
    }

    const waffleCells = [];
    assigned.forEach(category => {
      for (let index = 0; index < category.cells; index += 1) {
        waffleCells.push({
          language: category.language,
          num_books: category.num_books,
          share: category.share,
        });
      }
    });

    while (waffleCells.length < cellCount) {
      waffleCells.push({ language: 'Other', num_books: otherBooks, share: otherBooks / totalBooks });
    }

    const color = d3.scaleOrdinal()
      .domain(categories.map(d => d.language))
      .range(categories.map((_, index) => index === categories.length - 1 && categories[index].language === 'Other'
        ? '#b8b8b1'
        : palette[index % palette.length]));

    const chart = d3.select('#waffle-chart');
    const svg = chart.append('svg')
      .attr('viewBox', `0 0 ${svgWidth} ${svgHeight}`)
      .attr('preserveAspectRatio', 'xMidYMid meet')
      .attr('role', 'img')
      .attr('aria-label', 'Waffle chart showing books by language');

    const cells = svg.append('g');

    const grid = waffleCells.map((d, index) => ({
      ...d,
      index,
      row: Math.floor(index / gridSize),
      col: index % gridSize,
    }));

    cells.selectAll('rect')
      .data(grid)
      .enter()
      .append('rect')
      .attr('x', d => d.col * (cellSize + gap))
      .attr('y', d => d.row * (cellSize + gap))
      .attr('width', cellSize)
      .attr('height', cellSize)
      .attr('rx', 6)
      .attr('fill', d => color(d.language))
      .attr('opacity', 0)
      .attr('stroke', 'rgba(255,255,255,0.9)')
      .attr('stroke-width', 1);

    svg.selectAll('rect')
      .transition()
      .delay((_, index) => index * 10)
      .duration(420)
      .attr('opacity', 1);

    const legendList = d3.select('#waffle-legend-list');
    const legendItems = categories.map(category => ({
      ...category,
      share: category.num_books / totalBooks,
    }));

    legendList.selectAll('li')
      .data(legendItems)
      .enter()
      .append('li')
      .attr('class', 'waffle-legend-item')
      .html(d => `
        <span class="waffle-swatch" style="background:${color(d.language)}"></span>
        <span>
          <span class="waffle-legend-name">${d.language}</span>
          <span class="waffle-legend-detail">${d3.format(',')(d.num_books)} books · ${d3.format('.1%')(d.share)}</span>
        </span>
      `);
  });
});
</script>
{{< /rawhtml >}}
