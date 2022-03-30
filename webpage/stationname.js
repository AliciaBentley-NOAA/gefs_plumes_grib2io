//Search for a name within an object
function searchByName(keyname, arr){
    for (var i=0; i < arr.length; i++){
        if (arr[i].name === keyname){
            return i;
        }
    }
	return -1;
}

//Update the URL in the address bar by the current stationname
function generate_url(){
	var url = window.location.href.split('?')[0] + "?";
	var append = "";

        //Add stationname
        append += "stationname=" + imageObj.stationname;

        //Get new URL
        var total = url + append;

	//Update in address bar without reloading page
	var pagename = window.location.href.split('/');

        if (url.indexOf(".html") != -1){
        pagename = pagename[pagename.length-1];
        pagename = pagename.split(".html")[0];
        var stateObj = { foo: "bar" };
        history.replaceState(stateObj, "", pagename+".html?"+append);
	}
        if (url.indexOf(".html") == -1){
	pagename = pagename[pagename.length-1];
	pagename = pagename.split(".html")[0];
	var stateObj = { foo: "bar" };
	history.replaceState(stateObj, "", pagename+"index.html?"+append);
	}

	return total;
}
