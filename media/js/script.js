$(function(){

    var $container = $('.interers');
   	$container.imagesLoaded( function(){
   		$container.masonry({
   	    	itemSelector : '.interer',
   	    	columnWidth: 195
   		});
   	});

// fancybox

    $('.fancybox').fancybox();

    function OpenFancyLoading(){
        $.fancybox.showLoading();
        $.fancybox.helpers.overlay.open({closeClick : false,css: {'background' : 'rgba(0, 0, 0, 0.45)'}});
    }

    function CloseFancyLoading(){
        $.fancybox.hideLoading();
        $.fancybox.helpers.overlay.close();
    }

    $('.fancybox-modal').fancybox({
        padding: '0px',
        scrolling: 'true',
        openEffect : 'elastic',
        closeEffect : 'elastic',
        fitToView: false,
        helpers: {overlay: {css: {'background' : 'rgba(0, 0, 0, 0.45)'}}}
    });

    $('.fancybox-media').fancybox({
        padding:0,
        helpers : {
            media : {}
        }
    });

});

function plural_str(i, str1, str2, str3){
    function plural (a){
            if ( a % 10 == 1 && a % 100 != 11 ) return 0
            else if ( a % 10 >= 2 && a % 10 <= 4 && ( a % 100 < 10 || a % 100 >= 20)) return 1
            else return 2;
        }

    switch (plural(i)) {
        case 0: return str1;
        case 1: return str2;
        default: return str3;
    }
}