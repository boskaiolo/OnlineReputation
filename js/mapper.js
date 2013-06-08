var data={};

function mapper() {
	var	company = '',
		options = {},
		chart = '',
		preppedData = {};
	
	google.load("visualization", "1", {"packages": ["geochart"]});
	
	//load, prep stuff
	$('document').ready(function () {
		$('#company')
			.select2({minimumResultsForSearch: 10, width: '150px'})
			.change(main)
		
		chart = new google.visualization.GeoChart(document.getElementById("chart_div"));
		main()
	})	
	
	function main() {		
		company = $('#company').select2('val');
		
		if (company in preppedData) chart.draw(preppedData[company], options)
		else if (location.protocol == "file:") { //offline version is being used		
			//using jQuery to attach script does not work reliably 
			//$('body').append("<script type='text/javascript' src='jdb/"+ iso3 +".js'></script>")			
		
			var script   = document.createElement("script");
			script.type  = "text/javascript";
			script.src   = "data/"+company+".js"; //?_="+ (new Date());
			document.body.appendChild(script),
			i=0;
			
			//this function simulates async requests
			var intervalId = setInterval( function () { 
				if (company in data || i>10) { //console.log(data)
					clearInterval(intervalId);					
					preppedData[company] = google.visualization.arrayToDataTable(data[company]) //transform data format
					chart.draw(preppedData[company], options)
				}
				
				i++;
			}, 100)
		}
		//else no option for ajax right now, don't do anything
	}
	
	main.options = function (obj) {
		if (!arguments.length) return options;
		options = obj;
		return main;
	}
	
	return main;
}

