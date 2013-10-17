
function checkCookie() {
    if (navigator.cookieEnabled) {
    } else {
	alert('You should enable your cookie.');
    }
}


function loadJavascript(filename){
    var fileref=document.createElement('script')
    fileref.setAttribute("type","text/javascript")
    fileref.setAttribute("src", filename)
    document.body.appendChild(fileref);
}

var modules = ["menu",
	   "events",
	   "eventadmin",
	   "pagination",
	   "event_filter",
	   "login"];

function loadModules(modules, module_id, callback) {
    if (module_id == modules.length) {
	callback();
	return;
    }
    var name = modules[module_id]
    loadTemplate("static/templates/"+ name +".html", name,
		 loadModules(modules, module_id + 1, callback));

    //    loadTemplate("../templates/"+ name +".html", name);
}

var withModules = function(modules, initFn) {
    loadModules(modules, 0, initFn);
};

function a() {
    loadJavascript("static/app/models/event.js");
    loadJavascript("static/app/models/menu.js");
    loadJavascript("static/app/controllers/pagination_mixin.js");
    loadJavascript("static/app/controllers/event_controller.js");
    loadJavascript("static/app/controllers/events_controller.js");
    loadJavascript("static/app/controllers/eventadmin_controller.js");
    loadJavascript("static/app/controllers/menu_controller.js");
    loadJavascript("static/app/controllers/menu_item_controller.js");
    loadJavascript("static/app/controllers/login_controller.js");
    loadJavascript("static/app/views/pagination_view.js");
    loadJavascript("static/app/views/login_view.js");
    loadJavascript("static/app/routes/events_route.js");
    loadJavascript("static/app/routes/menu_route.js");
    loadJavascript("static/app/routes/events_page_route.js");
    loadJavascript("static/app/routes/event_filter_route.js");
}

function loadEmberTemplate(template_name) {
    console.log("test");
    var source = $("#" + template_name);
    var compiledTemplate = Ember.Handlebars.compile(source.html());
    console.log(source.html());
    Ember.TEMPLATES[name] = compiledTemplate;
    console.log(compiledTemplate);
}

var initFn = function() {
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
};

//withModules(modules, initFn);
//console.log(Handlebars.templates);

loadEmberTemplate("events");
loadEmberTemplate("menu");
loadEmberTemplate("pagination");
loadEmberTemplate("eventadmin");
loadEmberTemplate("login");
//console.log(document.getElementById("menu").innerHTML);
//Ember.TEMPLATES["events"] = Handlebars.templates["events"];
//Ember.TEMPLATES["menu"] = Handlebars.templates["menu"];
//Ember.TEMPLATES["eventadmin"] = Handlebars.templates["eventadmin"];
//a();
//initFn();
checkCookie();

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
