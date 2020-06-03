//@param Icon(string) Fontawesome icon name
image = "home";
//@param Category(string) Fontawesome icon category, eg. solid, brands, regular
category = "solid";
//@param Radious(float) Outside radious of the keychain
R = 12; // [10:20]
//@param Thickness(float) Thickness of the keychain
h = 1.5; // [0.5:5]

svg_path = str("svg/",category,"/",image,".svg");
$fn = 100;
H = h + h/3;

linear_extrude(2) {
    resize([16, 16, H])
    import(svg_path, center = true);
}

union() {
    difference() {
        cylinder(H, R, R);
        cylinder(H + 0.1, R-1, R - 1); //+0.1 is for more accurate quick rendering
    }
    difference() { 
        cylinder(h, R, R);
        translate([0, R-2, 0]) cylinder(h + 0.1, 1.2, 1.2);
    }
}