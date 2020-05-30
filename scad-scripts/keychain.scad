$fn = 100;

svg_path = "svg/solid/home.svg";

linear_extrude(2) {
    resize([16, 16, 2])
    import(svg_path, center = true);
}

//translate([-12, -12, 0])
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