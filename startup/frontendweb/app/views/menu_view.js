function getTemplate(path, view){
    $.ajax({
        url: path,
        xhrFields: {
            withCredentials: true
        },
        //cache: true,
        success: function(data, templateName) {
            Ember.TEMPLATES[templateName] = Ember.Handlebars.compile(data);
            if(view != null){
                view.set("templateName", templateName);
                view.rerender();
            }

        }               
    });    
}

App.MenuView = Ember.View.create({
    willInsertElement : function(){
        var isLoaded = this.isLoaded;
	var templateName = "menu";
        if(!isLoaded){
            getTemplate("/static/templates/" + templateName + ".html", this);
        }
    }
});