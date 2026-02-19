using System;
using System.Collections.Generic;

class VacunacionCovid
{
    static void Main()
    {
        // ─────────────────────────────────────────
        // 1. GENERACIÓN DE CONJUNTOS FICTICIOS
        // ─────────────────────────────────────────

        // Conjunto U: 500 ciudadanos (universo)
        HashSet<string> ciudadanos = new HashSet<string>();
        for (int i = 1; i <= 500; i++)
            ciudadanos.Add("Ciudadano " + i);

        // Conjunto P: 75 vacunados con Pfizer (Ciudadano 1 al 75)
        HashSet<string> pfizer = new HashSet<string>();
        for (int i = 1; i <= 75; i++)
            pfizer.Add("Ciudadano " + i);

        // Conjunto A: 75 vacunados con AstraZeneca (Ciudadano 51 al 125)
        // (se superponen del 51 al 75 para simular quienes recibieron ambas dosis)
        HashSet<string> astrazeneca = new HashSet<string>();
        for (int i = 51; i <= 125; i++)
            astrazeneca.Add("Ciudadano " + i);

        // ─────────────────────────────────────────
        // 2. OPERACIONES DE TEORÍA DE CONJUNTOS
        // ─────────────────────────────────────────

        // LISTA 1: No vacunados = U - (P ∪ A)
        HashSet<string> vacunados = new HashSet<string>(pfizer);
        vacunados.UnionWith(astrazeneca);                        // P ∪ A

        HashSet<string> noVacunados = new HashSet<string>(ciudadanos);
        noVacunados.ExceptWith(vacunados);                       // U - (P ∪ A)

        // LISTA 2: Ambas dosis = P ∩ A
        HashSet<string> ambasDosis = new HashSet<string>(pfizer);
        ambasDosis.IntersectWith(astrazeneca);                   // P ∩ A

        // LISTA 3: Solo Pfizer = P - A
        HashSet<string> soloPfizer = new HashSet<string>(pfizer);
        soloPfizer.ExceptWith(astrazeneca);                      // P - A

        // LISTA 4: Solo AstraZeneca = A - P
        HashSet<string> soloAstraZeneca = new HashSet<string>(astrazeneca);
        soloAstraZeneca.ExceptWith(pfizer);                      // A - P

        // ─────────────────────────────────────────
        // 3. MOSTRAR RESULTADOS
        // ─────────────────────────────────────────

        Mostrar("LISTA 1 - Ciudadanos NO vacunados (U - (P ∪ A))", noVacunados);
        Mostrar("LISTA 2 - Ciudadanos con AMBAS dosis (P ∩ A)", ambasDosis);
        Mostrar("LISTA 3 - Ciudadanos con SOLO Pfizer (P - A)", soloPfizer);
        Mostrar("LISTA 4 - Ciudadanos con SOLO AstraZeneca (A - P)", soloAstraZeneca);
    }

    static void Mostrar(string titulo, HashSet<string> conjunto)
    {
        Console.WriteLine("\n╔══════════════════════════════════════════════╗");
        Console.WriteLine("  " + titulo);
        Console.WriteLine("  Total: " + conjunto.Count + " ciudadanos");
        Console.WriteLine("╚══════════════════════════════════════════════╝");

        List<string> lista = new List<string>(conjunto);
        lista.Sort(Comparar); // Ordenar numéricamente

        foreach (string c in lista)
            Console.WriteLine("  - " + c);
    }

    // Comparador para ordenar "Ciudadano X" numéricamente
    static int Comparar(string a, string b)
    {
        int numA = int.Parse(a.Replace("Ciudadano ", ""));
        int numB = int.Parse(b.Replace("Ciudadano ", ""));
        return numA.CompareTo(numB);
    }
}