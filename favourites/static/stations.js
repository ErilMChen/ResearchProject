function getStops(){
         fetch("show_favs", {
                method:'GET'}).then(function(response) {
                    return response.json();
                })
            .then(function(myData) {
                myData.forEach(element => {
                        for (var key in myData){
                        console.log(myData[key])
}
                });
            });
        }

function unpack(data){
        console.log(data)
        }
