public class Link
{
    public int Id { get; set; }

    // Foreign keys
    public int SourceId { get; set; }
    public int TargetId { get; set; }

    // Navigation properties
    public Node Source { get; set; }
    public Node Target { get; set; }
}
