define([
    'jquery',
    'underscore',
    'backbone',     
    "text!core/event_template.js"
], function($, _, Backbone, eventTemplate) {
    var EVENT_API = '/api/v1/core/event/';
    window.Event = Backbone.Model.extend({
	url: function(){
	    return this.get('resource_uri') || this.collection.url;
	}
    });

    window.Events = Backbone.Collection.extend({
	baseUrl: EVENT_API,
	initialize: function() {
	    _.bindAll(this, 'parse', 'url', 'nextPage', 'previousPage', 'sort_by', 'hasNextPage', 'hasPreviousPage', 'updatePageInfo');
	    typeof(options) != 'undefined' || (options = {});
	    typeof(this.limit) != 'undefined' || (this.limit = 10);
	    typeof(this.offset) != 'undefined' || (this.offset = 0);
	    typeof(this.filter_options) != 'undefined' || (this.filter_options = {});
	    typeof(this.sort_field) != 'undefined' || (this.sort_field = '')
	},
	url: function() {
	    urlparams = {offset: this.offset, limit: this.limit, format: 'json'};
	    urlparams = $.extend(urlparams, this.filter_options);
	    if (this.sort_field) {
		urlparams = $.extend(urlparams, {sort_by: this.sort_field});
	    }
	    console.log(this.baseUrl + '?' + $.param(urlparams));
	    return this.baseUrl + '?' + $.param(urlparams);
	},
	hasNextPage: function() {
	    return this.offset + this.limit < this.total;
	},
	hasPreviousPage: function() {
	    return this.offset - this.limit >= 0;
	},
	updatePageInfo: function() {
	    this.range = [this.offset + 1, Math.min(this.offset + this.limit, this.total)];
	    this.prev = this.hasPreviousPage();
	    this.next = this.hasNextPage();
	},
	nextPage: function() {
	    if (!this.hasNextPage()) {
		return false;
	    }
	    this.offset = this.offset + this.limit;
	    this.updatePageInfo();
	    return this.fetch();
	},
	previousPage: function() {
	    if (!this.hasPreviousPage()) {
		return false;
	    }
	    this.offset = this.offset - this.limit;
	    this.updatePageInfo();
	    return this.fetch();
	},
	filterByToday: function() {
	    this.offest = 0;
	    var today = new Date();
	    today = today.getFullYear() + "-" + (today.getMonth()  + 1)+ "-" + today.getDate();
	    this.filter_options = {};
	    this.filter_options['start_date'] = today;
	    this.updatePageInfo();
	    return this.fetch();
	},
	filterByThisWeek: function() {
	    this.offest = 0;
	    if (Date.today().is().sunday()) {
		var weekBegin = Date.today();
		var weekEnd = Date.today().next().sunday();
	    } else {
		var weekBegin = Date.today().previous().sunday();
		var weekEnd = Date.today().next().sunday();
	    }
	    this.filter_options = {};
	    this.filter_options['start_date__gte'] = weekBegin.toString("yyyy-MM-dd");
	    this.filter_options['start_date__lte'] = weekEnd.toString("yyyy-MM-dd");
	    this.updatePageInfo();
	    return this.fetch();
	},
	filterByNextWeek: function() {
	    this.offest = 0;
	    var weekBegin = Date.today().next().sunday();
	    var weekEnd = Date.today().next().sunday().next().sunday();
	    this.filter_options = {};
	    this.filter_options['start_date__gte'] = weekBegin.toString("yyyy-MM-dd");
	    this.filter_options['start_date__lte'] = weekEnd.toString("yyyy-MM-dd");
	    this.updatePageInfo();
	    return this.fetch();
	},
	filterByLocation: function(location) {
	    this.offset = 0;
	    this.filter_options = {};
	    this.filter_options['city'] = location;
	    this.updatePageInfo();
	    return this.fetch();
	},
	filterByCategory: function(category) {
	    this.offset = 0;
	    this.filter_options = {};
	    this.filter_options['category'] = category;
	    this.updatePageInfo();
	    return this.fetch();
	},
	parse: function(response){
	    //		    this.offset = response.meta.offset;
	    //		    this.limit = response.meta.limit;
	    this.total = response.meta.total_count;
	    this.pages = Math.ceil(this.total / this.limit);
	    this.updatePageInfo();
	    return response.objects;
	},
	sort_by: function (field) {
	    this.sort_field = field;
	    this.offset = 0;
	    return this.fetch();
	}
    });
    
    EventView = Backbone.View.extend({
	initialize: function(model){
	    this.model = model;
	    this.render();
	},
	render: function(){
	    // Compile the template using underscore
	    var template = _.template(eventTemplate, this.model);
	    // Load the compiled HTML into the Backbone "el"
	    this.$el.html( template );
	    return this;
	}
    });

    window.EventApp = Backbone.View.extend({
	el: $('#container_body'),
	events : {
	    'click a.prev': 'previous',
	    'click a.next': 'next',
	    'click a.filter_by_today': 'filterByToday',
	    'click a.filter_by_this_week': 'filterByThisWeek',
	    'click a.filter_by_next_week': 'filterByNextWeek',
	},
	initialize: function(){
	    var container = document.createDocumentFragment();
	    _.bindAll(this, 'previous', 'next', 'render', 'refresh', 'filterByToday', 'filterByThisWeek', 'filterByNextWeek');
	    var eventList = new Events();
	    this.collection = eventList;
	    eventList.bind('fetch', this.render);
	    $.when(eventList.fetch()).done(function(model) {
		_.each(model.objects, function(object) {
		    var event_view = new EventView(object);
		    $(container).append(event_view.render().el);
		});
		$('#container_events').append(container);
		console.log(eventList);
		var pagination_template = _.template( $("#pagination_template").html(), eventList);
		$('#container_events').append( pagination_template );
	    });
	},
	previous: function() {
	    this.refresh(this.collection.previousPage());
	},
	next: function() {
	    this.refresh(this.collection.nextPage());
	},
	filterByToday: function() {
	    this.refresh(this.collection.filterByToday());
	},
	filterByThisWeek: function() {
	    this.refresh(this.collection.filterByThisWeek());
	},
	filterByNextWeek: function() {
	    this.refresh(this.collection.filterByNextWeek());
	},
	refresh: function(fetchFn) {
	    var collection = this.collection;
	    var container = document.createDocumentFragment();
	    $.when(fetchFn).done(function(model) {
		_.each(model.objects, function(object) {
		    var event_view = new EventView(object);
		    $(container).append(event_view.render().el);
		});
		$('#container_events').html('');
		$('#container_events').append(container);
		var pagination_template = _.template( $("#pagination_template").html(), collection);
		$('#container_events').append( pagination_template );
	    });
	},
	render: function() {
	    alert('');
	}
    });

    window.filter_by_location = function(location) {
	window.app.refresh(window.app.collection.filterByLocation(location));
    }
    window.filter_by_category = function(category) {
	window.app.refresh(window.app.collection.filterByCategory(category));
    }
    $.ajax({
	url: "/all_filter_options/",
    }).done(function ( data ) {
	if( console && console.log ) {
	    console.log(data);
	    for (var i = 0; i < data['locations'].length; ++i)  {
		var location = data['locations'][i];
		var link = $('<a>', {href : '#', onclick: 'window.filter_by_location("' + location + '");', name : location, class : "filter_by_location"}).html(location);
		$('#filter_location').append($('<div>').append(link));
	    }

	    for (var i = 0; i < data['categories'].length; ++i)  {
		var category = data['categories'][i];
		var link = $('<a>', {href : '#', onclick: 'window.filter_by_category("' + category + '");', name : category, class : "filter_by_category"}).html(category);
		$('#filter_category').append($('<div>').append(link));
	    }
	}
    });

    var initialize = function(){
	// Pass in our Router module and call it's initialize function
	window.app = new window.EventApp();
    };

    return { 
	initialize: initialize
    };
});