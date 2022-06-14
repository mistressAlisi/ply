class smart_select {
    _selectize(e,o) {
        e.removeClass(this.settings.input_class);
        this.input_sel = e.selectize(o);
    }

    constructor(e,settings) {
       this.settings =  {
       input_class: 'form-select',
       create: true,
       maxItems: null,
       valueField: 'h',
       searchField: 'n',
       labelField:'n',
       query_url: '/keywords/api/get/',
       f_option_render: function(item, escape) {
                    return '<div>' +
                    '<span class="title">' +
                    '<span class="name"><strong>'+ escape(item.n) +'</strong><em> ('+escape(item.h)+')</em></span>' +
                    '</span>'+
					'<p class="meta">' +
                    '<span class="items"><i class="fas fa-sitemap"></i> Items: ' + escape(item.i) + ' </span>' +
					'<span class="spankes"><i class="fas fa-heart"></i> Likes:' + escape(item.l) + ' </span>' +
					'<span class="watchers"><i class="fas fa-share-alt"></i> Shares:' + escape(item.s) + ' </span>' +
					'<span class="forks"><i class="far fa-comments"></i> Comments:' + escape(item.c) + ' </span>' +
					'</p>' +
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
        console.warn(this.settings);
        this.ie = $(e);
        this.ies = $(e).selectize({
            'create':this.settings.create,
            'maxItems':this.settings.maxItems,
            'valueField':this.settings.valueField,
            'labelField':this.settings.labelField,
            'searchField':this.settings.searchField,
            'options':[],
            render: {
                option: this.settings.f_option_render,
            },
            score: this.settings.f_option_score,
            load: this.settings.f_option_load,
            onload: this.settings.f_onLoad
        });


    }
};



