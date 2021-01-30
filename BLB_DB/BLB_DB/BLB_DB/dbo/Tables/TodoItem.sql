CREATE TABLE [dbo].[TodoItem]
(
    [Id] INT PRIMARY KEY IDENTITY(1,1),
	[Todo_items_Order] INT NOT NULL, 
    [Todo_List_ID] INT NOT NULL, 
    [Description] VARCHAR(50) NOT NULL, 
    [Costs] INT NOT NULL, 
    [created_on] DATE NULL DEFAULT GETDATE(),
    [updated_on] DATE NULL DEFAULT GETDATE(),
    [Title] VARCHAR(50) NOT NULL, 
    CONSTRAINT [FK_TodoItem_ToTable] FOREIGN KEY ([Todo_List_ID]) REFERENCES [TodoList]([Todo_List_ID])
)

GO

CREATE TRIGGER [dbo].[Trigger_TodoItem_updated_on]
    ON [dbo].[TodoItem]
    AFTER UPDATE AS
    BEGIN
        UPDATE TodoItem
        SET updated_on = GETDATE() 
        WHERE Id IN (SELECT Id FROM Inserted)
        SET NoCount ON
    END
