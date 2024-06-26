"""Repository Layer"""

from abc import ABC, abstractmethod
from typing import List, Type

from pydantic import UUID4
from sqlalchemy.orm.session import Session

from app.models import ElevatorDemand
from app.schemas import ElevatorDemandInput, ElevatorDemandOutput


class AbstractRepository(ABC):
    """Abstract Repository Class"""

    @abstractmethod
    def create(self, item):
        """Create items"""
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        """List items"""
        raise NotImplementedError

    @abstractmethod
    def get_item(self, item_id):
        """Get item by ID"""
        raise NotImplementedError

    @abstractmethod
    def update(self, item, new_data):
        """Update item"""
        raise NotImplementedError

    @abstractmethod
    def delete(self, item):
        """Delete item"""
        raise NotImplementedError


class ElevatorDemandRepository(AbstractRepository):
    """Elevator Demand Repository Class"""

    def __init__(self, session: Session) -> None:
        """
        Init function.
        :return: None
        """
        self.session = session

    def create(self, item: ElevatorDemandInput) -> ElevatorDemandOutput:
        """
        Create demand objects.
        :parameter item: Elevator Demand object.
        :return: Created object from database.
        """
        demand = ElevatorDemand(**item.model_dump())
        self.session.add(demand)
        self.session.commit()
        self.session.refresh(demand)
        return ElevatorDemandOutput(
            id=demand.id, origin=demand.origin, destination=demand.destination
        )

    def get_all(self) -> List[ElevatorDemandOutput]:
        """
        List demand objects.
        :return: List of existing object from database.
        """
        items = self.session.query(ElevatorDemand).all()
        return [ElevatorDemandOutput(**item.__dict__) for item in items]

    def get_item(self, item_id: UUID4) -> Type[ElevatorDemand]:
        """
        Get demand object by ID.
        :parameter item_id: Object ID.
        :return: Elevator Demand object from database.
        """
        return self.session.query(ElevatorDemand).filter_by(id=item_id).first()

    def update(
        self, item: Type[ElevatorDemand], new_data: ElevatorDemandInput
    ) -> ElevatorDemandOutput:
        """
        Update demand object.
        :parameter item: Elevator Demand object.
        :parameter new_data: Data to update in object.
        :return: Updated Elevator Demand object from database.
        """
        item.origin = new_data.origin
        item.destination = new_data.destination
        self.session.commit()
        self.session.refresh(item)
        return ElevatorDemandOutput(**item.__dict__)

    def delete(self, item: Type[ElevatorDemand]) -> bool:
        """
        Delete demand object.
        :parameter item: Elevator Demand object.
        """
        id_ = item.id
        self.session.delete(item)
        self.session.commit()
        return bool(self.session.query(ElevatorDemand).filter_by(id=id_).first())
