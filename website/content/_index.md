---
title: "Welcome to Dataviz! :tada:"
date: 2026-04-13
description: "This is a website to host our book visualizations."
tags: ["d3", "sample", "graph", "shortcodes"]
---

{{< lead >}}
A powerful, lightweight visualization for COM-480 built with Hugo, Tailwind CSS.
{{< /lead >}}

# Visualizations



## Genres and gender
<!-- prettier-ignore-start-->
{{< d3 >}}
const width = container.clientWidth;
const height = 500;
const svg = d3.select(container).append("svg")
  .attr("width", width)
  .attr("height", height);

const genderLabels = {
  "m":   "Male",
  "w":   "Female",
  "w;m": "Female & Male",
  "m;m": "Male & Male",
  "m;m;m": "Male & Male & Male",
  "w;w": "Female & Female"
};
const genders = Object.keys(genderLabels);
const isDark = document.documentElement.classList.contains("dark");
const labelColor = isDark ? congoColors.neutral100 : "#000000";

const selector = d3.select(container).insert("div", "svg")
  .style("margin-bottom", "10px");
selector.append("label")
  .text("Select gender: ")
  .style("color", labelColor);
const select = selector.append("select")
  .style("margin-bottom", "8px")
  .style("padding", "6px 12px")
  .style("background", congoColors.primary400)
  .style("color", congoColors.neutral100)
  .style("border", "none")
  .style("border-radius", "4px")
  .style("cursor", "pointer");
select.selectAll("option")
  .data(genders)
  .enter()
  .append("option")
  .text(d => genderLabels[d])
  .attr("value", d => d);

const genreColorScale = d3.scaleOrdinal()
  .range([
    congoColors.primary200,
    congoColors.primary300,
    congoColors.primary400,
    congoColors.primary500,
    "#a78bfa", "#34d399", "#f97316",
    "#e879f9", "#facc15", "#38bdf8"
  ]);

d3.csv("/data/genders_genres.csv").then(data => {
  data.forEach(d => d.count = +d.count);
  const allGenres = [...new Set(data.map(d => d.genres))];
  genreColorScale.domain(allGenres);

  // Shelf layout constants
  const shelfHeight = 18;
  const shelfPadding = 6;
  const shelfColor = isDark ? "#5a3e2b" : "#8B5E3C";
  const shelfShadow = isDark ? "#3a2518" : "#6b4423";
  const bookGap = 3;
  const marginLeft = 30;
  const marginTop = 30;
  const availableWidth = width - marginLeft - 20;

  // Min/max book dimensions
  const minBookWidth = 18;
  const maxBookWidth = 60;
  const minBookHeight = 80;
  const maxBookHeight = 160;

  function update(selectedGender) {
    const filtered = data.filter(d => d.gender === selectedGender)
      .sort((a, b) => b.count - a.count);

    const maxCount = d3.max(filtered, d => d.count);
    const minCount = d3.min(filtered, d => d.count);

    const widthScale = d3.scaleLinear()
      .domain([minCount, maxCount])
      .range([minBookWidth, maxBookWidth]);
    const heightScale = d3.scaleLinear()
      .domain([minCount, maxCount])
      .range([minBookHeight, maxBookHeight]);

    svg.selectAll("*").remove();

    // Pack books into rows (shelves)
    const rows = [];
    let currentRow = [];
    let currentRowWidth = 0;
    filtered.forEach(d => {
      const bw = Math.round(widthScale(d.count));
      if (currentRowWidth + bw + bookGap > availableWidth && currentRow.length > 0) {
        rows.push(currentRow);
        currentRow = [];
        currentRowWidth = 0;
      }
      currentRow.push({ ...d, bookWidth: bw, bookHeight: Math.round(heightScale(d.count)) });
      currentRowWidth += bw + bookGap;
    });
    if (currentRow.length > 0) rows.push(currentRow);

    const rowSpacing = maxBookHeight + shelfHeight + shelfPadding + 10;
    const totalHeight = marginTop + rows.length * rowSpacing + 20;
    svg.attr("height", totalHeight);

    rows.forEach((row, rowIndex) => {
      const baseY = marginTop + rowIndex * rowSpacing;
      const shelfY = baseY + maxBookHeight;

      // Draw shelf plank
      const rowWidth = d3.sum(row, d => d.bookWidth + bookGap) - bookGap;
      const g = svg.append("g");

      // Shelf top surface
      g.append("rect")
        .attr("x", marginLeft - 4)
        .attr("y", shelfY)
        .attr("width", rowWidth + 8)
        .attr("height", shelfHeight)
        .attr("rx", 2)
        .attr("fill", shelfColor);

      // Shelf shadow/depth
      g.append("rect")
        .attr("x", marginLeft - 4)
        .attr("y", shelfY + shelfHeight)
        .attr("width", rowWidth + 8)
        .attr("height", 4)
        .attr("rx", 1)
        .attr("fill", shelfShadow);

      // Draw books
      let xCursor = marginLeft;
      row.forEach(d => {
        const bookTop = shelfY - d.bookHeight;
        const bookG = g.append("g").style("cursor", "default");

        // Book body
        bookG.append("rect")
          .attr("x", xCursor)
          .attr("y", bookTop)
          .attr("width", d.bookWidth)
          .attr("height", d.bookHeight)
          .attr("rx", 1)
          .attr("fill", genreColorScale(d.genres))
          .attr("fill-opacity", 0.9)
          .attr("stroke", d3.color(genreColorScale(d.genres)).darker(0.8))
          .attr("stroke-width", 0.8);

        // Spine highlight (left edge gleam)
        bookG.append("rect")
          .attr("x", xCursor)
          .attr("y", bookTop)
          .attr("width", Math.max(2, d.bookWidth * 0.12))
          .attr("height", d.bookHeight)
          .attr("rx", 1)
          .attr("fill", "rgba(255,255,255,0.18)");

        // Top of book (page edges)
        bookG.append("rect")
          .attr("x", xCursor + 1)
          .attr("y", bookTop)
          .attr("width", d.bookWidth - 2)
          .attr("height", 3)
          .attr("fill", isDark ? "#ccc" : "#f0ece4")
          .attr("opacity", 0.7);

        // Spine text (rotated) — only if book is wide enough
        if (d.bookWidth >= 22) {
          const fontSize = Math.min(10, Math.max(7, d.bookWidth * 0.3));
          const cx = xCursor + d.bookWidth / 2;
          const cy = bookTop + d.bookHeight / 2;
          bookG.append("text")
            .attr("transform", `translate(${cx}, ${cy}) rotate(-90)`)
            .attr("text-anchor", "middle")
            .attr("dominant-baseline", "middle")
            .style("font-size", `${fontSize}px`)
            .style("font-family", "serif")
            .style("fill", "#fff")
            .style("paint-order", "stroke")
            .style("stroke", "rgba(0,0,0,0.5)")
            .style("stroke-width", "2px")
            .style("stroke-linejoin", "round")
            .style("pointer-events", "none")
            .text(d.genres);
        }

        // Count label below shelf
        g.append("text")
          .attr("x", xCursor + d.bookWidth / 2)
          .attr("y", shelfY + shelfHeight + 14)
          .attr("text-anchor", "middle")
          .style("font-size", "9px")
          .style("fill", labelColor)
          .style("opacity", 0.6)
          .text(d.count);

        xCursor += d.bookWidth + bookGap;
      });
    });
  }

  update("m");
  select.on("change", function() { update(this.value); });
});
{{< /d3 >}}

<!-- prettier-ignore-end -->
