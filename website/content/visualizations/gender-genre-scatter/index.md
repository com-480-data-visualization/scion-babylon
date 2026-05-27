---
title: "The gender-genre scatter"
description: "Compare average price and average rating by genre or author nationality and gender group."
tags: ["d3", "visualization"]
---

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
