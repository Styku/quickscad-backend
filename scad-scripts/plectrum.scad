/**
    @name Plectrum
    @description Guitar pick
*/

//@param Length(float) length of plectrum
length = 30;
//@param Thickness(float) thickness of plectrum
thickness = 0.75;

linear_extrude(thickness) scale( length/40 ){
    hull() {
        translate ([-10,16]) rotate(30) scale([0.2,1]) circle (r=20,  $fn=72);
        translate ([10,16]) rotate(-30) scale([0.2,1]) circle (r=20,  $fn=72);
        translate ([0,33]) rotate(90) scale([0.4,1]) circle (r=20.5,  $fn=72);
    }
}