//  __  __ ____             _____ _        _       
// |  \/  |  _ \   /\      / ____| |      | |      
// | \  / | |_) | /  \    | (___ | |_ __ _| |_ ___ 
// | |\/| |  _ < / /\ \    \___ \| __/ _` | __/ __|
// | |  | | |_) / ____ \   ____) | || (_| | |_\__ \
// |_|  |_|____/_/    \_\ |_____/ \__\__,_|\__|___/
//                                                 
  
// author : Bob Williams
// url    : bobwilliams.me 


// our config file
GLOBAL.config = require(process.argv[2] || './config.json');

/**
 * Module dependencies.
 */
var express = require('express')
  , http = require('http')
  , path = require('path');

// logging
console.log(( config.logging.silent ? 'Warning: Logging disabled' : 'Logging enabled (' + config.logging.level +')' ) );

var app = express();

app.configure(function(){
  app.set('port', process.env.PORT || 3000);
  app.set('views', __dirname + '/views');
  app.set('view engine', 'ejs');
  app.use(express.favicon());
  app.use(express.logger('dev'));
  app.use(express.bodyParser());
  app.use(express.methodOverride());
  app.use(express.cookieParser('your secret here'));
  app.use(express.session());
  app.use(app.router);
  app.use(require('stylus').middleware(__dirname + '/public'));
  app.use(express.static(path.join(__dirname, 'public')));
});

app.configure('development', function(){
  app.use(express.errorHandler());
});

// routes
require('./routes/home')(app);

http.createServer(app).listen(app.get('port'), function(){
  console.log("Express server listening on port " + app.get('port'));
});