using System;  
using System.Collections; // Для ArrayList
using System.Collections.Generic; // Для List<T> и Dictionary

namespace Lab3_Collections
{
    interface IPrint
    {
        void Print();
    }

    abstract class GeometricFigure : IComparable
    {
        public string Type { get; protected set; }
        public abstract double Area();

        public override string ToString()
        {
            return $"{Type}: Площадь = {Area():F2}";
        }

        // Реализация сравнения для сортировки (по площади)
        public int CompareTo(object obj)
        {
            GeometricFigure p = obj as GeometricFigure;
            if (p != null) return this.Area().CompareTo(p.Area());
            else throw new Exception("Невозможно сравнить два объекта");
        }
    }

    class Rectangle : GeometricFigure, IPrint
    {
        public double Width { get; set; }
        public double Height { get; set; }
        public Rectangle(double w, double h) { Width = w; Height = h; Type = "Прямоугольник"; }
        public override double Area() => Width * Height;
        public void Print() => Console.WriteLine(this.ToString());
    }

    class Square : Rectangle
    {
        public Square(double size) : base(size, size) { Type = "Квадрат"; }
    }

    class Circle : GeometricFigure, IPrint
    {
        public double Radius { get; set; }
        public Circle(double r) { Radius = r; Type = "Круг"; }
        public override double Area() => Math.PI * Radius * Radius;
        public void Print() => Console.WriteLine(this.ToString());
    }

    class Matrix3D<T>
    {
        Dictionary<(int, int, int), T> _matrix = new Dictionary<(int, int, int), T>();
        public T this[int x, int y, int z]
        {
            get
            {
                var key = (x, y, z);
                if (_matrix.ContainsKey(key)) return _matrix[key];
                else return default(T); // Возвращаем null или 0, если элемента нет
            }
            set
            {
                var key = (x, y, z);
                _matrix[key] = value;
            }
        }

        public override string ToString()
        {
            string res = "";
            foreach (var item in _matrix)
            {
                res += $"x=[{item.Key.Item1}, y={item.Key.Item2}, z={item.Key.Item3}] -> {item.Value}\n";
            }
            return res;
        }
    }

    class Node<T>
    {
        public T Data;
        public Node<T> Next;
        public Node(T data)
        {
            this.Data = data;
            this.Next = null;
        }
    }

    class SimpleList<T>
    {
        protected Node<T> head;
    }

    class SimpleStack<T> : SimpleList<T>
    {
        public void Push(T element)
        {
            Node<T> newNode = new Node<T>(element);
            newNode.Next = head;
            head = newNode;
        }

        public T Pop()
        {
            if (head == null) throw new InvalidOperationException("Стек пуст");
            T data = head.Data;
            head = head.Next;

            return data;
        }

        public bool IsEmpty() => head == null;
    }

    class Program
    {
        static void Main(string[] args)
        {
            Console.Title = "Лабораторная работа №3. Коллекции";
            Rectangle rect = new Rectangle(5, 4);
            Square square = new Square(5);
            Circle circle = new Circle(2);

            Console.WriteLine("=== Array List (До сортировки) ===");
            ArrayList arrayList = new ArrayList();
            arrayList.Add(rect);
            arrayList.Add(square);
            arrayList.Add(circle);

            foreach (var item in arrayList) Console.WriteLine(item);

            Console.WriteLine("=== Array List (После сортировки) ===");
            arrayList.Sort();
            foreach (var item in arrayList) Console.WriteLine(item);

            Console.WriteLine("=== List<Figure> (После сортировки) ===");

            List<GeometricFigure> list = new List<GeometricFigure> { rect, square, circle };
            list.Sort();
            foreach (var item in list) Console.WriteLine(item);

            Console.WriteLine("=== 3D Разреженная матрица (После сортировки) ===");
            Matrix3D<GeometricFigure> matrix = new Matrix3D<GeometricFigure>();
            matrix[0, 0, 0] = rect;
            matrix[10, 5, 2] = square;
            matrix[10, 5, 2] = null; // Удаление элемента
            matrix[2, 2, 2] = circle;

            Console.WriteLine(matrix.ToString());

            Console.WriteLine("=== SimpleStack ===");
            SimpleStack<GeometricFigure> stack = new SimpleStack<GeometricFigure>();
            stack.Push(rect);
            stack.Push(square);
            stack.Push(circle);

            Console.WriteLine("Извлечение элементов из стека (LIFO):");
            while (!stack.IsEmpty())
            {
                Console.WriteLine(stack.Pop());
            }

            Console.ReadKey();
        }
    }
}
