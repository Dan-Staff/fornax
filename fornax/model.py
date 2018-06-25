from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

JOIN_DEPTH = 2


class QueryEdge(Base):

    __tablename__ = 'query_edge'
    start = Column(Integer, ForeignKey("query_node.id"), primary_key=True)
    end = Column(Integer, ForeignKey("query_node.id"), primary_key=True)

    def __repr__(self):
        return "<QueryEdge(id={}, start={}, end={})>".format(
            self.id, self.start, self.end
        )


class TargetEdge(Base):

    __tablename__ = 'target_edge'
    start = Column(Integer, ForeignKey("target_node.id"), primary_key=True)
    end = Column(Integer, ForeignKey("target_node.id"), primary_key=True)

    def __repr__(self):
        return "<TargetEdge(id={}, start={}, end={})>".format(
            self.id, self.start, self.end
        )


class Match(Base):

    __tablename__ = 'matching_edge'
    start = Column(Integer, ForeignKey("query_node.id"), primary_key=True)
    end = Column(Integer, ForeignKey("target_node.id"), primary_key=True)
    weight = Column(Float, nullable=False)

    def __repr__(self):
        return "<TargetEdge(id={}, start={}, end={})>".format(
            self.id, self.start, self.end
        )


class QueryNode(Base):

    __tablename__ = 'query_node'
    id = Column(Integer, primary_key=True)
    neighbours = relationship(
        "QueryNode",
        secondary=QueryEdge.__table__,
        primaryjoin=id==QueryEdge.__table__.c.start,
        secondaryjoin=id==QueryEdge.__table__.c.end,
        join_depth=JOIN_DEPTH,
        lazy="joined",

    )
    def __repr__(self):
        return "<QueryNode(id={})>".format(self.id)


class TargetNode(Base):

    __tablename__ = 'target_node'
    id = Column(Integer, primary_key=True)
    neighbours = relationship(
        "TargetNode",
        secondary=TargetEdge.__table__,
        primaryjoin=id==TargetEdge.__table__.c.start,
        secondaryjoin=id==TargetEdge.__table__.c.end,
        join_depth=JOIN_DEPTH,
        lazy="joined",
    )
    def __repr__(self):
        return "<TargetNode(id={})>".format(self.id)

