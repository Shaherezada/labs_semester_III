use std::f64::consts::PI;
use std::fmt;

// Аналог абстрактного метода Area
trait GeometricFigure {
    fn area(&self) -> f64;
}

trait IPrint: fmt::Display {
    fn print(&self) {
        // Реализация по умолчанию, использует Display (аналог ToString)
        println!("{}", self);
    }
}

// Cтруктура Прямоугольник
struct Rectangle {
    width: f64,
    height: f64,
}

impl Rectangle {
    fn new(width: f64, height: f64) -> Self {
        Rectangle { width, height }
    }
}

impl GeometricFigure for Rectangle {
    fn area(&self) -> f64 {
        self.width * self.height
    }
}

// Аналог override ToString()
impl fmt::Display for Rectangle {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Прямоугольник: Ширина = {}, Высота = {}, Площадь = {}",
               self.width, self.height, self.area())
    }
}

impl IPrint for Rectangle {}

// В Rust нет наследования структур. Мы создаем отдельную структуру.
// Либо можно было бы использовать Rectangle, но с логической точки зрения 
// для демонстрации полиморфизма создадим отдельный тип.

// Структура Квадрат
struct Square {
    side: f64,
}

impl Square {
    fn new(side: f64) -> Self {
        Square { side }
    }
}

impl GeometricFigure for Square {
    fn area(&self) -> f64 {
        self.side * self.side
    }
}

impl fmt::Display for Square {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Квадрат: Сторона = {}, Площадь = {}", 
               self.side, self.area())
    }
}

impl IPrint for Square {}

// --- Структура Круг ---
struct Circle {
    radius: f64,
}

impl Circle {
    fn new(radius: f64) -> Self {
        Circle { radius }
    }
}

impl GeometricFigure for Circle {
    fn area(&self) -> f64 {
        PI * self.radius * self.radius
    }
}

impl fmt::Display for Circle {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Круг: Радиус = {}, Площадь = {:.2}", 
               self.radius, self.area())
    }
}

impl IPrint for Circle {}

fn main() {
    let rect = Rectangle::new(10.0, 20.0);
    let square = Square::new(15.0);
    let circle = Circle::new(5.0);

    // Полиморфизм в Rust реализуется через Trait Objects (Box<dyn Trait>)
    let figures: Vec<Box<dyn IPrint>> = vec![
        Box::new(rect),
        Box::new(square),
        Box::new(circle),
    ];

    println!("=== Вывод информации о фигурах (Rust) ===");
    for figure in figures {
        figure.print();
    }
}

// PS C:\Users\Matthew\Documents\VSProjects\lab2\hello_rust\target\debug> .\hello_rust.exe
// === Вывод информации о фигурах (Rust) ===
// Прямоугольник: Ширина = 10, Высота = 20, Площадь = 200
// Квадрат: Сторона = 15, Площадь = 225
// Круг: Радиус = 5, Площадь = 78.54

