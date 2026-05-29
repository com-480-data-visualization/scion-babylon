---
title: "The Bestseller's Timeline"
description: "Follow bestseller ratings year by year, with women-led titles above the timeline and men-led titles below."
tags: ["d3", "visualization", "timeline"]
layout: "simple"
---

This timeline compares Goodreads-style ratings by publication year for books that appeared in the monthly international bestseller rankings, using all author origins together. Drag or swipe horizontally to move through the full timeline.

It is interesting to note that between 1927 and 1990, there are remarkably few women bestsellers. Which seems to match with the historical context of these years. This visualisations allows us to see that there is not real rating disparity between the women's besteller and the men's bestseller for a given year.

<style>
.bestsellers-timeline .timeline-card {
  cursor: pointer;
  opacity: 0.65;
  transform-box: fill-box;
  transform-origin: center;
  transition: opacity 140ms ease, transform 170ms cubic-bezier(0.2, 0.9, 0.25, 1.12);
  will-change: transform, opacity;
}
.bestsellers-timeline .timeline-year.is-focused .timeline-card {
  opacity: 1;
  transform: translateY(var(--pop-y, -7px)) scale(1.1);
}
.bestsellers-timeline .timeline-year:hover .timeline-card {
  opacity: 1;
  transform: translateY(var(--pop-y, -7px)) scale(1.1);
}
.bestsellers-timeline .timeline-viewport {
  cursor: grab;
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.bestsellers-timeline .timeline-viewport::-webkit-scrollbar {
  display: none;
}
.bestsellers-timeline .timeline-viewport.is-dragging {
  cursor: grabbing;
  user-select: none;
}
.bestsellers-timeline .timeline-viewport.is-dragging .timeline-card {
  transition: none;
}
</style>

<!-- prettier-ignore-start -->
{{< d3 >}}
const timelineRoot = d3.select(container)
  .attr("class", "bestsellers-timeline")
  .style("position", "relative")
  .style("max-width", "100%")
  .style("font-family", "inherit");

const timelineDark = document.documentElement.classList.contains("dark");
const timelineTheme = timelineDark ? {
  foreground: "#f5f4f1",
  secondary: "#d7d4ce",
  panel: "#272932",
  panelStrong: "#30323d",
  border: "#77747d",
  axis: "#c6c2ba",
  faint: "#454751",
} : {
  foreground: "#27282c",
  secondary: "#59565d",
  panel: "#fbfaf8",
  panelStrong: "#ffffff",
  border: "#c6c2ba",
  axis: "#8a8580",
  faint: "#ebe7e0",
};
const timelineColors = {
  women: "#bd93f9",
  men: "#a5d8ff",
  mixed: "#ffbd4a",
  unknown: "#d6d3cd",
};
const timelineLabel = {
  women: "Women-led",
  men: "Men-led",
  mixed: "Mixed authorship",
  unknown: "Unclassified",
};

const timelineHeader = timelineRoot.append("div")
  .style("display", "flex")
  .style("justify-content", "space-between")
  .style("align-items", "end")
  .style("gap", "16px")
  .style("flex-wrap", "wrap")
  .style("margin", "4px 0 18px");

const timelineContext = timelineHeader.append("div")
  .style("display", "grid")
  .style("gap", "4px")
  .style("font-size", "13px")
  .style("color", timelineTheme.foreground);
timelineContext.append("span")
  .style("font-weight", 700)
  .text("All origins");
timelineContext.append("span")
  .style("color", timelineTheme.secondary)
  .text("Combined author origins");

const timelineControls = timelineHeader.append("div")
  .style("display", "flex")
  .style("align-items", "center")
  .style("gap", "8px");

function timelineButton(label, description) {
  return timelineControls.append("button")
    .attr("type", "button")
    .attr("aria-label", description)
    .style("border", "none")
    .style("background", "transparent")
    .style("color", timelineTheme.foreground)
    .style("font-size", "20px")
    .style("font-weight", 750)
    .style("line-height", 1)
    .style("padding", "4px 7px")
    .style("cursor", "pointer")
    .text(label);
}

const previousYearButton = timelineButton("<", "Scroll timeline earlier");
const visibleYearLabel = timelineControls.append("span")
  .style("min-width", "106px")
  .style("text-align", "center")
  .style("margin", "0 8px")
  .style("font-size", "13px")
  .style("font-weight", 700)
  .style("color", timelineTheme.foreground);
const nextYearButton = timelineButton(">", "Scroll timeline later");

const timelineLegend = timelineHeader.append("div")
  .style("display", "flex")
  .style("gap", "16px")
  .style("flex-wrap", "wrap")
  .style("font-size", "13px")
  .style("color", timelineTheme.secondary);
[
  ["Women-led titles", timelineColors.women],
  ["Men-led titles", timelineColors.men],
].forEach(([label, color]) => {
  const item = timelineLegend.append("span")
    .style("display", "inline-flex")
    .style("align-items", "center")
    .style("gap", "7px");
  item.append("span")
    .style("display", "inline-block")
    .style("width", "14px")
    .style("height", "10px")
    .style("border-radius", "3px")
    .style("background", color);
  item.append("span").text(label);
});

const timelineStatus = timelineRoot.append("div")
  .style("color", timelineTheme.secondary)
  .style("font-size", "13px")
  .style("margin", "0 0 9px")
  .text("Drag, swipe, or use the arrows to move through the full timeline. Hover on a year to focus its ratings.");

const timelineViewport = timelineRoot.append("div")
  .attr("class", "timeline-viewport")
  .style("overflow-x", "auto")
  .style("overscroll-behavior-x", "contain")
  .style("touch-action", "pan-x")
  .style("padding", "5px 0 3px");
const timelineSvg = timelineViewport.append("svg")
  .style("display", "block")
  .style("overflow", "visible");

let dragStartX = 0;
let dragStartScrollLeft = 0;
let isDraggingTimeline = false;
let pendingDragScrollLeft = 0;
let dragFrame = null;
timelineViewport
  .on("pointerdown", event => {
    isDraggingTimeline = true;
    dragStartX = event.clientX;
    dragStartScrollLeft = timelineViewport.node().scrollLeft;
    timelineViewport.classed("is-dragging", true);
    timelineViewport.node().setPointerCapture?.(event.pointerId);
  })
  .on("pointermove", event => {
    if (!isDraggingTimeline) return;
    event.preventDefault();
    pendingDragScrollLeft = dragStartScrollLeft - (event.clientX - dragStartX);
    if (dragFrame) return;
    dragFrame = requestAnimationFrame(() => {
      timelineViewport.node().scrollLeft = pendingDragScrollLeft;
      dragFrame = null;
    });
  })
  .on("pointerup pointercancel pointerleave", event => {
    if (!isDraggingTimeline) return;
    isDraggingTimeline = false;
    if (dragFrame) {
      cancelAnimationFrame(dragFrame);
      dragFrame = null;
    }
    timelineViewport.classed("is-dragging", false);
    timelineViewport.node().releasePointerCapture?.(event.pointerId);
  });

const detailPanel = timelineRoot.append("section")
  .style("border", `1px solid ${timelineTheme.border}`)
  .style("border-radius", "10px")
  .style("background", timelineTheme.panel)
  .style("padding", "15px 16px")
  .style("margin-top", "14px");
const detailHeader = detailPanel.append("div")
  .style("display", "flex")
  .style("justify-content", "space-between")
  .style("gap", "12px")
  .style("align-items", "baseline")
  .style("flex-wrap", "wrap")
  .style("margin-bottom", "13px");
const detailTitle = detailHeader.append("strong")
  .style("font-size", "19px")
  .style("color", timelineTheme.foreground);
const detailOrigin = detailHeader.append("span")
  .style("font-size", "13px")
  .style("color", timelineTheme.secondary);
const detailGrid = detailPanel.append("div")
  .style("display", "grid")
  .style("grid-template-columns", "repeat(auto-fit, minmax(205px, 1fr))")
  .style("gap", "10px");

function detailCard(gender) {
  const panel = detailGrid.append("div")
    .style("border-left", `4px solid ${timelineColors[gender]}`)
    .style("border-radius", "5px")
    .style("background", timelineTheme.panelStrong)
    .style("padding", "10px 12px");
  panel.append("div")
    .style("font-size", "12px")
    .style("font-weight", 700)
    .style("color", timelineTheme.secondary)
    .style("text-transform", "uppercase")
    .style("letter-spacing", "0.04em")
    .text(timelineLabel[gender]);
  return {
    root: panel,
    count: panel.append("div")
      .style("font-size", "22px")
      .style("line-height", 1.25)
      .style("font-weight", 700)
      .style("color", timelineTheme.foreground),
    sub: panel.append("div")
      .style("font-size", "12px")
      .style("color", timelineTheme.secondary)
      .style("margin-bottom", "7px"),
    feature: panel.append("div")
      .style("font-size", "13px")
      .style("line-height", 1.45)
      .style("color", timelineTheme.foreground),
  };
}
const detailWomen = detailCard("women");
const detailMen = detailCard("men");
const detailOther = detailCard("mixed");

let focusedYear;
let timelineData;
let scrollTimelineBy = () => {};
let initialScrollApplied = false;

function shorten(text, limit) {
  if (!text) return "";
  return text.length > limit ? `${text.slice(0, limit - 3)}...` : text;
}

function rowFor(rows, gender) {
  return rows.find(d => d.gender_class === gender);
}

function formatRating(value) {
  return value == null || Number.isNaN(value) ? "n/a" : d3.format(".2f")(value);
}

function updateDetail(yearRows, year, origin) {
  const women = rowFor(yearRows, "women");
  const men = rowFor(yearRows, "men");
  const otherRows = yearRows.filter(d => ["mixed", "unknown"].includes(d.gender_class));
  const otherRating = otherRows.length ? d3.mean(otherRows, d => d.average_rating) : null;
  const otherAppearances = d3.sum(otherRows, d => d.appearances);
  const otherTitles = d3.sum(yearRows.filter(d => ["mixed", "unknown"].includes(d.gender_class)), d => d.titles);
  const otherFeatured = otherRows
    .filter(d => d.featured_title)
    .sort((a, b) => d3.descending(a.featured_rating || 0, b.featured_rating || 0))[0];
  detailTitle.text(year);
  detailOrigin.text(origin === "All origins" ? "All author origins" : `Authors from ${origin}`);

  [
    [detailWomen, women],
    [detailMen, men],
  ].forEach(([card, row]) => {
    card.count.text(row ? formatRating(row.average_rating) : "n/a");
    card.sub.text(row ? `${d3.format(",")(row.titles)} rated titles - ${d3.format(",")(row.appearances)} chart appearances` : "No rated books in this year");
    card.feature.text(row ? `Top rated: ${row.featured_title} by ${row.featured_author} (${formatRating(row.featured_rating)})` : "No rated title");
  });
  detailOther.count.text(formatRating(otherRating));
  detailOther.sub.text(`${d3.format(",")(otherTitles)} rated titles - ${d3.format(",")(otherAppearances)} chart appearances`);
  detailOther.feature.text(otherFeatured
    ? `Top rated: ${otherFeatured.featured_title} by ${otherFeatured.featured_author} (${formatRating(otherFeatured.featured_rating)})`
    : "No mixed or unclassified rated title in this year.");
}

function renderTimeline(data) {
  const origin = "All origins";
  const visible = data.filter(d => d.origin === origin);
  const allOriginRows = data.filter(d => d.origin === "All origins");
  const minimumYear = d3.min(allOriginRows, d => d.year);
  const maximumYear = d3.max(allOriginRows, d => d.year);
  const byYear = d3.group(visible, d => d.year);
  const years = Array.from(byYear, ([year, rows]) =>
    rows.some(row => ["women", "men"].includes(row.gender_class)) ? year : null
  ).filter(year => year != null).sort(d3.ascending);
  const populatedYears = years;
  const yearSpacing = 112;
  const outerWidth = Math.max(container.clientWidth, (years.length - 1) * yearSpacing + 160);
  const height = 502;
  const axisY = 253;
  const margin = { left: 80, right: 80 };
  const x = d3.scaleTime()
    .domain([new Date(years[0], 0, 1), new Date(years[years.length - 1], 0, 1)])
    .range([margin.left, outerWidth - margin.right]);
  const spacing = x(new Date(years[1], 0, 1)) - x(new Date(years[0], 0, 1));
  const cardWidth = Math.min(96, spacing - 9);
  const cardHeight = 98;

  timelineSvg.attr("viewBox", `0 0 ${outerWidth} ${height}`)
    .attr("width", outerWidth)
    .attr("height", height);
  timelineSvg.selectAll("*").remove();

  const chart = timelineSvg.append("g");
  chart.append("line")
    .attr("x1", margin.left - 24)
    .attr("x2", outerWidth - margin.right + 24)
    .attr("y1", axisY)
    .attr("y2", axisY)
    .attr("stroke", timelineTheme.axis)
    .attr("stroke-width", 2);

  const axis = chart.append("g")
    .attr("transform", `translate(0,${axisY})`)
    .call(d3.axisBottom(x)
      .tickValues(years.map(year => new Date(year, 0, 1)))
      .tickFormat(d3.timeFormat("%Y"))
      .tickSize(10)
      .tickPadding(9));
  axis.select(".domain").remove();
  axis.selectAll("line").attr("stroke", timelineTheme.axis).attr("stroke-width", 1.5);
  axis.selectAll("text")
    .attr("fill", timelineTheme.secondary)
    .attr("font-size", 12)
    .attr("font-weight", 650);

  chart.selectAll(".year-hit")
    .data(years)
    .join("rect")
    .attr("class", "year-hit")
    .attr("x", year => x(new Date(year, 0, 1)) - spacing / 2)
    .attr("y", 12)
    .attr("width", spacing)
    .attr("height", height - 24)
    .attr("fill", "transparent")
    .on("mouseenter", (_, year) => focusYear(year));

  const yearGroup = chart.selectAll(".timeline-year")
    .data(years)
    .join("g")
    .attr("class", "timeline-year")
    .attr("data-year", year => year)
    .attr("transform", year => `translate(${x(new Date(year, 0, 1))},0)`)
    .on("mouseenter", (_, year) => focusYear(year));

  yearGroup.append("circle")
    .attr("cy", axisY)
    .attr("r", 5)
    .attr("fill", timelineTheme.panelStrong)
    .attr("stroke", timelineTheme.axis)
    .attr("stroke-width", 2);

  function addLane(gender, cardY, connectionY, popDirection) {
    const positioned = yearGroup.append("g").attr("transform", `translate(0,${cardY})`);
    positioned.append("line")
      .attr("y1", connectionY)
      .attr("y2", gender === "women" ? axisY - cardY - 8 : axisY - cardY + 8)
      .attr("stroke", timelineColors[gender])
      .attr("stroke-opacity", 0.6);
    const cards = positioned.append("g")
      .attr("class", "timeline-card")
      .style("--pop-y", popDirection);
    cards.append("rect")
      .attr("x", -cardWidth / 2)
      .attr("width", cardWidth)
      .attr("height", cardHeight)
      .attr("rx", 7)
      .attr("fill", year => rowFor(byYear.get(year) || [], gender) ? timelineColors[gender] : timelineTheme.panel)
      .attr("fill-opacity", year => rowFor(byYear.get(year) || [], gender) ? 0.27 : 1)
      .attr("stroke", year => rowFor(byYear.get(year) || [], gender) ? timelineColors[gender] : timelineTheme.border)
      .attr("stroke-dasharray", year => rowFor(byYear.get(year) || [], gender) ? null : "3 3");
    cards.append("text")
      .attr("x", -cardWidth / 2 + 8)
      .attr("y", 17)
      .attr("fill", timelineTheme.secondary)
      .attr("font-size", 10)
      .attr("font-weight", 700)
      .text(gender === "women" ? "WOMEN" : "MEN");
    cards.append("text")
      .attr("x", -cardWidth / 2 + 8)
      .attr("y", 37)
      .attr("fill", timelineTheme.foreground)
      .attr("font-size", 11)
      .attr("font-weight", 700)
      .text(year => {
        const row = rowFor(byYear.get(year) || [], gender);
        return row ? shorten(row.featured_title, 14) : "No rating";
      });
    cards.append("text")
      .attr("x", -cardWidth / 2 + 8)
      .attr("y", 54)
      .attr("fill", timelineTheme.secondary)
      .attr("font-size", 10)
      .text(year => {
        const row = rowFor(byYear.get(year) || [], gender);
        return row ? shorten(row.featured_author, 15) : "";
      });
    cards.append("text")
      .attr("x", -cardWidth / 2 + 8)
      .attr("y", 80)
      .attr("fill", timelineTheme.foreground)
      .attr("font-size", 10)
      .attr("font-weight", 650)
      .text(year => {
        const row = rowFor(byYear.get(year) || [], gender);
        return row ? `★ ${formatRating(row.featured_rating)}` : "";
      });
  }
  addLane("women", 48, cardHeight, "-8px");
  addLane("men", 307, 0, "8px");

  if (!focusedYear || !years.includes(focusedYear)) {
    focusedYear = populatedYears[populatedYears.length - 1] || years[years.length - 1];
  }
  focusYear(focusedYear);
  if (!initialScrollApplied) {
    scrollToYear(focusedYear, "auto");
    initialScrollApplied = true;
  }

  function focusYear(year) {
    focusedYear = year;
    yearGroup.classed("is-focused", d => d === year);
    updateDetail(byYear.get(year) || [], year, origin);
    visibleYearLabel.text(`${minimumYear}-${maximumYear}`);
    updateArrowState();
  }

  function scrollToYear(year, behavior = "smooth") {
    const viewport = timelineViewport.node();
    const targetLeft = x(new Date(year, 0, 1)) - viewport.clientWidth / 2;
    viewport.scrollTo({ left: Math.max(0, targetLeft), behavior });
    updateArrowState();
  }

  function updateArrowState() {
    const viewport = timelineViewport.node();
    const maxScroll = Math.max(0, viewport.scrollWidth - viewport.clientWidth - 2);
    previousYearButton
      .property("disabled", viewport.scrollLeft <= 2)
      .style("opacity", viewport.scrollLeft <= 2 ? 0.45 : 1)
      .style("cursor", viewport.scrollLeft <= 2 ? "not-allowed" : "pointer");
    nextYearButton
      .property("disabled", viewport.scrollLeft >= maxScroll)
      .style("opacity", viewport.scrollLeft >= maxScroll ? 0.45 : 1)
      .style("cursor", viewport.scrollLeft >= maxScroll ? "not-allowed" : "pointer");
  }

  scrollTimelineBy = direction => {
    timelineViewport.node().scrollBy({ left: direction * yearSpacing * 5, behavior: "smooth" });
  };

  timelineViewport.on("scroll.timeline", updateArrowState);
  updateArrowState();
}

d3.csv("{{< asset-url "data/bestsellers_timeline.csv" >}}", d3.autoType).then(data => {
  timelineData = data;
  renderTimeline(timelineData);
  previousYearButton.on("click", () => scrollTimelineBy(-1));
  nextYearButton.on("click", () => scrollTimelineBy(1));
  window.addEventListener("resize", () => renderTimeline(timelineData));
}).catch(error => {
  timelineStatus.text("Could not load the bestseller timeline data.");
  console.error("Error loading bestseller timeline:", error);
});
{{< /d3 >}}
<!-- prettier-ignore-end -->
