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
                        html += "<p> --------------- </p></div>"
                });
                done(html)
                }catch(err){
                console.log(err)
                document.getElementById('data').innerHTML = "<p>Error</p>"
                }
            })
        }

function unpack(data){
        var temp = ""
        Object.keys(data).forEach(k => {
            if(k == 'Route'){
                //pass
            }
            else{
            temp += "<p class=" + k + "><b>" + k + "</b>: " + data[k]+ "<p>"
            }
            if (k == 'Bus'){
                buses.push(data[k])
                html += "stop_div' " +  "data-tag= [" + data[k] + ","

            }
            if (k == 'stop' || k == 'Stop'){
            stops.push(data[k])
             html +=  data[k] + "]>"
            }
                });
            html += temp
        }

function done(html){
    sel_stops(stops)
    get_buses(buses)
    document.getElementById("data").innerHTML = html

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

    var disabled_op = document.createElement("option")
        var label = 'Pick a Bus'
        disabled_op.text = 'All'
        disabled_op.name = 'buses'
        disabled_op.class = 'bus_drop'
        disabled_op.value = 'all'
        disabled_op.setAttribute('selected', true)
        selectList.appendChild(disabled_op)

    for (var i = 0; i < unique.length; i++) {
      var option=document.createElement("option")
        var label = unique[i]
        option.text = unique[i]
        option.name = 'buses'
        option.name = unique[i]
        option.class = 'bus_drop'

        option.setAttribute("value", unique[i])

        var optionText = document.createTextNode(unique[i]);
        selectList.appendChild(option)
        }
        console.log(selectList)
        document.getElementById("bus_dropdown").appendChild(selectList)

}

function sel_stops(stops){
    let unique = stops.filter((x, i, a) => a.indexOf(x) === i)
     var selectList = document.createElement("select");
    selectList.id = "myStopSelect";
    var label = document.createElement('label');
    label.setAttribute('for', 'stops')
    var txt = document.createTextNode("Select Stop Filter")
    label.appendChild(txt)
    document.getElementById("select_stop").appendChild(label)

    var disabled_op = document.createElement("option")
        var label = 'Pick a Stop'
        disabled_op.text = 'All'
        disabled_op.name = 'stops'
        disabled_op.class = 'stop_drop'
        disabled_op.value = 'all'
        //disabled_op.setAttribute('disabled', true)
        disabled_op.setAttribute('selected', true)
        selectList.appendChild(disabled_op)

    for (var i = 0; i < unique.length; i++) {
      var option=document.createElement("option")
        var label = unique[i]
        option.text = unique[i]
        option.name = 'stops'
        option.name = unique[i]
        option.class = 'stop_drop'
        option.setAttribute("value", unique[i])

        var optionText = document.createTextNode(unique[i]);

        selectList.appendChild(option)
        }
        console.log(selectList)
        document.getElementById("select_stop").appendChild(selectList)

}