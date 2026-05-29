---
title: "The Countries Race"
date: 2026-04-13
description: "Bar race representing books published by each author nationality over time, with optional population scaling."
tags: ["d3", "visualization"]
layout: "simple"
---
This visualisation represents the number of authors from each country over time, with the option to scale by million inhabitants. The data spans from 2013 to 2022, which corresponds to the range available in the International Bestsellers dataset. We chose to only show the top 10 countries.

Even though the United States publishes more books overall, it does not have the highest ratio of authors per million inhabitants. Switching to the scaled view reveals that Iceland reaches around 32 authors per million inhabitants in 2022, making it by far the most represented country relative to its size.

It is interesting to see the top 3 shift between views: scaled it is Iceland, Norway and Spain, unscaled it is the United States, France and Spain. Spain's author count is high enough that it holds its place in the top 3 either way.

*Toggle the button to see the race with data scaled by inhabitants. Please note that the toggle is disabled while the race is running :)*
<!-- prettier-ignore-start -->
{{< d3 >}}
const n = 10;
const k = 10;
const barSize = 48;
const margin = { top: 20, right: 6, bottom: 6, left: 50 };
const width = container.clientWidth - margin.left - margin.right;
const height = margin.top + barSize * n + margin.bottom;


const svg = d3.select(container).append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", `translate(${margin.left},${margin.top})`);

d3.select(container).style("position", "relative");

const isDark = document.documentElement.classList.contains("dark");
const labelColor = isDark ? congoColors.neutral100 : congoColors.neutral700;

// --- Toggle ---
let useScaled = false;
let animDuration = 250;

const toggleWrapper = d3.select(container).insert("div", "svg")
  .style("margin-bottom", "10px")
  .style("display", "flex")
  .style("align-items", "center")
  .style("gap", "10px");

toggleWrapper.append("span")
  .text("Unscaled")
  .style("font-size", "15px")
  .style("color", congoColors.neutral700);

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
  .text("Scaled per inhabitants")
  .style("font-size", "15px")
  .style("color", congoColors.neutral700);

toggleWrapper.append("span")
  .text("Speed:")
  .style("font-size", "15px")
  .style("color", congoColors.neutral700)
  .style("margin-left", "20px");


const speedSlider = toggleWrapper.append("input")
  .attr("type", "range")
  .attr("min", 50)
  .attr("max", 1000)
  .attr("value", 250)
  .attr("step", 50)
  .style("accent-color", congoColors.primary300)
  .style("cursor", "pointer");


const speedLabel = toggleWrapper.append("span")
  .text("1x")
  .style("font-size", "15px")
  .style("min-width", "35px")
  .style("color", congoColors.neutral700);


// --- Toggle ---
const tooltip = d3.select(container).append("div")
  .style("position", "absolute")
  .style("background", isDark ? "#333" : "#fff")
  .style("color", isDark ? "#fff" : "#333")
  .style("border", "1px solid #ccc")
  .style("border-radius", "6px")
  .style("padding", "4px 10px")
  .style("font-size", "13px")
  .style("pointer-events", "none")
  .style("opacity", 0)
  .style("transition", "opacity 0.15s");

function toFlag(alpha2) {
  if (!alpha2 || alpha2.length !== 2) return "🏳";
  return String.fromCodePoint(
    ...alpha2.toUpperCase().split("").map(c => 0x1F1E6 - 65 + c.charCodeAt(0))
  );
}

d3.csv("{{< asset-url "data/nat_date.csv" >}}").then(data => {
  data.forEach(d => {
    d.counts_raw = +d.counts_raw;
    d.counts = +d.counts;
    d.year = +d.year;
  });

  // Build flag map from raw rows
  const natToFlag = new Map();
  data.forEach(d => {
    if (!natToFlag.has(d.nationality) && d.alpha2) {
      natToFlag.set(d.nationality, toFlag(d.alpha2.trim()));
    }
  });

  const nationalities = new Set(data.map(d => d.nationality));

  const colorScale = d3.scaleOrdinal()
    .domain([...nationalities])
    .range([
      congoColors.primary200, congoColors.primary300,
      congoColors.primary400, congoColors.primary500,
    ]);

  const x = d3.scaleLinear([0, 1], [0, width]);
  const y = d3.scaleBand()
    .domain(d3.range(n + 1))
    .rangeRound([margin.top, margin.top + barSize * (n + 1 + 0.1)])
    .padding(0.1);

  speedSlider.on("input", function(event) {
    animDuration = 1050 - +event.target.value;
    // Invert so higher slider = faster, display as multiplier
    const mult = (250 / animDuration).toFixed(1);
    speedLabel.text(`${mult}x`);

    svg.selectAll("*").interrupt();
    run(keyframes);
  });

  function rank(valueFn) {
    const arr = Array.from(nationalities, nationality => ({
      nationality,
      counts: valueFn(nationality)
    }));
    arr.sort((a, b) => d3.descending(a.counts, b.counts));
    for (let i = 0; i < arr.length; ++i) arr[i].rank = Math.min(n, i);
    return arr;
  }

  // Build keyframes from a given value column
  function buildKeyframes(valueCol) {
    const datevalues = Array.from(
      d3.rollup(data, ([d]) => d[valueCol], d => d.year, d => d.nationality)
    )
      .map(([year, data]) => [year, data])
      .sort(([a], [b]) => d3.ascending(a, b));

    const kf = [];
    let ka, a, kb, b;
    for ([[ka, a], [kb, b]] of d3.pairs(datevalues)) {
      for (let i = 0; i < k; ++i) {
        const t = i / k;
        kf.push([
          ka * (1 - t) + kb * t,
          rank(nat => (a.get(nat) || 0) * (1 - t) + (b.get(nat) || 0) * t)
        ]);
      }
    }
    kf.push([kb, rank(nat => b.get(nat) || 0)]);
    return kf;
  }

  let keyframes = buildKeyframes("counts_raw");

  function getPrevNext(kf) {
    const nameframes = d3.groups(kf.flatMap(([, data]) => data), d => d.nationality);
    const prev = new Map(nameframes.flatMap(([, data]) => d3.pairs(data, (a, b) => [b, a])));
    const next = new Map(nameframes.flatMap(([, data]) => d3.pairs(data, (a, b) => [a, b])));
    return { prev, next };
  }

  let { prev, next } = getPrevNext(keyframes);

  const formatRaw    = d3.format(",d");
  const formatScaled = d3.format(".2f");
  let formatNumber   = formatRaw;
  const formatDate   = d => Math.round(d).toString();

  function bars(svg) {
    let bar = svg.append("g").attr("fill-opacity", 0.85).selectAll("rect");
    return ([, data], transition) => bar = bar
      .data(data.slice(0, n), d => d.nationality)
      .join(
        enter => enter.append("rect")
          .attr("fill", d => colorScale(d.nationality))
          .attr("height", y.bandwidth())
          .attr("x", x(0))
          .attr("y", d => y((prev.get(d) || d).rank))
          .attr("width", d => Math.max(0, x((prev.get(d) || d).counts) - x(0)))
          .on("mouseover", (event, d) => {
            tooltip.style("opacity", 1).text(d.nationality);
          })
          .on("mousemove", (event) => {
            const [x, y] = d3.pointer(event, container);
            tooltip
              .style("left", `${x + 12}px`)
              .style("top", `${y - 28}px`);
          })
          .on("mouseout", () => tooltip.style("opacity", 0)),
        update => update,
        exit => exit.transition(transition).remove()
          .attr("y", d => y((next.get(d) || d).rank))
          .attr("width", d => Math.max(0, x((next.get(d) || d).counts) - x(0)))
      )
      .call(bar => bar.transition(transition)
        .attr("y", d => y(d.rank))
        .attr("width", d => Math.max(0, x(d.counts) - x(0))));
  }

  function flags(svg) {
    let flag = svg.append("g")
      .style("font-size", `${barSize * 0.55}px`)
      .style("font-family", "sans-serif")
      .selectAll("text");
    return ([, data], transition) => flag = flag
      .data(data.slice(0, n), d => d.nationality)
      .join(
        enter => enter.append("text")
          .attr("x", -8)
          .attr("y", d => y((prev.get(d) || d).rank) + y.bandwidth() / 2)
          .attr("dy", "0.35em")
          .attr("text-anchor", "end")
          .attr("opacity", 0)
          .text(d => natToFlag.get(d.nationality) ?? "🏳")
          .on("mouseover", (event, d) => {
            tooltip.style("opacity", 1).text(d.nationality);
          })
          .on("mousemove", (event) => {
            const rect = container.getBoundingClientRect();
            tooltip
              .style("left", (event.clientX - rect.left + 12) + "px")
              .style("top",  (event.clientY - rect.top  - 28) + "px");
          })
          .on("mouseout", () => tooltip.style("opacity", 0)),
          update => update,
          exit => exit.transition(transition).remove()
            .attr("y", d => y((next.get(d) || d).rank) + y.bandwidth() / 2)
            .attr("opacity", 0)
      )
      .call(flag => flag.transition(transition)
        .attr("y", d => y(d.rank) + y.bandwidth() / 2)
        .attr("opacity", 1));
  }

  // Value tags: inside bar if wide enough, outside if not
  const TAG_MIN_WIDTH = 40;
  function valueTags(svg) {
    let tag = svg.append("g")
      .style("font-size", "11px")
      .style("font-family", "sans-serif")
      .style("font-variant-numeric", "tabular-nums")
      .selectAll("text");
    return ([, data], transition) => tag = tag
      .data(data.slice(0, n), d => d.nationality)
      .join(
        enter => enter.append("text")
          .attr("y", d => y((prev.get(d) || d).rank) + y.bandwidth() / 2)
          .attr("dy", "0.35em")
          .attr("opacity", 0.85),
        update => update,
        exit => exit.transition(transition).remove()
          .attr("y", d => y((next.get(d) || d).rank) + y.bandwidth() / 2)
      )
      .call(tag => tag.transition(transition)
        .attr("y", d => y(d.rank) + y.bandwidth() / 2)
        .attr("x", d => {
          const barW = Math.max(0, x(d.counts) - x(0));
          return barW > TAG_MIN_WIDTH ? barW - 4 : barW + 4;
        })
        .attr("text-anchor", d => {
          const barW = Math.max(0, x(d.counts) - x(0));
          return barW > TAG_MIN_WIDTH ? "end" : "start";
        })
        .attr("fill", d => {
          const barW = Math.max(0, x(d.counts) - x(0));
          return barW > TAG_MIN_WIDTH ? "white" : labelColor;
        })
        .tween("text", d => {
          const i = d3.interpolateNumber((prev.get(d) || d).counts, d.counts);
          return function(t) { this.textContent = formatNumber(i(t)); };
        }));
  }

  function axis(svg) {
    const g = svg.append("g").attr("transform", `translate(0,${margin.top})`);
    const ax = d3.axisTop(x)
      .ticks(width / 160)
      .tickSizeOuter(0)
      .tickSizeInner(-barSize * (n + y.padding()));
    return (_, transition) => {
      g.transition(transition).call(ax);
      g.select(".tick:first-of-type text").remove();
      g.selectAll(".tick:not(:first-of-type) line")
        .attr("stroke", isDark ? "rgba(255,255,255,0.1)" : "rgba(0,0,0,0.1)");
      g.select(".domain").remove();
      g.selectAll("text").attr("fill", labelColor);
    };
  }

  function ticker(svg) {
    const now = svg.append("text")
      .style("font-size", `${barSize * 1.0}px`)
      .style("font-weight", "bold")
      .style("font-family", "sans-serif")
      .style("font-variant-numeric", "tabular-nums")
      .attr("text-anchor", "end")
      .attr("x", width - 6)
      .attr("y", margin.top + barSize * (n - 0.45))
      .attr("dy", "0.32em")
      .attr("fill", labelColor)
      .text(formatDate(keyframes[0][0]));
    return ([date], transition) => {
      transition.end().then(() => now.text(formatDate(date)));
    };
  }

  let runId = 0;

async function run(kf) {
  const myId = ++runId;  // claim a unique ID for this run

  svg.selectAll("*").remove();

  const updateBars      = bars(svg);
  const updateFlags     = flags(svg);
  const updateValueTags = valueTags(svg);
  const updateAxis      = axis(svg);
  const updateTicker    = ticker(svg);

  try {
    for (const keyframe of kf) {
      if (runId !== myId) break;
      const transition = svg.transition().duration(animDuration).ease(d3.easeLinear);
      x.domain([0, d3.max(keyframe[1], d => d.counts)]);
      updateAxis(keyframe, transition);
      updateBars(keyframe, transition);
      updateFlags(keyframe, transition);
      updateValueTags(keyframe, transition);
      updateTicker(keyframe, transition);
      await transition.end();
    }
  } catch {
  }
}

  run(keyframes)

  checkbox.on("change", function(event) {
    useScaled = event.target.checked;
    knob.style("background-color", useScaled ? congoColors.primary500 : congoColors.primary300);
    knob.select(".knob-inner").style("transform", useScaled ? "translateX(22px)" : "translateX(0)");

    formatNumber = useScaled ? formatScaled : formatRaw;
    keyframes = buildKeyframes(useScaled ? "counts" : "counts_raw");
    ({ prev, next } = getPrevNext(keyframes));

    svg.selectAll("*").interrupt();
    run(keyframes);
  });
});
{{< /d3 >}}
<!-- prettier-ignore-end -->
