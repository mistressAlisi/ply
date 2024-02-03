gallery_core.loadPlugin('gallery_photos');
$(".core-card").on('click',function(e){
   gallery_core.launch_publisher(e); 
   e.preventDefault();
});
