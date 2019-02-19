var cal = new CalHeatMap();

var data_json = {
  "1546297200.0": 10,
  "1546399300.0": 70
};

cal.init({
  domain: "month",
  subDomain: "x_day",
  //data: "datas-years2.json", //data_json,
  start: new Date(2019, 0, 0),
  cellSize: 20,
  cellPadding: 5,
  domainGutter: 30,
  range: 3,
  domainDynamicDimension: false,
  previousSelector: "#example-g-PreviousDomain-selector",
  nextSelector: "#example-g-NextDomain-selector",
  domainLabelFormat: function(date) {
    moment.lang("en");
    return moment(date).format("MMMM").toUpperCase();
  },
  subDomainTextFormat: "%d",
  legend: [15, 40, 60, 80],
  legendColors: ["#ecf5e2", "#232181"],
  onComplete: function() {
    var main = document.getElementById("main");
    var cal_e = document.getElementById("cal-heatmap");
    var val = cal_e.firstElementChild.width.baseVal.value;
    var dif = main.offsetWidth - val;
    r = String(Math.round(dif / 2)) + "px";
    //cal_e.style.paddingLeft = r;
    console.log("LOL!3", r, main.offsetWidth, val);
    return r;
  }
});

cal.update(data_json);

var doThis = function() {
  var main = document.getElementById("main");
  var cal_e = document.getElementById("cal-heatmap");
  var val = cal_e.firstElementChild.width.baseVal.value;
  var dif = main.offsetWidth - val;
  r = String(Math.round(dif / 2)) + "px";
  cal_e.style.paddingLeft = r;
  console.log("LOL!2", r, main.offsetWidth, val);
  return r;
}



window.addEventListener('DOMContentLoaded', function() {
  console.log('window - DOMContentLoaded - capture'); // 1st
}, true);

window.onload = function() {
  console.log("LOL!");

  //window.document.body.onload = doThis; // note removed parentheses
  doThis();
};


function calendarOnCenter() {
var width = 0;
var id = setInterval(frame, 20);
function frame() {
  if (width >= 3) {
    clearInterval(id);
  } else {
    width++;
    doThis();
  }
}
}

window.addEventListener("resize", doThis);

calendarOnCenter();
