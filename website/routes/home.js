 /**
 * our routes
 * @author Bob Williams <bobwilliams.ii@gmail.com>
 */

var http = require('http');

module.exports = function(app){

	// landing page
	app.get('/', function(req, res){
		// send it all to the page
		res.render('home', {title: 'MBA Stats'});
	});

	// /memory
	app.get('/memory', function(req, res){

		var query = '{"reduce" : [ {"avg-wired" : {"avg": "MEM_WIRED"}} , {"avg-active" : {"avg": "MEM_ACTIVE"}}, {"avg-inactive" : {"avg": "MEM_INACTIVE"}}, {"avg-used" : {"avg": "MEM_USED"}}, {"avg-free" : {"avg": "MEM_FREE"}} ]}';
		// var query = '{"group":[{"duration":"minute"}],"reduce":[{"avg-free":{"avg":"MEM_FREE"}}]}';
		
		var options = {
		    host : config.turbinedb.host,
		    port : config.turbinedb.port,
		    path : config.turbinedb.path + '/memory?q=' + encodeURIComponent(query), 
		    method : 'GET' // do GET
		};

		var req = http.request(options, function(response) {
		    response.on('data', function(chunk) {
		    	var data = JSON.parse(chunk)[0].data[0].data[0];
		    	var retJson = [{"name": "Average Memory Totals", "data": 
		    		[
		    			{"x": 0, "y": data["avg-wired"]}, 
		    			{"x": 1, "y": data["avg-active"]},  
		    			{"x": 2, "y": data["avg-inactive"]},
		    			{"x": 3, "y": data["avg-used"]},
		    			{"x": 4, "y": data["avg-free"]},
	    			]}];
		        res.json(retJson);
		    });		 
		});
		 
		req.end();
		req.on('error', function(e) {
		    console.error(e);
		});
	});

};

