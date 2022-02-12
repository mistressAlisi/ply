$(".gallery-card").on('click',function(e){
   gallery_core.launch_gallery_card(e); 
   e.preventDefault();
});
gallery_core.launch_gallery_init();
