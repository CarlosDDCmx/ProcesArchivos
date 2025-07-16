import pytest
from memory.bus import MemoryBus

# ── Clase de evento de prueba ──────────────────────────────────────────
class SampleEvent:
    def __init__(self, value):
        self.value = value

# ── Fixture: callback que acumula valores recibidos ────────────────────
@pytest.fixture
def callback_collector():
    calls = []

    def callback(evt):
        calls.append(evt.value)

    return calls, callback

# ── Prueba: suscripción y emisión del evento ───────────────────────────
def test_subscribe_and_emit(callback_collector):
    calls, callback = callback_collector
    MemoryBus.subscribe(SampleEvent, callback)

    event = SampleEvent("data")
    MemoryBus.emit(event)

    assert calls == ["data"]

    # Limpieza manual
    MemoryBus.unsubscribe(SampleEvent, callback)

# ── Prueba: desuscripción evita que se llame el callback ───────────────
def test_unsubscribe(callback_collector):
    calls, callback = callback_collector
    MemoryBus.subscribe(SampleEvent, callback)
    MemoryBus.unsubscribe(SampleEvent, callback)

    event = SampleEvent("no debe llamar")
    MemoryBus.emit(event)

    assert calls == []
