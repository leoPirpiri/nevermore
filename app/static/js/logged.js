$(document).ready(function() {
	$('#topo').click(function(){
		$('html, body').animate({scrollTop:0}, 'slow');
		return false;
	});
	$('.ctpost').keydown(function(event) {
        if (event.keyCode == 13 && !event.shiftKey) {
            var content = this.value.trim()
            var post_id = this.id
            if (content!=''){
                console.log(content)
                $("<div style='display: none;'>"+content+"</div>").appendTo('#comentarios'+post_id).show("slow")
//                $.post("/teste", {
//                    texto: content,
//                    tipo: 'COMMENT',
//                    post: post_id
//                }, function(msg){
//                    $('#'post_id).val('')
//                    $("<div style='display: none;'>"+content+"</div>").appendTo('#comentarios'+post_id).show()
//                    console.log(msg);
//                })
            }
            $('#'+post_id).val('')
        }
    });
});