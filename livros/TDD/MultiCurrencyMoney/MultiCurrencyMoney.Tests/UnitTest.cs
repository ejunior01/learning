
namespace MultiCurrencyMoney.Tests;

[TestClass]
public class UnitTest
{
    [TestMethod]
    public void TestMultiplication()
    {
        Money five = Money.Dollar(5);
        Assert.AreEqual(Money.Dollar(10), five.Times(2));
        Assert.AreEqual(Money.Dollar(15), five.Times(3));
    }

    [TestMethod]
    public void TestEquality()
    {
        Assert.IsTrue(Money.Dollar(5).Equals(Money.Dollar(5)));
        Assert.IsFalse(Money.Dollar(5).Equals(Money.Dollar(6)));
        Assert.IsFalse(Money.Franc(5).Equals(Money.Dollar(5)));
    }

    [TestMethod]
    public void TestCurrency()
    {
        Assert.AreEqual("USD", Money.Dollar(1).Currency());
        Assert.AreEqual("CHF", Money.Franc(1).Currency());

    }


    [TestMethod]
    public void TestSimpleAddition()
    {
        Money five = Money.Dollar(5);
        IExpression sum = five.Plus(five);
        Bank bank = new Bank();
        Money reduced = bank.Reduce(sum, "USD");
        Assert.AreEqual(reduced, Money.Dollar(10));
    }

    [TestMethod]
    public void TestReduceSum()
    {
        IExpression sum = new Sum(Money.Dollar(3), Money.Dollar(4));
        Bank bank = new Bank();
        Money result = bank.Reduce(sum, "USD");
        Assert.AreEqual(result, Money.Dollar(7));
    }


    [TestMethod]
    public void TestReduceMoney()
    {
        Bank bank = new Bank();
        Money result = bank.Reduce(Money.Dollar(1), "USD");
        Assert.AreEqual(result, Money.Dollar(1));
    }
}