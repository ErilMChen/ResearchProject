window.onload = getupdates()
function getupdates(){

        // This function splits the json object returned from django
         fetch("get_live_updates", {
                method:'GET'}).then(function(response) {
                    return response.json();
                })
            .then(function(myData) {
                try{
                   myData.forEach(element => {
                        unpack(element['fields'])
                     });
                }catch(err){
                console.log(err)
                document.getElementById('test').innerHTML = "<p>Error</p>"
                }
            })
        }

function unpack(data){
        var vals = []
        const newDiv = document.createElement("div");
        const btn = document.createElement('button')
        Object.keys(data).forEach(k => {
            if(k == 'lat'){
            j = 'Latitude'
            }
            else if (k =='long'){
            j = 'Longitude'}
            else if (k =='report'){
            j = 'Report'}
            else if (k =='location'){
            j = 'Location'}

            var node = document.createTextNode(j + ": " + data[k])
            newDiv.append(node)
            var br = document.createElement("br");
            newDiv.appendChild(br);

            if (k== 'lat'){
                vals.push(data[k].toString())
            }
            if(k=='long'){
            vals.push(data[k].toString())
            }

                });

            newDiv.setAttribute('data-tags', vals)
            newDiv.classList.add('update-item')
            btn.setAttribute('value', vals)
            btn.setAttribute('onclick', 'see_on_map(this.value)')
            btn.innerHTML = 'See on Map!'
            btn.classList.add('btn')
            btn.classList.add('btn-primary')
            btn.classList.add('btn_profile')
            btn.classList.add('text-center')
            var br = document.createElement("br")
            newDiv.appendChild(br);
            newDiv.appendChild(btn)
            var br = document.createElement("br")
            newDiv.appendChild(br);
            newDiv.classList.add('traffic_card')
            newDiv.classList.add('justify-content-center')
            document.getElementById('traffic_updates').append(newDiv)
            document.getElementById('traffic_updates').append(br)
        }

function see_on_map(vals){
    // split the string into two values (lat and long
    const myArr = vals.split(",");
    //get map
    directionsRenderer.setMap(map);
    lat = parseFloat(vals)
    lon = parseFloat(myArr[1])
    // make marker
    var latlng = new google.maps.LatLng(lat,lon);
    //make info window
    const infowindow = new google.maps.InfoWindow({
    content: 'AA RoadWatch Incident Reported',
    });

    var marker = new google.maps.Marker({
    position: latlng,
    title:"Incident",
    center: { lat: lat, lng: lon },
    });

    marker.addListener("click", () => {
    infowindow.open({
      anchor: marker,
      map,
      shouldFocus: false,
    });
  });

    marker.setMap(map);
    // center map on this
    var myOptions = {
            center: { lat: lat, lng: lon},
            zoom : 14
        };
        map.setOptions(myOptions);
    }


function clear_messages(){
    document.getElementById('messages_div').style.display = 'none';
}

function confirm_me(){
    if (confirm("Confirm you wish to delete this account and all of your data?")){
    var form = document.createElement("form");
    form.id = "del_form";
    form.setAttribute("method", "post");
    form.setAttribute("action", "/delete_acc/")
    document.body.appendChild(form);
    document.getElementById('del_form').submit();
    }
    else {
        return
    }
}