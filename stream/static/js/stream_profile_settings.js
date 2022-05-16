stream_settings = Object({
    
    settings: {
        bcp1:"#bkg1",
        bcp2:"#bkg2",
        gmc:"#gradient-mp",
        g1c:"#opacity1",
        g2c:"#opacity2",
        gmc:"#midpoint",
        gtc:"#bkgt",
        gac:"#angle",
        mdv: "#streamSettingsModal",
        sfc: "#stream_settings_form",
        set_url: "/stream/api/set/profile/settings"
    },
    rgb2rgba: function(hex,a) {
         if(hex.length == 4){
            r = "0x" + hex[1] + hex[1];
            g = "0x" + hex[2] + hex[2];
            b = "0x" + hex[3] + hex[3];
        
        }else if (hex.length == 7){

            r = "0x" + hex[1] + hex[2];
            g = "0x" + hex[3] + hex[4];
            b = "0x" + hex[5] + hex[6];
        };
        return "rgba("+r*1+","+g*1+","+b*1+","+a+")"
    },
    save: function() {
        set_str = $(this.settings.sfc).serialize();
        $.post(this.settings.set_url,set_str,function(){ });
        $(this.settings.mdv).modal('hide');
    },
    show: function() {
        $(this.settings.mdv).modal('show');
    },
    preview_bkg: function() {
        docBod = $(document.body);
        bkg1 = $(this.settings.bcp1)[0].value;
        bkg2 = $(this.settings.bcp2)[0].value;
        bgt = $(this.settings.gtc)[0].value;
        g1o = $(this.settings.g1c)[0].value;
        g2o = $(this.settings.g2c)[0].value;
        gmp = $(this.settings.gmc)[0].value;
        gha = $(this.settings.gac)[0].value;
        gtv = $(this.settings.gtc)[0].value;
        switch (gtv) {
            case "s1":
                docBod.css('background',bkg1);
            break;   
            case "s2":
                docBod.css('background',bkg2);
            break;   
            case "gl":
                stop = 
                bkgstr = "linear-gradient("+gha+"deg, "+this.rgb2rgba(bkg1,g1o)+" "+gmp+"%, "+this.rgb2rgba(bkg2,g2o)+" 100%)";
//                 console.warn(bkgstr);
                docBod.css('background',bkgstr);
            break;
            case "gr":
                bkgstr = "radial-gradient(circle, "+this.rgb2rgba(bkg1,g1o)+" "+gmp+"%, "+this.rgb2rgba(bkg2,g2o)+" 100%)";
//                 console.warn(bkgstr);
                docBod.css('background',bkgstr);
            break;
        }
        
    }
});


