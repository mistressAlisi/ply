$(".gallery-card").on('click',function(e){
   gallery_core.launch_gallery(e); 
   e.preventDefault();
});
gallery_core.launch_gallery();
