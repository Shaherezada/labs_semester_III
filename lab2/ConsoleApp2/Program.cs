using System;
using System.Collections.Generic;

namespace Lab2_Classes
{
    interface IPrint
    {
        void Print();
    }

    abstract class GeometricFigure
    {
        public abstract double Area();
    }

    class Rectangle : GeometricFigure, IPrint
    {
        public double Width { get; set; }
        public double Height { get; set; }

        public Rectangle(double width, double height)
        {
            this.Width = width;
            this.Height = height;
        }

        public override double Area()
        {
            return Width * Height;
        }

        public override string ToString()
        {
            return $"Прямоугольник: Ширина = {Width}, Высота = {Height}, Площадь = {Area()}";
        }

        public void Print()
        {
            Console.WriteLine(this.ToString());
        }
    }

    class Square : Rectangle
    {
        public Square(double side) : base(side, side)
        {
        }

        public override string ToString()
        {
            return $"Квадрат: Сторона = {Width}, Площадь = {Area()}";
        }
    }

    class Circle : GeometricFigure, IPrint
    {
        public double Radius { get; set; }

        public Circle(double radius)
        {
            this.Radius = radius;
        }

        public override double Area()
        {
            return Math.PI * Radius * Radius;
        }

        public override string ToString()
        {
            return $"Круг: Радиус = {Radius}, Площадь = {Area():F2}";
        }

        public void Print()
        {
            Console.WriteLine(this.ToString());
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Console.Title = "Лабораторная работа №2";

            // Создание объектов
            Rectangle rect = new Rectangle(10, 20);
            Square square = new Square(15);
            Circle circle = new Circle(5);

            List<IPrint> figures = new List<IPrint> { rect, square, circle };

            Console.WriteLine("=== Вывод информации о фигурах ===");
            foreach (var figure in figures)
            {
                figure.Print();
            }

            Console.ReadLine();
        }
    }
}

/*
PS C:\Users\Matthew\Documents\VSProjects\lab2\ConsoleApp2\bin\Debug\net9.0> .\ConsoleApp2.exe      
=== Вывод информации о фигурах ===
Прямоугольник: Ширина = 10, Высота = 20, Площадь = 200
Квадрат: Сторона = 15, Площадь = 225
Круг: Радиус = 5, Площадь = 78.54
*/