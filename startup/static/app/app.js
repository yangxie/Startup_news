function loadJavascript(filename){
    var fileref=document.createElement('script')
    fileref.setAttribute("type","text/javascript")
    fileref.setAttribute("src", filename)
}

var loadTemplateFast = function(name) {
    loadTemplate("static/templates/"+ name +".html", name);    
    loadTemplate("../templates/"+ name +".html", name);
}

loadTemplateFast("menu");
loadTemplateFast("events");
loadTemplateFast("eventadmin");
loadTemplateFast("pagination");
loadTemplateFast("event_filter");
loadTemplateFast("login");

App = Ember.Application.create();

//App.LSAdapter = DS.LSAdapter.extend({
//    namespace : 'event_emberjs'
//});
//App.ApplicationAdapter = App.LSAdapter;

App.ApplicationAdapter = DS.DjangoRESTAdapter.extend({
})

App.Router.map(function() {
    this.resource('menu', {path: '/'}, function() {
	this.resource('events', {path: '/events'}, function() {
	    this.route('page', {path: '/page/:page_id'}); 
	});
	this.resource('eventadmin', {path: '/eventadmin'}, function() {
	});
    });
});

App.IndexRoute = Ember.Route.extend({
  model: function() {
    return ['red', 'yellow', 'blue'];
  }
});
