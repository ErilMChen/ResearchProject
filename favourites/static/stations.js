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
    select_stop += "<option disabled selected value> -- Select an Stop -- </option>"

     for(var i=0; i < unique.length; i++){
        select_stop+= "<option value=" + unique[i] + ">" + unique[i] + "</option>"

        }
        select_stop += "</select>"
        document.getElementById("select_stop").innerHTML = select_stop

        edit_stops2(unique)
}



function edit_stops2(stops){
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "/delete_my_stop")
    for(var i=0; i < stops.length; i++){
        var option=document.createElement("input")
        option.setAttribute("value",stops[i])
        option.setAttribute('readonly', 'readonly')
        form.appendChild(option);
        //console.log(form)

      let btn = document.createElement("button")
      btn.innerHTML = "Delete this Stop from";
      btn.setAttribute('value', stops[i])
      form.appendChild(btn);
        }
        console.log(form)

       document.getElementById("edit_stops").appendChild(form)
    }