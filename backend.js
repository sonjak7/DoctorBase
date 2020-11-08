// using express module to create express application
var express = require("express");

var app = express();

// set main.handlebars as the default layout
var handlebars = require("express-handlebars").create({defaultLayout:"main"});

// handlebar.engine handles everything with .handlebars extension
app.engine("handlebars", handlebars.engine);
app.set("view engine", "handlebars");

// set the port number for the URL
app.set("port", 7020);

// sets the folder from which static files such as images and css code are used
app.use(express.static('public'));

app.get('/',function(req,res){
  res.render('home');
});

app.get('/delete',function(req,res){
  res.render('delete');
});

app.get('/inquire',function(req,res){
  res.render('inquire');
});

app.get('/inquire_doctors',function(req,res){
  res.render('inquire_doctors');
});

app.get('/inquire_patients',function(req,res){
  res.render('inquire_patients');
});

app.get('/inquire_orders',function(req,res){
  res.render('inquire_orders');
});

app.get('/inquire_results',function(req,res){
  res.render('inquire_results');
});

app.get('/inquire_staff',function(req,res){
  res.render('inquire_staff');
});

app.get('/add',function(req,res){
  res.render('add');
});
app.get('/add_doctors',function(req,res){
  res.render('add_doctors');
});
app.get('/add_patients',function(req,res){
  res.render('add_patients');
});
app.get('/add_orders',function(req,res){
  res.render('add_orders');
});
app.get('/add_staff',function(req,res){
  res.render('add_staff');
});
app.get('/add_results',function(req,res){
  res.render('add_results');
});



app.get('/update',function(req,res){
  res.render('update');
});

app.use(function(req,res){
  res.status(404);
  res.render('404');
});

app.use(function(err, req, res, next){
  console.error(err.stack);
  res.type('plain/text');
  res.status(500);
  res.render('500');
});

app.listen(app.get('port'), function(){
  console.log('Express started on http://localhost:' + app.get('port') + '; press Ctrl-C to terminate.');
});
