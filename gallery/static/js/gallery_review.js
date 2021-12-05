gallery_core.loadPlugin('gallery_photos');
$(".gallery-card").on('click',function(e){
   gallery_core.launch_publisher(e); 
   e.preventDefault();
});
