var svg = d3.select("#container")
            .append("svg")
            .attr("width", "100%")
            .attr("height", "100%")
            // .attr("preserveAspectRatio", "xMinYMin meet")
            // .attr("viewBox", "0 0 600 400")
            ;

var references;
var referents;
var people;
var titles;

// d3.json("/data/community/referents.json").then(function(data) {
Promise.all([
  d3.json("/data/community/references.json"),
  d3.json("/data/community/referents.json")
]).then(function(files) {
  references = files[0];
  referents = files[1];
  people = Object.values(files[1].people);
  titles = Object.values(files[1].titles);

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
        // d3.select(this).style("opacity", 1);
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
    for (season in d.countBySeason) {
      if (d.countBySeason[season] > 0) {
        this.classList.add(season);
      }
    }
  });
  // dataPts.attr("data-legend", function(d) { return d.classList; });
  
  var bigBars = dataPts
    .append("rect")
    .classed("bigBar", true)
    .attr("width", 5)
    .attr("height", function(d) { return d.count * 30 })
    .attr("transform", "translate(-2.5, 0)")
    ;

  var smallBars = dataPts
    .append("rect")
    .classed("smallBar", true)
    .attr("width", 5)
    .attr("height", function(d) {
      var seasonChoice = document.querySelector("input:checked");
      if (seasonChoice) {
        var season = seasonChoice.value;
        return d.countBySeason[season] * 30;
      }
      return 0;
    })
    .attr("transform", function(d) {
      var seasonChoice = document.querySelector("input:checked");
      if (seasonChoice) {
        var season = seasonChoice.value;
        return "translate(-2.5," + (d.count - d.countBySeason[season]) * 30 + ")";
      }
      return 0;
    })
    ;

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

  var seasonButtons = document.getElementsByName("seasonButton");
  var dataPts = document.getElementsByClassName("dataPts");
  for (button of seasonButtons) {
    button.addEventListener("click", (event) => {
      var season = event.target.value;

      calculateSeasonStats(season);

      for (pt of dataPts) {
        if (pt.classList.contains(season)) {
          var references = pt.__data__.references;
          var countInSeason = 0;
          for (instance of references) {
            if (instance.epCode.slice(0, 3) == season) {
              countInSeason++;
            }
          }
          var startYear = pt.__data__.details.startYear;
          var x1 = (startYear - 1930) * 16;
          var y = window.innerHeight - 50;
          y -= countInSeason * 30;
          pt.style.transform = "translate(" + x1 + "," + y + ")";
          pt.style.opacity = Math.min(countInSeason / 23 + 0.5, 1);
        } else {
          pt.style.opacity = 0;
        }
      }

      smallBars
        .attr("height", function(d) {
          var season = document.querySelector("input:checked").value;
          var countInSeason = 0;
          for (instance of d.references) {
            var epCode = instance.epCode;
            if (epCode.slice(0, 3) == season) {
              countInSeason++;
            }
          }
          return countInSeason * 30;
        })
        .attr("transform", function(d) {
          var season = document.querySelector("input:checked").value;
          var countInSeason = 0;
          for (instance of d.references) {
            var epCode = instance.epCode;
            if (epCode.slice(0, 3) == season) {
              countInSeason++;
            }
          }
          return "translate(-2.5," + (d.count - countInSeason) * 30 + ")";
        })
        ;
    });
  }
});

function calculateSeasonStats(value) {
  var numRefs = 0;
  var numPeopleRefs = 0;
  var numTitleRefs = 0;
  for (name in referents["people"]) {
    var ent = referents["people"][name];
    if (ent["countBySeason"][value] > 0) {
      numRefs++;
      numPeopleRefs++;
    }
  }
  for (title in referents["titles"]) {
    var ent = referents["titles"][title];
    if (ent["countBySeason"][value] > 0) {
      numRefs++;
      numTitleRefs++;
    }
  }
  // for (refType of Object.values(referents)) {
  //   for (entity in refType) {
  //     if (refType[entity]["countBySeason"][value] > 0) {
  //       numRefs++;
  //     }
  //   }
  // }
  document.getElementById("numRefs").textContent = numRefs;
  document.getElementById("numPeopleRefs").textContent = numPeopleRefs;
  document.getElementById("numTitleRefs").textContent = numTitleRefs;
}