from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # 🔗 العلاقة مع Category
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", backref="products")
    order_items = relationship("OrderItem", back_populates="product")
