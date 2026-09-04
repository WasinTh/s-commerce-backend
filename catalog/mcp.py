from mcp_server import ModelQueryToolset
from catalog.models import Category, Product


class CatagoryQueryTool(ModelQueryToolset):
    model = Category
    extra_instructions = (
        "Catagory means ชนิดของสินค้า"
    )

class ProductQueryTool(ModelQueryToolset):
    model = Product

