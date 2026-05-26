---
title: "Publishers — Gender by Publisher"
date: 2026-05-23
---

{{< rawhtml >}}
<div>
  <div style="margin-bottom: 16px;">
    <label style="font-size: 13px; color: #666;">Sort by:</label>
    <button id="sort-pct" style="margin-left: 8px; padding: 6px 12px; background: #d8b3f0; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">Women %</button>
    <button id="sort-total" style="margin-left: 4px; padding: 6px 12px; background: #eee; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">Total books</button>
  </div>
  <div id="publisher-chart"></div>
</div>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
  const margin = { top: 48, right: 180, bottom: 52, left: 240 };
  const colorFemale = '#d8b3f0', colorMale = '#a3d5ff', colorNeutral = '#b4b2a9';
  let currentSort = 'pct'; // 'pct' or 'total'

  d3.csv("/data/publisher_gender_counts.csv").then(raw => {
    let data = raw.map(d => ({
      publisher: d.publisher,
      num_male: +d.num_male,
      num_female: +d.num_female,
      top_genres: d.top_genres || "",
    }));
    data = data.map(d => ({ ...d, total: d.num_male + d.num_female }))
      .filter(d => d.total > 150)
      .map(d => ({ ...d, femalePct: d.num_female / d.total }));

    const rowHeight = 30;
    const innerHeight = data.length * rowHeight;
    const totalW = Math.min(900, window.innerWidth - 40);
    const width = totalW - margin.left - margin.right;
    const height = innerHeight + margin.top + margin.bottom;

    const rScale = d3.scaleSqrt()
      .domain(d3.extent(data, d => d.total))
      .range([4, 10]);

    const x = d3.scaleLinear().domain([0, 1]).range([0, width]);
    const centerX = x(0.5);

    const publisherTotals = new Map(data.map(d => [d.publisher, d.total]));

    const createChart = (sortedData) => {
      d3.select('#publisher-chart').html(''); // Clear

      const y = d3.scaleBand()
        .domain(sortedData.map(d => d.publisher))
        .range([0, innerHeight])
        .padding(0.3);

      const svg = d3.select('#publisher-chart')
        .append('svg')
        .attr('width', totalW).attr('height', height)
        .append('g').attr('transform', `translate(${margin.left},${margin.top})`);

      // Grid lines + center axis
      [0.25, 0.5, 0.75].forEach(v => {
        svg.append('line')
          .attr('x1', x(v)).attr('x2', x(v))
          .attr('y1', 0).attr('y2', innerHeight + 8)
          .attr('stroke', v === 0.5 ? '#aaa' : '#ddd')
          .attr('stroke-width', v === 0.5 ? 1 : 0.5)
          .attr('stroke-dasharray', v === 0.5 ? null : '3,3');
      });

      const rows = svg.selectAll('.row').data(sortedData).enter()
        .append('g').attr('transform', d => `translate(0,${y(d.publisher) + y.bandwidth() / 2})`);

      const dotColor = d => {
        const diff = d.femalePct - 0.5;
        return Math.abs(diff) < 0.03 ? colorNeutral : diff > 0 ? colorFemale : colorMale;
      };

      rows.append('line')
        .attr('x1', centerX).attr('x2', d => x(d.femalePct))
        .attr('y1', 0).attr('y2', 0)
        .attr('stroke', dotColor).attr('stroke-width', 1.5).attr('opacity', 0.7);

      rows.append('circle')
        .attr('cx', d => x(d.femalePct)).attr('cy', 0)
        .attr('r', d => rScale(3))
        .attr('fill', dotColor)
        .attr('stroke', d => {
          const diff = d.femalePct - 0.5;
          return Math.abs(diff) < 0.03 ? '#888' : diff > 0 ? '#b07cd4' : '#5aabdf';
        })
        .attr('stroke-width', 1);

      rows.append('text')
        .attr('x', d => {
          const r = rScale(d.total);
          return d.femalePct >= 0.5 ? x(d.femalePct) + r + 4 : x(d.femalePct) - r - 4;
        })
        .attr('y', 0).attr('dy', '0.35em')
        .attr('text-anchor', d => d.femalePct >= 0.5 ? 'start' : 'end')
        .text(d => Math.round(d.femalePct * 100) + '%')
        .style('font-size', '11px').style('fill', '#888');

      // Genre badges on the right
      rows.append('g')
        .selectAll('rect')
        .data(d => {
          const genres = d.top_genres ? d.top_genres.split(', ') : [];
          return genres.map((g, i) => ({ genre: g, index: i, parent: d }));
        })
        .enter()
        .append('rect')
        .attr('x', d => 500 + d.index * 56)
        .attr('y', -7)
        .attr('width', 50)
        .attr('height', 14)
        .attr('rx', 3)
        .style('fill', '#f0f0f0')
        .style('stroke', '#ddd')
        .style('stroke-width', 0.5);

      rows.append('g')
        .selectAll('text')
        .data(d => {
          const genres = d.top_genres ? d.top_genres.split(', ') : [];
          return genres.map((g, i) => ({ genre: g, index: i, parent: d }));
        })
        .enter()
        .append('text')
        .attr('x', d => d.index * 56 + 525)
        .attr('y', 3)
        .attr('text-anchor', 'middle')
        .text(d => d.genre)
        .style('font-size', '9px')
        .style('fill', '#666');


      // Publisher labels
      svg.append('g')
        .call(d3.axisLeft(y).tickSize(0).tickFormat(p => `${p} (${publisherTotals.get(p)})`))
        .call(ax => ax.select('.domain').remove())
        .selectAll('text')
        .style('font-size', '13px').attr('x', -8).attr('text-anchor', 'end');

      // Top axis labels
      [[0.25, '25% female'], [0.5, '50%'], [0.75, '75% female']].forEach(([v, label]) => {
        svg.append('text')
          .attr('x', x(v)).attr('y', -10).attr('text-anchor', 'middle')
          .text(label).style('font-size', '11px').style('fill', '#888');
      });

      // Legend
      const legendY = innerHeight + 32;
      [
        { color: colorFemale, stroke: '#b07cd4', label: 'more female' },
        { color: colorMale, stroke: '#5aabdf', label: 'more male' },
        { color: colorNeutral, stroke: '#888', label: '~50%' },
      ].forEach((item, i) => {
        const lx = centerX - 100 + i * 100;
        svg.append('circle').attr('cx', lx).attr('cy', legendY).attr('r', 6)
          .attr('fill', item.color).attr('stroke', item.stroke).attr('stroke-width', 1);
        svg.append('text').attr('x', lx + 10).attr('y', legendY).attr('dy', '0.35em')
          .text(item.label).style('font-size', '12px').style('fill', '#888');
      });
    };

    // Initial sort by women percentage
    data.sort((a, b) => b.femalePct - a.femalePct);
    createChart(data);

    // Sort buttons
    document.getElementById('sort-pct').addEventListener('click', () => {
      if (currentSort !== 'pct') {
        currentSort = 'pct';
        data.sort((a, b) => b.femalePct - a.femalePct);
        createChart(data);
        document.getElementById('sort-pct').style.background = '#d8b3f0';
        document.getElementById('sort-total').style.background = '#eee';
      }
    });

    document.getElementById('sort-total').addEventListener('click', () => {
      if (currentSort !== 'total') {
        currentSort = 'total';
        data.sort((a, b) => b.total - a.total);
        createChart(data);
        document.getElementById('sort-pct').style.background = '#eee';
        document.getElementById('sort-total').style.background = '#a3d5ff';
      }
    });
  });
});
</script>
{{< /rawhtml >}}
