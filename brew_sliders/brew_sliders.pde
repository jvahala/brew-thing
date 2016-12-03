Slider srm, str, mou, hon, swe, ibu;
int hs = 60;

void setup() {
  size(1000,1000);
  noStroke();
  
  srm = new Slider(0,height/2-5*hs, width, hs, 20, 74, 39, 150);
  str = new Slider(0,height/2-3*hs, width, hs, 20, 243, 3, 15);
  mou = new Slider(0,height/2-hs, width, hs, 20, 51, 102, 153);
  hon = new Slider(0,height/2+hs, width, hs, 20, 69, 104, 20);
  swe = new Slider(0,height/2+3*hs, width, hs, 20, 30, 190, 41);
  ibu = new Slider(0,height/2+5*hs, width, hs, 20, 190, 89, 104);
}

void draw() {
  background(255);

  srm.update();
  str.update();
  mou.update();
  hon.update();
  swe.update();
  ibu.update();
  
  srm.display();
  str.display();
  mou.display();
  hon.display();
  swe.display();
  ibu.display();
  
  stroke(0);
  line(0, height/2+hs/2, width, height/2+hs/2);
  line(0, height/2+3*hs/2, width, height/2+3*hs/2);
  
  line(0, height/2-hs/2, width, height/2-hs/2);
  line(0, height/2-3*hs/2, width, height/2-3*hs/2);
  
  line(0, height/2+5*hs/2, width, height/2+5*hs/2);
  line(0, height/2+7*hs/2, width, height/2+7*hs/2);
  
  line(0, height/2-5*hs/2, width, height/2-5*hs/2);
  line(0, height/2-7*hs/2, width, height/2-7*hs/2);
  
  line(0, height/2+9*hs/2, width, height/2+9*hs/2);
  line(0, height/2+11*hs/2, width, height/2+11*hs/2);
  
  line(0, height/2-9*hs/2, width, height/2-9*hs/2);
  line(0, height/2-11*hs/2, width, height/2-11*hs/2);
}


class Slider {
  int swidth, sheight;    // width and height of bar
  float xpos, ypos;       // x and y position of bar
  float spos, newspos;    // x position of slider
  float sposMin, sposMax; // max and min values of slider
  int loose;              // how loose/heavy
  boolean over;           // is the mouse over the slider?
  boolean locked;
  float ratio;
  int c1;
  int c2;
  int c3;

  Slider (float xp, float yp, int sw, int sh, int l, int co1, int co2, int co3) {
    swidth = sw;
    sheight = sh;
    int widthtoheight = sw - sh;
    ratio = (float)sw / (float)widthtoheight;
    xpos = xp;
    ypos = yp-sheight/2;
    spos = xpos + swidth/2 - sheight/2;
    newspos = spos;
    sposMin = xpos;
    sposMax = xpos + swidth - sheight;
    loose = l;
    c1 = co1;
    c2 = co2;
    c3 = co3;
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
      newspos = constrain(mouseX-sheight/2, sposMin, sposMax);
    }
    if (abs(newspos - spos) > 1) {
      spos = spos + (newspos-spos)/loose;
    }
  }

  float constrain(float val, float minv, float maxv) {
    return min(max(val, minv), maxv);
  }

  boolean overEvent() {
    if (mouseX > xpos && mouseX < xpos+swidth &&
       mouseY > ypos && mouseY < ypos+sheight) {
      return true;
    } else {
      return false;
    }
  }

  void display() {
    noStroke();
    fill(204);
    rect(xpos, ypos, swidth, sheight);
    if (over || locked) {
      fill(0, 0, 0);
    } else {
      fill(c1, c2, c3);
    }
    rect(spos, ypos, sheight, sheight);
  }

  float getPos() {
    // Convert spos to be values between
    // 0 and the total width of the scrollbar
    return spos * ratio;
  }
}