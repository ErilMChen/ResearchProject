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

            var node = document.createTextNode(k + ": " + data[k])
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
            newDiv.appendChild(btn)
            var br = document.createElement("br")
            newDiv.appendChild(br);
            document.getElementById('traffic_updates').append(newDiv)
        }

function see_on_map(vals){
    // Meng google map co-ordinates are the vals here
    console.log(vals)
    }