Promise.all([
  d3.json("/data/references.json"),
  d3.json("/data/referents.json")
]).then(function(files) {
  references = files[0];
  referents = files[1];
  people = Object.values(files[1].people);
  titles = Object.values(files[1].titles);
  console.log(people);
  console.log(titles);

  people.forEach(d => {
    let list = d3.select("#people");
    let div = list.append("div");
    div.append("dt").text(d.details.name).classed("entity", true);
    let def = div.append("dd");
    let epRefs = {};
    d.references.forEach(ref => {
      if (epRefs[ref.epCode]) {
        epRefs[ref.epCode].push(ref);
      } else {
        epRefs[ref.epCode] = [ref];
      }
    });
    for ([epCode, refs] of Object.entries(epRefs)) {
      let subList = def.append("dl");
      let ep = subList.append("dt").text(epCode);
      refs.forEach(ref => {
        let sent = subList.append("dd");
        let startInSent = ref.startInSent;
        let endInSent = ref.endInSent;
        let markedSent = ref.sentence.substring(0, startInSent) +
                         "<span class='entity'>" +
                         ref.sentence.substring(startInSent, endInSent) + 
                         "</span>" +
                         ref.sentence.substring(endInSent, ref.sentence.length);
        sent.html(markedSent);
      });
    };
  });

  titles.forEach(d => {
    let list = d3.select("#titles");
    let div = list.append("div");
    div.append("dt").text(d.details.title).classed("entity", true);
    let def = div.append("dd");
    let epRefs = {};
    d.references.forEach(ref => {
      if (epRefs[ref.epCode]) {
        epRefs[ref.epCode].push(ref);
      } else {
        epRefs[ref.epCode] = [ref];
      }
    });
    for ([epCode, refs] of Object.entries(epRefs)) {
      let subList = def.append("dl");
      let ep = subList.append("dt").text(epCode);
      refs.forEach(ref => {
        let sent = subList.append("dd");
        let startInSent = ref.startInSent;
        let endInSent = ref.endInSent;
        let markedSent = ref.sentence.substring(0, startInSent) +
                         "<span class='entity'>" +
                         ref.sentence.substring(startInSent, endInSent) + 
                         "</span>" +
                         ref.sentence.substring(endInSent, ref.sentence.length);
        sent.html(markedSent);
      });
    };
  });


});