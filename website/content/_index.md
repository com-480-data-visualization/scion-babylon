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

### Scale countries by amount of books published by author's from these countries


## Bar chart

<!-- prettier-ignore-start -->
{{< d3 >}}
const margin = {top: 20, right: 20, bottom: 40, left: 40};
const width = container.clientWidth - margin.left - margin.right;
const height = 300 - margin.top - margin.bottom;

const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
const data = [65, 59, 80, 81, 56, 55, 40];

const svg = d3.select(container).append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", `translate(${margin.left},${margin.top})`);

const x = d3.scaleBand().domain(labels).range([0, width]).padding(0.2);
const y = d3.scaleLinear().domain([0, d3.max(data)]).nice().range([height, 0]);

svg.append("g").attr("transform", `translate(0,${height})`).call(d3.axisBottom(x));
svg.append("g").call(d3.axisLeft(y));

svg.selectAll(".bar")
  .data(data)
  .enter().append("rect")
  .attr("x", (d, i) => x(labels[i]))
  .attr("y", d => y(d))
  .attr("width", x.bandwidth())
  .attr("height", d => height - y(d))
  .attr("fill", congoColors.primary300)
  .attr("stroke", congoColors.primary500)
  .attr("stroke-width", 1);
{{< /d3 >}}
<!-- prettier-ignore-end -->

## Gender explorer - filtered comparison

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
  Male: "#36bfd0",
  Female: "#ff6e9f",
  Other: "#ffbd4a",
};

const comparisonLayout = comparisonRoot.append("div")
  .style("display", "grid")
  .style("grid-template-columns", "minmax(190px, 230px) minmax(0, 1fr)")
  .style("gap", "18px")
  .style("align-items", "start");

const comparisonPanel = comparisonLayout.append("aside")
  .style("background", comparisonTheme.panel)
  .style("border", `1px solid ${comparisonTheme.border}`)
  .style("border-radius", "6px")
  .style("padding", "14px")
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
  .style("justify-content", "space-between")
  .style("align-items", "center")
  .style("gap", "8px")
  .style("margin-bottom", "8px");

const categoryTitle = categoryHeader.append("span")
  .style("font-size", "13px")
  .style("font-weight", 700);

const comparisonAll = categoryHeader.append("button")
  .attr("type", "button")
  .style("border", `1px solid ${comparisonTheme.border}`)
  .style("border-radius", "5px")
  .style("background", "transparent")
  .style("color", comparisonTheme.foreground)
  .style("font-size", "11px")
  .style("padding", "3px 7px")
  .style("cursor", "pointer")
  .text("All");

const categoryList = comparisonPanel.append("div")
  .style("display", "grid")
  .style("gap", "6px")
  .style("max-height", "330px")
  .style("overflow-y", "auto")
  .style("padding-right", "3px");

const comparisonChartWrap = comparisonLayout.append("div")
  .style("min-width", 0);

const comparisonSummary = comparisonChartWrap.append("div")
  .style("font-size", "14px")
  .style("font-weight", 650)
  .style("color", comparisonTheme.foreground)
  .style("margin", "0 0 10px");

const comparisonSvg = comparisonChartWrap.append("svg")
  .style("display", "block")
  .style("width", "100%")
  .style("background", comparisonTheme.panel)
  .style("border", `1px solid ${comparisonTheme.border}`)
  .style("border-radius", "6px");

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
  comparisonLayout.style(
    "grid-template-columns",
    layoutWidth < 720 ? "minmax(0, 1fr)" : "minmax(190px, 230px) minmax(0, 1fr)"
  );
  categoryList.style("max-height", layoutWidth < 720 ? "210px" : "330px");

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

d3.csv("/data/gender_attribute_summary.csv", d3.autoType).then(data => {
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
  window.addEventListener("resize", () => renderComparison(data));
}).catch(err => {
  comparisonSummary.text("Could not load comparison data.");
  console.error("Error loading filtered gender comparison:", err);
});
{{< /d3 >}}
<!-- prettier-ignore-end -->

## The gender-genre scatter

<!-- prettier-ignore-start -->
{{< d3 >}}
const scatterRoot = d3.select(container)
  .style("position", "relative")
  .style("max-width", "100%")
  .style("font-family", "inherit");

const scatterDark = document.documentElement.classList.contains("dark");
const scatterTheme = scatterDark ? {
  foreground: "#f5f4f1",
  secondary: "#d7d4ce",
  grid: "#56545b",
  pointStroke: "#171821",
  chartBackground: "#272932",
  tooltipBackground: "#f8f7f4",
  tooltipText: "#1f2026",
  border: "#77747d",
} : {
  foreground: "#27282c",
  secondary: "#545158",
  grid: "#c6c2ba",
  pointStroke: "#ffffff",
  chartBackground: "#fbfaf8",
  tooltipBackground: "#ffffff",
  tooltipText: "#27282c",
  border: "#c6c2ba",
};
const scatterColors = [
  "#37c6d0", "#ff6e9f", "#ffbf47", "#63dc8a", "#bd93f9",
  "#ff755e", "#6eafff", "#ff9955", "#b6df58", "#f98dd1", "#c8ccd7",
];
const symbolByGender = {
  "Male authors": d3.symbolCircle,
  "Non-male authors": d3.symbolDiamond,
};

const scatterControls = scatterRoot.append("div")
  .style("display", "flex")
  .style("flex-wrap", "wrap")
  .style("gap", "22px")
  .style("margin", "6px 0 18px")
  .style("color", scatterTheme.foreground);

const scatterModeWrap = scatterControls.append("label")
  .style("display", "grid")
  .style("gap", "7px")
  .style("font-size", "13px")
  .style("font-weight", 650);
scatterModeWrap.append("span").text("Group by");
const scatterMode = scatterModeWrap.append("select")
  .style("border", `1px solid ${scatterTheme.border}`)
  .style("border-radius", "6px")
  .style("padding", "6px 9px")
  .style("background", scatterTheme.chartBackground)
  .style("color", scatterTheme.foreground);
scatterMode.selectAll("option")
  .data([
    { value: "genre", label: "Book genre" },
    { value: "nationality", label: "Author nationality" },
  ])
  .join("option")
  .attr("value", d => d.value)
  .text(d => d.label);

const scatterMinWrap = scatterControls.append("label")
  .style("display", "grid")
  .style("gap", "7px")
  .style("font-size", "13px")
  .style("font-weight", 650);
const scatterMinLabel = scatterMinWrap.append("span");
const scatterMin = scatterMinWrap.append("input")
  .attr("type", "range")
  .attr("min", 1)
  .attr("max", 50)
  .attr("value", 5)
  .attr("step", 1)
  .style("accent-color", "#37c6d0");

const genderFilter = scatterControls.append("fieldset")
  .style("border", "none")
  .style("padding", 0)
  .style("margin", 0);
genderFilter.append("legend")
  .style("font-size", "13px")
  .style("font-weight", 650)
  .style("margin-bottom", "7px")
  .text("Gender group");
const genderOptions = genderFilter.append("div")
  .style("display", "flex")
  .style("gap", "14px")
  .style("flex-wrap", "wrap");

["Male authors", "Non-male authors"].forEach(group => {
  const label = genderOptions.append("label")
    .style("display", "inline-flex")
    .style("align-items", "center")
    .style("gap", "6px")
    .style("font-size", "13px");
  label.append("input")
    .attr("type", "checkbox")
    .attr("name", "scatter-gender")
    .attr("value", group)
    .property("checked", true);
  label.append("svg")
    .attr("width", 15)
    .attr("height", 15)
    .append("path")
    .attr("transform", "translate(7.5,7.5)")
    .attr("d", d3.symbol().type(symbolByGender[group]).size(80)())
    .attr("fill", scatterTheme.foreground);
  label.append("span").text(group);
});

const genreFilter = scatterControls.append("fieldset")
  .style("border", "none")
  .style("padding", 0)
  .style("margin", 0)
  .style("flex", "1 1 380px");
const genreHeader = genreFilter.append("div")
  .style("display", "flex")
  .style("justify-content", "space-between")
  .style("align-items", "center")
  .style("gap", "12px")
  .style("margin-bottom", "7px");
const attributeHeading = genreHeader.append("span")
  .style("font-size", "13px")
  .style("font-weight", 650);
const resetGenres = genreHeader.append("button")
  .attr("type", "button")
  .style("border", `1px solid ${scatterTheme.border}`)
  .style("background", "transparent")
  .style("color", scatterTheme.foreground)
  .style("border-radius", "6px")
  .style("font-size", "12px")
  .style("padding", "4px 9px")
  .style("cursor", "pointer")
  .text("Select all");
const genreOptions = genreFilter.append("div")
  .style("display", "grid")
  .style("grid-template-columns", "repeat(auto-fit, minmax(128px, 1fr))")
  .style("gap", "6px 12px");

const scatterSummary = scatterRoot.append("div")
  .style("font-size", "14px")
  .style("font-weight", 650)
  .style("margin", "0 0 10px")
  .style("color", scatterTheme.foreground);

const scatterTooltip = scatterRoot.append("div")
  .style("position", "absolute")
  .style("z-index", 5)
  .style("opacity", 0)
  .style("pointer-events", "none")
  .style("background", scatterTheme.tooltipBackground)
  .style("color", scatterTheme.tooltipText)
  .style("border", `1px solid ${scatterTheme.border}`)
  .style("box-shadow", "0 8px 24px rgba(0, 0, 0, 0.28)")
  .style("border-radius", "6px")
  .style("padding", "9px 11px")
  .style("font-size", "13px")
  .style("line-height", 1.45);

const scatterSvg = scatterRoot.append("svg")
  .style("display", "block")
  .style("width", "100%")
  .style("background", scatterTheme.chartBackground)
  .style("border", `1px solid ${scatterTheme.border}`)
  .style("border-radius", "6px");
const scatterChart = scatterSvg.append("g");
const scatterGrid = scatterChart.append("g");
const scatterXAxis = scatterChart.append("g");
const scatterYAxis = scatterChart.append("g");
const scatterXTitle = scatterChart.append("text");
const scatterYTitle = scatterChart.append("text");

function scatterFiltered(data) {
  const attributeType = scatterMode.property("value");
  const minimum = +scatterMin.property("value");
  const genders = new Set(
    genderOptions.selectAll("input:checked").nodes().map(node => node.value)
  );
  const attributes = new Set(
    genreOptions.selectAll("input:checked").nodes().map(node => node.value)
  );
  return data.filter(d =>
    d.attribute_type === attributeType &&
    d.books >= minimum &&
    genders.has(d.gender_group) &&
    attributes.has(d.attribute)
  );
}

function drawScatter(data, color) {
  const visible = scatterFiltered(data);
  const attributeType = scatterMode.property("value");
  const minimum = +scatterMin.property("value");
  const available = data.filter(d => d.attribute_type === attributeType && d.books >= minimum);
  const width = Math.max(container.clientWidth, 320);
  const compact = width < 640;
  const margin = { top: 22, right: compact ? 18 : 30, bottom: 53, left: compact ? 54 : 68 };
  const height = compact ? 390 : 470;
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  scatterSvg.attr("viewBox", `0 0 ${width} ${height}`).attr("height", height);
  scatterChart.attr("transform", `translate(${margin.left},${margin.top})`);

  const plotData = available.length ? available : data.filter(d => d.attribute_type === attributeType);
  const xExtent = d3.extent(plotData, d => d.average_rating);
  const yExtent = d3.extent(plotData, d => d.average_price);
  const x = d3.scaleLinear()
    .domain([xExtent[0] - 0.03, xExtent[1] + 0.03])
    .nice()
    .range([0, innerWidth]);
  const y = d3.scaleLinear()
    .domain([Math.max(0, yExtent[0] - 1), yExtent[1] + 1])
    .nice()
    .range([innerHeight, 0]);

  scatterGrid
    .call(d3.axisLeft(y).ticks(6).tickSize(-innerWidth).tickFormat(""))
    .call(group => group.select(".domain").remove())
    .call(group => group.selectAll(".tick line")
      .attr("stroke", scatterTheme.grid)
      .attr("stroke-opacity", 0.7)
      .attr("stroke-dasharray", "3 5"));

  scatterXAxis
    .attr("transform", `translate(0,${innerHeight})`)
    .transition()
    .duration(300)
    .call(d3.axisBottom(x).ticks(compact ? 4 : 6).tickFormat(d3.format(".2f")));
  scatterYAxis
    .transition()
    .duration(300)
    .call(d3.axisLeft(y).ticks(6).tickFormat(value => `$${value}`));
  scatterXAxis.selectAll(".domain, .tick line").attr("stroke", scatterTheme.grid);
  scatterYAxis.selectAll(".domain, .tick line").attr("stroke", scatterTheme.grid);
  scatterChart.selectAll(".tick text").attr("fill", scatterTheme.secondary);

  scatterXTitle
    .attr("x", innerWidth / 2)
    .attr("y", innerHeight + 43)
    .attr("text-anchor", "middle")
    .attr("font-size", 13)
    .attr("font-weight", 650)
    .attr("fill", scatterTheme.foreground)
    .text("Average rating");
  scatterYTitle
    .attr("transform", "rotate(-90)")
    .attr("x", -innerHeight / 2)
    .attr("y", -47)
    .attr("text-anchor", "middle")
    .attr("font-size", 13)
    .attr("font-weight", 650)
    .attr("fill", scatterTheme.foreground)
    .text("Average price");

  const totalBooks = d3.sum(visible, d => d.books);
  scatterMinLabel.text(`Minimum books per point: ${minimum}`);
  scatterSummary.text(`${visible.length} groups shown - ${d3.format(",")(totalBooks)} priced books`);

  const points = scatterChart.selectAll(".scatter-point")
    .data(visible, d => `${d.attribute_type}-${d.attribute}-${d.gender_group}`)
    .join(
      enter => enter.append("path")
        .attr("class", "scatter-point")
        .attr("opacity", 0)
        .attr("transform", d => `translate(${x(d.average_rating)},${y(d.average_price)})`)
        .attr("d", d => d3.symbol().type(symbolByGender[d.gender_group]).size(0)()),
      update => update,
      exit => exit.transition().duration(160).attr("opacity", 0).remove()
    );

  points
    .attr("fill", d => color(d.attribute))
    .attr("stroke", scatterTheme.pointStroke)
    .attr("stroke-width", 2)
    .on("mousemove", (event, d) => {
      const [left, top] = d3.pointer(event, container);
      scatterTooltip
        .style("opacity", 1)
        .style("left", `${left + 14}px`)
        .style("top", `${top - 36}px`)
        .html(`<strong style="color: #111318; font-weight: 750;">${d.attribute}</strong><br/>${d.gender_group}<br/>Average price: $${d.average_price.toFixed(2)}<br/>Average rating: ${d.average_rating.toFixed(2)}<br/>Books: ${d3.format(",")(d.books)}`);
    })
    .on("mouseout", () => scatterTooltip.style("opacity", 0))
    .transition()
    .duration(350)
    .attr("opacity", 0.9)
    .attr("transform", d => `translate(${x(d.average_rating)},${y(d.average_price)})`)
    .attr("d", d => d3.symbol().type(symbolByGender[d.gender_group]).size(compact ? 105 : 135)());
}

function populateAttributes(data, color) {
  const attributeType = scatterMode.property("value");
  const minimum = +scatterMin.property("value");
  const attributes = Array.from(new Set(
    data
      .filter(d => d.attribute_type === attributeType && d.books >= minimum)
      .map(d => d.attribute)
  )).sort(d3.ascending);

  attributeHeading.text(attributeType === "genre" ? "Genres" : "Author nationalities");
  genreOptions.selectAll("*").remove();
  attributes.forEach(attribute => {
    const label = genreOptions.append("label")
      .style("display", "inline-flex")
      .style("align-items", "center")
      .style("gap", "6px")
      .style("font-size", "12px");
    label.append("input")
      .attr("type", "checkbox")
      .attr("name", "scatter-attribute")
      .attr("value", attribute)
      .property("checked", true);
    label.append("span")
      .style("display", "inline-block")
      .style("width", "10px")
      .style("height", "10px")
      .style("border-radius", "2px")
      .style("background", color(attribute));
    label.append("span").text(attribute);
  });
}

d3.csv("/data/gender_price_scatter.csv", d3.autoType).then(data => {
  const attributes = Array.from(new Set(data.map(d => d.attribute)));
  const color = d3.scaleOrdinal().domain(attributes).range(scatterColors);

  populateAttributes(data, color);
  drawScatter(data, color);
  genderOptions.selectAll("input").on("change", () => drawScatter(data, color));
  genreOptions.on("change", () => drawScatter(data, color));
  scatterMode.on("change", () => {
    populateAttributes(data, color);
    drawScatter(data, color);
  });
  scatterMin.on("input", () => {
    populateAttributes(data, color);
    drawScatter(data, color);
  });
  resetGenres.on("click", () => {
    genreOptions.selectAll("input").property("checked", true);
    drawScatter(data, color);
  });
  window.addEventListener("resize", () => drawScatter(data, color));
}).catch(err => {
  scatterSummary.text("Could not load gender-genre pricing data.");
  console.error("Error loading gender-genre scatter data:", err);
});
{{< /d3 >}}
<!-- prettier-ignore-end -->

## Line chart

<!-- prettier-ignore-start -->
{{< d3 >}}
const margin = {top: 20, right: 20, bottom: 40, left: 40};
const width = container.clientWidth - margin.left - margin.right;
const height = 300 - margin.top - margin.bottom;

const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
const data = [65, 59, 80, 81, 56, 55, 40];

const svg = d3.select(container).append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", `translate(${margin.left},${margin.top})`);

const x = d3.scalePoint().domain(labels).range([0, width]);
const y = d3.scaleLinear().domain([0, d3.max(data)]).nice().range([height, 0]);

svg.append("g").attr("transform", `translate(0,${height})`).call(d3.axisBottom(x));
svg.append("g").call(d3.axisLeft(y));

const line = d3.line()
  .x((d, i) => x(labels[i]))
  .y(d => y(d))
  .curve(d3.curveCatmullRom.alpha(0.2));

svg.append("path")
  .datum(data)
  .attr("fill", "none")
  .attr("stroke", congoColors.primary400)
  .attr("stroke-width", 2)
  .attr("d", line);

svg.selectAll(".dot")
  .data(data)
  .enter().append("circle")
  .attr("cx", (d, i) => x(labels[i]))
  .attr("cy", d => y(d))
  .attr("r", 4)
  .attr("fill", congoColors.primary300)
  .attr("stroke", congoColors.primary400);
{{< /d3 >}}
<!-- prettier-ignore-end -->

## Doughnut chart

<!-- prettier-ignore-start -->
{{< d3 >}}
const width = container.clientWidth;
const height = 300;
const radius = Math.min(width, height) / 2 - 20;

const labels = ['Red', 'Blue', 'Yellow'];
const data = [300, 50, 100];

const svg = d3.select(container).append("svg")
  .attr("width", width)
  .attr("height", height)
  .append("g")
  .attr("transform", `translate(${width / 2},${height / 2})`);

const pie = d3.pie().value(d => d);
const arc = d3.arc().innerRadius(radius * 0.6).outerRadius(radius);
const arcHover = d3.arc().innerRadius(radius * 0.6).outerRadius(radius + 4);

const color = d3.scaleOrdinal()
  .domain(labels)
  .range([congoColors.primary200, congoColors.primary300, congoColors.primary400]);


svg.selectAll(".slice")
  .data(pie(data))
  .enter().append("path")
  .attr("d", arc)
  .attr("fill", (d, i) => color(labels[i]))
  .attr("stroke", "none")
  .on("mouseover", function() { d3.select(this).attr("d", arcHover); })
  .on("mouseout", function() { d3.select(this).attr("d", arc); });

const legend = svg.selectAll(".legend")
  .data(labels)
  .enter().append("g")
  .attr("transform", (d, i) => `translate(${radius + 10}, ${-radius + i * 22})`);

legend.append("rect").attr("width", 14).attr("height", 14).attr("fill", (d, i) => color(labels[i]));
legend.append("text").attr("x", 18).attr("y", 11).style("font-size", "13px").text(d => d);
{{< /d3 >}}
<!-- prettier-ignore-end -->

## Cartogram

<!-- prettier-ignore-start -->
<script src="https://unpkg.com/topojson@3/dist/topojson.min.js"></script>
<script src="/js/cartogram.js"></script>

{{< d3 >}}
d3.cartogram = cartogramFactory;
const width = container.clientWidth;
const height = 500;
d3.select(container).style("position", "relative");

const svg = d3.select(container).append("svg")
  .attr("width", width)
  .attr("height", height);

const proj = d3.geoNaturalEarth1()
  .translate([width / 2, height / 2])
  .scale(width / (2 * Math.PI));

const carto = d3.cartogram()
  .projection(proj);

const staticPath = d3.geoPath().projection(proj);

// --- Tooltip ---
const tooltip = d3.select(container).append("div")
  .style("position", "absolute")
  .style("background", congoColors.neutral100)
  .style("color", congoColors.neutral700)
  .style("padding", "6px 10px")
  .style("border-radius", "4px")
  .style("font-size", "13px")
  .style("pointer-events", "none")
  .style("opacity", 0);

// --- Toggle button ---
let distorted = true;
const button = d3.select(container).append("button")
  .text("Show Normal Map")
  .style("margin-bottom", "8px")
  .style("padding", "6px 12px")
  .style("background", congoColors.primary400)
  .style("color", congoColors.neutral100)
  .style("border", "none")
  .style("border-radius", "4px")
  .style("cursor", "pointer");

Promise.all([
  d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json"),
  d3.csv("/data/nationalities.csv")
]).then(([topology, data]) => {
  const dataById = new Map(
    data
      .filter(d => d["ID"] && d["ID"] !== "nan")
      .map(d => [+d["ID"], { counts: +d["counts"], name: d["nationality"] }])
  );
  const nameById = new Map(
    topology.objects.countries.geometries.map(d => [+d.id, d.properties?.name ?? "Unknown"])
  );


  // Split geometries
  const problematicIDs = [10, 643, 242]; // Antarctica, Russia
  const cartoGeometries = topology.objects.countries.geometries
    .filter(d => !problematicIDs.includes(+d.id));

  const staticGeometries = topology.objects.countries.geometries
    .filter(d => problematicIDs.includes(+d.id)); // Russia yes, Antarctica no


  const values = cartoGeometries.map(d =>  dataById.get(+d.id)?.counts ?? 0);

  const lo = d3.min(values), hi = d3.max(values);

  const scale = d3.scaleLinear().domain([lo, hi]).range([1, 20]);
  const colorScale = d3.scaleSequentialLog(d3.interpolate(
  congoColors.neutral100,
  congoColors.primary500
  )).domain([1, hi]);

  const color = d => {
    const counts = dataById.get(+d.id)?.counts ?? 0;
    return counts === 0 ? congoColors.neutral100 : colorScale(counts);
  };

  // Tooltip handlers
  const onMouseover = (event, d) => {
    const id = +d.id;
    const entry = dataById.get(id);
    const name = entry?.name ?? nameById.get(id) ?? "Unknown";
    const counts = entry?.counts ?? 0;
    tooltip.style("opacity", 1)
      .html(`<strong>${name}</strong><br/>${counts} book${counts !== 1 ? "s" : ""}`);
  };

  const onMousemove = (event) => {
    const [x, y] = d3.pointer(event, container);
    tooltip
      .style("left", `${x + 12}px`)
      .style("top", `${y - 28}px`);
  };

  const onMouseout = () => tooltip.style("opacity", 0);

  carto
    .properties(d => ({ id: d.ID }))
    .value(d => scale(dataById.get(+d.id)?.counts ?? 0));

  const features = carto(topology, cartoGeometries).features;
  const cartoFeatures = carto(topology, cartoGeometries).features;
  const normalFeatures = cartoGeometries.map(d => topojson.feature(topology, d));

  // Draw exluded countries because of anti-meridian as static layer first
  svg.selectAll(".static-country")
    .data(staticGeometries.map(d => topojson.feature(topology, d)))
    .enter().append("path")
    .attr("class", "static-country")
    .attr("d", staticPath)
    .attr("fill", color)
    .attr("stroke", congoColors.neutral100)
    .attr("stroke-width", 0.5)
    .on("mouseover", onMouseover)
    .on("mousemove", onMousemove)
    .on("mouseout", onMouseout);

  // Draw cartogram countries
  const paths = svg.selectAll(".carto-country")
    .data(cartoFeatures)
    .enter().append("path")
    .attr("class", "carto-country")
    .attr("d", carto.path)
    .attr("fill", color)
    .attr("stroke", congoColors.neutral100)
    .attr("stroke-width", 0.5)
    .on("mouseover", onMouseover)
    .on("mousemove", onMousemove)
    .on("mouseout", onMouseout);

  // Toggle between distorted and normal
  button.on("click", () => {
    distorted = !distorted;
    button.text(distorted ? "Show Normal Map" : "Show Cartogram");

    paths.transition().duration(750)
      .attr("d", (d, i) => distorted
        ? carto.path(d)
        : staticPath(normalFeatures[i])
      );
  });

}).catch(err => {
  console.error("Error loading data:", err);
});
{{< /d3 >}}
<!-- prettier-ignore-end -->

## Gender explorator

<!-- prettier-ignore-start -->
{{< d3 >}}
const root = d3.select(container)
  .style("position", "relative")
  .style("max-width", "100%")
  .style("font-family", "inherit");

const controls = root.append("div")
  .style("display", "grid")
  .style("grid-template-columns", "repeat(auto-fit, minmax(150px, 1fr))")
  .style("gap", "12px")
  .style("align-items", "end")
  .style("margin", "4px 0 18px");

function control(labelText) {
  const wrap = controls.append("label")
    .style("display", "grid")
    .style("gap", "6px")
    .style("font-size", "13px")
    .style("color", congoColors.neutral700);
  wrap.append("span")
    .style("font-weight", 650)
    .text(labelText);
  return wrap;
}

function styleInput(selection) {
  selection
    .style("width", "100%")
    .style("box-sizing", "border-box")
    .style("border", `1px solid ${congoColors.primary200}`)
    .style("border-radius", "6px")
    .style("padding", "7px 9px")
    .style("background", congoColors.neutral100)
    .style("color", congoColors.neutral700);
}

const viewSelect = control("Explore by").append("select");
viewSelect.selectAll("option")
  .data([
    { value: "genre", label: "Book genre" },
    { value: "origin", label: "Author nationality" },
  ])
  .join("option")
  .attr("value", d => d.value)
  .text(d => d.label);
styleInput(viewSelect);

const sortSelect = control("Sort").append("select");
sortSelect.selectAll("option")
  .data([
    { value: "total", label: "Most books" },
    { value: "women", label: "Most women-led" },
    { value: "men", label: "Most men-led" },
    { value: "gap", label: "Largest gap" },
    { value: "name", label: "Name" },
  ])
  .join("option")
  .attr("value", d => d.value)
  .text(d => d.label);
styleInput(sortSelect);

const minWrap = control("Minimum books");
const minValue = minWrap.append("span")
  .style("font-weight", 500)
  .style("font-size", "12px");
const minInput = minWrap.append("input")
  .attr("type", "range")
  .attr("min", 1)
  .attr("max", 100)
  .attr("value", 10)
  .attr("step", 1);

const topWrap = control("Rows shown");
const topValue = topWrap.append("span")
  .style("font-weight", 500)
  .style("font-size", "12px");
const topInput = topWrap.append("input")
  .attr("type", "range")
  .attr("min", 5)
  .attr("max", 30)
  .attr("value", 14)
  .attr("step", 1);

const legend = root.append("div")
  .style("display", "flex")
  .style("flex-wrap", "wrap")
  .style("gap", "12px")
  .style("align-items", "center")
  .style("margin", "0 0 8px")
  .style("font-size", "13px");

const colors = {
  men: "#287c8e",
  women: "#c94f7c",
  mixed: "#d19a2c",
  neutral: "#d6d3cd",
  axis: "#8a8580",
};

[
  ["Men-led", colors.men],
  ["Women-led", colors.women],
  ["Mixed authorship", colors.mixed],
].forEach(([label, color]) => {
  const item = legend.append("span")
    .style("display", "inline-flex")
    .style("align-items", "center")
    .style("gap", "6px");
  item.append("span")
    .style("display", "inline-block")
    .style("width", "12px")
    .style("height", "12px")
    .style("border-radius", "2px")
    .style("background", color);
  item.append("span").text(label);
});

const summary = root.append("div")
  .style("margin", "0 0 12px")
  .style("font-size", "14px")
  .style("font-weight", 650)
  .style("color", congoColors.neutral700);

const tooltip = root.append("div")
  .style("position", "absolute")
  .style("z-index", 5)
  .style("opacity", 0)
  .style("pointer-events", "none")
  .style("background", congoColors.neutral100)
  .style("color", congoColors.neutral700)
  .style("border", `1px solid ${congoColors.primary200}`)
  .style("box-shadow", "0 8px 24px rgba(0, 0, 0, 0.14)")
  .style("border-radius", "6px")
  .style("padding", "9px 11px")
  .style("font-size", "13px")
  .style("line-height", 1.45);

const svg = root.append("svg")
  .style("display", "block")
  .style("width", "100%");

const margin = { top: 24, right: 96, bottom: 36, left: 150 };
const rowHeight = 34;

function formatPercent(value) {
  return d3.format(".0%")(value);
}

function updateControls(data) {
  const view = viewSelect.property("value");
  const maxTotal = d3.max(data.filter(d => d.attribute_type === view), d => d.total) ?? 100;
  const maxMin = Math.max(1, Math.min(500, Math.floor(maxTotal / 2)));
  minInput.attr("max", maxMin);
  if (+minInput.property("value") > maxMin) minInput.property("value", maxMin);
  minValue.text(`${minInput.property("value")}+`);
  topValue.text(topInput.property("value"));
}

function filteredRows(data) {
  const view = viewSelect.property("value");
  const sort = sortSelect.property("value");
  const minimum = +minInput.property("value");
  const limit = +topInput.property("value");

  const rows = data
    .filter(d => d.attribute_type === view && d.total >= minimum && d.gendered_total > 0);

  rows.sort((a, b) => {
    if (sort === "women") return d3.descending(a.pct_women, b.pct_women) || d3.descending(a.total, b.total);
    if (sort === "men") return d3.descending(a.pct_men, b.pct_men) || d3.descending(a.total, b.total);
    if (sort === "gap") return d3.descending(Math.abs(a.disparity), Math.abs(b.disparity)) || d3.descending(a.total, b.total);
    if (sort === "name") return d3.ascending(a.attribute, b.attribute);
    return d3.descending(a.total, b.total);
  });

  return rows.slice(0, limit);
}

function render(data) {
  updateControls(data);

  const rows = filteredRows(data);
  const containerWidth = Math.max(container.clientWidth, 320);
  const compact = containerWidth < 680;
  margin.left = compact ? 112 : 150;
  margin.right = compact ? 58 : 96;
  const width = containerWidth - margin.left - margin.right;
  const height = margin.top + margin.bottom + rows.length * rowHeight;

  svg.attr("viewBox", `0 0 ${containerWidth} ${height}`)
    .attr("height", height);

  const x = d3.scaleLinear()
    .domain([-1, 1])
    .range([margin.left, margin.left + width]);

  const y = d3.scaleBand()
    .domain(rows.map(d => d.attribute))
    .range([margin.top, height - margin.bottom])
    .paddingInner(0.32)
    .paddingOuter(0.1);

  summary.text(`${rows.length} ${viewSelect.property("value") === "genre" ? "genres" : "author nationalities"} shown after filtering`);

  const axis = svg.selectAll(".gender-axis")
    .data([0])
    .join("line")
    .attr("class", "gender-axis")
    .attr("x1", x(0))
    .attr("x2", x(0))
    .attr("y1", margin.top - 12)
    .attr("y2", height - margin.bottom + 10)
    .attr("stroke", colors.axis)
    .attr("stroke-width", 1)
    .attr("stroke-dasharray", "3 4");

  svg.selectAll(".axis-label")
    .data([
      { label: "Men", x: x(-0.98), anchor: "start" },
      { label: "Women", x: x(0.98), anchor: "end" },
    ])
    .join("text")
    .attr("class", "axis-label")
    .attr("x", d => d.x)
    .attr("y", 13)
    .attr("text-anchor", d => d.anchor)
    .attr("fill", congoColors.neutral700)
    .attr("font-size", compact ? 11 : 12)
    .attr("font-weight", 650)
    .text(d => d.label);

  svg.selectAll(".tick-label")
    .data([-1, -0.5, 0, 0.5, 1])
    .join("text")
    .attr("class", "tick-label")
    .attr("x", d => x(d))
    .attr("y", height - 10)
    .attr("text-anchor", "middle")
    .attr("fill", colors.axis)
    .attr("font-size", 11)
    .text(d => d === 0 ? "50/50" : formatPercent(Math.abs(d)));

  const row = svg.selectAll(".gender-row")
    .data(rows, d => d.attribute)
    .join(
      enter => {
        const g = enter.append("g")
          .attr("class", "gender-row")
          .attr("opacity", 0)
          .attr("transform", d => `translate(0,${y(d.attribute) ?? margin.top})`);
        g.append("text").attr("class", "row-name");
        g.append("line").attr("class", "row-guide");
        g.append("rect").attr("class", "men-bar");
        g.append("rect").attr("class", "women-bar");
        g.append("circle").attr("class", "mixed-dot");
        g.append("text").attr("class", "row-value");
        return g;
      },
      update => update,
      exit => exit.transition().duration(180).attr("opacity", 0).remove()
    );

  row.transition()
    .duration(360)
    .attr("opacity", 1)
    .attr("transform", d => `translate(0,${y(d.attribute)})`);

  row.select(".row-name")
    .attr("x", margin.left - 10)
    .attr("y", y.bandwidth() / 2)
    .attr("dy", "0.35em")
    .attr("text-anchor", "end")
    .attr("fill", congoColors.neutral700)
    .attr("font-size", compact ? 11 : 12)
    .attr("font-weight", 600)
    .text(d => compact && d.attribute.length > 16 ? `${d.attribute.slice(0, 15)}...` : d.attribute);

  row.select(".row-guide")
    .attr("x1", margin.left)
    .attr("x2", margin.left + width)
    .attr("y1", y.bandwidth() / 2)
    .attr("y2", y.bandwidth() / 2)
    .attr("stroke", colors.neutral)
    .attr("stroke-width", 1);

  row.select(".men-bar")
    .attr("y", 0)
    .attr("height", y.bandwidth())
    .attr("rx", 3)
    .attr("fill", colors.men)
    .on("mousemove", showTooltip)
    .on("mouseout", hideTooltip)
    .transition()
    .duration(360)
    .attr("x", d => x(-d.pct_men))
    .attr("width", d => Math.max(1, x(0) - x(-d.pct_men)));

  row.select(".women-bar")
    .attr("y", 0)
    .attr("height", y.bandwidth())
    .attr("rx", 3)
    .attr("fill", colors.women)
    .on("mousemove", showTooltip)
    .on("mouseout", hideTooltip)
    .transition()
    .duration(360)
    .attr("x", x(0))
    .attr("width", d => Math.max(1, x(d.pct_women) - x(0)));

  row.select(".mixed-dot")
    .attr("cy", y.bandwidth() / 2)
    .attr("fill", colors.mixed)
    .attr("stroke", congoColors.neutral100)
    .attr("stroke-width", 1)
    .on("mousemove", showTooltip)
    .on("mouseout", hideTooltip)
    .transition()
    .duration(360)
    .attr("cx", d => x(d.disparity))
    .attr("r", d => d.mixed > 0 ? Math.max(3, Math.min(8, Math.sqrt(d.mixed))) : 0);

  row.select(".row-value")
    .attr("x", margin.left + width + 10)
    .attr("y", y.bandwidth() / 2)
    .attr("dy", "0.35em")
    .attr("fill", congoColors.neutral700)
    .attr("font-size", compact ? 10 : 12)
    .attr("font-weight", 650)
    .text(d => `${formatPercent(d.pct_women)} W`);
}

function showTooltip(event, d) {
  const [x, y] = d3.pointer(event, container);
  tooltip
    .style("opacity", 1)
    .style("left", `${x + 14}px`)
    .style("top", `${y - 34}px`)
    .html(`<strong>${d.attribute}</strong><br/>Women-led: ${d.women}<br/>Men-led: ${d.men}<br/>Mixed authorship: ${d.mixed}<br/>Total books: ${d.total}`);
}

function hideTooltip() {
  tooltip.style("opacity", 0);
}

d3.csv("/data/gender_attribute_summary.csv", d3.autoType).then(data => {
  render(data);
  viewSelect.on("change", () => render(data));
  sortSelect.on("change", () => render(data));
  minInput.on("input", () => render(data));
  topInput.on("input", () => render(data));
  window.addEventListener("resize", () => render(data));
}).catch(err => {
  summary.text("Could not load gender disparity data.");
  console.error("Error loading gender explorator data:", err);
});
{{< /d3 >}}
<!-- prettier-ignore-end -->
