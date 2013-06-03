__author__ = "Alberto Boschetti"
__status__ = "Prototype"

"""

simple way to write the target output html file like this

<html>
  <head>
    <script type='text/javascript' src='https://www.google.com/jsapi'></script>
    <script type='text/javascript'>
     google.load('visualization', '1', {'packages': ['geochart']});
     google.setOnLoadCallback(drawRegionsMap);

      function drawRegionsMap() {
        var data = google.visualization.arrayToDataTable([
          ['Country', 'Popularity'],
          ['Germany', 200],
          ['United States', 300],
          ['Brazil', 400],
          ['Canada', 500],
          ['France', 600],
          ['RU', 700]
        ]);

        var options = {};

        var chart = new google.visualization.GeoChart(document.getElementById('chart_div'));
        chart.draw(data, options);
    };
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: 900px; height: 500px;"></div>
  </body>
</html>
"""


HEADER =    '\
            <html>\
            <head>\
            <script type="text/javascript" src="https://www.google.com/jsapi"></script>\
            <script type="text/javascript">\
            google.load("visualization", "1", {"packages": ["geochart"]});\
            google.setOnLoadCallback(drawRegionsMap);\
            function drawRegionsMap() {\
            var data = google.visualization.arrayToDataTable([\
            '

TRAILER =   '\
            ]);\
            var options = {};\
            var chart = new google.visualization.GeoChart(document.getElementById("chart_div"));\
            chart.draw(data, options);\
            };\
            </script>\
            </head>\
            <body>\
            <div id="chart_div" style="width: 900px; height: 500px;"></div>\
            </body>\
            </html>\
            '

def array_to_html_page(arr, filename):
    arrstring = "['Country', 'Sentiment'],"
    for entry in arr:
        arrstring += "[\'" + entry[0] + "\'," + str(entry[1]) + "],"
        print arrstring

    arrstring = arrstring[:-1]
    print arrstring

    htmlstring = HEADER + arrstring + TRAILER

    fh = open(filename, "w")
    fh.write(htmlstring)
    fh.close()

