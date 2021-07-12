// Submit the starting and ending stations and return to the navigation route
function markBusRoute( ){
    // read user input from form
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

    // create url
    let url = 'route/'+'?start_stop='+start+'&end_stop='+end +'&date='+date +'&time='+time;
    fetch(url, {
        // send request to django server
        method:'GET'}).then(function(response) {
            return response.json();
        })
    .then(function(routeDate){
        // use google api to set route on map
        directionsRenderer.setMap(map);
        // set strat posiotion and end posiotion
        var start_position = new google.maps.LatLng(routeDate[0].stop_lat, routeDate[0].stop_long);
        var end_position = new google.maps.LatLng(routeDate[1].stop_lat, routeDate[1].stop_long);
        var request = {
            origin: start_position,
            destination: end_position,
            travelMode: google.maps.TravelMode["TRANSIT"],
            provideRouteAlternatives :false,
            transitOptions: {
                modes: ['BUS'],
            },

        };
        directionsService.route(request, function(response, status) {
            if (status == 'OK') {
                //draw route on map (google api)
                directionsRenderer.setDirections(response);
                //show route detail
                showRoutedetail(response, "detail_container")
            }
        });
    });
}

// show plan route detail
function showPlan(url){
    // use the key of every local storage item as url
    // send request to django server
    fetch(url, {
        method:'GET'}).then(function(response) {
            return response.json();
        })
    .then(function(routeDate){
        // use google api to set route on map
        directionsRenderer.setMap(map);
        // set strat posiotion and end posiotion
        var start_position = new google.maps.LatLng(routeDate[0].stop_lat, routeDate[0].stop_long);
        var end_position = new google.maps.LatLng(routeDate[1].stop_lat, routeDate[1].stop_long);
        var request = {
            origin: start_position,
            destination: end_position,
            travelMode: google.maps.TravelMode["TRANSIT"],
            provideRouteAlternatives :false,
            transitOptions: {
                modes: ['BUS'],
            },

        };
        // send request to google map server
        directionsService.route(request, function(response, status) {
            if (status == 'OK') {
                //draw route on map (google api)
                directionsRenderer.setDirections(response);
                //show route detail
                showRoutedetail(response, "plan_detail_container")
            }
        });
    });
}

// show route detail infromation
function showRoutedetail(response, element){
    // extract data from google response
    var myRoute = response.routes[0].legs[0];
    var locations = new Array();
    var total_distance = 0, total_duration = 0;
    // var jsonData = {};
    for (var i = 0; i < myRoute.steps.length; i++) {
        if(myRoute.steps[i].travel_mode == "TRANSIT")
        {
            // route detail from google server
            var location={
                startStop : myRoute.steps[i].transit.departure_stop.name,
                endStop : myRoute.steps[i].transit.arrival_stop.name,
                line : myRoute.steps[i].transit.line.short_name,
                distance : myRoute.steps[i].distance.text,
                duration : myRoute.steps[i].duration.text,
            }
            total_duration += Math.round(myRoute.steps[i].duration.value/60);
            total_distance += Math.round(myRoute.steps[i].distance.value/1000);
            locations.push(location)
        }
    }

    // write infrom mation on certain element
    var element = document.getElementById(element);
    element.innerHTML = "";

    var target = document.createElement("div");
    setRouteTitle(target);
    element.appendChild(target);

    var target = document.createElement("div");
    setRouteDetailDiv(target);
    element.appendChild(target);
    var text ="Total distance: " + total_distance + " kilometres\n" + "Total duration: " + total_duration + " minnuites";
    writeLine(text, target);
    for (var i = 0; i< locations.length; i++){
        var target = document.createElement("div");
        setRouteDetailDiv(target);
        element.appendChild(target);
        writeLine("The "+ (i+1) + " leg of the journey", target)
        writeLine("Departure Stop: "+locations[i].startStop, target)
        writeLine("Arrival Stop: "+ locations[i].endStop, target)
        writeLine("Bus line: "+ locations[i].line, target)
        writeLine("Distance: "+ locations[i].distance, target)
        writeLine("Duration: "+ locations[i].duration, target)
    }
}

// write text on certain element
function writeLine(text ,target){
    var container = document.createElement("div");
    var node = document.createTextNode(text);
    container.appendChild(node);
    target.appendChild(container);
}

function setRouteDetailDiv(element){
    element.setAttribute("class", "route-detail");
}

function setRouteTitle(element){
    element.setAttribute("class", "route-title");
    element.innerHTML = "ROUTE DETAIL";
}