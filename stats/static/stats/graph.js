function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

var gbtnContainer = document.getElementById("filterBtnContainer");
var gbtns = gbtnContainer.getElementsByClassName("btn");
for (var i = 0; i < gbtns.length; i++) {
  gbtns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("gactive");
    current[0].className = current[0].className.replace(" gactive", "");
    this.className += " gactive";
  });
}