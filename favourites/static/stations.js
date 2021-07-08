var html = ""
var stops = []
var buses = []
function getStops(){
         fetch("show_favs", {
                method:'GET'}).then(function(response) {
                    return response.json();
                })
            .then(function(myData) {
                try{
                myData.forEach(element => {
                        html += "<div class='"
                        unpack(element)
                        //console.log(element)
                        html += "<p> --------------- </p></div>"
                });
                done(html)
                }catch(err){
                console.log(err)
                document.getElementById('data').innerHTML = "<p>Error</p>"
                }
            })
        }

function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}

function unpack(data){
        var temp = ""
        Object.keys(data).forEach(k => {
            if(k == 'Route'){
                //pass
            }

            else{
            //console.log(k, data[k]);
            temp += "<p class=" + k + "><b>" + k + "</b>: " + data[k]+ "<p>"
            //console.log(k)
            }
            if (k == 'stop' || k == 'Stop'){
            stops.push(data[k])
            html += data[k] + "'>"}

            if (k == 'Bus'){
                buses.push(data[k])
            }
                });
            html += temp
        }

function done(html){
    get_stops(stops)
    get_buses(buses)
    document.getElementById("data").innerHTML = html

}

function get_stops(stops){
    let unique = stops.filter((x, i, a) => a.indexOf(x) === i)
    var select_stop = "<label for=stops>Filter by Stop:</label>"
    select_stop += "<select name='stops' id='stops'>"
    select_stop += "<option disabled selected value> -- Select an Stop -- </option>"

     for(var i=0; i < unique.length; i++){
        select_stop+= "<option value=" + unique[i] + ">" + unique[i] + "</option>"

        }
        select_stop += "</select>"
        document.getElementById("select_stop").innerHTML = select_stop

        edit_stops3(unique)
}

function get_buses(buses){
    let unique = buses.filter((x, i, a) => a.indexOf(x) === i)
    var selectList = document.createElement("select");
    selectList.id = "mySelect";
    var label = document.createElement('label');
    label.setAttribute('for', 'buses')
    var txt = document.createTextNode("Select Bus Filter")
    label.appendChild(txt)
    document.getElementById("bus_dropdown").appendChild(label)


    selectList.setAttribute('label', 'Select Bus Filter')

    for (var i = 0; i < unique.length; i++) {
      var option=document.createElement("option")
        var label = unique[i]
        option.text = unique[i]
        option.name = 'buses'
        option.name = unique[i]
        option.class = 'bus_drop'

        option.setAttribute("value", unique[i])

        var optionText = document.createTextNode(unique[i]);
        //option.appendChild(optionText);

        selectList.appendChild(option)
        }
        console.log(selectList)
        document.getElementById("bus_dropdown").appendChild(selectList)

}


function edit_stops2(stops){
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.id = 'form1'
    form.setAttribute("action", "/delete_my_stop/")
    for(var i=0; i < stops.length; i++){
        var option=document.createElement("input")
        option.type = "radio"
        option.text = stops[i]
        option.name = 'stops'
        option.class = 'stops'

        option.setAttribute("value", stops[i])

        var label = document.createElement('label');
        label.innerHTML = stops[i]
        option.appendChild(label)

        //option.setAttribute('readonly', 'readonly')
        form.appendChild(option);
        form.appendChild(label)
        //console.log(form)

      //let btn = document.createElement("button")
      //btn.innerHTML = "Delete this Stop from my Favourites";
      //btn.setAttribute('value', stops[i])
      //form.appendChild(btn);
        }
        console.log(form)
        let btn = document.createElement("button")
        btn.id = 'submit_stop'
        btn.innerHTML = "Delete this Stop from my Favourites";
        form.appendChild(btn)
       document.getElementById("edit_stops").appendChild(form)
    }

function edit_stops3(stops){
        var select_stop = "<label for=stops>Delete Stop:</label>"
        select_stop += "<select name='stops' id='del_stops'>"
        select_stop += "<option disabled selected value> -- Select a Stop -- </option>"

     for(var i=0; i < stops.length; i++){
        select_stop+= "<option value=" + stops[i] + " onlick=addStop()>" + stops[i] + "</option>"
        }
        select_stop += "</select>"
        document.getElementById("edit_stops").innerHTML = select_stop
}