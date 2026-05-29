---
title: "The Gender Scatter"
description: "Compare average price and average rating by genre or author nationality and gender group."
tags: ["d3", "visualization"]
layout: "simple"
---

This scatterplot compares average book price and average rating for male and female author groups across genres or author nationalities.

Each point summarizes one category, making it easier to see whether rating and price patterns differ between gender groups for the same part of the dataset.

Use the group selector and category filters to clean up the cloud of points, then hover around to spot the categories that behave a little differently from the rest.

Selecting all genres and all nationalities allows us to see that one average women are selling books for a lower price and their books seem to be consitentily rated lower. Across genres the disparity seems more stricking that accross nationalities. It should mentionned that the rating scale does not have a very big range as most books seem to be in the range between 3 to 5.

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
const genderColors = {
  "Male authors": "#a5d8ff",
  "Non-male authors": "#bd93f9",
};
const symbolByGender = {
  "Male authors": d3.symbolCircle,
  "Non-male authors": d3.symbolDiamond,
};
const genderLabels = {
  "Male authors": "Male authors",
  "Non-male authors": "Female authors",
};
const minimumBooks = 2;

const scatterLayout = scatterRoot.append("div")
  .style("display", "grid")
  .style("grid-template-columns", "minmax(150px, 184px) minmax(0, 1fr)")
  .style("align-items", "stretch")
  .style("column-gap", "18px");

const scatterControls = scatterLayout.append("aside")
  .style("display", "grid")
  .style("gap", "16px")
  .style("border-right", `1px solid ${scatterTheme.border}`)
  .style("padding", "4px 16px 4px 0")
  .style("color", scatterTheme.foreground);

const scatterModeWrap = scatterControls.append("label")
  .style("display", "grid")
  .style("gap", "7px")
  .style("font-size", "13px")
  .style("font-weight", 650);
scatterModeWrap.append("span").text("Group by");
const scatterMode = scatterModeWrap.append("select")
  .style("width", "100%")
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

const genderLegend = scatterControls.append("div");
genderLegend.append("div")
  .style("font-size", "13px")
  .style("font-weight", 650)
  .style("margin-bottom", "7px")
  .text("Gender group");
const genderOptions = genderLegend.append("div")
  .style("display", "flex")
  .style("gap", "14px")
  .style("flex-wrap", "wrap");

["Male authors", "Non-male authors"].forEach(group => {
  const label = genderOptions.append("label")
    .style("display", "inline-flex")
    .style("align-items", "center")
    .style("gap", "6px")
    .style("font-size", "13px");
  label.append("svg")
    .attr("width", 15)
    .attr("height", 15)
    .append("path")
    .attr("transform", "translate(7.5,7.5)")
    .attr("d", d3.symbol().type(symbolByGender[group]).size(80)())
    .attr("fill", genderColors[group])
    .attr("stroke", scatterTheme.pointStroke)
    .attr("stroke-width", 1);
  label.append("span").text(genderLabels[group]);
});

const genreFilter = scatterControls.append("fieldset")
  .style("border", "none")
  .style("padding", 0)
  .style("margin", 0);
const genreHeader = genreFilter.append("div")
  .style("display", "flex")
  .style("flex-wrap", "wrap")
  .style("justify-content", "space-between")
  .style("align-items", "center")
  .style("gap", "12px")
  .style("margin-bottom", "7px");
const attributeHeading = genreHeader.append("span")
  .style("font-size", "13px")
  .style("font-weight", 650);
const attributeActions = genreHeader.append("div")
  .style("display", "flex")
  .style("gap", "6px");
function attributeButton(label) {
  return attributeActions.append("button")
    .attr("type", "button")
    .style("border", `1px solid ${scatterTheme.border}`)
    .style("background", "transparent")
    .style("color", scatterTheme.foreground)
    .style("border-radius", "6px")
    .style("font-size", "12px")
    .style("padding", "4px 9px")
    .style("cursor", "pointer")
    .text(label);
}
const resetGenres = attributeButton("Select all");
const clearGenres = attributeButton("None");
const genreOptions = genreFilter.append("div")
  .style("display", "grid")
  .style("gap", "6px")
  .style("max-height", "380px")
  .style("overflow-y", "auto")
  .style("padding-right", "3px");

const scatterChartWrap = scatterLayout.append("div")
  .style("min-width", 0)
  .style("padding", "0");

const scatterSummary = scatterChartWrap.append("div")
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

const scatterSvg = scatterChartWrap.append("svg")
  .style("display", "block")
  .style("width", "100%");
const scatterChart = scatterSvg.append("g");
const scatterGrid = scatterChart.append("g");
const scatterXAxis = scatterChart.append("g");
const scatterYAxis = scatterChart.append("g");
const scatterXTitle = scatterChart.append("text");
const scatterYTitle = scatterChart.append("text");

function eligibleAttributes(data) {
  const attributeType = scatterMode.property("value");
  const grouped = d3.group(
    data.filter(d => d.attribute_type === attributeType),
    d => d.attribute
  );
  return new Set(Array.from(grouped, ([attribute, rows]) => {
    const counts = new Map(rows.map(d => [d.gender_group, d.books]));
    return counts.get("Male authors") >= minimumBooks && counts.get("Non-male authors") >= minimumBooks
      ? attribute
      : null;
  }).filter(Boolean));
}

function compoundedPoints(data) {
  const attributeType = scatterMode.property("value");
  const eligible = eligibleAttributes(data);
  const attributes = new Set(
    genreOptions.selectAll("input:checked").nodes().map(node => node.value)
  );
  const selected = data.filter(d =>
    d.attribute_type === attributeType && eligible.has(d.attribute) && attributes.has(d.attribute)
  );

  return ["Male authors", "Non-male authors"].map(group => {
    const rows = selected.filter(d => d.gender_group === group);
    const books = d3.sum(rows, d => d.books);
    return {
      gender_group: group,
      average_price: books ? d3.sum(rows, d => d.average_price * d.books) / books : null,
      average_rating: books ? d3.sum(rows, d => d.average_rating * d.books) / books : null,
      books,
      attributes: new Set(rows.map(d => d.attribute)).size,
    };
  }).filter(d => d.books > 0);
}

function drawScatter(data) {
  const visible = compoundedPoints(data);
  const attributeType = scatterMode.property("value");
  const eligible = eligibleAttributes(data);
  const available = data.filter(d => d.attribute_type === attributeType && eligible.has(d.attribute));
  const layoutWidth = Math.max(container.clientWidth, 290);
  const stacked = layoutWidth < 430;
  scatterLayout.style(
    "grid-template-columns",
    stacked ? "minmax(0, 1fr)" : "minmax(150px, 184px) minmax(0, 1fr)"
  ).style("row-gap", stacked ? "16px" : "0");
  scatterControls.style("border-right", stacked ? "none" : `1px solid ${scatterTheme.border}`)
    .style("border-bottom", stacked ? `1px solid ${scatterTheme.border}` : "none")
    .style("padding", stacked ? "0 0 14px" : "4px 16px 4px 0");
  genreOptions.style("max-height", stacked ? "180px" : "380px");

  const width = Math.max(scatterChartWrap.node().clientWidth, 290);
  const compact = width < 560;
  const margin = { top: 22, right: compact ? 18 : 30, bottom: 53, left: compact ? 54 : 68 };
  const height = compact ? 430 : 530;
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
  const selectedCount = visible.length ? d3.max(visible, d => d.attributes) : 0;
  scatterSummary.text(`${selectedCount} ${attributeType === "genre" ? "genres" : "author nationalities"} combined - ${d3.format(",")(totalBooks)} priced records`);

  const points = scatterChart.selectAll(".scatter-point")
    .data(visible, d => d.gender_group)
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
    .attr("fill", d => genderColors[d.gender_group])
    .attr("stroke", scatterTheme.pointStroke)
    .attr("stroke-width", 2)
    .on("mousemove", (event, d) => {
      const [left, top] = d3.pointer(event, container);
      scatterTooltip
        .style("opacity", 1)
        .style("left", `${left + 14}px`)
        .style("top", `${top - 36}px`)
        .html(`<strong style="color: #111318; font-weight: 750;">${genderLabels[d.gender_group]}</strong><br/>Selected categories: ${d.attributes}<br/>Average price: $${d.average_price.toFixed(2)}<br/>Average rating: ${d.average_rating.toFixed(2)}<br/>Books: ${d3.format(",")(d.books)}`);
    })
    .on("mouseout", () => scatterTooltip.style("opacity", 0))
    .transition()
    .duration(350)
    .attr("opacity", 0.9)
    .attr("transform", d => `translate(${x(d.average_rating)},${y(d.average_price)})`)
    .attr("d", d => d3.symbol().type(symbolByGender[d.gender_group]).size(compact ? 105 : 135)());
}

function populateAttributes(data) {
  const attributeType = scatterMode.property("value");
  const attributes = Array.from(eligibleAttributes(data)).sort(d3.ascending);

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
    label.append("span").text(attribute);
  });
}

d3.csv("{{< asset-url "data/gender_price_scatter.csv" >}}", d3.autoType).then(data => {
  populateAttributes(data);
  drawScatter(data);
  genreOptions.on("change", () => drawScatter(data));
  scatterMode.on("change", () => {
    populateAttributes(data);
    drawScatter(data);
  });
  resetGenres.on("click", () => {
    genreOptions.selectAll("input").property("checked", true);
    drawScatter(data);
  });
  clearGenres.on("click", () => {
    genreOptions.selectAll("input").property("checked", false);
    drawScatter(data);
  });
  window.addEventListener("resize", () => drawScatter(data));
}).catch(err => {
  scatterSummary.text("Could not load gender-genre pricing data.");
  console.error("Error loading gender-genre scatter data:", err);
});
{{< /d3 >}}
<!-- prettier-ignore-end -->
