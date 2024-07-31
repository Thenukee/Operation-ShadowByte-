using Microsoft.EntityFrameworkCore;

namespace ShadowByte_v3.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<Node> Nodes { get; set; }
        public DbSet<Link> Links { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Link>()
                .HasOne(l => l.Source)
                .WithMany(n => n.OutgoingLinks)
                .HasForeignKey(l => l.SourceId)
                .OnDelete(DeleteBehavior.NoAction); // Changed from NoAction to Restrict

            modelBuilder.Entity<Link>()
                .HasOne(l => l.Target)
                .WithMany(n => n.IncomingLinks)
                .HasForeignKey(l => l.TargetId)
                .OnDelete(DeleteBehavior.NoAction); // Changed from NoAction to Restrict
        }
    }
}
