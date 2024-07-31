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
            base.OnModelCreating(modelBuilder);

            // Configure the Node entity
            modelBuilder.Entity<Node>()
                .HasKey(n => n.Id);

            modelBuilder.Entity<Node>()
                .Property(n => n.Name)
                .IsRequired()
                .HasMaxLength(100);

            // Configure the Link entity
            modelBuilder.Entity<Link>()
                .HasKey(l => l.Id);

            // Configure the relationship between Link and Node
            modelBuilder.Entity<Link>()
                .HasOne(l => l.Source)
                .WithMany(n => n.OutgoingLinks)
                .HasForeignKey(l => l.SourceId)
                .OnDelete(DeleteBehavior.Restrict); // Use Restrict to avoid cascade delete issues

            modelBuilder.Entity<Link>()
                .HasOne(l => l.Target)
                .WithMany(n => n.IncomingLinks)
                .HasForeignKey(l => l.TargetId)
                .OnDelete(DeleteBehavior.Restrict); // Use Restrict to avoid cascade delete issues

            // Seed Nodes
            modelBuilder.Entity<Node>().HasData(
                new Node { Id = 1, Name = "Node1" },
                new Node { Id = 2, Name = "Node2" },
                new Node { Id = 3, Name = "Node3" }
            );

            // Seed Links
            modelBuilder.Entity<Link>().HasData(
                new Link { Id = 1, SourceId = 1, TargetId = 2 },
                new Link { Id = 2, SourceId = 2, TargetId = 3 },
                new Link { Id = 3, SourceId = 3, TargetId = 1 }
            );
        }



    }
}
