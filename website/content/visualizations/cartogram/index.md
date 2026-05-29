---
title: "Authors Across The World"
date: 2026-04-13
description: "Map that scales countries by the number of books published by authors from those countries."
tags: ["d3", "visualization"]
layout: "simple"
---
This map explores the voices amplified by the publishing industry by scaling each country by the number of authors from that country.

This deformed map, called a cartogram, shows that as expected most published authors come from Europe and North America. The United States, Italy and France are among the countries with the most published authors in our dataset. It should be noted that this visualisation was built from the International Bestsellers dataset, which may skew results towards larger countries with more global reach.

We looked for other datasets tracking author origin but this was the best available. As a result, African, Central American and Central Asian authors are underrepresented.

*Toggle the button to discover the scaled map and hover above the countries to see their author counts!*
<!-- prettier-ignore-start -->
<script src="https://unpkg.com/topojson@3/dist/topojson.min.js"></script>
<script src="{{< asset-url "js/cartogram.js" >}}"></script>

{{< d3 >}}
d3.cartogram = cartogramFactory;
const width = container.clientWidth;
const height = 500;
d3.select(container).style("position", "relative");

const svg = d3.select(container).append("svg")
  .attr("width", width)
  .attr("height", height);

const isDark = document.documentElement.classList.contains("dark");
const axisColor = isDark ? congoColors.neutral300 : congoColors.neutral700;

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
let distorted = false;

const toggleWrapper = d3.select(container).insert("div", "svg")
  .style("margin-bottom", "10px")
  .style("display", "flex")
  .style("align-items", "center")
  .style("gap", "10px");

toggleWrapper.append("span")
  .text("Normal map")
  .style("font-size", "15px")
  .style("color", axisColor);

const toggleLabel = toggleWrapper.append("label")
  .style("position", "relative")
  .style("display", "inline-block")
  .style("width", "48px")
  .style("height", "26px")
  .style("cursor", "pointer");

const checkbox = toggleLabel.append("input")
  .attr("type", "checkbox")
  .style("opacity", "0")
  .style("width", "0")
  .style("height", "0");

const knob = toggleLabel.append("span")
  .style("position", "absolute")
  .style("inset", "0")
  .style("background-color", congoColors.primary300)
  .style("border-radius", "26px")
  .style("transition", "background-color .3s");

knob.append("span")
  .attr("class", "knob-inner")
  .style("position", "absolute")
  .style("height", "20px")
  .style("width", "20px")
  .style("left", "3px")
  .style("bottom", "3px")
  .style("background-color", "white")
  .style("border-radius", "50%")
  .style("transition", "transform .3s");

toggleWrapper.append("span")
  .text("Cartogram")
  .style("font-size", "15px")
  .style("color", axisColor);

Promise.all([
  d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json"),
  d3.csv("{{< asset-url "data/nationalities.csv" >}}")
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
  const problematicIDs = [643, 242]; // Antarctica, Russia
  const cartoGeometries = topology.objects.countries.geometries
    .filter(d => !problematicIDs.includes(+d.id));

  const staticGeometries = topology.objects.countries.geometries
    .filter(d => problematicIDs.includes(+d.id));


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

  // Draw normal map first
  const paths = svg.selectAll(".carto-country")
    .data(cartoFeatures)
    .enter().append("path")
    .attr("class", "carto-country")
    .attr("d", (d, i) => staticPath(normalFeatures[i]))
    .attr("fill", color)
    .attr("stroke", congoColors.neutral100)
    .attr("stroke-width", 0.5)
    .on("mouseover", onMouseover)
    .on("mousemove", onMousemove)
    .on("mouseout", onMouseout);

  checkbox.on("change", function() {
  distorted = this.checked;

  knob.style("background-color", distorted ? congoColors.primary500 : congoColors.primary300);
  knob.select(".knob-inner")
    .style("transform", distorted ? "translateX(22px)" : "translateX(0)");

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
