$(function() {
    $('.buy_btn').live('click',function(){
        var product_id = $(this).attr('name')
        var parent_blk = $(this).parents('.product')

        if (product_id){
            $.ajax({
                type:'post',
                url:'/cart/add_product_to_cart/',
                data:{
                    'product_id':product_id
                },
                success:function(data){
                    $('.img_fly').remove();
                    create_img_fly(parent_blk.find('.product_img'));

                    $('.cartbox').replaceWith(data);

                    var fly = $('.img_fly');
                    var left_end = $('.cartbox').offset().left;
                    var top_end = $('.cartbox').offset().top;

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

    });

    $('.cart_qty_btn').live('click',function(){
        $('.cart_qty_btn').attr('disabled', true);
        $(this).attr('disabled', false);
        $(this).parents('.cart_qty').find('.cart_qty_modal').show();
        $(this).parents('.cart_qty').find('.cart_qty_modal').find('.cart_qty_modal_ok').attr('disabled', false);
        $('.cart_submit_btn').attr('disabled', true);
        $('.cart_back').attr('disabled', true);
        $('.delete_cart_id').attr('disabled', true);
    });

    $('.cart_qty_modal_text').live('keypress',function(e){
        if(e.which == 13)
            $('.cart_qty_modal_ok').trigger("click");
        else
        if( e.which!=8 && e.which!=0 && (e.which<48 || e.which>57))
        {
            alert("Только цифры");
            return false;
        }
    });

    //Подсчёт стоимости
    $('.cart_qty_modal_text').live('keyup',function(){
        var el = $(this)
        var count = el.val();
        if (count){
            count = parseInt(count);
            if (count==0){
                $('.cart_qty_modal_text').val('1');
                count = 1;
            }
            if (count > 999){
                $('.cart_qty_modal_text').val('999');
                count = 999;
            }

            var product_price = el.parent().find('.cart_qty_price span').html();

            product_price = parseFloat(product_price);
            var sum = product_price*count;
            if ((sum % 1)==0){
                sum = sum.toFixed(0);
            }
            else{
                sum = sum.toFixed(2);
            }
            el.parent().find('.cart_qty_total_price span').text(sum);
        }
    });

        //Кнопка Созранить в изменении количества в корзине
    $('.cart_qty_modal_ok').live('click', function(){
        var el = $(this);
        var parent = el.parents('.cart_qty_modal');
        var cart_item = el.parents('.cart_item');
        var initial_count = parent.find('.initial_count').val();
        var new_count = parent.find('.cart_qty_modal_text').val();
        var cart_product_id = parent.find('.cart_qty_item_id').val();

        if (new_count && cart_product_id && initial_count){
            if (new_count != initial_count){
                $.ajax({
                    type:'post',
                    url:'/cart/change_cart_product_count/',
                    data:{
                        'cart_product_id':cart_product_id,
                        'new_count':new_count
                    },
                    success:function(data){
                        data = eval('(' + data + ')');
                        cart_item.find('.cart_price>.item_price').html(data.tr_str_total+' <i>руб.</i>');
                        cart_item.find('.cart_qty_btn').html(new_count);
                        parent.find('.initial_count').val(new_count);
                        parent.find('.cart_qty_modal_text').val(new_count);
                        parent.find('.cart_qty_total_price span').text(data.tr_str_total);
                        $('.cart_summary .cart_total span').html(data.cart_str_total);
                        if (data.cart_str_total=='0')
                            {$('.cart_submit_btn').attr('disabled', true);}
                        else
                            {$('.cart_submit_btn').attr('disabled', false);}
                        $('.cart_qty_btn').attr('disabled', false);
                        $('.cart_back').attr('disabled', false);
                        parent.hide();
                        getCartboxHtml();
                    },
                    error:function(data){
                        $('.cart_submit_btn').attr('disabled', false);
                        $('.cart_qty_btn').attr('disabled', false);
                        $('.cart_back').attr('disabled', false);
                    }
                });
            } else {
                $('.cart_submit_btn').attr('disabled', false);
                $('.cart_qty_btn').attr('disabled', false);
                $('.cart_back').attr('disabled', false);
                parent.hide();
            }

        }
        $('.cart_submit_btn').attr('disabled', false);
        return false;

    });

    $('.cart_close').live('click', function(){
        var el = $(this)
        var parent = el.parents('.cart_qty_modal')
        parent.hide();
        parent.find('.cart_qty_modal_ok').attr('disabled', true);
        $('.cart_submit_btn').attr('disabled', false);
        $('.cart_qty_btn').attr('disabled', false);
        $('.delete_cart_id').attr('disabled', false);
        $('.cart_back').attr('disabled', false);
    });

    $('.delete_cart_id').live('click', function(){
        var el = $(this);
        var cart_product_id = el.attr('name');
        var parent = el.parents('.cart_item');
        if (cart_product_id){
            $.ajax({
                type:'post',
                url:'/cart/delete_product_from_cart/',
                data:{
                    'cart_product_id':cart_product_id
                },
                success:function(data){
                    data = eval('(' + data + ')');
                    $('.cart_summary .cart_total span').html(data.cart_total);
                    if (data.cart_total=='0')
                        {$('.cart_submit_btn').attr('disabled', true);}
                    else
                        {$('.cart_submit_btn').attr('disabled', false);}
                    parent.append('<div class="cart_item_deleted"><div class="btn2"><div class="btn2_in"><a class="cart_back" name="'+data.cart_product_id+'" href="#">Вернуть</a></div></div></div>')
                    getCartboxHtml();
                },
                error:function(data){
                }
            });
        }
        return false;
    });

    $('.cart_back').live('click', function(){
        var el = $(this);
        var cart_product_id = el.attr('name');
        var parent = el.parents('.cart_item');
        if (cart_product_id){
            $.ajax({
                type:'post',
                url:'/cart/restore_product_to_cart/',
                data:{
                    'cart_product_id':cart_product_id
                },
                success:function(data){
                    data = eval('(' + data + ')');
                    $('.cart_summary .cart_total span').html(data.cart_total);
                    if (data.cart_total=='0')
                        {$('.cart_submit_btn').attr('disabled', true);}
                    else
                        {$('.cart_submit_btn').attr('disabled', false);}
                    parent.find('.cart_item_deleted').remove();
                    getCartboxHtml();
                },
                error:function(data){
                }
            });
        }
        return false;
    });
});