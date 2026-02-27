using System;
using System.Collections.Generic;

class Traductor
{
    // Diccionario Español -> Inglés
    static Dictionary<string, string> diccionarioEsIngles = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
    {
        { "tiempo", "time" },
        { "persona", "person" },
        { "año", "year" },
        { "camino", "way" },
        { "día", "day" },
        { "cosa", "thing" },
        { "hombre", "man" },
        { "mundo", "world" },
        { "vida", "life" },
        { "mano", "hand" },
        { "parte", "part" },
        { "niño", "child" },
        { "ojo", "eye" },
        { "mujer", "woman" },
        { "lugar", "place" },
        { "trabajo", "work" },
        { "semana", "week" },
        { "caso", "case" },
        { "punto", "point" },
        { "gobierno", "government" },
        { "empresa", "company" }
    };

    // Diccionario Inglés -> Español
    static Dictionary<string, string> diccionarioIngEs = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
    {
        { "time", "tiempo" },
        { "person", "persona" },
        { "year", "año" },
        { "way", "camino" },
        { "day", "día" },
        { "thing", "cosa" },
        { "man", "hombre" },
        { "world", "mundo" },
        { "life", "vida" },
        { "hand", "mano" },
        { "part", "parte" },
        { "child", "niño" },
        { "eye", "ojo" },
        { "woman", "mujer" },
        { "place", "lugar" },
        { "work", "trabajo" },
        { "week", "semana" },
        { "case", "caso" },
        { "point", "punto" },
        { "government", "gobierno" },
        { "company", "empresa" }
    };

    static string TraducirFrase(string frase, Dictionary<string, string> diccionario, out int traducidas, out int noTraducidas)
    {
        string[] palabras = frase.Split(' ');
        string[] resultado = new string[palabras.Length];
        traducidas = 0;
        noTraducidas = 0;

        for (int i = 0; i < palabras.Length; i++)
        {
            // Separar puntuación al final de la palabra
            string palabraLimpia = palabras[i].Trim(',', '.', ';', ':', '!', '?');
            string puntuacion = palabras[i].Substring(palabraLimpia.Length);

            if (diccionario.ContainsKey(palabraLimpia))
            {
                string traduccion = diccionario[palabraLimpia];
                // Conservar mayúscula inicial si aplica
                if (palabraLimpia.Length > 0 && char.IsUpper(palabraLimpia[0]))
                    traduccion = char.ToUpper(traduccion[0]) + traduccion.Substring(1);

                resultado[i] = traduccion + puntuacion;
                traducidas++;
            }
            else
            {
                resultado[i] = palabras[i];
                if (!string.IsNullOrWhiteSpace(palabraLimpia))
                    noTraducidas++;
            }
        }

        return string.Join(" ", resultado);
    }

    static void MostrarDiccionario()
    {
        Console.WriteLine("\n--- Diccionario actual (Español ↔ Inglés) ---");
        Console.WriteLine($"{"#",-4} {"Español",-20} {"Inglés",-20}");
        Console.WriteLine(new string('-', 46));

        int num = 1;
        foreach (var par in diccionarioEsIngles)
        {
            Console.WriteLine($"{num,-4} {par.Key,-20} {par.Value,-20}");
            num++;
        }
        Console.WriteLine(new string('-', 46));
        Console.WriteLine($"Total de palabras: {diccionarioEsIngles.Count}");
    }

    static void AgregarPalabra()
    {
        Console.WriteLine("\n--- Agregar nueva palabra al diccionario ---");
        Console.Write("Ingrese la palabra en español: ");
        string español = Console.ReadLine()?.Trim();

        Console.Write("Ingrese la traducción en inglés: ");
        string ingles = Console.ReadLine()?.Trim();

        if (string.IsNullOrEmpty(español) || string.IsNullOrEmpty(ingles))
        {
            Console.WriteLine("Error: no puede ingresar palabras vacías.");
            return;
        }

        // Agregar en ambas direcciones
        diccionarioEsIngles[español.ToLower()] = ingles.ToLower();
        diccionarioIngEs[ingles.ToLower()] = español.ToLower();

        Console.WriteLine($"✔ Palabra agregada correctamente: '{español}' ↔ '{ingles}'");
    }

    static void Main(string[] args)
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;
        int opcion = -1;

        while (opcion != 0)
        {
            Console.WriteLine("\n==================== MENÚ ====================");
            Console.WriteLine("1. Traducir una frase");
            Console.WriteLine("2. Agregar palabras al diccionario");
            Console.WriteLine("3. Ver diccionario completo");
            Console.WriteLine("0. Salir");
            Console.WriteLine("==============================================");
            Console.Write("Seleccione una opción: ");

            string input = Console.ReadLine();

            if (!int.TryParse(input, out opcion))
            {
                Console.WriteLine("Opción no válida. Intente de nuevo.");
                continue;
            }

            switch (opcion)
            {
                case 1:
                    Console.WriteLine("\n--- Traducir frase ---");
                    Console.WriteLine("¿En qué dirección desea traducir?");
                    Console.WriteLine("  A) Español → Inglés");
                    Console.WriteLine("  B) Inglés → Español");
                    Console.Write("Seleccione (A/B): ");
                    string dir = Console.ReadLine()?.Trim().ToUpper();

                    Dictionary<string, string> diccionarioSeleccionado;
                    if (dir == "A")
                        diccionarioSeleccionado = diccionarioEsIngles;
                    else if (dir == "B")
                        diccionarioSeleccionado = diccionarioIngEs;
                    else
                    {
                        Console.WriteLine("Opción no válida.");
                        break;
                    }

                    Console.Write("Ingrese la frase: ");
                    string frase = Console.ReadLine();

                    if (string.IsNullOrEmpty(frase))
                    {
                        Console.WriteLine("La frase no puede estar vacía.");
                        break;
                    }

                    string traduccion = TraducirFrase(frase, diccionarioSeleccionado, out int traducidas, out int noTraducidas);
                    Console.WriteLine($"\nFrase original  : {frase}");
                    Console.WriteLine($"Frase traducida : {traduccion}");

                    if (traducidas == 0)
                        Console.WriteLine("⚠ Ninguna palabra de la frase está en el diccionario.");
                    else if (noTraducidas > 0)
                        Console.WriteLine($"ℹ {traducidas} palabra(s) traducida(s). {noTraducidas} palabra(s) no encontrada(s) en el diccionario y se dejaron igual.");
                    break;

                case 2:
                    AgregarPalabra();
                    break;

                case 3:
                    MostrarDiccionario();
                    break;

                case 0:
                    Console.WriteLine("¡Hasta luego!");
                    break;

                default:
                    Console.WriteLine("Opción no válida. Intente de nuevo.");
                    break;
            }
        }
    }
}