// save route
function saveBusRoute(){
    // read data from form
    var start = document.forms["bus_stop"]["start_stop"].value;
    var end = document.forms["bus_stop"]["end_stop"].value;
    var date = document.forms["bus_stop"]["date"].value;
    var time = document.forms["bus_stop"]["time"].value;
    var plan_name = document.forms["bus_stop"]["plan_name"].value;

    var slat = glocations[0].getPlace().geometry.viewport.mc.g
    var slng = glocations[0].getPlace().geometry.viewport.Eb.g
    var elat = glocations[1].getPlace().geometry.viewport.mc.g
    var elng = glocations[1].getPlace().geometry.viewport.Eb.g
    // creat url which use fro send request to django server
    let url = 'addplan/'+'?start_stop='+start+'&end_stop='+end +'&date='+date +'&time='+time +'&plan_name=' + plan_name
    +'&slat='+slat +'&slng='+slng +'&elat='+elat +'&elng='+elng;
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
    var plan_name = document.forms["bus_stop"]["plan_name"].value;

    // form validation
    // if(busStopsArray.includes(start) == false){
    //     alert("Wrong Start Bus Stop Input");
    //     return "wrong start stop name input"
    // }
    // if(busStopsArray.includes(end) == false){
    //     alert("Wrong End Bus Stop Input");
    //     return "wrong end stop name input"
    // }
    if(dateArray.includes(date) == false){
        alert("Wrong Date Input");
        return "wrong date input"
    }
    if(timeArray.includes(time) == false){
        alert("Wrong Time Input");
        return "wrong time input"   
    }  

    var slat = glocations[0].getPlace().geometry.viewport.mc.g
    var slng = glocations[0].getPlace().geometry.viewport.Eb.g
    var elat = glocations[1].getPlace().geometry.viewport.mc.g
    var elng = glocations[1].getPlace().geometry.viewport.Eb.g

    // creat url which use fro send request to django server
    // the url will be the key used in local storage
    let url = 'route/'+'?start_stop='+start+'&end_stop='+end +'&date='+date +'&time='+time +'&plan_name=' + plan_name
    +'&slat='+slat +'&slng='+slng +'&elat='+elat +'&elng='+elng;
    var locations = {
        startStop :  start,
        endStop : end,
        date : date,
        time : time,
        name : plan_name,
        slat : slat,
        slng : slng,
        elat : elat,
        elng : elng
    }
    str = JSON.stringify(locations);
    // key is url, value is location information
    // save to local storage
    localStorage.setItem(url,str);
}

function scy_plan(){
    for(var i=localStorage.length - 1 ; i >=0; i--){
        (function(i){
        // traverse each key
        var url = localStorage.key(i);
        // get value by using key
        var str=localStorage.getItem(url); 
        var locations=JSON.parse(str); 
        let url2 = 'addplan/'+'?start_stop='+locations.startStop+'&end_stop='+locations.endStop +'&date='+locations.date +'&time='+locations.time +'&plan_name=' + locations.name
        +'&slat='+locations.slat +'&slng='+locations.slng +'&elat='+locations.elat +'&elng='+locations.elng;
        fetch(url2, {
            method:'GET'}).then(function(response) {
                // read data from django server and prase to json
                // console.log(response.json());
                // return response.json();
            });
        }(i));
    }
    let url3 = 'loadplan/'
    fetch(url3, {
        method:'GET'}).then(function(response) {
            // read data from django server and prase to json
            return response.json();
    }).then(function(planDate){
        planDate.forEach(element => {
            let url4 = 'route/'+'?start_stop='+element.start_stop+'&end_stop='+element.end_stop+'&date='+element.date+'&time='+ element.time+'&plan_name=' +element.plan_name
            +'&slat='+element.start_lat +'&slng='+element.start_long +'&elat='+element.end_lat +'&elng='+element.end_long;
            var location = {
                startStop :  element.start_stop,
                endStop : element.end_stop,
                date : element.date,
                time : element.time,
                name : element.plan_name,
                slat : element.start_lat,
                slng : element.start_long,
                elat : element.end_lat,
                elng : element.end_long
            }
            str = JSON.stringify(location);
            // key is url, value is location information
            // save to local storage
            localStorage.setItem(url4,str);
        });
    });
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
        writeLine("name: "+ locations.name, container); 
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
    element.setAttribute("class", "card route_card shadow ");
    element.innerHTML="MY PLAN"
}

function setDiv(element){
    element.setAttribute("class", "btn-group plan-group");
    element.setAttribute("role", "group");
}

function setPlanButton(element){
    element.setAttribute("href", "#plan_detail_panel");
    element.setAttribute("class", "btn btn-dark btn button-plan");
    element.setAttribute("data-bs-toggle", "collapse")
    element.setAttribute("aria-expanded", "false")
    element.setAttribute("aria-controls", "plan_detail_panel")
    element.setAttribute("overflow", "hidden;")
}

function setDeleteButton(element){
    element.setAttribute("class", "btn btn-danger btn button-delete");
}

function deletePlan(url){
    // remove item from database
    var url = localStorage.key(url);
    // get value by using key
    var str=localStorage.getItem(url); 
    var locations=JSON.parse(str);
    let url2 = 'removeplan/'+'?start_stop='+locations.startStop+'&end_stop='+locations.endStop +'&date='+locations.date +'&time='+locations.time +'&plan_name=' + locations.name;
    fetch(url2, {
        method:'GET'}).then(function(response) {
            // read data from django server and prase to json
            return response.json();
    });

    // remove item from local storage
    localStorage.removeItem(url);


    // clean plan pannel and reload
    document.getElementById("plan_container").innerHTML=""
    document.getElementById("plan_detail_container").innerHTML=""
    loadPlanFromJson();
    showPlanPage();
}

