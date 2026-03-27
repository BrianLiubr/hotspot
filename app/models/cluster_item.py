from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class ClusterItem(Base):
    __tablename__ = "cluster_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cluster_id: Mapped[int] = mapped_column(ForeignKey("event_clusters.id"), nullable=False)
    news_item_id: Mapped[int] = mapped_column(ForeignKey("news_items.id"), nullable=False)
    cluster = relationship("EventCluster")
    news_item = relationship("NewsItem")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
