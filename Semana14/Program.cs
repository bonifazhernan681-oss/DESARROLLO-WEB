using System;

namespace ArbolBinarioBusqueda
{
    // Clase Nodo
    class Nodo
    {
        public int Valor;
        public Nodo Izquierdo;
        public Nodo Derecho;

        public Nodo(int valor)
        {
            Valor = valor;
            Izquierdo = null;
            Derecho = null;
        }
    }

    // Clase Árbol Binario de Búsqueda
    class ArbolBST
    {
        private Nodo raiz;

        public ArbolBST()
        {
            raiz = null;
        }

        // ── INSERTAR ──────────────────────────────────────────────
        public void Insertar(int valor)
        {
            raiz = InsertarRec(raiz, valor);
        }

        private Nodo InsertarRec(Nodo nodo, int valor)
        {
            if (nodo == null)
                return new Nodo(valor);

            if (valor < nodo.Valor)
                nodo.Izquierdo = InsertarRec(nodo.Izquierdo, valor);
            else if (valor > nodo.Valor)
                nodo.Derecho = InsertarRec(nodo.Derecho, valor);
            else
                Console.WriteLine($"  ⚠  El valor {valor} ya existe en el árbol.");

            return nodo;
        }

        // ── BUSCAR ────────────────────────────────────────────────
        public bool Buscar(int valor)
        {
            return BuscarRec(raiz, valor);
        }

        private bool BuscarRec(Nodo nodo, int valor)
        {
            if (nodo == null) return false;
            if (nodo.Valor == valor) return true;
            return valor < nodo.Valor
                ? BuscarRec(nodo.Izquierdo, valor)
                : BuscarRec(nodo.Derecho, valor);
        }

        // ── ELIMINAR ──────────────────────────────────────────────
        public void Eliminar(int valor)
        {
            if (!Buscar(valor))
            {
                Console.WriteLine($"  ⚠  El valor {valor} no existe en el árbol.");
                return;
            }
            raiz = EliminarRec(raiz, valor);
            Console.WriteLine($"  ✔  Valor {valor} eliminado correctamente.");
        }

        private Nodo EliminarRec(Nodo nodo, int valor)
        {
            if (nodo == null) return null;

            if (valor < nodo.Valor)
                nodo.Izquierdo = EliminarRec(nodo.Izquierdo, valor);
            else if (valor > nodo.Valor)
                nodo.Derecho = EliminarRec(nodo.Derecho, valor);
            else
            {
                // Caso 1 y 2: 0 o 1 hijo
                if (nodo.Izquierdo == null) return nodo.Derecho;
                if (nodo.Derecho == null)   return nodo.Izquierdo;

                // Caso 3: 2 hijos → sucesor inorden (mínimo del subárbol derecho)
                int sucesor = ObtenerMinimo(nodo.Derecho);
                nodo.Valor = sucesor;
                nodo.Derecho = EliminarRec(nodo.Derecho, sucesor);
            }
            return nodo;
        }

        // ── RECORRIDOS ────────────────────────────────────────────
        public void Preorden()
        {
            Console.Write("  Preorden  (Raíz-Izq-Der): ");
            PreordenRec(raiz);
            Console.WriteLine();
        }

        private void PreordenRec(Nodo nodo)
        {
            if (nodo == null) return;
            Console.Write($"{nodo.Valor} ");
            PreordenRec(nodo.Izquierdo);
            PreordenRec(nodo.Derecho);
        }

        public void Inorden()
        {
            Console.Write("  Inorden   (Izq-Raíz-Der): ");
            InordenRec(raiz);
            Console.WriteLine();
        }

        private void InordenRec(Nodo nodo)
        {
            if (nodo == null) return;
            InordenRec(nodo.Izquierdo);
            Console.Write($"{nodo.Valor} ");
            InordenRec(nodo.Derecho);
        }

        public void Postorden()
        {
            Console.Write("  Postorden (Izq-Der-Raíz): ");
            PostordenRec(raiz);
            Console.WriteLine();
        }

        private void PostordenRec(Nodo nodo)
        {
            if (nodo == null) return;
            PostordenRec(nodo.Izquierdo);
            PostordenRec(nodo.Derecho);
            Console.Write($"{nodo.Valor} ");
        }

        // ── MÍNIMO, MÁXIMO Y ALTURA ───────────────────────────────
        private int ObtenerMinimo(Nodo nodo)
        {
            while (nodo.Izquierdo != null)
                nodo = nodo.Izquierdo;
            return nodo.Valor;
        }

        public void MostrarEstadisticas()
        {
            if (raiz == null)
            {
                Console.WriteLine("  ⚠  El árbol está vacío.");
                return;
            }
            Console.WriteLine($"  Mínimo : {ObtenerMinimo(raiz)}");
            Console.WriteLine($"  Máximo : {ObtenerMaximo(raiz)}");
            Console.WriteLine($"  Altura : {ObtenerAltura(raiz)}");
        }

        private int ObtenerMaximo(Nodo nodo)
        {
            while (nodo.Derecho != null)
                nodo = nodo.Derecho;
            return nodo.Valor;
        }

        private int ObtenerAltura(Nodo nodo)
        {
            if (nodo == null) return 0;
            int altIzq = ObtenerAltura(nodo.Izquierdo);
            int altDer = ObtenerAltura(nodo.Derecho);
            return 1 + Math.Max(altIzq, altDer);
        }

        // ── LIMPIAR ───────────────────────────────────────────────
        public void Limpiar()
        {
            raiz = null;
            Console.WriteLine("  ✔  Árbol limpiado completamente.");
        }

        public bool EstaVacio() => raiz == null;
    }

    // ── PROGRAMA PRINCIPAL ────────────────────────────────────────
    class Program
    {
        static void Main(string[] args)
        {
            ArbolBST arbol = new ArbolBST();
            bool salir = false;

            Console.OutputEncoding = System.Text.Encoding.UTF8;

            while (!salir)
            {
                MostrarMenu();
                string opcion = Console.ReadLine()?.Trim();
                Console.WriteLine();

                switch (opcion)
                {
                    case "1":
                        Console.Write("  Ingrese el valor a insertar: ");
                        if (int.TryParse(Console.ReadLine(), out int valIns))
                        {
                            arbol.Insertar(valIns);
                            Console.WriteLine($"  ✔  Valor {valIns} insertado.");
                        }
                        else Console.WriteLine("  ✖  Valor inválido.");
                        break;

                    case "2":
                        Console.Write("  Ingrese el valor a buscar: ");
                        if (int.TryParse(Console.ReadLine(), out int valBus))
                        {
                            bool encontrado = arbol.Buscar(valBus);
                            Console.WriteLine(encontrado
                                ? $"  ✔  El valor {valBus} SÍ existe en el árbol."
                                : $"  ✖  El valor {valBus} NO existe en el árbol.");
                        }
                        else Console.WriteLine("  ✖  Valor inválido.");
                        break;

                    case "3":
                        Console.Write("  Ingrese el valor a eliminar: ");
                        if (int.TryParse(Console.ReadLine(), out int valElim))
                            arbol.Eliminar(valElim);
                        else Console.WriteLine("  ✖  Valor inválido.");
                        break;

                    case "4":
                        if (arbol.EstaVacio()) Console.WriteLine("  ⚠  El árbol está vacío.");
                        else { arbol.Preorden(); arbol.Inorden(); arbol.Postorden(); }
                        break;

                    case "5":
                        arbol.MostrarEstadisticas();
                        break;

                    case "6":
                        arbol.Limpiar();
                        break;

                    case "7":
                        salir = true;
                        Console.WriteLine("  Hasta luego. ");
                        break;

                    default:
                        Console.WriteLine("  ✖  Opción no válida. Intente de nuevo.");
                        break;
                }

                Console.WriteLine();
            }
        }

        static void MostrarMenu()
        {
            Console.WriteLine("╔══════════════════════════════════════╗");
            Console.WriteLine("║   Árbol Binario de Búsqueda (BST)   ║");
            Console.WriteLine("╠══════════════════════════════════════╣");
            Console.WriteLine("║  1. Insertar valor                   ║");
            Console.WriteLine("║  2. Buscar valor                     ║");
            Console.WriteLine("║  3. Eliminar valor                   ║");
            Console.WriteLine("║  4. Mostrar recorridos               ║");
            Console.WriteLine("║  5. Mínimo, Máximo y Altura          ║");
            Console.WriteLine("║  6. Limpiar árbol                    ║");
            Console.WriteLine("║  7. Salir                            ║");
            Console.WriteLine("╚══════════════════════════════════════╝");
            Console.Write("  Seleccione una opción: ");
        }
    }
}
