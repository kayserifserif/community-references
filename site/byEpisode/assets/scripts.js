//////////////
// PROG BAR //
//////////////

let svg, width, height, progbar, refs, tips, labels;

let epCode = /s\d{2}e\d{2}/g.exec(location.pathname)[0];
Promise.all([
  d3.text(`/transcripts/${epCode}.txt`),
  d3.json("/output/references.json")
]).then(init);

function init(files) {

  // data

  let transcript = files[0];
  let totalLength = transcript.split("").length;

  let references = files[1];
  let epRefs = [];
  for (let refType in references[epCode]) {
    for (let ref of references[epCode][refType]) {
      ref.pct = ref.reference.startInDoc / totalLength;
      epRefs.push(ref);
    }
  }
  epRefs.sort((a, b) => {
    return a.pct - b.pct;
  });

  // graphics

  svg = d3.select("svg");

  // gradient
  let linGrad = document.getElementById("linGrad");
  let stops = document.getElementsByTagName("stop");
  let gradVals = [];
  for (let i = 0; i < stops.length; i++) {
    let offset = i / (stops.length - 1);
    let counter = 0;
    for (let ref of epRefs) {
      if (ref.pct >= offset - 0.05 && ref.pct < offset + 0.05) {
        counter++;
      }
    }
    gradVals.push(counter);
  }
  let max = Math.max(...gradVals);
  if (max) {
    gradVals = gradVals.map(x => x / max);
  }
  for (let i = 0; i < stops.length; i++) {
    let stop = document.getElementsByTagName("stop")[i];
    let col = gradVals[i] * (255 - 200) + 200;
    stop.setAttribute("stop-color", `rgb(${col}, ${col}, ${col})`);
  }
  gradient = svg
    .append("rect")
    .attr("fill", "url(#linGrad)")
    ;

  progBar = svg
    .append("line")
    .attr("id", "progBar")
    .attr("x1", 0)
    ;

  refs = svg
    .selectAll("g")
    .data(epRefs)
    .enter()
    .append("g")
    .classed("refg", true)
    .classed("name", (d) => { return "name" in d.referent })
    .classed("title", (d) => { return "title" in d.referent })
    ;
  refs
    .on("mouseover", (val, i, arr) => {
      refs.style("opacity", 0.15);
      d3.select(arr[i]).style("opacity", 1);
    })
    .on("mouseout", () => {
      refs.style("opacity", 1);
    })
    ;

  tips = refs
    .append("line")
    .classed("tip", true)
    .attr("x1", 0)
    .attr("x2", 0)
    .attr("y1", -20)
    .attr("y2", 10)
    ;

  labels = refs
    .append("text")
    .text(d => { return ("name" in d.referent) ? d.referent.name : d.referent.title })
    .attr("transform", "translate(5, 0)")
    ;

  pcts = refs
    .append("text")
    .text(d => { return parseInt(d.pct * 100) + "%" })
    .classed("pct", true)
    .attr("transform", "translate(5, 10)")
    ;

  render();
}

function render() {
  updateDimensions(window.innerWidth);

  svg
    .attr("width", width)
    .attr("height", height)
    ;

  gradient
    .attr("width", width)
    .attr("height", height)
    ;

  progBar
    .attr("x2", window.innerWidth)
    .attr("y1", height * 0.5)
    .attr("y2", height * 0.5)
    ;

  refs
    .attr("transform", (d, i) => {
      let x = window.innerWidth * d.pct;
      let y = height * 0.5 + ((i % 2) * 2 - 1) * 20;
      return `translate(${x}, ${y})`
    })
    ;

  tips.each((el, i, arr) => {
    let parent = arr[i].parentNode;
    let parentXY = parent.getAttribute("transform").split("(")[1].split(")")[0].split(", ");
    let tipY1, tipY2;
    if (parentXY[1] < height * 0.5) {
      tipY1 = -10;
      tipY2 = 20;
    } else {
      tipY1 = -20;
      tipY2 = 10;
    }
    arr[i].setAttribute("y1", tipY1);
    arr[i].setAttribute("y2", tipY2);
  })
}

function updateDimensions(winWidth) {
  width = winWidth;
  height = width * 0.2;
}

window.addEventListener("resize", () => {
  render();
});

/////////////////
// OTHER STUFF //
/////////////////

// document.getElementById("random").addEventListener("click", () => {
  
// });