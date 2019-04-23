$( function() {
    $( "#slider-range" ).slider({
      range: true,
      min: 1,
      max: 12,
      values: [ 0, 12 ],
      slide: function( event, ui ) {
        if (ui.values[0] == ui.values[1]){
            $( "#amount" ).html(ui.values[0])
        } else {
        $( "#amount" ).html(ui.values[ 0 ] + '-' + ui.values[ 1 ] );
        }
      }
    });
    $( "#amount" ).html("1-12");
  } );

var filters;
/*filters = ""*/
filters = {
    'gender':'anyGender',
    'company':'anyCompany',
    'generation':'anyGeneration',
    'memberCount':'anyMemberCount'
};

function checkFilter(group, f) {
    var classList, i;
    classList = group.className.split(" ");
    for (i=0; i<classList.length; i++) {
        if (filters[f] == classList[i]) {
            return true;
        }
    }
    return false;
}

function filterSelection(c, select) {
  var objects, i, arr1;
  filters[select] = c;
  objects = document.getElementsByClassName("filterDiv");
  for (i=0; i<objects.length; i++) {
    w3RemoveClass(objects[i], "show");
    if (checkFilter(objects[i], 'gender') & checkFilter(objects[i], 'company')) {
        w3AddClass(objects[i], "show");
    }
  }
}

/*function filterGender(c) {
  var objects, i, arr1;
  objects = document.getElementsByClassName("filterDiv");
  if (filters['gender'] != '') {
    for (i=0; i<objects.length; i++) {
        arr1 = objects[i].className.split(" ");
        if (arr1.indexOf(filters['gender']) > -1) w3RemoveClass(objects[i], "show");
    }
  }
  filters['gender'] = c;
    for (i=0; i<objects.length; i++) {
        arr1 = objects[i].className.split(" ");
        if (arr1.indexOf(filters['gender']) > -1) {
            w3AddClass(objects[i], "show");
        } else {
            w3RemoveClass(objects[i], "show");
        }
    }
}

function filterCompany(c) {
  var objects, i, arr1;
  objects = document.getElementsByClassName("filterDiv");
  if (filters['company'] != '') {
    for (i=0; i<objects.length; i++) {
        arr1 = objects[i].className.split(" ");
        if (arr1.indexOf(filters['company']) > -1) w3RemoveClass(objects[i], "show");
    }
  }
  filters['company'] = c;
    for (i=0; i<objects.length; i++) {
        arr1 = objects[i].className.split(" ");
        if (arr1.indexOf(filters['company']) > -1) {
            w3AddClass(objects[i], "show");
        } else {
            w3RemoveClass(objects[i], "show");
        }
    }
}*/

//filterSelection("all")
/*function filterSelection(c) {
  var objects, i, j, arr1, arr2;
  objects = document.getElementsByClassName("filterDiv");
  if (c == "all") c = "";
  if (filters == "") {
    filters = c;
  } else if (c != "") {
    filters = filters + " " + c;
  }
  genderCheck(filters, c);
  companyCheck(filters, c);
  // Add the "show" class (display:block) to the filtered elements, and remove the "show" class from the elements that are not selected
  if (filters == "") {
    for (i = 0; i < objects.length; i++) {
        w3AddClass(objects[i], "show");
    }
  } else {
    for (i = 0; i < objects.length; i++) {
        w3RemoveClass(objects[i], "show");
        arr1 = filters.split(" ")
        for (j=0; j<arr1.length; j++){
            arr2 = objects[i].className.split(" ");
            if (arr2.indexOf(arr1[j]) > -1) w3AddClass(objects[i], "show");
        }
    }
  }
}

function genderCheck(f, want) {
    var i, arr1, check;
    arr1 = filters.split(" ");
    if (want == 'G') {
        check = 'B';
    } else if (want == 'B') {
        check = 'G';
    } else {
        check = 0;
    }
    if (check != 0) {
        for (i=0; i<arr1.length; i++) {
            if (arr1[i] == check) {
                arr1.splice(i, 1);
                filters = arr1.join(" ");
            }
        }
    }
}

function companyCheck(f, want) {
    var i, j, arr1, arr2, check;
    arr1 = filters.split(" ");
    if (want == 'YG') {
        check = 'JYP Big';
    } else if (want == 'JYP') {
        check = 'YG Big';
    } else if (want == 'Big') {
        check = 'YG JYP';
    } else {
        check = 0;
    }
    if (check != 0) {
        arr2 = check.split(" ");
        for (i=0; i<arr1.length; i++) {
            for (j=0; j<arr2.length; j++) {
                if (arr1[i] == arr2[j]) {
                    arr1.splice(i, 1);
                    filters = arr1.join(" ");
                }
            }
        }
    }
}*/

function resetFilter(bundle) {
    var i, arr1;
    if (bundle == "Gender") {
        arr1 = filters.split(" ")
        for (i=0; i<arr1.length; i++) {
            if (arr1[i] == 'B' | arr1[i] == 'G') {
                arr1.splice(i, 1);
                i--;
                filters = arr1.join(" ");
            }
        }
    } else if (bundle == "Company") {
        arr1 = filters.split(" ")
        for (i=0; i<arr1.length; i++) {
            if (arr1[i] == 'YG' | arr1[i] == 'JYP' | arr1[i] == 'Big') {
                arr1.splice(i, 1);
                i--;
                filters = arr1.join(" ");
            }
        }
    }
    filterSelection("all");
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
