namespace UtmBuilder.Core.ValueObjects;

public sealed class Campaign: ValueObject
{
    public string Id { get; set; }
    public string Source { get; set; }
    public string Medium { get; set; }
    public string Name { get; set; }
    public string Term { get; set; }
    public string Content { get; set; }
}