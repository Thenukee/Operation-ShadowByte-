using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ShadowByte_v3.Migrations
{
    /// <inheritdoc />
    public partial class SeedTestData : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Links_Nodes_SourceId",
                table: "Links");

            migrationBuilder.DropForeignKey(
                name: "FK_Links_Nodes_TargetId",
                table: "Links");

            migrationBuilder.AddForeignKey(
                name: "FK_Links_Nodes_SourceId",
                table: "Links",
                column: "SourceId",
                principalTable: "Nodes",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);

            migrationBuilder.AddForeignKey(
                name: "FK_Links_Nodes_TargetId",
                table: "Links",
                column: "TargetId",
                principalTable: "Nodes",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Links_Nodes_SourceId",
                table: "Links");

            migrationBuilder.DropForeignKey(
                name: "FK_Links_Nodes_TargetId",
                table: "Links");

            migrationBuilder.AddForeignKey(
                name: "FK_Links_Nodes_SourceId",
                table: "Links",
                column: "SourceId",
                principalTable: "Nodes",
                principalColumn: "Id");

            migrationBuilder.AddForeignKey(
                name: "FK_Links_Nodes_TargetId",
                table: "Links",
                column: "TargetId",
                principalTable: "Nodes",
                principalColumn: "Id");
        }
    }
}
