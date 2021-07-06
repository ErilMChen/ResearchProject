function getStops(){
         fetch("show_favs", {
                method:'GET'}).then(function(response) {
                    return response.json();
                })
            .then(function(myData) {
                myData.forEach(element => {
                     var string =JSON.stringify(myData);
                        str = string.replace(/\\/g, '');
                        unpack(str)
                });
            });
        }

function unpack(data){
        console.log('hello')
}