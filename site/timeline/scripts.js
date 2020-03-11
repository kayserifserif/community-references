var svg = d3.select("#container")
            .append("svg")
            .attr("width", "100%")
            .attr("height", "100%");

d3.json("/output/referents.json").then(function(data) {
  titles = Object.values(data.titles);

  var timeline = svg
    // .data([1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020])
    // .append("line")
    .append("g")
    .attr("id", "timeline")
    // .call(axis)
    .attr("transform", "translate(0," + window.innerHeight + ")")
    // .attr("x1", (1950 - 1900) * 10)
    // .attr("y1", window.innerHeight - 50)
    // .attr("x2", (2020 - 1900) * 10)
    // .attr("y2", window.innerHeight - 50)
    ;
  // timeline.call(axis);

  var dataPts = svg
    .selectAll(".dataPts")
    .data(titles)
    .enter().append("g")
      .classed("dataPts", true)
      .style("opacity", function(d) { return Math.min(d.count / 23 + 0.5, 1); })
      .attr("transform", function(d) {
        var x1 = (d.details.startYear - 1930) * 16;
        var y = window.innerHeight - 50;
        y -= d.count * 30;
        return "translate(" + x1 + "," + y + ")";
      })
      // .filter(function(d) { return d.details.titleType == "movie" })
      // .filter(function(d) { return d. })
      .on("mouseover", function(d) {
        d3.select(this).raise();
        d3.select(this).style("opacity", 1);
        d3.select(this).classed("active", true);
      })
      .on("mouseout", function(d) {
        d3.select(this).style("opacity", function(d) {
          return Math.min(d.count / 23 + 0.5, 1);
        });
        d3.select(this).classed("active", false);
      })
      ;
  dataPts.each(function(d) {
    // add title type
    this.classList.add(d.details.titleType);
    // add seasons
    var seasons = [];
    for (instance of d.references) {
      var epCode = instance.epCode;
      var season = epCode.slice(0, 3);
      seasons.push(season);
    }
    for (season of seasons) {
      this.classList.add(season);
    }
  });
  // dataPts.attr("data-legend", function(d) { return d.classList; });

  var bgs = dataPts
    .append("rect")
    .classed("bg", true)
    .attr("width", "120px")
    .attr("height", "20px")
    .attr("transform", "translate(-5, -25)")
    ;

  var circles = dataPts
    .append("circle")
    .classed("circle", true)
    .attr("r", 5)
    ;

  var info = dataPts
    .append("text")
    .classed("label", true)
    .text(function(d) { return d.details.title; })
    .attr("transform", "translate(0,-10)")
    ;

  var legend = svg.append("g")
    .classed("legend", true)
    .attr("transform","translate(300,300)")
    ;

  var legendItem = legend
    .selectAll(".legendItem")
    .data(["movie", "tvSeries", "tvMovie", "tvMiniSeries"])
    .enter().append("g")
      .classed("legendItem", true)
      .attr("transform", function(d, i) {
        return "translate(0," + i*20 + ")";
      })
      ;
  legendItem.each(function(d) {
    this.classList.add(d);
  })

  var legendText = legendItem
    .append("text")
    .classed("legendText", true)
    .text(function(d) { return d; })
    ;

  var legendCircle = legendItem
    .append("circle")
    .classed("legendCircle", true)
    .attr("r", 5)
    .attr("transform", "translate(-10, -4)")
    ;
});

var seasonButtons = document.getElementsByName("seasonButton");
var dataPts = document.getElementsByClassName("dataPts");
for (button of seasonButtons) {
  button.addEventListener("click", (event) => {
    var value = event.target.value;
    for (pt of dataPts) {
      if (pt.classList.contains(value)) {
        var count = pt.__data__.count;
        pt.style.opacity = Math.min(count / 23 + 0.5, 1);
      } else {
        // pt.style.display = "none";
        pt.style.opacity = 0;
      }
    }
  });
}