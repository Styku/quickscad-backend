//@param Icon(string) Fontawesome icon name
image = "home";
//@param Category(string) Fontawesome icon category, eg. solid, brands, regular
category = "solid";
//@param Radious(float) Outside radious of the keychain
R = 12;

svg_path = str("svg/",category,"/",image,".svg");
$fn = 100;

linear_extrude(2) {
    resize([16, 16, 2])
    import(svg_path, center = true);
}

union() {
    difference() {
        cylinder(2, R, R);
        cylinder(2, R-1, R-1);
    }
    difference() { 
        cylinder(1.5, R, R);
        translate([0, R-2, 0]) cylinder(1.5, 1.2, 1.2);
    }
}