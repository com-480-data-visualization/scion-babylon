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
