/*
	Purpose: Map company twitter-based reputation using google viz library
	Author: Edgar Sioson
	Date: 2013-06-08
*/

//var data={};

function mapper() {
	var	params = {},
		company = '',
		options = {},
		chart = '',
		preppedData = {},
		dataAlias = '';
	
	google.load("visualization", "1", {"packages": ["geochart"]});
	
	//load, prep stuff
	$('document').ready(function () {
		$('#company, #joined, #popularity')
			.select2({minimumResultsForSearch: 10, width: '250px'})
			.change(main)
			
		$('#joined, #popularity')
			.select2({minimumResultsForSearch: 10, width: '150px'})
			.change(main)
			
		$('#sexBox').buttonset().click(main);
		
		chart = new google.visualization.GeoChart(document.getElementById("chart_div"));
		main()
	})	
	
	function main() {		
		params.company = $('#company').select2('val');
		params.popularity = $('#popularity').select2('val');
		params.joined = $('#joined').select2('val');
		params.sex = $('input[name=sex]:checked', '#topBar').val()
		dataAlias = params.company+'-'+params.sex+'-'+params.joined+'-'+params.popularity; console.log(dataAlias)
				
		if (dataAlias in preppedData) draw()
		else if (dataAlias in data) { //data has been preloaded as script file 
			preppedData[dataAlias] = google.visualization.arrayToDataTable(data[dataAlias]); //console.log(preppedData[dataAlias])
			draw()
		}
		else if (location.protocol == "file:") { //offline version is being used		
			//using jQuery to attach script does not work reliably 
			//$('body').append("<script type='text/javascript' src='jdb/"+ iso3 +".js'></script>")			
		
			var script   = document.createElement("script");
			script.type  = "text/javascript";
			script.src   = "data/data.js"; 
			document.body.appendChild(script),
			i=0;
			
			//this function simulates async requests
			var intervalId = setInterval( function () {
				if (dataAlias in data || i>10) { //console.log(data);
					clearInterval(intervalId);					
					preppedData[dataAlias] = google.visualization.arrayToDataTable(data[dataAlias]) //transform data format
					draw()
				}
				
				i++;
			}, 100)
		}
		//else no option for ajax right now, don't do anything
	}
	
	function draw() {
		chart.draw(preppedData[dataAlias], options)
		
		//must wait for draw to render chart before looking for legend
		setTimeout(function () {
			var legend = d3.select('svg').selectAll('g').selectAll('g')[1][6]; console.log(legend)
			d3.select(legend).attr('transform','translate(300,0)')
		}, 500)
	}
	
	main.options = function (obj) {
		if (!arguments.length) return options;
		options = obj;
		return main;
	}
	
	return main;
}

