using ShadowByte_v3.Models;

public class Node
{
    public int Id { get; set; }
    public string Name { get; set; }
    public ICollection<Link> OutgoingLinks { get; set; }
    public ICollection<Link> IncomingLinks { get; set; }
}
