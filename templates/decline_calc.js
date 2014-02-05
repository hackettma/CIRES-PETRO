$(document).ready(function() {
	
/*	This was experimental code on getting values from forms using jquery	


		$("#calc").click(function () {
		var Phase = $("#Phase").val();
		var Qi = $("#qi").val();
		var Units = $("#Units").val();
		var decline_i = $("#Decline").val();
		var dec_terminal = $("#Terminal").val();
		var start_dt = $("#start_dt").val();
		var table_string ="<table><tr><td>Phase:</td><td>Qi:</td><td>Units:</td><td>Di:</td><td>Term:</td><td>Start Date:</td></tr><tr><td>" + Phase + "</td><td>" + Qi + "</td><td>" + Units + "</td><td>" + decline_i + "</td><td>" + dec_terminal + "</td><td>" + start_dt + "</td></tr></table>"
		$("#output").append(table_string)

		
	});		
	
*/
	
	var curve = {
		segment: {}, /* object to hold the calculation data for each segment */
		forecast_oil: {}, // object to hold the result of build_segment for oil only
		forecast_gas: {}, // same as above for gas
		forecast_ngl: {}, // ngl
		forecast_water: {}, // water
		history_oil: {}, // historical data for oil ajax query of database
		history_gas: {}, // gas
		history_ngl: {}, // likely blank
		history_water: {}, // water
		
		
		// takes segement data and adds it to the forecast for the specified phase

		build_segment: function(Phase, Qi, start_dt, b_factor, decline_i, dec_term, term) {
		//test
		//console.log(Phase);
		//necessary variables
		days_per_month = 30.4;
		rate_initial = parseFloat(Qi);  //required data for formula
		rate = parseFloat(Qi);		//while loop counter for now
		date = new Date(start_dt.split("-")[0],start_dt.split("-")[1]-1,start_dt.split("-")[2]);
		b_fac = parseFloat(b_factor);
		//console.log("b-fac=" + b_fac);
		decline_initial = parseFloat(decline_i)/100;
		//console.log(decline_initial);
		nom_decline_numerator = (Math.pow((1 - decline_initial), (-1 * b_fac)) - 1);
		//console.log(nom_decline_numerator);
		nom_decline = nom_decline_numerator / b_fac;
		//console.log(nom_decline);
		month = 0;
	
		if (Phase === "Oil"){
			while (rate > parseFloat(term)) {
				curve.forecast_oil[date] = rate * days_per_month;
				month += 1;
				date.setMonth(date.getMonth() + 1);
				rate = rate_initial / Math.pow(1 + b_fac * (month / 12) * nom_decline, (1/b_fac));
				//console.log(rate);
			}


		}
		else {
			console.log("Feature not implemented yet!");
		} //eventually same loop for other phases		
	
	
	}
	};

	$("#calc").click(function () {
		$(":input").each(function(){
			curve.segment[$(this).attr("id")] = $(this).val();
		
		});
		for (propt in curve.segment) {
			console.log(propt + ": " + curve.segment[propt]);
		}
		//console.log(curve.segment.Phase)
		curve.build_segment(curve.segment.Phase, curve.segment.qi, curve.segment.start_dt, curve.segment.b_factor, curve.segment.Decline, curve.segment.Terminal, 10);
		for (month in curve.forecast_oil) {
			console.log(month + " : " + curve.forecast_oil[month]);
		}
	});

});
