using System;
using System.Collections.Generic;

namespace Lab1_Biquadratic
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.Title = "Лабораторная работа №1 - Биквадратное уравнение";

            double a = 0, b = 0, c = 0;
            bool hasArgs = args.Length == 3;

            if (hasArgs)
            {
                if (!double.TryParse(args[0], out a) ||
                    !double.TryParse(args[1], out b) ||
                    !double.TryParse(args[2], out c))
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("Ошибка: Некорректные аргументы командной строки.");
                    Console.ResetColor();
                    return;
                }
            }
            else
            {
                a = readCoefficient("A");
                b = readCoefficient("B");
                c = readCoefficient("C");
            }

            List<double> roots = SolveBiquadratic(a, b, c);

            if (roots.Count > 0)
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.Write("Корни уравнения: ");
                foreach (var root in roots)
                {
                    Console.Write($"{root} ");
                }
                Console.WriteLine();
            }
            else
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("Корней нет.");
            }

            Console.ResetColor();
            if (!hasArgs) Console.ReadKey();

        }

        static double readCoefficient(string name)
        {
            double value;
            while (true)
            {
                Console.Write($"Введите коэффициент {name}: ");
                string input = Console.ReadLine();
                if (double.TryParse(input, out value))
                {
                    return value;
                }
            }
        }

        static List<double> SolveBiquadratic(double a, double b, double c)
        {
            List<double> result = new List<double>();

            if (a == 0)
            {
                if (b == 0)
                {
                    double t = -c / b;
                    if (t >= 0)
                    {
                        double x = Math.Sqrt(t);
                        result.Add(x);
                        if (x != 0) result.Add(-x);
                    }
                }
                return result;
            }

            double D = b * b - 4 * a * c;

            if (D < 0) return result; // Корней нет

            double t1 = (-b + Math.Sqrt(D)) / (2 * a);
            double t2 = (-b - Math.Sqrt(D)) / (2 * a);

            foreach (double t in new[] { t1, t2 })
            {
                if (t > 0)
                {
                    result.Add(Math.Sqrt(t));
                    result.Add(-Math.Sqrt(t));
                }
                else if (t == 0)
                {
                    if (!result.Contains(0)) result.Add(0);
                }
            }

            result.Sort();
            return result;
        }
    }
}

// .\ConsoleApp1.exe 1 -5 4
// Корни уравнения: -2 -1 1 2

// .\ConsoleApp1.exe 1 -13 36
// Корни уравнения: -3 -2 2 3

// .\ConsoleApp1.exe 1 5 6
// Корней нет.

// .\ConsoleApp1.exe 1 0 -16
// Корни уравнения: -2 2

// .\ConsoleApp1.exe 1 0 0
// Корни уравнения: 0

// .\ConsoleApp1.exe abc
// Введите коэффициент A: abc
// Введите коэффициент A:

// .\ConsoleApp1.exe 1 f 5
// Ошибка: Некорректные аргументы командной строки.