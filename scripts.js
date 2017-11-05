// TIMELINE

const timeline = document.querySelector(".timeline ol"),
	elH = document.querySelectorAll(".timeline li > div"),
	arrows = document.querySelectorAll(".timeline .arrows .arrow"),
	arrowPrev = document.querySelector(".timeline .arrows .arrow__prev"),
	arrowNext = document.querySelector(".timeline .arrows .arrow__next"),
	firstItem = document.querySelector(".timeline li:first-child"),
	lastItem = document.querySelector(".timeline li:last-child"),
	xScrolling = 280,
	disabledClass = "disabled";

csv = d3.csv('letterboxd.csv', function(d) {
	return {
		comment : d.comment,
		title : d.title,
		year : d.year
	};
}, function(data) {
	console.log(data);
	populateDOM(data);
});

function populateDOM(data) {
	numberOfFilms = Object.keys(data).length;
	for (film = 0; film < numberOfFilms - 1; film++) {
		var comment = '<p>' + data[film]['comment'] + '</p>'
		var title = '<p>' + data[film]['title'] + '</p>'
		var year = '<time>' + data[film]['year'] + '</time>'
		$('.timeline ol').append('<li><div>' + year + title + comment + '</div></li>');
	}
	// setEqualHeights(elH);
}
// console.log(csv);

// window.addEventListener("load", init);

// function init() {
// 	setEqualHeights(elH);
// 	animateTl(xScrolling, arrows, timeline);
// 	setSwipeFn(timeline, arrowPrev, arrowNext);
// 	setKeyboardFn(arrowPrev, arrowNext);
// }

// function setEqualHeights(el) {
//   let counter = 0;
//   for (let i = 0; i < el.length; i++) {
//     const singleHeight = el[i].offsetHeight;
     
//     if (counter < singleHeight) {
//       counter = singleHeight;
//     }
//   }
//     for (let i = 0; i < el.length; i++) {
//     el[i].style.height = `${counter}px`;
//   }
// }