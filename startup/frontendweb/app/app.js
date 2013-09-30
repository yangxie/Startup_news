loadTemplate("../templates/menu.html", "menu");
loadTemplate("../templates/events.html", "events");
loadTemplate("../templates/eventadmin.html", "eventadmin");
loadTemplate("../templates/pagination.html", "pagination");
loadTemplate("../templates/event_filter.html", "event_filter");

loadTemplate("static/templates/menu.html", "menu");
loadTemplate("static/templates/events.html", "events");
loadTemplate("static/templates/eventadmin.html", "eventadmin");
loadTemplate("static/templates/pagination.html", "pagination");
loadTemplate("static/templates/event_filter.html", "event_filter");

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
