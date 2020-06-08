/**
    @name Rectangular keychain
    @description Rectangular keychain with embossed logo
*/

//@param Icon(image) Fontawesome icon
image = "solid/home";
//@param Height(float) Height of the keychain
height = 40;
//@param Width(float) Width of the keychain
width = 16;
//@param Thickness(float) Thickness of the keychain
h = 1.5;

svg_path = str("svg/",image,".svg");
$fn = 100;
H = h + h/3;

linear_extrude(2) {
    translate([8, width/2]) resize([12, 12, H])
    import(svg_path, center = true);
}

union() {
    difference() {
        cube([height, width, H]);
        translate([1, 1, 0]) cube([height-2, width-2, H+0.1]);; //+0.1 is for more accurate quick rendering
    }
    difference() { 
        cube([height, width, h]);
        translate([height-2.2, width-2.2, 0]) cylinder(h + 0.1, 1.2, 1.2);
    }
}