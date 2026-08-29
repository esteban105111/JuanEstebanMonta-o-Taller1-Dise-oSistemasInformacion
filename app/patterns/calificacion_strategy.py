from abc import ABC, abstractmethod
from decimal import Decimal


class CalificacionStrategy(ABC):
    @abstractmethod
    def estado(self, calificacion: Decimal) -> str:
        raise NotImplementedError


class CalificacionColombianaStrategy(CalificacionStrategy):
    def estado(self, calificacion: Decimal) -> str:
        return "Aprobado" if calificacion >= Decimal("3.0") else "Reprobado"


class EvaluadorCalificacion:
    def __init__(self, strategy: CalificacionStrategy):
        self.strategy = strategy

    def evaluar(self, calificacion: Decimal) -> str:
        return self.strategy.estado(calificacion)

