// let svg, width, height, progbar, refs, tips, labels, pcts;

let epCodes = Array.from(document.getElementsByClassName("epCode"), x => x.textContent);
let promises = [d3.json("/data/community/references.json")];
for (let epCode of epCodes) {
  promises.push(d3.text(`/transcripts/${epCode}.txt`));
}
Promise.all(promises).then(init);

function init(files) {

  let references = files[0];
  let transcripts = files.slice(1);

  // data
  
  let allEpRefs = [];
  for (let i = 0; i < epCodes.length; i++) {

    let epCode = epCodes[i];

    let transcript = transcripts[i];
    let totalLength = transcript.split("").length;

    let epRefs = [];
    for (let refType in references[epCode]) {
      for (let ref of references[epCode][refType]) {
        ref.pct = ref.reference.startInDoc / totalLength;
        epRefs.push(ref);
      }
    }
    epRefs.sort((a, b) => {
      // render in reverse for visibility
      return b.pct - a.pct;
    });
    allEpRefs.push(epRefs);
  }

  // graphics
  
  let width = d3.select(".episode").node().offsetWidth;
  let height = width * 0.4;

  let svgs = d3.selectAll(".svg")
    .attr("width", width)
    .attr("height", height)
    .data(allEpRefs)
    ;

  // gradient
  let linGrads = d3.selectAll(".linGrad");
  let allGradVals = [];
  linGrads.each(function(linGrad, i) {
    let gradVals = [];
    let lStops = d3.select(this).selectAll("stop");
    lStops.each((stop, j, arr) => {
      let offset = j / (arr.length - 1);
      let counter = 0;
      for (let ref of allEpRefs[i]) {
        if (ref.pct >= offset - 0.05 && ref.pct < offset + 0.05) {
          counter++;
        }
      }
      gradVals.push(counter);
    });
    let max = Math.max(...gradVals);
    if (max) {
      gradVals = gradVals.map(x => x / max);
    }
    allGradVals.push(gradVals);
  });
  linGrads
    .data(allGradVals);
  let stops = linGrads.selectAll("stop")
    .data(d => d)
    .attr("stop-color", (d) => {
      let col = d * (255 - 200) + 200;
      return `rgb(${col}, ${col}, ${col})`;
    })
    ;

  let gradient = svgs
    .append("rect")
    .attr("fill", (d, i) => { return `url(#linGrad${i+1})` })
    .attr("width", width)
    .attr("height", height)
    ;

  let progBar = svgs
    .append("line")
    .attr("class", "progBar")
    .attr("x1", 0)
    .attr("x2", width)
    .attr("y1", height * 0.5)
    .attr("y2", height * 0.5)
    ;

  let refYShift = 10;
  let refs = svgs
    .selectAll("g")
    .data(d => d)
    .join("g")
    .classed("refg", true)
    .classed("name", (d) => { return "name" in d.referent })
    .classed("title", (d) => { return "title" in d.referent })
    .attr("transform", (d, i) => {
      let x = width * d.pct;
      let y = height * 0.5 + ((i % 2) * 2 - 1) * refYShift;
      return `translate(${x}, ${y})`
    })
    ;
  refs
    .on("mouseover", function(d) {
      let parent = this.parentNode;
      d3.select(parent).selectAll("g").style("opacity", 0.15);
      d3.select(this).style("opacity", 1);
    })
    .on("mouseout", function(d) {
      let parent = this.parentNode;
      d3.select(parent).selectAll("g").style("opacity", 1);
    })
    ;

  tips = refs
    .append("line")
    .classed("tip", true)
    .attr("x1", 0)
    .attr("x2", 0)
    ;

  labels = refs
    .append("text")
    .text(d => { return ("name" in d.referent) ? d.referent.name : d.referent.title })
    .classed("label", true)
    .attr("transform", "translate(5, 0)")
    ;

  pcts = refs
    .append("text")
    .text(d => { return parseInt(d.pct * 100) + "%" })
    .classed("pct", true)
    .attr("transform", "translate(5, 10)")
    ;

  labels.attr("transform", function(d, i, arr) {
    let transform = d3.select(this).attr("transform");
    let rect = this.getBoundingClientRect();
    let right = this.parentNode.parentNode.getBoundingClientRect().right;
    if (rect.right >= right) {
      let xy = transform.split("(")[1].split(")")[0].split(", ").map(x => parseInt(x));
      // xy[0] -= rect.width + 5;
      xy[0] = -rect.width - 5;
      transform = `translate(${xy[0]}, ${xy[1]})`;
      // let sibPct = arr[i].parentNode.getElementsByClassName("pct")[0];
      // sibPct.setAttribute("transform", "translate(-")
    } 
    return transform;
  });

  for (let x = 0; x < 3; x++) {
    refs.attr("transform", function(val, i, arr) {
      let thisRect = this.getElementsByClassName("label")[0].getBoundingClientRect();
      let transform = d3.select(this).attr("transform");
      if (i > 0) {
        for (let j = 0; j < arr.length; j++) {
          if (i != j) {
            let otherRect = arr[j].getElementsByClassName("label")[0].getBoundingClientRect();
            if (thisRect.x >= otherRect.x &&
                thisRect.x <= otherRect.right &&
                thisRect.y == otherRect.y) {
              let xy = transform.split("(")[1].split(")")[0].split(", ").map(x => parseInt(x));
              if (xy[1] < height * 0.5) {
                xy[1] -= refYShift + 10;
              } else {
                xy[1] += refYShift + 10;
              }
              transform = `translate(${xy[0]}, ${xy[1]})`;
            }
          }
        }
      }
      return transform;
    });
  }

  tips.each(function(d, i, arr) {
    let parent = this.parentNode;
    let parentXY = d3.select(parent).attr("transform").split("(")[1].split(")")[0].split(", ").map(x => parseInt(x));
    let tipY1, tipY2;
    let shift = parentXY[1] - height * 0.5;
    if (shift < 0) {
      tipY1 = -10;
      tipY2 = -shift;
    } else {
      tipY1 = -shift;
      tipY2 = 10;
    }
    d3.select(this).attr("y1", tipY1);
    d3.select(this).attr("y2", tipY2);
  })
}