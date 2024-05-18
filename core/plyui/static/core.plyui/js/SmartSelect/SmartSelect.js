export class SmartSelect {
    _selectize(e,o) {
        e.removeClass(this.settings.input_class);
        this.input_sel = e.selectize(o);
    }
    addOption(id,title) {

      this.ie[0].selectize.addOption({'id':id,'title':title});
    }
    constructor(e,settings) {
       this.settings =  {
       input_class: 'form-select',
       create: false,
       maxItems: null,
       valueField: 'id',
       searchField: 'title',
       labelField:'title',
       options: [],
       query_url: '/keywords/api/get/',
       f_option_render: function(item, escape) {
                    return '<div>' +
                    '<span class="title">' +
                    '<span class="name"><strong>'+ escape(item.title) +'</strong></span>' +
					'</div>';
                    },
        f_option_search: function(search) {
						var score = this.getScoreFunction(search);
						return function(item) {
							return score(item) * (1 + Math.min(item.i / 100, 1));
						};
					},
        f_option_load: function(query,callback) {
           return callback();
        },

        f_onLoad: function(data) {

        },
        f_option_score: function(search) {
						var score = this.getScoreFunction(search);
						return function(item) {
							return score(item) * (1 + Math.min(item.i / 100, 1));
						};
        }};
        $.extend( this.settings, settings );

        this.ie = $(e);
        this.selectize = $(e).selectize({
            'create':this.settings.create,
            'maxItems':this.settings.maxItems,
            'valueField':this.settings.valueField,
            'labelField':this.settings.labelField,
            'searchField':this.settings.searchField,
            'options':this.settings.options,
            render: {
                option: this.settings.f_option_render,
            },
            score: this.settings.f_option_score,
            load: this.settings.f_option_load,
            onload: this.settings.f_onLoad
        });


    }
};



