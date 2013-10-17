/*
 * Loads a handlebars.js template at a given URL. Takes an optional name, 
 * in which case, the template is added and is reference-able via templateName.
 */
function loadTemplate(url, name, callback) {
    var contents = $.get(url, function(templateText) {
	var compiledTemplate = Ember.Handlebars.compile(templateText);
	if (name) {
	    Ember.TEMPLATES[name] = compiledTemplate
	} else {
	    Ember.View.create({ template: compiledTemplate }).append();
	}
	if (callback) {
	    callback();
	}
    });
}
