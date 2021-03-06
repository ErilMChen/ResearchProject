// Submit the starting and ending stations and return to the navigation route

function getLocation() {
	var x = document.getElementById("demo1");
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
        } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
        }
    }

function showPosition(position) {
    var x = document.getElementById("demo1");
  x.innerHTML = "Latitude: " + position.coords.latitude +
  "<br>Longitude: " + position.coords.longitude;
  document.getElementById('floatingStart').value = "My Location";
  document.getElementById('demo1').value = (position.coords.latitude).toString() + "/" +(position.coords.longitude).toString();
}

function clear_details(){
    document.getElementById('floatingStart').value = "";
    document.getElementById('floatingEnd').value = "";
    document.getElementById('floatingDate').value = "";
    document.getElementById('floatingTime').value = "";
	// document.getElementById("add_stop1").disabled = false;
}



function markBusRoute( ){
    // read user input from form
    var start = document.forms["bus_stop"]["start_stop"].value;
    var end = document.forms["bus_stop"]["end_stop"].value;
    var date = document.forms["bus_stop"]["date"].value;
    var time = document.forms["bus_stop"]["time"].value;
    var my_loc = 0;

    // form validation
    if(start == 'My Location'){
        my_loc = (document.getElementById('demo1').value).toString()
    }
    else if(start == ""){
        alert("Wrong Start Bus Stop Input");
        return "wrong start stop name input"
    }
    if(end == ""){
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
    console.log(start)
    if(start.includes('Dublin') == false && start.includes('Wicklow') == false && start.includes('My Location') == false)
    {alert('Wrong county at origin!')
        return "wrong county"
    }
    if(end.includes('Dublin') == false && end.includes('Wicklow') == false)
    {alert('Wrong county at destination!')
        return "wrong county"
    }

    // create url
    let url = 'route/'+'?start_stop='+start+'&end_stop='+end +'&date='+date +'&time='+time + '&my_loc=' + my_loc;
    var pairs = url.split("&");
    var date = pairs[2].split("=")[1];
    var time = pairs[3].split("=")[1];
    var hour = time.split(":")[0];
    var year = date.split("/")[2];
    var month = date.split("/")[1];
    var day = date.split("/")[0];
    // fetch(url, {
    //     // send request to django server
    //     method:'GET'}).then(function(response) {
    //         return response.json();
    //     })
    // .then(function(routeDate){
        // use google api to set route on map
    directionsRenderer.setMap(map);
    console.log(glocations[0])
        // set strat posiotion and end posiotion
        // var start_position = new google.maps.LatLng(routeDate[0].stop_lat, routeDate[0].stop_long);
        // var end_position = new google.maps.LatLng(routeDate[1].stop_lat, routeDate[1].stop_long);
    var start = document.forms["bus_stop"]["start_stop"].value;
    if (start == 'My Location'){
        coord = document.getElementById('demo1').value;
        coord_arr = coord.split("/")
        var slat = coord_arr[0]
        var slng = coord_arr[1]
        console.log(slat,slng)
    }
    else{
    var slat = glocations[0].getPlace().geometry.viewport.tc.g
    var slng = glocations[0].getPlace().geometry.viewport.Hb.g
    }
	//var slat = glocations[0].getPlace().geometry.viewport.mc.g
    //var slng = glocations[0].getPlace().geometry.viewport.Eb.g
    var elat = glocations[1].getPlace().geometry.viewport.tc.g
    var elng = glocations[1].getPlace().geometry.viewport.Hb.g
    var start_position = new google.maps.LatLng(slat, slng);
    var end_position = new google.maps.LatLng(elat, elng);
        // console.log(start_position)
        // console.log(end_position)
    var request = {
        origin: start_position ,
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
        else{
        alert('Oops! Google could not find a bus route between these two destinations!')}
    });
    // });
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
    var slat = pairs[5].split("=")[1];
    var slng = pairs[6].split("=")[1];
    var elat = pairs[7].split("=")[1];
    var elng = pairs[8].split("=")[1];
    // fetch(url, {
    //     method:'GET'}).then(function(response) {
    //         return response.json();
    //     })
    // .then(function(routeDate){
        // use google api to set route on map
    directionsRenderer.setMap(map);
    // set strat posiotion and end posiotion
    // var start_position = new google.maps.LatLng(routeDate[0].stop_lat, routeDate[0].stop_long);
    // var end_position = new google.maps.LatLng(routeDate[1].stop_lat, routeDate[1].stop_long);

    var start_position = new google.maps.LatLng(slat, slng);
    var end_position = new google.maps.LatLng(elat, elng);
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
    // });
}

// show route detail infromation
function showRoutedetail(response, element, url){
    // extract data from google response
	console.log(response);
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
    //var text ="Total distance: " + total_distance + " kilometres\n" + "Total duration: " + total_duration + " minuites";
    var text = 'Your Journey Estimates'
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
        if (response.ok){//????????????????????????
            return response.json()
        }
        throw new Error('??????????????????')
    })
    .then(function(timeData){
        for(var i = 0; i< locations.length; i++){
            (function(i){
                allowed = ['1','4', '6', '7', '7A', '7B', '7D', '9', '11', '13',
                 '14', '15', '15A', '15B', '15D', '16','16C',
                '16D', '17', '17A', '18','25', '25A','25B', '25D', '25X', '26', '27',
                 '27A', '27B', '27X','29A', '31', '31A', '31B', '31D', '32','32X', '33','33A',
		'33B', '33D',
                '33E', '33X', '37', '38','38A', '38B', '38D', '39', '39A', '39X', '40', '40B',
                 '40D', '40E', '41','41A','41B','41C', '41D', '41X', '42','42D',
                '43', '44', '44B','45A', '46A', '46E', '47', '49', '51D',
                '53', '54A','56A', '59','61','63', '65', '65B', '66', '66A',
                '66B', '66X', '67', '67X', '68','69X', '70','70D','75','76', '76A', '77A',
                 '77X', '79A', '83', '83A', '84', '84A', '84X', '116', '102','104', '111', '114', '116',
                '118', '120', '122', '123', '130','140', '142','145','150', '151', '155', '161', '184',
		'185', '220','236', '238', '239', '270']
                var target = document.createElement("div");
                setRouteDetailDiv(target);
                element.appendChild(target);
                writeLine("Leg "+ (i+1) + " of the journey", target)
                writeLine("Departure Stop: "+locations[i].startStop, target)
                writeLine("Arrival Stop: "+ locations[i].endStop, target)
                if(allowed.includes(locations[i].line) == true){
                writeLine("Bus Line: "+ locations[i].line, target)
                }
                else{
                writeLine("Bus Line: No Dublin Bus service available.", target)
                }
                writeLine("Distance: "+ locations[i].distance, target)
                console.log(timeData[i])
                if (timeData[i] != "false")
                    writeLine("Duration: "+ timeData[i] + " mins", target)
                else
                    writeLine("Duration: "+ locations[i].duration, target)
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
