CREATE TABLE [dbo].[TodoItem]
(
	[Todo_items_Order] INT IDENTITY NOT NULL PRIMARY KEY, 
    [Todo_List_ID] INT NOT NULL, 
    [Description] VARCHAR(50) NOT NULL, 
    [Costs] INT NOT NULL, 
    [created_on] DATE NOT NULL, 
    [updated_on] DATE NOT NULL, 
    CONSTRAINT [FK_TodoItem_ToTable] FOREIGN KEY ([Todo_List_ID]) REFERENCES [TodoList]([Todo_List_ID])
)
