

$(document).ready(function(){

	var value = 0

	$("nav #id_images-1-photo").hide("fast");
	$("nav #id_images-2-photo").hide("fast");
	$("b #id_images-3-photo").hide("fast");
	$("b #id_images-4-photo").hide("fast");
	$("b #id_images-5-photo").hide("fast");
$("#add").click(function(){
	if(value ==2){
		alert("Вы не можете добавлять более трех фото")
		return false
	};
		value++
		$("#id_images-"+value+"-photo").show("slow");

});
$("#del").click(function(){
	if (value == 0){
		alert("Вы должны опублитковать хотя бы одну фотографию")
		return false
	}

		$("#id_images-"+value+"-photo").hide("slow");
			value--
		});
});
	