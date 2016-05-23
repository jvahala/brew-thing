window.onload = function squiggleApp(){
  // Initialization
  var canvas,
  		context,
  		canvasWidth,
  		canvasHeight,
  		paint = false;

  var colorBlack = "#000000";

  var currColor = colorBlack,
      currSize = 5,
      clickColor = new Array(),
      clickSize = new Array();

  var clickX = new Array(),
      clickY = new Array(),
      clickDrag = new Array(),
      clickLog = new Array(),
      currLog = 0;  

  clickX = []; 
  clickY = [];
  clickDrag = []; 
  clickLog = [0];

  var canvasDiv = document.getElementById('canvasDiv');
  canvas = document.createElement('canvas');
  canvasWidth = canvasDiv.clientWidth;
  canvasHeight = canvasDiv.clientHeight;
  canvas.setAttribute('width', canvasWidth);
  canvas.setAttribute('height', canvasHeight);
  canvas.setAttribute('id', 'canvas');
  if(typeof G_vmlCanvasManager != 'undefined') {
    canvas = G_vmlCanvasManager.initElement(canvas);
  }
  context = canvas.getContext("2d");
  context.lineWidth = currSize;
  canvasDiv.appendChild(canvas);
  // end initialization

  // button and clicking actions - general jquery stuff
  $('#clear-canvas-btn').click(function(e){
    clearCanvas();
    clickX = []; 
    clickY = [];
    clickDrag = []; 
    clickColor = [];
    clickSize = [];
    currLog = 0; 
    clickLog = [0]; 
  });

  $('#undo-btn').click(function(e){
    if (currLog > 0) {
      currLog = Math.max.apply(Math, clickLog.filter(function(x){return x < currLog}));
    }
    redraw(); 
    console.log('after undo click: (clickXlength/currlog/clickLog)', clickX.length,currLog,clickLog);
  });

  $('#redo-btn').click(function(e){
    if (currLog >= clickLog[clickLog.length-1]) {
      currLog = clickX.length; 
    } else {
      currLog = Math.min.apply(Math, clickLog.filter(function(x){return x > currLog})); 
    }
    redraw(); 
    console.log('after redo click: (clickXlength/currlog/clickLog)', clickX.length,currLog,clickLog);

  });

  $('.color-btn').click( function(e){
      var x = $(this).css('backgroundColor');
      hexc(x);
      currColor = color; 
      $('#size-icon').css('backgroundColor','#'+currColor);
  });

  function hexc(colorval) {
      var parts = colorval.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
      delete(parts[0]);
      for (var i = 1; i <= 3; ++i) {
          parts[i] = parseInt(parts[i]).toString(16);
          if (parts[i].length == 1) parts[i] = '0' + parts[i];
      }
      color = '#' + parts.join('');
  }

  $('#slider').css('width',canvasWidth-200);
  $('#slider').css('display','inline-block');
  $('#size-icon').css('display','inline-block');
  $(function() {
    $( '#slider' ).slider({
      value:currSize,
      min: 2,
      max: 30,
      step: 2,
      slide: handleSliderChange
    });
    //$( "#amount" ).val( "$" + $( "#slider" ).slider( "value" ) );
  });

  function handleSliderChange(event,slider) {
    currSize = slider.value; 
    $('#size-icon').css('width', slider.value); 
    $('#size-icon').css('height', slider.value); 
  } 

  // mouse down event
  $('#canvas').mousedown(function(e){
    var mouseX = e.pageX - this.offsetLeft;
    var mouseY = e.pageY - this.offsetTop;
  	
    paint = true;
    if (currLog != clickLog[0]) {
      clickLog = filterInRange(clickLog,0,currLog-1);
    }

      clickX = clickX.slice(0,currLog); 
      clickY = clickY.slice(0,currLog);
      clickColor = clickColor.slice(0,currLog);
      clickSize = clickSize.slice(0,currLog); 
      clickDrag = clickDrag.slice(0,currLog);
    
    if (currLog > 0) {
      clickLog.push(currLog);
    }
    console.log('after mousedown: (x length, currLog, clickLog): ', clickX.length, currLog, clickLog);
    addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop);
    redraw();
  });

  // mouse move event
  $('#canvas').mousemove(function(e){
    if(paint){
      addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
      redraw();
    }
  });

  // mouse up event
  $('#canvas').mouseup(function(e){
    paint = false;
    console.log(clickLog)
  });

  // mouse leave event
  $('#canvas').mouseleave(function(e){
    paint = false;
  });
  // end jquery stuff

  var filterInRange = function(arr, min, max) {
    console.log(arr)
    if (arr.length == 1) return arr; 
    return arr.filter(function(item) {
        return item >= min && item < max;
    });
  }

  // will want to the following: createSquiggle() - random num lines, random curvatures,  

  function addClick(x, y, dragging)
  {
    clickX.push(x);
    clickY.push(y);
    clickDrag.push(dragging);
    clickColor.push(currColor);
    clickSize.push(currSize);
    currLog++;
  }

  // redraw
  function redraw(){
    context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
    context.lineJoin = "round";
    for(var i=0; i < currLog; i++) {		
      context.beginPath();
      if(clickDrag[i] && i){
        context.moveTo(clickX[i-1], clickY[i-1]);
       }else{
         context.moveTo(clickX[i]-1, clickY[i]);
       }
       context.lineTo(clickX[i], clickY[i]);
       context.closePath();
       context.strokeStyle = clickColor[i];
       context.lineWidth = clickSize[i]; 
       context.stroke();
    }
  }

  clearCanvas = function () {
    context.clearRect(0, 0, canvasWidth, canvasHeight);
  }

} //close squiggleApp
