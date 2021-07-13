// save route
function saveBusRoute(){
    // read data from form
    var start = document.forms["bus_stop"]["start_stop"].value;
    var end = document.forms["bus_stop"]["end_stop"].value;
    var date = document.forms["bus_stop"]["date"].value;
    var time = document.forms["bus_stop"]["time"].value;
    // creat url which use fro send request to django server
    let url = 'route/'+'?start_stop='+start+'&end_stop='+end +'&date='+date +'&time='+time;
    fetch(url, {
        method:'GET'}).then(function(response) {
            // read data from django server and prase to json
            return response.json();
        });
    savePlanToJson();
}
// save data to local storage
function savePlanToJson(){
    // read data from form
    var start = document.forms["bus_stop"]["start_stop"].value;
    var end = document.forms["bus_stop"]["end_stop"].value;
    var date = document.forms["bus_stop"]["date"].value;
    var time = document.forms["bus_stop"]["time"].value;

    // form validation
    if(busStopsArray.includes(start) == false){
        alert("Wrong Start Bus Stop Input");
        return "wrong start stop name input"
    }
    if(busStopsArray.includes(end) == false){
        alert("Wrong End Bus Stop Input");
        return "wrong end stop name input"
    }
    if(dateArray.includes(date) == false){
        alert("Wrong Date Input");
        return "wrong date input"
    }
    if(timeArray.includes(time) == false){
        alert("Wrong Time Input");
        return "wrong time input"   
    }  


    // creat url which use fro send request to django server
    // the url will be the key used in local storage
    let url = 'route/'+'?start_stop='+start+'&end_stop='+end +'&date='+date +'&time='+time;
    var locations = {
        startStop :  start,
        endStop : end,
        date : date,
        time : time
    }
    str = JSON.stringify(locations);
    // key is url, value is location information
    // save to local storage
    localStorage.setItem(url,str);
}

// read data from local storage
function loadPlanFromJson(){
    var target = document.getElementById("plan_container");
    var key;
    var div = document.createElement("div");
    setPlanDiv(div);
    target.appendChild(div);
    for(var i=localStorage.length - 1 ; i >=0; i--){
        (function(i){

        var div = document.createElement("div");
        setDiv(div);
        target.appendChild(div);

        // traverse each key
        var url = localStorage.key(i);
        // get value by using key
        var str=localStorage.getItem(url); 
        var locations=JSON.parse(str); 

        // create plan buttons 
        var container = document.createElement("button");
        setPlanButton(container);
        // bind button with function
        container.addEventListener("click", function(){ showPlan(url);}); 
        // write route infromation on buuton       
        writeLine("start stop: "+ locations.startStop, container);
        writeLine("end stop: "+ locations.endStop, container);
        writeLine("date: "+ locations.date, container);
        writeLine("time: "+ locations.time, container);
        div.appendChild(container);   

        // create delete button
        var deleteButton = document.createElement("button");
        setDeleteButton(deleteButton)
        // bind button with function
        deleteButton.addEventListener("click", function(){ deletePlan(url);});
        writeLine("DELETE", deleteButton);
        div.appendChild(deleteButton);
        }(i));
    }
}

function setPlanDiv(element){
    element.setAttribute("class", "plan-title");
    element.innerHTML="MY PLAN"
}

function setDiv(element){
    element.setAttribute("class", "btn-group");
    element.setAttribute("role", "group");
}

function setPlanButton(element){
    element.setAttribute("href", "#plan_detail_panel");
    element.setAttribute("class", "button-plan button-inverse");
    element.setAttribute("data-bs-toggle", "collapse")
    element.setAttribute("aria-expanded", "false")
    element.setAttribute("aria-controls", "plan_detail_panel")
    element.setAttribute("overflow", "hidden;")
}

function setDeleteButton(element){
    element.setAttribute("class", "button-delete button-caution");
}

function deletePlan(url){
    // remove item from local storage
    localStorage.removeItem(url);
    // clean plan pannel and reload
    document.getElementById("plan_container").innerHTML=""
    document.getElementById("plan_detail_container").innerHTML=""
    loadPlanFromJson();
    showPlanPage();
}

