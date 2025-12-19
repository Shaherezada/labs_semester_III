use std::env;
use std::io::{self, Write};

fn main() {
    let args: Vec<String> = env::args().collect();
    let (a, b, c);

    let color_green = "\x1b[32m";
    let color_red = "\x1b[31m";
    let color_reset = "\x1b[0m";

    if args.len() == 4 { // args[0] - это имя исполняемого файла
        let parsed_a = args[1].parse::<f64>();
        let parsed_b = args[2].parse::<f64>();
        let parsed_c = args[3].parse::<f64>();

        match (parsed_a, parsed_b, parsed_c) {
            (Ok(val_a), Ok(val_b), Ok(val_c)) => {
                a = val_a;
                b = val_b;
                c = val_c;
            },
            _ => {
                eprintln!("{}Ошибка: Некорректные аргументы командной строки.{}", color_red, color_reset);
                return;
            }
        }
    } else {
        a = read_coefficient("A");
        b = read_coefficient("B");
        c = read_coefficient("C");
    }

    let roots = solve_biquadratic(a, b, c);

    if !roots.is_empty() {
        print!("{}", color_green);
        print!("Корни уравнения: ");
        for root in roots {
            print!("{} ", root);
        }
        println!("{} ", color_reset);
    } else {
        println!("{}Корней нет.{}", color_red, color_reset);
    }
}

fn read_coefficient(name: &str) -> f64 {
    loop {
        print!("Введите коэффициент {}: ", name);
        io::stdout().flush().unwrap(); // Принудительный вывод буфера

        let mut input = String::new();
        match io::stdin().read_line(&mut input) {
            Ok(_) => {
                if let Ok(val) = input.trim().parse::<f64>() {
                    return val;
                }
            }
            Err(_) => continue,
        }
    }
}

fn solve_biquadratic(a: f64, b: f64, c: f64) -> Vec<f64> {
    let mut roots = Vec::new();

    if a == 0.0 {
        if b != 0.0 {
            let t = -c / b;
            if t >= 0.0 {
                let x = t.sqrt();
                roots.push(x);
                if x > 1e-9 { roots.push(-x); }
            }
        }
        return roots;
    }

    let d = b * b - 4.0 * a * c;

    if d < 0.0 {
        return roots;
    }

    let t1 = (-b + d.sqrt()) / (2.0 * a);
    let t2 = (-b - d.sqrt()) / (2.0 * a);

    for &t in &[t1, t2] {
        if t >= 1e-9 {
            let x = t.sqrt();
            roots.push(x);
            roots.push(-x);
        } else if t.abs() <= 1e-9 { // t == 0
            if !roots.contains(&0.0) {
                roots.push(0.0);
            }
        }
    }

    roots.sort_by(|x, y| x.partial_cmp(y).unwrap());
    roots
}

// .\hello_rust.exe 1 -5 4
// Корни уравнения: -2 -1 1 2 
// .\hello_rust.exe 1 -13 36
// Корни уравнения: -3 -2 2 3 
// .\hello_rust.exe 1 5 6
// Корней нет.
// .\hello_rust.exe 1 0 -16 
// Корни уравнения: -2 2 
// .\hello_rust.exe 1 0 0  
// Корни уравнения: 0 
// .\hello_rust.exe avc  
// Введите коэффициент A: abc
// Введите коэффициент A:
// .\hello_rust.exe 1 d 5
// Ошибка: Некорректные аргументы командной строки.