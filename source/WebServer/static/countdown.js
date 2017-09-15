window.onload = function(){
	var current = new Date().getTime() + 1000;
	var begin = parseInt(document.getElementById("beginning_time").value)*1000;
	var end = current + begin;

	// Update the count down every 1 second
	var x = setInterval(function() {

		// Get todays date and time
		var now = new Date().getTime();
    
		// Find the distance between now an the count down date
		var distance = end - now;
    
		// Time calculations for days, hours, minutes and seconds
		var seconds = Math.floor(distance / 1000);
    
		// Output the result in an element with id="demo"
		document.getElementById("time_to_display").innerHTML = "Còn lại: " + seconds + "s ";
    
		// If the count down is over, write some text 
		if (distance < 0) {
			clearInterval(x);
			document.getElementById("time_to_display").innerHTML = "Hết thời gian";
		}
	}, 1000);
	
}
