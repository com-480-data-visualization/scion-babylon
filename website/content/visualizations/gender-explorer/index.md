---
title: "Gender explorer - filtered comparison"
description: "Filter genres or author nationalities and compare male, female, and other authorship totals."
tags: ["d3", "visualization"]
layout: "simple"
---

This filtered comparison lets you select either book genres or author nationalities, then compare the total number of books attributed to male, female, and other authorship groups.

Use the filters to focus on specific categories and see how the gender distribution changes across different slices of the Goodreads dataset.

Try switching between genres and nationalities, then raise the minimum-books slider to let the small categories step aside and reveal the bigger patterns.

<!-- prettier-ignore-start -->
{{< d3 >}}
const comparisonRoot = d3.select(container)
  .style("position", "relative")
  .style("font-family", "inherit");

const comparisonDark = document.documentElement.classList.contains("dark");
const comparisonTheme = comparisonDark ? {
  foreground: "#f5f4f1",
  secondary: "#d7d4ce",
  panel: "#272932",
  border: "#77747d",
  grid: "#575963",
  tooltipBackground: "#faf9f5",
  tooltipText: "#15171d",
} : {
  foreground: "#27282c",
  secondary: "#59565d",
  panel: "#fbfaf8",
  border: "#c6c2ba",
  grid: "#ddd9d1",
  tooltipBackground: "#ffffff",
  tooltipText: "#27282c",
};

const comparisonColors = {
  Male: "#a5d8ff",
  Female: "#bd93f9",
  Other: "#ffbd4a",
};

const comparisonLayout = comparisonRoot.append("div")
  .style("display", "grid")
  .style("grid-template-columns", "minmax(150px, 184px) minmax(0, 1fr)")
  .style("align-items", "stretch")
  .style("column-gap", "18px");

const comparisonPanel = comparisonLayout.append("aside")
  .style("border-right", `1px solid ${comparisonTheme.border}`)
  .style("padding", "4px 16px 4px 0")
  .style("color", comparisonTheme.foreground);

comparisonPanel.append("div")
  .style("font-size", "13px")
  .style("font-weight", 700)
  .style("margin-bottom", "7px")
  .text("Filter by");

const dimensionSelect = comparisonPanel.append("select")
  .style("width", "100%")
  .style("border", `1px solid ${comparisonTheme.border}`)
  .style("border-radius", "6px")
  .style("padding", "7px 8px")
  .style("background", comparisonTheme.panel)
  .style("color", comparisonTheme.foreground)
  .style("margin-bottom", "14px");
dimensionSelect.selectAll("option")
  .data([
    { value: "genre", label: "Genres" },
    { value: "origin", label: "Author nationalities" },
  ])
  .join("option")
  .attr("value", d => d.value)
  .text(d => d.label);

comparisonPanel.append("div")
  .style("font-size", "13px")
  .style("font-weight", 700)
  .style("margin-bottom", "7px")
  .text("Minimum books");

const comparisonMinText = comparisonPanel.append("div")
  .style("font-size", "12px")
  .style("color", comparisonTheme.secondary)
  .style("margin-bottom", "4px");

const comparisonMin = comparisonPanel.append("input")
  .attr("type", "range")
  .attr("min", 1)
  .attr("max", 100)
  .attr("value", 10)
  .attr("step", 1)
  .style("width", "100%")
  .style("accent-color", comparisonColors.Male)
  .style("margin-bottom", "14px");

const categoryHeader = comparisonPanel.append("div")
  .style("display", "flex")
  .style("flex-wrap", "wrap")
  .style("justify-content", "space-between")
  .style("align-items", "center")
  .style("gap", "8px")
  .style("margin-bottom", "8px");

const categoryTitle = categoryHeader.append("span")
  .style("font-size", "13px")
  .style("font-weight", 700);

const categoryActions = categoryHeader.append("div")
  .style("display", "flex")
  .style("gap", "5px");

function comparisonActionButton(label) {
  return categoryActions.append("button")
  .attr("type", "button")
  .style("border", `1px solid ${comparisonTheme.border}`)
  .style("border-radius", "5px")
  .style("background", "transparent")
  .style("color", comparisonTheme.foreground)
  .style("font-size", "11px")
  .style("padding", "3px 7px")
  .style("cursor", "pointer")
  .text(label);
}

const comparisonAll = comparisonActionButton("All");
const comparisonNone = comparisonActionButton("None");

const categoryList = comparisonPanel.append("div")
  .style("display", "grid")
  .style("gap", "6px")
  .style("max-height", "330px")
  .style("overflow-y", "auto")
  .style("padding-right", "3px");

const comparisonChartWrap = comparisonLayout.append("div")
  .style("min-width", 0)
  .style("padding", "0");

const comparisonSummary = comparisonChartWrap.append("div")
  .style("font-size", "14px")
  .style("font-weight", 650)
  .style("color", comparisonTheme.foreground)
  .style("margin", "0 0 10px");

const comparisonSvg = comparisonChartWrap.append("svg")
  .style("display", "block")
  .style("width", "100%");

const comparisonTooltip = comparisonRoot.append("div")
  .style("position", "absolute")
  .style("opacity", 0)
  .style("pointer-events", "none")
  .style("z-index", 8)
  .style("padding", "9px 11px")
  .style("background", comparisonTheme.tooltipBackground)
  .style("color", comparisonTheme.tooltipText)
  .style("border", `1px solid ${comparisonTheme.border}`)
  .style("border-radius", "6px")
  .style("box-shadow", "0 8px 24px rgba(0,0,0,0.28)")
  .style("font-size", "13px")
  .style("line-height", 1.45);

function populateComparisonCategories(data) {
  const dimension = dimensionSelect.property("value");
  const minimum = +comparisonMin.property("value");
  const categories = data
    .filter(d => d.attribute_type === dimension && d.total >= minimum)
    .sort((a, b) => d3.descending(a.total, b.total));

  categoryTitle.text(dimension === "genre" ? "Genres" : "Author nationalities");
  comparisonMinText.text(`${minimum}+ books per option`);

  categoryList.selectAll("label")
    .data(categories, d => d.attribute)
    .join(
      enter => {
        const label = enter.append("label")
          .style("display", "grid")
          .style("grid-template-columns", "auto minmax(0, 1fr) auto")
          .style("align-items", "center")
          .style("gap", "7px")
          .style("font-size", "12px")
          .style("color", comparisonTheme.secondary);
        label.append("input")
          .attr("type", "checkbox")
          .attr("name", "comparison-category")
          .property("checked", true);
        label.append("span").attr("class", "comparison-category-name");
        label.append("span")
          .attr("class", "comparison-category-total")
          .style("font-variant-numeric", "tabular-nums");
        return label;
      },
      update => update,
      exit => exit.remove()
    )
    .each(function(d) {
      const label = d3.select(this);
      label.select("input").attr("value", d.attribute).property("checked", true);
      label.select(".comparison-category-name").text(d.attribute);
      label.select(".comparison-category-total").text(d3.format(",")(d.total));
    });
}

function selectedComparisonData(data) {
  const dimension = dimensionSelect.property("value");
  const selected = new Set(
    categoryList.selectAll("input:checked").nodes().map(node => node.value)
  );
  return data.filter(d => d.attribute_type === dimension && selected.has(d.attribute));
}

function renderComparison(data) {
  const selected = selectedComparisonData(data);
  const bars = [
    { label: "Male", value: d3.sum(selected, d => d.men) },
    { label: "Female", value: d3.sum(selected, d => d.women) },
    { label: "Other", value: d3.sum(selected, d => d.mixed + d.unknown) },
  ];
  const total = d3.sum(bars, d => d.value);
  bars.forEach(d => d.share = total ? d.value / total : 0);

  const layoutWidth = Math.max(container.clientWidth, 290);
  const stacked = layoutWidth < 430;
  comparisonLayout.style(
    "grid-template-columns",
    stacked ? "minmax(0, 1fr)" : "minmax(150px, 184px) minmax(0, 1fr)"
  ).style("row-gap", stacked ? "16px" : "0");
  comparisonPanel.style("border-right", stacked ? "none" : `1px solid ${comparisonTheme.border}`)
    .style("border-bottom", stacked ? `1px solid ${comparisonTheme.border}` : "none")
    .style("padding", stacked ? "0 0 14px" : "4px 16px 4px 0");
  categoryList.style("max-height", stacked ? "180px" : "330px");

  const outerWidth = Math.max(comparisonChartWrap.node().clientWidth, 290);
  const compact = outerWidth < 530;
  const margin = { top: 25, right: 18, bottom: 55, left: compact ? 51 : 64 };
  const height = compact ? 360 : 430;
  const innerWidth = outerWidth - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  comparisonSvg.attr("viewBox", `0 0 ${outerWidth} ${height}`).attr("height", height);
  const chart = comparisonSvg.selectAll(".comparison-chart")
    .data([0])
    .join("g")
    .attr("class", "comparison-chart")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const x = d3.scaleBand()
    .domain(bars.map(d => d.label))
    .range([0, innerWidth])
    .padding(0.34);
  const y = d3.scaleLinear()
    .domain([0, d3.max(bars, d => d.value) || 1])
    .nice()
    .range([innerHeight, 0]);

  chart.selectAll(".comparison-grid")
    .data([0])
    .join("g")
    .attr("class", "comparison-grid")
    .call(d3.axisLeft(y).ticks(5).tickSize(-innerWidth).tickFormat(""))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll("line")
      .attr("stroke", comparisonTheme.grid)
      .attr("stroke-dasharray", "3 5"));

  chart.selectAll(".comparison-y-axis")
    .data([0])
    .join("g")
    .attr("class", "comparison-y-axis")
    .call(d3.axisLeft(y).ticks(5).tickFormat(d3.format("~s")))
    .call(g => g.selectAll(".domain, line").attr("stroke", comparisonTheme.grid))
    .call(g => g.selectAll("text").attr("fill", comparisonTheme.secondary));

  chart.selectAll(".comparison-x-axis")
    .data([0])
    .join("g")
    .attr("class", "comparison-x-axis")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x).tickSizeOuter(0))
    .call(g => g.selectAll(".domain, line").attr("stroke", comparisonTheme.grid))
    .call(g => g.selectAll("text")
      .attr("fill", comparisonTheme.foreground)
      .attr("font-size", 13)
      .attr("font-weight", 650));

  chart.selectAll(".comparison-y-title")
    .data([0])
    .join("text")
    .attr("class", "comparison-y-title")
    .attr("transform", "rotate(-90)")
    .attr("x", -innerHeight / 2)
    .attr("y", -44)
    .attr("text-anchor", "middle")
    .attr("fill", comparisonTheme.foreground)
    .attr("font-size", 12)
    .attr("font-weight", 650)
    .text("Number of books");

  const rects = chart.selectAll(".comparison-bar")
    .data(bars, d => d.label)
    .join("rect")
    .attr("class", "comparison-bar")
    .attr("x", d => x(d.label))
    .attr("width", x.bandwidth())
    .attr("fill", d => comparisonColors[d.label])
    .attr("rx", 4)
    .on("mousemove", (event, d) => {
      const [left, top] = d3.pointer(event, container);
      comparisonTooltip
        .style("opacity", 1)
        .style("left", `${left + 14}px`)
        .style("top", `${top - 34}px`)
        .html(`<strong style="color:#111318;font-weight:750;">${d.label}</strong><br/>Books: ${d3.format(",")(d.value)}<br/>Share: ${d3.format(".1%")(d.share)}`);
    })
    .on("mouseout", () => comparisonTooltip.style("opacity", 0));

  rects.transition()
    .duration(320)
    .attr("y", d => y(d.value))
    .attr("height", d => innerHeight - y(d.value));

  chart.selectAll(".comparison-bar-label")
    .data(bars, d => d.label)
    .join("text")
    .attr("class", "comparison-bar-label")
    .attr("x", d => x(d.label) + x.bandwidth() / 2)
    .attr("text-anchor", "middle")
    .attr("fill", comparisonTheme.foreground)
    .attr("font-size", compact ? 11 : 12)
    .attr("font-weight", 650)
    .transition()
    .duration(320)
    .attr("y", d => y(d.value) - 8)
    .text(d => d3.format(",")(d.value));

  const selectionCount = selected.length;
  const dimensionLabel = dimensionSelect.property("value") === "genre" ? "genres" : "author nationalities";
  comparisonSummary.text(`${selectionCount} ${dimensionLabel} selected - ${d3.format(",")(total)} books`);
}

d3.csv("{{< asset-url "data/gender_attribute_summary.csv" >}}", d3.autoType).then(data => {
  populateComparisonCategories(data);
  renderComparison(data);

  dimensionSelect.on("change", () => {
    populateComparisonCategories(data);
    renderComparison(data);
  });
  comparisonMin.on("input", () => {
    populateComparisonCategories(data);
    renderComparison(data);
  });
  categoryList.on("change", () => renderComparison(data));
  comparisonAll.on("click", () => {
    categoryList.selectAll("input").property("checked", true);
    renderComparison(data);
  });
  comparisonNone.on("click", () => {
    categoryList.selectAll("input").property("checked", false);
    renderComparison(data);
  });
  window.addEventListener("resize", () => renderComparison(data));
}).catch(err => {
  comparisonSummary.text("Could not load comparison data.");
  console.error("Error loading filtered gender comparison:", err);
});
{{< /d3 >}}
<!-- prettier-ignore-end -->
