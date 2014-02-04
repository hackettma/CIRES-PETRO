$(document).ready(function() {
	
/*	$("#calc").click(function () {
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
		segment: {},
		forecast_oil: {},
		forecast_gas: {},
		forecast_ngl: {},
		forecast_water: {},
		history_oil: {},
		history_gas: {},
		history_ngl: {},
		history_water: {},
		build_segment: function(Phase, Qi, start_dt, decline_i, dec_term, term) {
		console.log(Phase);
		if (Phase === "Oil"){
			rate = parseFloat(Qi);
			while (rate > parseFloat(term)) {
				console.log(rate);
				rate = rate - 1;
			}


		}
		else
		console.log("Feature not implemented yet!")
		
		
		}		
	}

	$("#calc").click(function () {
		$(":input").each(function(){
			curve.segment[$(this).attr("id")] = $(this).val();
		
		});
		
		//console.log(curve.segment.Phase)
		curve.build_segment(curve.segment.Phase, curve.segment.qi, curve.segment.start_dt, curve.segment.Decline, curve.segment.Terminal, 0);
	});

});
