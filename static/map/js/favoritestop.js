function addStop(element){
    if(element == "add_stop1")
        var stop_name = document.forms["bus_stop"]["start_stop"].value;
    else if (element == "add_stop2")
        var stop_name = document.forms["bus_stop"]["end_stop"].value;

    console.log(glocations)
    // form validation
    if(busStopsArray.includes(stop_name) == false){
        alert("Wrong Bus Stop Input");
        return "wront stop name input"
    }
       

    let url = 'add/' + '?stop_name=' + stop_name;
    fetch(url, {
        method:'GET'}).then(function(response) {
            // read data from django server and prase to json
            return response.json()
    }).then(function(userStatus) {
        if(userStatus == "false"){
            alert("You Haven't Log In !");
        }
    });
}