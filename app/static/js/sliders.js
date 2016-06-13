$(function(){
  $( "#SRM" ).slider({
    value: 50,
    min: 0,
    max: 100,
    orientation: "horizontal",
    range: "min",
    animate: true,
    slide: function (event, ui) {
          $("#vSRM").val(ui.value);
          $(ui.value).val( $('#vSRM').val() );
      }
  });
  $("#vSRM").change(function () {
    $("#SRM").slider("value", $(this).val() );
  });

  $( "#IBU" ).slider({
    value: 50,
    min: 0,
    max: 100,
    orientation: "horizontal",
    range: "min",
    animate: true,
    slide: function (event, ui) {
        $("#vIBU").val(ui.value);
        $(ui.value).val( $('#vIBU').val() );
      }
  });
  $("#vIBU").change(function () {
    $("#IBU").slider("value", $(this).val() );
  });


  $( "#SWE" ).slider({
    value: 50,
    min: 0,
    max: 100,
    orientation: "horizontal",
    range: "min",
    animate: true,
    slide: function (event, ui) {
      $("#vSWE").val(ui.value);
      $(ui.value).val( $('#vSWE').val() );
    }
  });
  $("#vSWE").change(function () {
      $("#SWE").slider("value", $(this).val() );
  });

  $( "#STR" ).slider({
    value: 50,
    min: 0,
    max: 100,
    orientation: "horizontal",
    range: "min",
    animate: true,
    slide: function (event, ui) {
      $("#vSTR").val(ui.value);
      $(ui.value).val( $('#vSTR').val() );
    }
  });
  $("#vSTR").change(function () {
      $("#STR").slider("value", $(this).val() );
  });

  $( "#MOU" ).slider({
    value: 50,
    min: 0,
    max: 100,
    orientation: "horizontal",
    range: "min",
    animate: true,
    slide: function (event, ui) {
      $("#vMOU").val(ui.value);
      $(ui.value).val( $('#vMOU').val() );
    }
  });
  $("#vMOU").change(function () {
      $("#MOU").slider("value", $(this).val() );
  });

  $( "#HON" ).slider({
    value: 50,
    min: 0,
    max: 100,
    orientation: "horizontal",
    range: "min",
    animate: true,
    slide: function (event, ui) {
      $("#vHON").val(ui.value);
      $(ui.value).val( $('#vHON').val() );
    }
  });
  $("#vHON").change(function () {
      $("#HON").slider("value", $(this).val() );
  });
});
