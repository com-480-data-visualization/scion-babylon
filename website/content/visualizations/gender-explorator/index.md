---
title: "Gender explorator"
description: "Explore gender disparity across genres and author nationalities."
tags: ["d3", "visualization"]
---

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

const minimumBooks = 6;

const topWrap = control("Rows shown");
const topValue = topWrap.append("span")
  .style("font-weight", 500)
  .style("font-size", "12px")
  .style("color", "#111318");
const topInput = topWrap.append("input")
  .attr("type", "range")
  .attr("min", 1)
  .attr("max", 30)
  .attr("value", 11)
  .attr("step", 1)
  .style("accent-color", "#bd93f9");

const legend = root.append("div")
  .style("display", "flex")
  .style("flex-wrap", "wrap")
  .style("gap", "12px")
  .style("align-items", "center")
  .style("margin", "0 0 8px")
  .style("font-size", "13px");

const colors = {
  men: "#a5d8ff",
  women: "#bd93f9",
  neutral: "#d6d3cd",
  axis: "#8a8580",
};

[
  ["Men-led", colors.men],
  ["Women-led", colors.women],
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
  const availableRows = data.filter(d =>
    d.attribute_type === view &&
    d.total >= minimumBooks &&
    d.gendered_total > 0
  ).length;
  const maximumRows = Math.max(1, availableRows);
  topInput.attr("max", maximumRows)
    .property("disabled", availableRows <= 1);
  if (+topInput.property("value") > maximumRows) topInput.property("value", maximumRows);
  topValue.text(`${availableRows ? topInput.property("value") : 0} of ${availableRows}`);
}

function filteredRows(data) {
  const view = viewSelect.property("value");
  const sort = sortSelect.property("value");
  const limit = +topInput.property("value");

  const rows = data
    .filter(d => d.attribute_type === view && d.total >= minimumBooks && d.gendered_total > 0);

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

  summary.text(`${rows.length} ${viewSelect.property("value") === "genre" ? "genres" : "author nationalities"} shown - categories with ${minimumBooks}+ books`);

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
    .html(`<strong>${d.attribute}</strong><br/>Women-led: ${d.women}<br/>Men-led: ${d.men}<br/>Other authorship: ${d.mixed + d.unknown}<br/>Total books: ${d.total}`);
}

function hideTooltip() {
  tooltip.style("opacity", 0);
}

d3.csv("{{< asset-url "data/gender_attribute_summary.csv" >}}", d3.autoType).then(data => {
  render(data);
  viewSelect.on("change", () => render(data));
  sortSelect.on("change", () => render(data));
  topInput.on("input", () => render(data));
  window.addEventListener("resize", () => render(data));
}).catch(err => {
  summary.text("Could not load gender disparity data.");
  console.error("Error loading gender explorator data:", err);
});
{{< /d3 >}}
<!-- prettier-ignore-end -->
