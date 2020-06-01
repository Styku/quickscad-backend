//@param image(string) Fontawesome icon name
image = "home";
//@param category(string) Fotawesome icon category, eg. solid, brands, regular
category = "solid";

svg_path = str("svg/",category,"/",image,".svg");
$fn = 100;

linear_extrude(2) {
    resize([16, 16, 2])
    import(svg_path, center = true);
}

union() {
    difference() {
        cylinder(2, 12, 12);
        cylinder(2, 11, 11);
    }
    difference() { 
        cylinder(1.5, 12, 12);
        translate([0, 10, 0]) cylinder(1.5, 1.2, 1.2);
    }
}