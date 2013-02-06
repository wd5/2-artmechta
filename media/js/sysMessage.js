function ShowSysMessage(sys_message, duration){
    $.fancybox({
        padding: '30px',
        openEffect : 'elastic',
        closeEffect : 'elastic',
        content: '<div id="sys_message" style="padding: 30px;">'+sys_message+'</div>',
        helpers: {overlay: {css: {'background' : 'rgba(0, 0, 0, 0.45)'}}}
    });
    if (duration) {
        setTimeout(function(){
            $.fancybox.close();
        },duration);
    }
}