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
