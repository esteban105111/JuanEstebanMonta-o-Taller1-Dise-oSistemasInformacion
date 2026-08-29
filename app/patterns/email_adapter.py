from typing import Protocol


class EmailProvider(Protocol):
    def send(self, to: str, subject: str, body: str) -> bool:
        ...


class ConsoleEmailProvider:
    def send(self, to: str, subject: str, body: str) -> bool:
        print(f"Email para {to}: {subject}\n{body}")
        return True


class EmailAdapter:
    def __init__(self, provider: EmailProvider):
        self.provider = provider

    def enviar_notificacion(self, destinatario: str, asunto: str, mensaje: str) -> bool:
        return self.provider.send(destinatario, asunto, mensaje)

