$(function(){

    var $container = $('.interers');
   	$container.imagesLoaded( function(){
   		$container.masonry({
   	    	itemSelector : '.interer',
   	    	columnWidth: 195
   		});
   	});

// каталог и товар

    $('a.add_favor').live('click',function(){
        var el = $(this);
        $.ajax({
            type:'post',
            url:'/cabinet/add_product_to_favorite/',
            data:{
                'product_id':el.attr('name')
            },
            success:function(data){
                data = data.split('|');
                $('.fav_count').html(data[0]);
                el.toggleClass('is_favor');
                if (el.parents('.favor').html()){
                    el.parents('.favor').hide('fast',function(){
                        el.parents('.favor').remove();
                    });
                    $('.cart_cnt').html(data[1]);
                }
                if (el.parents('.item_page').html()){
                    $('.add_favor').not(el).toggleClass('is_favor');
                }
            },
            error:function(data){}
        });
        return false;
    });

    $('.add_favor_alter').live('click',function(){
        var el = $(this);
        $.ajax({
            type:'post',
            url:'/cabinet/add_product_to_favorite/',
            data:{
                'product_id':el.attr('name')
            },
            success:function(data){
                data = data.split('|');
                $('.add_favor').toggleClass('is_favor');
                $('.fav_count').html(data[0]);
            },
            error:function(data){}
        });
        return false;
    });

    $('.item_pics a').live('click',function(){
        var el = $(this);
        var parent = el.parent();
        parent.find('a').removeClass('current');
        el.addClass('current');

        var new_image = $('img[alt="'+el.attr('name')+'"]');
        $('.big_pic img').hide();
        new_image.show();
        return false;
    });

    $('.rating_input span').live('click',function(){
        var el = $(this);
        var parent = el.parent();
        var value = parseInt(el.attr('title'));
        $('#id_rating').val(value);
        $('.rating_input span').each(function(num, el) {
            var el_val = parseInt($(el).attr('title'));
            if (el_val<=value){
                $(el).addClass('rating_all');
                $(el).removeClass('rating_non');
            } else {
                $(el).removeClass('rating_all');
                $(el).addClass('rating_non');
            }
        });
    });

    $('#send_comment').live('click',function(){
        $.ajax({
            url: "/catalog/product/"+$('#product_id').val()+"/add_comment/",
            data: {
                product:$('#id_product').val(),
                name:$('#id_name').val(),
                text:$('#id_text').val(),
                rating:$('#id_rating').val()
            },
            type: "POST",
            success: function(data) {
                if (data=='success'){
                    $.fancybox.close();
                    ShowSysMessage('Отзыв успешно добавлен. Он появится после проверки модератором.', 8000);
                } else {
                    $('.comment_form').replaceWith(data);
                }
            }
        });

        return false;
    });

    $('.catalog_ajax_load').live('click',function(){
        var parent = $('.catalog');
        $.ajax({
            url: window.location.pathname+"load_items/",
            data: {
                start_count: $(this).attr('name')
            },
            type: "POST",
            success: function(data) {
                parent.append(data);
                parent.find('.loaded:eq(0)').fadeIn("fast", function (){ //появление по очереди
                    $(this).next().fadeIn("fast", arguments.callee);
                });
                parent.find('div.item').removeClass('loaded');
                $('.items_load_out').hide('slow',function(){
                    $(this).remove();
                });
            }
        });
        return false;
    });

    $('.interer_ajax_load').live('click',function(){
        var next_page_num = parseInt($(this).attr('name'));
        $.ajax({
            url: '/',
            data: {
                page: ++next_page_num
            },
            type: "GET",
            success: function(data) {
                var $loaded_interers = $(data);
                $container.append( $loaded_interers ).masonry( 'appended', $loaded_interers );
                $container.find('.loaded:eq(0)').fadeIn("fast", function (){ //появление по очереди
                    $(this).next().fadeIn("fast", arguments.callee);
                });
                $container.find('div.interer').removeClass('loaded');
                $('.items_load_out').not('.new_items_load_out').replaceWith($('.new_items_load_out'));
                $('.items_load_out').removeClass('new_items_load_out');
                if ($('.remaining_count').val()=='0'){
                    $('.items_load_out').fadeOut('slow',function(){
                        $(this).remove();
                    });
                }
            }
        });
        return false;
    });



// корзина

    //Анимация корзины при изменении
    function animate_cart(){

        $('.blk_order').animate({
                opacity: 0.25
            }, 200, function() {
                $(this).animate({
                    opacity: 1
                },200);
            }
        );

    }

    function create_img_fly(el)
    {
        var img = el.html();
        var offset = el.find('img').offset();
        element = "<div class='img_fly'>"+img+"</div>";
        $('body').append(element);
        $('.img_fly').css({
            'position': "absolute",
            'z-index': "1000",
            'left': offset.left,
            'top': offset.top
        });

    }

    $('.add_to_cart').live('click',function(){
        var product_id = $(this).attr('name');
        var parent_blk = $(this).parents('.item_ajax');

        if (product_id){
            $.ajax({
                type:'post',
                url:'/cart/add_product_to_cart/',
                data:{
                    'product_id':product_id
                },
                success:function(data){
                    $('.img_fly').remove();
                    create_img_fly(parent_blk.find('.item_img_fly_block'));

                    $('.blk_order').replaceWith(data);

                    var fly = $('.img_fly');
                    var left_end = $('.blk_order').offset().left;
                    var top_end = $('.blk_order').offset().top;

                    fly.animate(
                        {
                            left: left_end,
                            top: top_end
                        },
                        {
                            queue: false,
                            duration: 600,
                            easing: "swing"
                        }
                    ).fadeOut(600);

                    setTimeout(function(){
                        animate_cart();
                    } ,600);

                },
                error:function(jqXHR,textStatus,errorThrown){

                }
            });
        }
        return false;
    });

    $('.cart_item_minus').live('click',function(){
        var el = $(this);
        var parent = el.parent();
        var curr_cnt = parseInt(parent.find('.count_val').html());
        if (curr_cnt>1){
            curr_cnt--;
        }
        if (curr_cnt==1){
            el.addClass('nomore');
        }
        if (curr_cnt<100){
            parent.find('.cart_item_plus').removeClass('nomore');
        }
        parent.find('.count_val').html(curr_cnt);
        ResetCartCount();
        ResetProductTotalPrice(parent.parents('.cart_item'));
        return false;
    });

    $('.cart_item_plus').live('click',function(){
        var el = $(this);
        var parent = el.parent();
        var curr_cnt = parseInt(parent.find('.count_val').html());
        if (curr_cnt<100){
            curr_cnt++;
        }
        if (curr_cnt==100){
            el.addClass('nomore');
        }
        if (curr_cnt>1){
            parent.find('.cart_item_minus').removeClass('nomore');
        }
        parent.find('.count_val').html(curr_cnt);
        ResetCartCount();
        ResetProductTotalPrice(parent.parents('.cart_item'));
        return false;
    });

    $('.cart_item_delete').live('click',function(){
        var parent = $(this).parents('.cart_item');
        $.ajax({
            type:'post',
            url:'/cart/delete_product_from_cart/',
            data:{
                'cart_product_id':parent.find('.cart_product_id').val()
            },
            success:function(data){
                $('.total_price_value').html(data);
                parent.hide('fast',function(){
                    parent.remove();
                    ResetCartCount();
                });
            },
            error:function(data){
            }
        });
        return false;
    });

// fancybox5

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

function ResetProductTotalPrice(parent){
    var count = parseInt(parent.find('.count_val').html());
    var price = parseFloat(parent.find('.prod_price').val().replace(',','.'));
    $.ajax({
        type:'post',
        url:'/cart/change_cart_product_count/',
        data:{
            'cart_product_id':parent.find('.cart_product_id').val(),
            'new_count':count
        },
        success:function(data){
            $('.total_price_value').html(data);
        },
        error:function(data){}
    });


    var total = 0;
    total = price * count;
    parent.find('.product_price_value').html(accounting.formatNumber(total, 0, " "));
}

function ResetCartCount(){
    var count = 0;
    $('.count_val').each(function(num, el) {
        count += parseInt($(el).html());
    });
    $('.cart_cnt').html(count+' '+plural_str(count,'товар','товара','товаров'));
    $('.blk_order a').html(count+' '+plural_str(count,'товар','товара','товаров'));
    if (count==0){
        $('.blk_order .blk_title').html('Корзина пока пуста');
        $('.blk_order .blk_lnk').remove();
        $('.cart').hide('fast',function(){
            $('.cart').html('<h1>Корзина пока пуста</h1>');
            $('.cart').show('fast');
        });
    }
}