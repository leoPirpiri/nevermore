$(document).ready(function() {
	$('#topo').click(function(){
		$('html, body').animate({scrollTop:0}, 'slow');
		return false;
	});
	$('.btn_rm').click(function(){
        id_post=this.value
        if (confirm("Press a button!")){
            $.post("/desopinar", {
                    post: post_id
                }, function(msg){

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