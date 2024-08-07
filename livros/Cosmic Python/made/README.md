
Customer -> Order


Product:
    SKU:str

Orders:
    Id:str
    
Order:
    SKU:str
    Quantity:int

Batch:
    Id:str
    SKU:str
    Quantity:int



Order(sku:"RED-CHAIR",quantity:10);
Order(sku:"TASTELESS-LAMP",quantity:1);


batch_Small_table = Batch(sku:"SMALL-TABLE",20)
batch_Small_table.allocate(2)
batch_Small_table.quantity


batch_blue_cushion = Batch(sku:"BLUE-CUSHION",1)

batch_blue_cushion.allocate(2) - raise error allocate














