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
    var pairs = url.split("&");
    var date = pairs[2].split("=")[1];
    var time = pairs[3].split("=")[1];
    var hour = time.split(":")[0];
    var year = date.split("/")[2];
    var month = date.split("/")[1];
    var day = date.split("/")[0];
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
                departureTime: new Date(year, month, day, hour),
                modes: ['BUS'],
            },

        };
        directionsService.route(request, function(response, status) {
            if (status == 'OK') {
                //draw route on map (google api)
                directionsRenderer.setDirections(response);
                //show route detail
                showRoutedetail(response, "detail_container", url)
            }
        });
    });
}

// show plan route detail
function showPlan(url){
    // use the key of every local storage item as url
    // send request to django server
    var pairs = url.split("&");
    var date = pairs[2].split("=")[1];
    var time = pairs[3].split("=")[1];
    var hour = time.split(":")[0];
    var year = date.split("/")[2];
    var month = date.split("/")[1];
    var day = date.split("/")[0];
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
                departureTime: new Date(year, month, day, hour),
                modes: ['BUS'],
            },
        };
        // send request to google map server
        directionsService.route(request, function(response, status) {
            if (status == 'OK') {
                //draw route on map (google api)
                directionsRenderer.setDirections(response);
                //show route detail
                showRoutedetail(response, "plan_detail_container", url)
            }
        });
    });
}

// show route detail infromation
function showRoutedetail(response, element, url){
    // extract data from google response
    var myRoute = response.routes[0].legs[0];
    var locations = new Array();
    var total_distance = 0, total_duration = 0;
    
    var pairs = url.split("&");
    var date = pairs[2].split("=")[1];
    var time = pairs[3].split("=")[1];
    // var jsonData = {};
    for (var i = 0; i < myRoute.steps.length; i++) {
        if(myRoute.steps[i].travel_mode == "TRANSIT")
        {
            // route detail from google server
            var location={
                startStop : myRoute.steps[i].transit.departure_stop.name,
                endStop : myRoute.steps[i].transit.arrival_stop.name,
                lineName : myRoute.steps[i].transit.line.name,
                line : myRoute.steps[i].transit.line.short_name,
                distance : myRoute.steps[i].distance.text,
                duration : myRoute.steps[i].duration.text,
                date : date,
                time : time,
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

    var pBody=new Array();
    for(var i = 0; i< locations.length; i++){
        (function(i){
            pBody.push({ "i" : locations[i]});
        }(i));
    }
    console.log(locations)
    fetch('predict/', {
    body: JSON.stringify({jsonArray : locations}),
    headers: {
        'content-type': 'application/json'
    },
    method: 'POST',
    })
    .then(function(response){
        if (response.ok){//判断请求是否成功
            return response.json()
        }
        throw new Error('请求发生错误')
    })
    .then(function(timeData){
        for(var i = 0; i< locations.length; i++){
            (function(i){
                var target = document.createElement("div");
                setRouteDetailDiv(target);
                element.appendChild(target);
                writeLine("The "+ (i+1) + " leg of the journey", target)
                writeLine("departure stop: "+locations[i].startStop, target)
                writeLine("arrival stop: "+ locations[i].endStop, target)
                writeLine("bus line: "+ locations[i].line, target)
                writeLine("distance: "+ locations[i].distance, target)
                
                if (timeData[i] != "false")
                    writeLine("duration: "+ timeData[i], target)
                else
                    writeLine("duration: "+ locations[i].duration, target)
            }(i));
        }
    })
    

    // for(var i = 0; i< locations.length; i++){
    //     (function(i){
    //         var target = document.createElement("div");
    //         setRouteDetailDiv(target);
    //         element.appendChild(target);
    //         writeLine("The "+ (i+1) + " leg of the journey", target)
    //         writeLine("departure stop: "+locations[i].startStop, target)
    //         writeLine("arrival stop: "+ locations[i].endStop, target)
    //         writeLine("bus line: "+ locations[i].line, target)
    //         writeLine("distance: "+ locations[i].distance, target)
    //         writeLine("duration: "+ locations[i].duration, target)
    //     }(i));
    // }
}

// write text on certain element
function writeLine(text ,target){
    var container = document.createElement("div");
    var node = document.createTextNode(text);
    container.appendChild(node);
    target.appendChild(container);
}

function setRouteDetailDiv(element){
    element.setAttribute("class", "card route_detail_card");
}

function setRouteTitle(element){
    element.setAttribute("class", "card route_card shadow");
    element.innerHTML = "ROUTE DETAIL";
}