$(function(){
   $("#send").on("click", function(event){
     $("#send").prop("disabled", true);
     const query = $("#main").val();
     $("#message").append('通信中です');
     $.ajax({
       type: "POST",
       url: '{% url "youtube:ajax_search" %}',
       data: { "query" : query },
       dataType : "json"
     }).done(function(data){
       $(".contents").empty();
       $("#message").empty();
       $("#send").prop("disabled", false);
       const d = JSON.parse(data);
       for (let i = 0; i < d.length; i++) {
           $("#return").append("<div class=\"item\"><img src=\"" + d[i].thumbnail_url + "\" class=\"img\" id=\"" + d[i].video_id + "\"/><p>" + d[i].title + "</p></div>");
       }

     }).fail(function(XMLHttpRequest, status, e){
       alert(e);
     });
   });
 });


$(function(){
 $("body").on("click", ".img", function(event) {
   const item_id = $(this).attr("id");
    //(".item").prop("disabled", true);
   $.ajax({
       type: "POST",
       url: '{% url "youtube:ajax_stream" %}',
       data:{ "id" : item_id },
       dataType : "json"
     }).done(function(data){
       const d = JSON.parse(data);
       $("#stream").empty();
       //$(".item").prop("disabled", false);
       if (d.error == null){
          $("#stream").append("<video src=\"" + d.stream_url + "\" controls autolay muted playsinline style=\"width: 56vw;\"></video><p><a href=\"" + d.stream_url + "\" download=\"example\">ダウンロード</a></p>");
       }else{
          $("#stream").append(d.error);
       }
     }).fail(function(XMLHttpRequest, status, e){
       alert(e);
     });
   });
  });

  $.ajax({
     success : function(response){
         alert('成功');
     },
     error: function(){
         //通信失敗時の処
         alert('通信失敗');
     }
 });