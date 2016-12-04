float z=0;
int x,y;
int num =4;
Wheel wh1;

void setup() {
  size(1000, 1000, P3D);
  x = width/2;
  y = height/2;
  ellipseMode(CENTER);
  smooth();
  
  wh1 = new Wheel(0,10,num);
}
void draw() {
  strokeWeight(1);
  noFill();
  background(255);
  translate(width/2, height/2);
  triangle(0, 0, width/3, (width/3)*tan(360/(2*num))/4, width/3, -(width/3)*tan(360/(2*num))/4);

  wh1.update();
  wh1.display();
  
  println(wh1.getAng());

}  
/*
void keyPressed(){
  if(key == CODED){
      if(keyCode == LEFT){
      z=z+(PI/100);
    } else if(keyCode == RIGHT){
      z=z-(PI/100);
    }
  }
}
*/

class Wheel {
  float sang, newsang;    // angle positions of wheel
  int loose;              // how loose/heavy
  boolean over;           // is the mouse over the slider?
  boolean locked;
  float ratio;
  int num;

  Wheel (float ang, int l, int numb) {
    sang = ang;
    newsang = sang;
    loose = l;
    num = numb;
  }

void update() {
    if (overEvent()) {
      over = true;
    } else {
      over = false;
    }
    if (mousePressed && over) {
      locked = true;
    }
    if (!mousePressed) {
      locked = false;
    }
    if (locked) {
      newsang = atan2(mouseY-y,mouseX-x);
    }
    if (abs(newsang - sang) > 1/360) {
      sang = sang + (newsang-sang)/loose;
      rotate(sang);
    }
  }
  


  boolean overEvent() {
    if (mouseX < abs(width*cos(atan2(mouseY-y,mouseX-x))) &&
       mouseY < abs(width*sin(atan2(mouseY-y,mouseX-x)))) {
      return true;
    } else {
      return false;
    }
  }

  void display() {

  //Wheel
  ellipse(0, 0, width/2, width/2);
  //Spokes in wheel 

  for (int i = 0; i<2*num; i++) {
    rotateZ(PI/num);
    line(0, 0, 0, width/4);
  }
}

  float getAng() {
    // Convert spos to be values between
    // 0 and the total width of the scrollbar
    return sang/(2*PI)*100+50;
  }
}