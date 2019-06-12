/*function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}*/

var gbtnContainer = document.getElementById("filterBtnContainer");
var gbtns = gbtnContainer.getElementsByClassName("btn");
for (var i = 0; i < gbtns.length; i++) {
  gbtns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("gactive");
    current[0].className = current[0].className.replace(" gactive", "");
    this.className += " gactive";
  });
}

/*function hashCode(str) { // java String#hashCode
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
       hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return hash;
}

function getRandomColor(i){
    var c = (i & 0x00FFFFFF).toString(16).toUpperCase();
    return "00000".substring(0, 6 - c.length) + c;
}

function getRandomColor(str){
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
       hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    var c = (hash & 0x00FFFFFF)
        .toString(16)
        .toUpperCase();

    return "00000".substring(0, 6 - c.length) + c;
}*/