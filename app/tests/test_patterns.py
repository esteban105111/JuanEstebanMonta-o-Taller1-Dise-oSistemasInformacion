from decimal import Decimal
from types import SimpleNamespace

from app.config.database import DatabaseConnection
from app.patterns.calificacion_strategy import CalificacionColombianaStrategy, EvaluadorCalificacion
from app.patterns.email_adapter import EmailAdapter
from app.patterns.service_factory import ServiceFactory
from app.services.estudiante_service import EstudianteService


class FakeEmailProvider:
    def __init__(self):
        self.sent = []

    def send(self, to: str, subject: str, body: str) -> bool:
        self.sent.append((to, subject, body))
        return True


def test_singleton_database_connection_reutiliza_instancia():
    assert DatabaseConnection() is DatabaseConnection()


def test_factory_method_crea_servicio_estudiante():
    fake_db = SimpleNamespace()
    service = ServiceFactory.crear_estudiante_service(fake_db)

    assert isinstance(service, EstudianteService)


def test_adapter_envia_notificacion_con_proveedor_externo():
    provider = FakeEmailProvider()
    adapter = EmailAdapter(provider)

    assert adapter.enviar_notificacion("ana@test.com", "Curso", "Creado")
    assert provider.sent == [("ana@test.com", "Curso", "Creado")]


def test_strategy_evalua_estado_de_calificacion():
    evaluador = EvaluadorCalificacion(CalificacionColombianaStrategy())

    assert evaluador.evaluar(Decimal("4.0")) == "Aprobado"
    assert evaluador.evaluar(Decimal("2.9")) == "Reprobado"

