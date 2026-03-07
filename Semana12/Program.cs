using System;
using System.Collections.Generic;
using System.Diagnostics;

var sistema = new SistemaPremacion();
bool salir = false;

while (!salir)
{
    Console.WriteLine("\n==========================================");
    Console.WriteLine("     SISTEMA DE PREMIACION DEPORTIVA      ");
    Console.WriteLine("==========================================");
    Console.WriteLine("  1. Registrar deportista");
    Console.WriteLine("  2. Consultar deportista por ID");
    Console.WriteLine("  3. Listar todos los deportistas");
    Console.WriteLine("  4. Ver disciplinas registradas");
    Console.WriteLine("  5. Ver ganador por disciplina");
    Console.WriteLine("  6. Eliminar deportista");
    Console.WriteLine("  7. Analisis de tiempo de ejecucion");
    Console.WriteLine("  8. Salir");
    Console.WriteLine("==========================================");
    Console.Write("  Seleccione una opcion: ");

    string opcion = Console.ReadLine();

    switch (opcion)
    {
        case "1":
            Console.Write("\n  ID: "); string id = Console.ReadLine();
            Console.Write("  Nombre: "); string nombre = Console.ReadLine();
            Console.Write("  Disciplina: "); string disciplina = Console.ReadLine();
            Console.Write("  Puntaje: "); double.TryParse(Console.ReadLine(), out double puntaje);
            sistema.RegistrarDeportista(id, nombre, disciplina, puntaje);
            break;
        case "2":
            Console.Write("\n  Ingrese el ID: ");
            sistema.ConsultarDeportista(Console.ReadLine());
            break;
        case "3":
            sistema.ListarDeportistas();
            break;
        case "4":
            sistema.VerDisciplinas();
            break;
        case "5":
            Console.Write("\n  Ingrese la disciplina: ");
            sistema.VerGanador(Console.ReadLine());
            break;
        case "6":
            Console.Write("\n  Ingrese el ID a eliminar: ");
            sistema.EliminarDeportista(Console.ReadLine());
            break;
        case "7":
            sistema.AnalizarTiempo();
            break;
        case "8":
            salir = true;
            Console.WriteLine("\n  Hasta luego!");
            break;
        default:
            Console.WriteLine("\n  Opcion no valida.");
            break;
    }
}

class Deportista
{
    public string Id { get; set; }
    public string Nombre { get; set; }
    public string Disciplina { get; set; }
    public double Puntaje { get; set; }

    public Deportista(string id, string nombre, string disciplina, double puntaje)
    {
        Id = id;
        Nombre = nombre;
        Disciplina = disciplina;
        Puntaje = puntaje;
    }

    public override string ToString()
    {
        return $"ID: {Id} | Nombre: {Nombre} | Disciplina: {Disciplina} | Puntaje: {Puntaje}";
    }
}

class SistemaPremacion
{
    private Dictionary<string, Deportista> deportistas = new Dictionary<string, Deportista>();
    private HashSet<string> disciplinas = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
    private Dictionary<string, List<string>> deportistasPorDisciplina = new Dictionary<string, List<string>>(StringComparer.OrdinalIgnoreCase);

    public void RegistrarDeportista(string id, string nombre, string disciplina, double puntaje)
    {
        if (deportistas.ContainsKey(id))
        {
            Console.WriteLine($"\n  El deportista con ID '{id}' ya esta registrado.");
            return;
        }
        var deportista = new Deportista(id, nombre, disciplina, puntaje);
        deportistas[id] = deportista;
        disciplinas.Add(disciplina);

        if (!deportistasPorDisciplina.ContainsKey(disciplina))
            deportistasPorDisciplina[disciplina] = new List<string>();

        deportistasPorDisciplina[disciplina].Add(id);
        Console.WriteLine($"\n  Deportista '{nombre}' registrado correctamente.");
    }

    public void ConsultarDeportista(string id)
    {
        if (deportistas.TryGetValue(id, out Deportista d))
            Console.WriteLine($"\n  {d}");
        else
            Console.WriteLine($"\n  No se encontro ningun deportista con ID '{id}'.");
    }

    public void ListarDeportistas()
    {
        if (deportistas.Count == 0)
        {
            Console.WriteLine("\n  No hay deportistas registrados.");
            return;
        }
        Console.WriteLine("\n==========================================");
        Console.WriteLine("         LISTA DE DEPORTISTAS             ");
        Console.WriteLine("==========================================");
        foreach (var d in deportistas.Values)
            Console.WriteLine($"  {d}");
    }

    public void VerDisciplinas()
    {
        if (disciplinas.Count == 0)
        {
            Console.WriteLine("\n  No hay disciplinas registradas.");
            return;
        }
        Console.WriteLine("\n==========================================");
        Console.WriteLine("         DISCIPLINAS REGISTRADAS          ");
        Console.WriteLine("==========================================");
        foreach (var d in disciplinas)
            Console.WriteLine($"  -> {d}");
    }

    public void VerGanador(string disciplina)
    {
        if (!deportistasPorDisciplina.ContainsKey(disciplina))
        {
            Console.WriteLine($"\n  No existe la disciplina '{disciplina}'.");
            return;
        }
        Deportista ganador = null;
        foreach (var id in deportistasPorDisciplina[disciplina])
        {
            var d = deportistas[id];
            if (ganador == null || d.Puntaje > ganador.Puntaje)
                ganador = d;
        }
        Console.WriteLine($"\n  Ganador en {disciplina}: {ganador}");
    }

    public void EliminarDeportista(string id)
    {
        if (!deportistas.TryGetValue(id, out Deportista d))
        {
            Console.WriteLine($"\n  No se encontro ningun deportista con ID '{id}'.");
            return;
        }
        deportistasPorDisciplina[d.Disciplina].Remove(id);
        if (deportistasPorDisciplina[d.Disciplina].Count == 0)
        {
            deportistasPorDisciplina.Remove(d.Disciplina);
            disciplinas.Remove(d.Disciplina);
        }
        deportistas.Remove(id);
        Console.WriteLine($"\n  Deportista '{d.Nombre}' eliminado correctamente.");
    }

    public void AnalizarTiempo()
    {
        Console.WriteLine("\n==========================================");
        Console.WriteLine("      ANALISIS DE TIEMPO DE EJECUCION     ");
        Console.WriteLine("==========================================");
        var sw = new Stopwatch();

        sw.Restart();
        RegistrarDeportista("TEST01", "Prueba", "TestDisciplina", 99.9);
        sw.Stop();
        Console.WriteLine($"  Insercion:   {sw.ElapsedTicks} ticks");

        sw.Restart();
        deportistas.TryGetValue("TEST01", out _);
        sw.Stop();
        Console.WriteLine($"  Busqueda:    {sw.ElapsedTicks} ticks");

        sw.Restart();
        EliminarDeportista("TEST01");
        sw.Stop();
        Console.WriteLine($"  Eliminacion: {sw.ElapsedTicks} ticks");
    }
}