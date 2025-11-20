from sqlalchemy import String, Date
from sqlalchemy.orm import  Mapped, mapped_column
from database import Base
from datetime import date

class User(Base):
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    registered: Mapped[date] = mapped_column()

    def __str__(self):
        return (f'''
                id={self.id} 
                name={self.name}
                registered={self.registered}
                ''')

    def __repr__(self):
        return str(self)


