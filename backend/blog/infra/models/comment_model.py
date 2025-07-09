import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from blog.domain.entities.comment import Comment
import uuid
from datetime import datetime
from blog.infra.database import Base


class CommentModel(Base):
    __tablename__ = "comments"

    id: Mapped[str] = mapped_column(
        sa.String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    comment: Mapped[str] = mapped_column(sa.Text, nullable=False)
    post_id: Mapped[str] = mapped_column(
        sa.String, sa.ForeignKey("posts.id", ondelete="CASCADE")
    )
    user_id: Mapped[str] = mapped_column(
        sa.String, sa.ForeignKey("users.id", ondelete="CASCADE")
    )
    date: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.now())

    post = relationship("PostModel", back_populates="comments", lazy="joined")
    user = relationship("UserModel", back_populates="comments", lazy="joined")

    @classmethod
    def from_entity(cls, entity: Comment) -> "CommentModel":
        return cls(
            id=entity.id,
            comment=entity.comment,
            post_id=entity.post_id,
            user_id=entity.user_id,
            date=entity.date,
        )

    def to_entity(self) -> Comment:
        return Comment(
            id=self.id,
            comment=self.comment,
            post_id=self.post_id,
            user_id=self.user_id,
            date=self.date,
        )
