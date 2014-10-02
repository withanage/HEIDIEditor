var http = require('http');
var express = require('express');
var path = require('path');
var CommonJSServer = require("substance-application/commonjs");
var Article = require("lens-article");
var _ = require("underscore");
var fs = require("fs");

var app = express();
var commonJSServer = new CommonJSServer(__dirname);
commonJSServer.boot({alias: "lens", source: "./src/lens.js"});

var port = process.env.PORT || 4001;
app.use(express.cookieParser());
app.use(express.bodyParser());
app.use(express.methodOverride());

app.get("/",
  function(req, res, next) {
    var config = require("./project.json");
    var template = fs.readFileSync(__dirname + "/index.html", 'utf8');
    var scripts = commonJSServer.list();

    var scriptsTags = scripts.map(function(script) {
      return ['<script type="text/javascript" src="/scripts', script, '"></script>'].join('');
    }).join('\n');

    var styleTags = _.map(config.styles, function(path, alias) {
      return ['<link href="', path, '" rel="stylesheet" type="text/css"/>'].join('');
    }).join("\n");

    var result = template.replace('#####scripts#####', scriptsTags);
    result = result.replace('#####styles#####', styleTags);

    res.send(result);
  }
);

app.use('/lib', express.static('lib'));
app.use('/lib/substance', express.static('node_modules'));
app.use('/node_modules', express.static('node_modules'));
app.use('/styles', express.static('styles'));
app.use('/src', express.static('src'));
app.use('/data', express.static('data'));
app.use('/config', express.static('config'));
app.use('/images', express.static('images'));

app.get("/scripts*",
  function(req, res, next) {
    var scriptPath = req.params[0];
    res.type('text/javascript');
    try {
      var script = commonJSServer.getScript(scriptPath);
      res.send(script);
    } catch (err) {
      res.send(err.stack);
    }
  }
);

// Serve Lens in dev mode
// --------

app.use(app.router);

http.createServer(app).listen(port, function(){
  console.log("Lens running on port " + port);
  console.log("http://127.0.0.1:"+port+"/");
});
