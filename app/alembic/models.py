import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))



from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship

try: from .database import Base
except ImportError: from database import Base
    

from datetime import date

class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    registered: Mapped[date] = mapped_column()
    lost_reports: Mapped[list["Lost_report"]] = relationship(back_populates="user")
    found_reports: Mapped[list["Found_report"]] = relationship(back_populates="user")
    def __str__(self):
        return (f'''
                id={self.id} 
                name={self.name}
                registered={self.registered}
                ''')

    def __repr__(self):
        return str(self)



class Lost_report(Base):
    id: Mapped[int] = mapped_column(primary_key=True)

    user: Mapped["User"] = relationship(back_populates="lost_reports")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    description: Mapped[str] = mapped_column(Text, nullable=False)
    photo_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)

    registered: Mapped[date] = mapped_column()


class Found_report(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates="found_reports")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    description: Mapped[str] = mapped_column(Text, nullable=False)
    photo_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)

    registered: Mapped[date] = mapped_column()









