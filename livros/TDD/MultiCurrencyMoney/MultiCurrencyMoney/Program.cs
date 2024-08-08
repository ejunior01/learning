namespace MultiCurrencyMoney;

internal class Program
{
    private static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");

        Bank bank = new();

        bank.AddRate("CHF", "USD", 0);

    }
}