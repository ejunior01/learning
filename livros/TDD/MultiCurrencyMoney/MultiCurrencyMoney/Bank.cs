using System.Collections;

namespace MultiCurrencyMoney;


public class Bank
{
    private readonly Hashtable _rates = [];
    public Money Reduce(IExpression source, string to)
    {
        return source.Reduce(this, to);
    }

    public int Rate(string from, string to)
    {
        if (from.Equals(to)) return 1;

        if (_rates.ContainsKey(new Pair(from, to)))
        {
            var value = _rates[new Pair(from, to)];

            if (value is not null)
            {
                return (int)value;
            }
        }

        return 1;
    }

    public void AddRate(string from, string to, int rate)
    {
        _rates.Add(new Pair(from, to), rate);
    }
}