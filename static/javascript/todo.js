function OrderOptions() {
    var ordnum = 1;
    var soptions = "<option value='0'>Valitse numero</option>";

    for (var i = ordnum; i < ordnum + 15; i++) {
    soptions += "<option value='"+i+"'>"+i+"</option>"
    }

    document.getElementById('select').innerHTML = soptions;

}

function chores() {
    var housechores = ["Siivoaminen","Kaupassa käynti","Ruuan laitto","Tiskaaminen","Imuroiminen","Pyykkääminen","Roskien vienti","Ruohon leikkuu","Haravointi","Puiden kanto","Lumen kolaus"];
    var chorelength = housechores.length;
    var yoptions = "<option value='Et valinnut kotityötä!'>Valitse kotityö</option>";

    for (var a = 0; a < chorelength; a++) {
    yoptions += "<option value='"+housechores[a]+"'>"+housechores[a]+"</option>"
    }

    document.getElementById('chores').innerHTML = yoptions;
}

function calDate(){
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; //January is 0!
    var yyyy = today.getFullYear();
        if(dd<10){
            dd='0'+dd
        }
            if(mm<10){
                mm='0'+mm
            }

    today = yyyy+'-'+mm+'-'+dd;
    document.getElementById("cal").setAttribute("min", today);
}

function caleDate(){
    var tod = new Date();
    var d = tod.getDate();
    var m = tod.getMonth()+1;
    var yyy = tod.getFullYear();
        if(d<10){
            d='0'+d
        }
            if(m<10){
                m='0'+m
            }

    tod = yyy+'-'+m+'-'+d;
    document.getElementById("cale").setAttribute("min", tod);
}

var options = { weekday: 'short', year: 'numeric', month: 'long', day: 'numeric' };