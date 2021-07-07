var html = ""
var stops = []
function getStops(){
         fetch("show_favs", {
                method:'GET'}).then(function(response) {
                    return response.json();
                })
            .then(function(myData) {
                myData.forEach(element => {
                        html += "<div class='"
                        unpack(element)
                        //console.log(element)
                        html += "<p> --------------- </p></div>"
                });
                done(html)
            });
        }

function unpack(data){
        var temp = ""
        console.log(typeof(data))
        Object.keys(data).forEach(k => {
            //console.log(k, data[k]);
            temp += "<p class=" + k + "><b>" + k + "</b>: " + data[k]+ "<p>"
            if (k == 'stop'){
            stops.push(data[k])
            html += data[k] + "'>"}
                });
            html += temp
        }

function done(html){
    get_stops(stops)
    document.getElementById("data").innerHTML = html

}

function get_stops(stops){
    let unique = stops.filter((x, i, a) => a.indexOf(x) === i)
    var select_stop = "<label for=stops>Choose a stop:</label>"
    select_stop += "<select name='stops' id='stops'>"

     for(var i=0; i < unique.length; i++){
        select_stop+= "<option value=" + unique[i] + ">" + unique[i] + "</option>"

        }
        select_stop += "</select>"
        document.getElementById("select_stop").innerHTML = select_stop
}