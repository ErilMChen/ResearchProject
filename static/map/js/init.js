function initControl(){
    var search_button = document.getElementById('search');
    search_button.index = 1;
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(search_button);

    var plan_button = document.getElementById('plan');
    plan_button.index = 2;
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(plan_button);

    var weather_button = document.getElementById('weather');
    weather_button.index = 3;
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(weather_button);

    var main_panel = document.getElementById('main_panel');
    main_panel.index = 4;
    map.controls[google.maps.ControlPosition.LEFT_TOP].push(main_panel);

    var weather_detail_container = document.getElementById('weather_detail_container');
    weather_detail_container.index = 6;
    map.controls[google.maps.ControlPosition.RIGHT_TOP].push(weather_detail_container);
}

function initDateTime(){
    var myDate = new Date();
    var date = document.getElementById('date');
    for(var i =0; i <5; i++){
        // Create dates for the next 5 days
        var newDate=new Date(myDate.getTime()+i*1000*60*60*24);
        var str =newDate.getDate() + "/" + (newDate.getMonth() + 1) + "/" +(newDate.getYear() + 1900);
        var dateOption=document.createElement("option");
        dateOption.setAttribute("value", str);
        date.appendChild(dateOption);
        dateArray.push(str);
    }
    // create time for the 24 hours
    var time = document.getElementById('time');
    for(var j= 1; j <= 24; j++){
        var str = j + ":00"
        var timeOption = document.createElement("option");
        timeOption.setAttribute("value", str);
        time.appendChild(timeOption);
        timeArray.push(str);
    }
}

function initBusStops(){
    // read bus station data from django server
    fetch("busstation", {
        method:'GET'}).then(function(response) {
            return response.json();
        })
    .then(function(busData) {
        // create bus station option 
        var startStop = document.getElementById('start_stop');
        var endStop = document.getElementById('end_stop');
        var str= "";
        var count = 0;
        busData.forEach(element => {
            // create strat option from each bus stop
            var startOption=document.createElement("option")
            startOption.setAttribute("value",element.stop_name);
            startStop.appendChild(startOption);
            // create end option from each bus stop
            var endOption=document.createElement("option")
            endOption.setAttribute("value",element.stop_name);
            endStop.appendChild(endOption);
            // array fro input validation (not done yet)
            busStopsArray.push(element.stop_name);
        });
    });
}

function iniEventListener(){
    // bind button with function
    document.getElementById("submit").addEventListener("click", markBusRoute);
    document.getElementById("save").addEventListener("click", saveBusRoute);
    document.getElementById("plan").addEventListener("click", showPlanPage);
    document.getElementById("search").addEventListener("click", showSearchPage);
    document.getElementById("weather").addEventListener("click", showWeatherWidget);
    document.getElementById("add_stop1").addEventListener("click", function(){ addStop("add_stop1");}); 
    document.getElementById("add_stop2").addEventListener("click", function(){ addStop("add_stop2");}); 

    document.getElementById("plan_panel").addEventListener("show.bs.collapse", function () {
        var search_panel = document.getElementById('search_panel');
        var collapse = bootstrap.Collapse.getInstance(search_panel);
        if (collapse) collapse.hide()

        var search_detail_panel = document.getElementById('search_detail_panel');
        var collapse = bootstrap.Collapse.getInstance(search_detail_panel);
        if (collapse) collapse.hide()
    });

    document.getElementById("plan_panel").addEventListener("hide.bs.collapse", function () {
        var plan_detail_panel = document.getElementById('plan_detail_panel');
        var collapse = bootstrap.Collapse.getInstance(plan_detail_panel);
        if (collapse) collapse.hide()
    });

    document.getElementById("search_panel").addEventListener("show.bs.collapse", function () {
        var plan_panel = document.getElementById('plan_panel');
        var collapse = bootstrap.Collapse.getInstance(plan_panel);
        if (collapse) collapse.hide()

        var plan_detail_panel = document.getElementById('plan_detail_panel');
        var collapse = bootstrap.Collapse.getInstance(plan_detail_panel);
        if (collapse) collapse.hide()
    });
 
    document.getElementById("search_panel").addEventListener("hide.bs.collapse", function () {
        var search_detail_panel = document.getElementById('search_detail_panel');
        var collapse = bootstrap.Collapse.getInstance(search_detail_panel);
        if (collapse) collapse.hide()
    });
}
function initUserStatus(){
    fetch("status", {
        method:'GET'}).then(function(response) {
            return response.json();
        })
    .then(function(userStatus) {
        if(userStatus == "true"){

        }else{
            var personal = document.getElementById('personal');
            personal.style.display = "none";
        }
    });
}
