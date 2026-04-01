using System;
using System.Collections.Generic;

class Nodo {
    public int dato;
    public Nodo izq, der;
    public Nodo(int val) { dato = val; izq = null; der = null; }
}

class ArbolBinario {

    static Nodo Insertar(Nodo raiz, int val) {
        if (raiz == null) return new Nodo(val);
        if (val < raiz.dato)
            raiz.izq = Insertar(raiz.izq, val);
        else if (val > raiz.dato)
            raiz.der = Insertar(raiz.der, val);
        return raiz;
    }

    static void Graficar(Nodo nodo, int nivel = 0) {
        if (nodo == null) return;
        Graficar(nodo.der, nivel + 1);
        for (int i = 0; i < nivel; i++) Console.Write("    ");
        Console.WriteLine("[" + nodo.dato + "]");
        Graficar(nodo.izq, nivel + 1);
    }

    static void Inorden(Nodo nodo) {
        if (nodo == null) return;
        Inorden(nodo.izq);
        Console.Write(nodo.dato + " ");
        Inorden(nodo.der);
    }

    static Nodo CargarDatos(int[] datos) {
        Nodo raiz = null;
        foreach (int val in datos)
            raiz = Insertar(raiz, val);
        return raiz;
    }

    static void Main(string[] args) {

        // Ejemplo 1 - arbol1
        int[] datos1 = { 50, 30, 70, 20, 40, 60, 80 };

        Console.WriteLine("==============================");
        Console.WriteLine("  EJEMPLO 1");
        Console.WriteLine("  Datos: 50, 30, 70, 20, 40, 60, 80");
        Console.WriteLine("==============================");
        Nodo arbol1 = CargarDatos(datos1);
        Console.WriteLine("\nGrafica del arbol:\n");
        Graficar(arbol1);
        Console.Write("\nRecorrido inorden: ");
        Inorden(arbol1);
        Console.WriteLine();

        // Ejemplo 2 - arbol2
        int[] datos2 = { 10, 5, 15, 3, 7, 12, 20 };

        Console.WriteLine("\n==============================");
        Console.WriteLine("  EJEMPLO 2");
        Console.WriteLine("  Datos: 10, 5, 15, 3, 7, 12, 20");
        Console.WriteLine("==============================");
        Nodo arbol2 = CargarDatos(datos2);
        Console.WriteLine("\nGrafica del arbol:\n");
        Graficar(arbol2);
        Console.Write("\nRecorrido inorden: ");
        Inorden(arbol2);
        Console.WriteLine();

        Console.ReadKey();
    }
}