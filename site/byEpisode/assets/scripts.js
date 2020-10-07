//////////////
// PROG BAR //
//////////////

let svg, width, height, progbar, refs, tips, labels, pcts;

let epCode = /s\d{2}e\d{2}/g.exec(location.pathname)[0];
Promise.all([
  d3.text(`/transcripts/community/${epCode}.txt`),
  d3.json("/data/community/references.json")
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
    // return a.pct - b.pct;
    // render in reverse for visibility
    return b.pct - a.pct;
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

  let refYShift = 20;
  refs
    .attr("transform", (d, i) => {
      let x = window.innerWidth * d.pct;
      let y = height * 0.5 + ((i % 2) * 2 - 1) * refYShift;
      return `translate(${x}, ${y})`
    })
    ;

  labels.attr("transform", (val, i, arr) => {
    let transform = arr[i].getAttribute("transform");
    let rect = arr[i].getBoundingClientRect();
    if (rect.right >= width) {
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
    refs.attr("transform", (val, i, arr) => {
      let thisRect = arr[i].getElementsByClassName("label")[0].getBoundingClientRect();
      let transform = arr[i].getAttribute("transform");
      if (i > 0) {
        for (let j = 0; j < arr.length; j++) {
          if (i != j) {
            let otherRect = arr[j].getElementsByClassName("label")[0].getBoundingClientRect();
            // console.log(thisRect, otherRect);
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

  tips.each((el, i, arr) => {
    let parent = arr[i].parentNode;
    let parentXY = parent.getAttribute("transform").split("(")[1].split(")")[0].split(", ").map(x => parseInt(x));
    let tipY1, tipY2;
    let shift = parentXY[1] - height * 0.5;
    if (shift < 0) {
      tipY1 = -10;
      tipY2 = -shift;
    } else {
      tipY1 = -shift;
      tipY2 = 10;
    }
    arr[i].setAttribute("y1", tipY1);
    arr[i].setAttribute("y2", tipY2);
  })

  
}

function updateDimensions(winWidth) {
  width = winWidth;
  height = width * 0.3;
}

window.addEventListener("resize", () => {
  render();
});

/////////////////
// OTHER STUFF //
/////////////////

// document.getElementById("random").addEventListener("click", () => {
  
// });