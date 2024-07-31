using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ShadowByte_v3.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Links_Nodes_SourceNodeId",
                table: "Links");

            migrationBuilder.DropForeignKey(
                name: "FK_Links_Nodes_TargetNodeId",
                table: "Links");

            migrationBuilder.RenameColumn(
                name: "TargetNodeId",
                table: "Links",
                newName: "TargetId");

            migrationBuilder.RenameColumn(
                name: "SourceNodeId",
                table: "Links",
                newName: "SourceId");

            migrationBuilder.RenameIndex(
                name: "IX_Links_TargetNodeId",
                table: "Links",
                newName: "IX_Links_TargetId");

            migrationBuilder.RenameIndex(
                name: "IX_Links_SourceNodeId",
                table: "Links",
                newName: "IX_Links_SourceId");

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

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Links_Nodes_SourceId",
                table: "Links");

            migrationBuilder.DropForeignKey(
                name: "FK_Links_Nodes_TargetId",
                table: "Links");

            migrationBuilder.RenameColumn(
                name: "TargetId",
                table: "Links",
                newName: "TargetNodeId");

            migrationBuilder.RenameColumn(
                name: "SourceId",
                table: "Links",
                newName: "SourceNodeId");

            migrationBuilder.RenameIndex(
                name: "IX_Links_TargetId",
                table: "Links",
                newName: "IX_Links_TargetNodeId");

            migrationBuilder.RenameIndex(
                name: "IX_Links_SourceId",
                table: "Links",
                newName: "IX_Links_SourceNodeId");

            migrationBuilder.AddForeignKey(
                name: "FK_Links_Nodes_SourceNodeId",
                table: "Links",
                column: "SourceNodeId",
                principalTable: "Nodes",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);

            migrationBuilder.AddForeignKey(
                name: "FK_Links_Nodes_TargetNodeId",
                table: "Links",
                column: "TargetNodeId",
                principalTable: "Nodes",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);
        }
    }
}
