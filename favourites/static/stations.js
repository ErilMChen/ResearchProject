var stops = []
var buses = []

function getStops2(){
         fetch("show_favs", {
                method:'GET'}).then(function(response) {
                    return response.json();
                })
            .then(function(myData) {
                try{
                   myData.forEach(element => {
                        unpack(element)
                     });
                    done2()
                }catch(err){
                console.log(err)
                document.getElementById('test').innerHTML = "<p>Error</p>"
                }
            })
        }

function unpack(data){
        const newDiv = document.createElement("div");
        var tags = []
        Object.keys(data).forEach(k => {
            if(k == 'Route'){
                //pass
                return
            }
            else{
            var node = document.createTextNode(k + ": " + data[k])
            newDiv.append(node)
            var br = document.createElement("br");
            newDiv.appendChild(br);

            }
            if (k == 'Bus'){
                buses.push(data[k])
                tags.push(data[k])
                }
            if (k == 'stop' || k == 'Stop'){
            stops.push(data[k])
            tags.push(data[k])
            }

                });
            //console.log(newDiv)
            newDiv.setAttribute('data-tag', tags)
            newDiv.classList.add('bus-item')
            newDiv.classList.add("shadow") //p-3 mb-5 bg-body rounded")
            newDiv.classList.add("p-3")
            newDiv.classList.add("bg-body")
            newDiv.classList.add("rounded")
            var br = document.createElement("br");
            newDiv.appendChild(br);
            document.getElementById('test').append(newDiv)
        }


function done2(html){
    sel_stops(stops)
    get_buses(buses)
    edit_stops3(stops)
}
function edit_stops3(stops){
            let unique = stops.filter((x, i, a) => a.indexOf(x) === i)
     var selectList = document.createElement("select");
    selectList.id = "myStopDelete";
    var label = document.createElement('label');
    label.setAttribute('for', 'stops')
    var txt = document.createTextNode("Delete Stop")
    label.appendChild(txt)
    document.getElementById("edit_stops").appendChild(label)
   // var br = document.createElement("br");
    //document.getElementById("edit_stops").appendChild(br);

    var disabled_op = document.createElement("option")
        var label = 'Pick a Stop'
        disabled_op.text = 'My Favourites'
        disabled_op.name = 'stops'
        disabled_op.class = "form-control"
        disabled_op.value = 'all'
        disabled_op.setAttribute('selected', true)
        disabled_op.setAttribute('disabled', true)
        selectList.appendChild(disabled_op)

    for (var i = 0; i < unique.length; i++) {
      var option=document.createElement("option")
        var label = unique[i]
        option.text = unique[i]
        option.name = 'stops'
        option.name = unique[i]
        option.class = "form-control"
        option.setAttribute("value", unique[i])

        var optionText = document.createTextNode(unique[i]);

        selectList.appendChild(option)
        }
        console.log(selectList)
        document.getElementById("edit_stops").appendChild(selectList)

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
   // var br = document.createElement("br");
   // document.getElementById("bus_dropdown").appendChild(br);


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
   // var br = document.createElement("br");
   // document.getElementById("select_stop").appendChild(br);


    var disabled_op = document.createElement("option")
        var label = 'Pick a Stop'
        disabled_op.text = 'All'
        disabled_op.name = 'stops'
        disabled_op.class = 'active'
        disabled_op.value = 'all'
        disabled_op.setAttribute('selected', true)
        selectList.appendChild(disabled_op)

    for (var i = 0; i < unique.length; i++) {
      var option=document.createElement("option")
        var label = unique[i]
        option.text = unique[i]
        option.name = 'stops'
        option.name = unique[i]
        option.class = 'active'
        option.setAttribute("value", unique[i])

        var optionText = document.createTextNode(unique[i]);

        selectList.appendChild(option)
        }
        console.log(selectList)
        document.getElementById("select_stop").appendChild(selectList)

}