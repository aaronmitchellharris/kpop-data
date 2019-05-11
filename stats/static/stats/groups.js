$( function() {
    $( "#slider-range" ).slider({
      range: true,
      min: 1,
      max: 18,
      values: [ 1, 18 ],
      slide: function( event, ui ) {
        if (ui.values[0] == ui.values[1]){
            $( "#amount" ).html(ui.values[0])
            countAdjust(ui.values[0], 'down');
            countAdjust(ui.values[1], 'up');
            filterSelection('', 'memberCount')
        } else {
            $( "#amount" ).html(ui.values[ 0 ] + '-' + ui.values[ 1 ] );
            countAdjust(ui.values[0], 'down');
            countAdjust(ui.values[1], 'up');
            filterSelection('', 'memberCount')
        }
      }
    });
    $( "#amount" ).html("1-18");
  } );


function countAdjust(number, direction) {
    var i;
    if (direction == 'up') {
        for (i=0; i<filters['memberCount'].length; i++) {
            if (number < filters['memberCount'][i]) {
                filters['memberCount'].splice(i, 1)
            }
        }
        if (number > Math.max.apply(null, filters['memberCount'])) {
            for (i=Math.max.apply(null, filters['memberCount'])+1; i<=number; i++) {
                filters['memberCount'].push(i.toString());
            }
        }
    }
    if (direction == 'down') {
        for (i=0; i<filters['memberCount'].length; i++) {
            if (number > filters['memberCount'][i]) {
                filters['memberCount'].splice(i, 1)
            }
        }
        if (number < Math.min.apply(null, filters['memberCount'])) {
            for (i=number; i<=Math.min.apply(null, filters['memberCount']); i++) {
                filters['memberCount'].unshift(i.toString());
            }
        }
    }
}




var filters;
/*filters = ""*/
filters = {
    'gender':'anyGender',
    'company':'anyCompany',
    'memberCount':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18'],
};

function checkFilter(group, f) {
    var classList, i, j;
    classList = group.className.split(" ");
    for (i=0; i<classList.length; i++) {
        if (f == 'memberCount'){
            for (j=0; j<filters['memberCount'].length; j++){
                if (filters[f][j] == classList[i]) {
                    return true
                }
            }
        } else if (filters[f] == classList[i]) {
            return true;
        }
    }
    return false;
}

function filterSelection(c, select) {
  var objects, i, arr1;
  if (select == "company") {
    filters[select] = formatCompany(c);
  } else if (select == 'memberCount') {
  } else {
  filters[select] = c;
  }
  objects = document.getElementsByClassName("filterDiv");
  for (i=0; i<objects.length; i++) {
    w3RemoveClass(objects[i], "show");
    if (checkFilter(objects[i], 'gender') & checkFilter(objects[i], 'company') & checkFilter(objects[i], 'memberCount')) {
        w3AddClass(objects[i], "show");
    }
  }
}

// Show filtered elements
function w3AddClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    if (arr1.indexOf(arr2[i]) == -1) {
      element.className += " " + arr2[i];
    }
  }
}

// Hide elements that are not selected
function w3RemoveClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    while (arr1.indexOf(arr2[i]) > -1) {
      arr1.splice(arr1.indexOf(arr2[i]), 1);
    }
  }
  element.className = arr1.join(" ");
}

// Add active class to the current control button (highlight it)
var gbtnContainer = document.getElementById("genderBtnContainer");
var gbtns = gbtnContainer.getElementsByClassName("btn");
for (var i = 0; i < gbtns.length; i++) {
  gbtns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("gactive");
    current[0].className = current[0].className.replace(" gactive", "");
    this.className += " gactive";
  });
}

var cbtnContainer = document.getElementById("companyBtnContainer");
var cbtns = cbtnContainer.getElementsByClassName("btn");
for (var i = 0; i < cbtns.length; i++) {
  cbtns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("cactive");
    current[0].className = current[0].className.replace(" cactive", "");
    this.className += " cactive";
  });
}

function formatCompany(c) {
    var hold;
    hold = c.split(" ");
    if (c == 'anyCompany') {
        $("#dropdownMenuButton").html('Any')
    } else {
        $("#dropdownMenuButton").html(c)
    }
    return hold[0]
}