namespace MultiCurrencyMoney;


public class Money : IExpression
{
    protected readonly int _amount;
    protected string _currency;

    public Money(int amount, string currency)
    {
        _amount = amount;
        _currency = currency;
    }

    public string Currency() => _currency;
    public int Amount() => _amount;

    public Money Times(int multiplier)
    {
        return new Money(_amount * multiplier, _currency);
    }

    public Money Reduce(Bank bank,string to)
    {
        int rate = bank.Rate(_currency, to);
        return new Money(_amount / rate, to);
    }

    public IExpression Plus(Money addend)
    {
        return new Sum(this, addend);
    }

    public static Money Dollar(int amount)
    {
        return new Money(amount, "USD");
    }
    public static Money Franc(int amount)
    {
        return new Money(amount, "CHF");
    }

    public override bool Equals(Object obj)
    {
        Money money = (Money)obj;
        return money._amount == _amount && Currency().Equals(money.Currency());
    }

    public override string ToString()
    {
        return $"{_currency} {_amount}";
    }
}