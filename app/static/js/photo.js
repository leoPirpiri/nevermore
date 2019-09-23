
function foto_upload() {
    const furl = '/foto_perfil_atualizar';
    var formData = new FormData(document.getElementById("form-input-img"));

    $.ajax({
        url: furl,
        type: 'POST',
        data: formData,
        success: function (data) {
            location.reload()
        },
        cache: false,
        contentType: false,
        processData: false
    });
};
$("form#form-input-img").submit(function(e){
    e.preventDefault();
    foto_upload();
});
document.getElementById("foto").onchange = function() {
    foto_upload();
};


