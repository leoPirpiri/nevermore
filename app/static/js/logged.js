$(document).ready(function() {
	$('#topo').click(function(){
		$('html, body').animate({scrollTop:0}, 'slow');
		return false;
	});
	$('#user_config').click(function(){
	    $('#user_bio').prop("disabled", false);
	    $('#user_bio').focus();
	});
	$('#user_bio').keydown(function(event) {
        if (event.keyCode == 13 && !event.shiftKey) {
            var content = this.value.trim()
            if (content!=''){
                if (confirm("Deseja atualizar o texto de sua biografia? :)")){
                    $.post("/atualizarbio", {
                        biografia: content
                    }, function(msg){
                        if(msg != undefined){
                            $('#user_bio').prop("disabled", true);
                        }
                    })

                }
            }
        }else if(event.keyCode == 27){
            $('#user_bio').prop("disabled", true);
        }
    });
	$('.btn_rm').click(function(){
        id_post=this.value
        if (confirm("Deseja mesmo excluir essa postagem? :(")){
            $.post("/desopinar", {
                post: id_post
            }, function(msg){
                if(msg != undefined){
                    $('#post_div'+id_post).hide()
                }
            })
        }
	});
	$('.btn_rm_com').click(function(){
        id_post=this.value
        if (confirm("Deseja mesmo excluir seu comentario? :(")){
            $.post("/descomentar", {
                post: id_post
            }, function(msg){
                if(msg != undefined){
                    $('#com_div'+id_post).fadeOut()
                }
            })
        }
	});
	$('.ctpost').keydown(function(event) {
        if (event.keyCode == 13 && !event.shiftKey) {
            var content = this.value.trim()
            var post_id = this.id
            if (content!=''){
                console.log(content)
                $.post("/comentar", {
                    texto: content,
                    tipo: 'COMMENT',
                    post: post_id
                }, function(msg){
                    $("<div class='comentario row my-1 py-1'>"+
                        "<div class='pic-thumbnail col-2'>"+
                            "<img class='img-fluid' src='/static/images_app/default-user.png' alt='Foto do usuário'>"+
                        "</div><div class='col-10' align='left'><p class='my-0' title='Comentou às "+msg.data_post+"'><a style='font-weight: bold' href='/perfil/"+
                        msg.dono+"'>@"+$('#user').val()+": </a> "+
                        content+"</p></div>"+
                        "</div>")
                        .appendTo('#comentarios'+post_id);
                })
            }
            $('#'+post_id).val('');
        }
    });
});