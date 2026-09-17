import cocotb
from cocotb.triggers import Timer, ClockCycles
from cocotb.clock import Clock

@cocotb.test()
async def test_neuron_learning(dut):
    """Prueba avanzada: Plasticidad STDP al extremo (Potenciacion y Depresion)"""
    
    # 1. Configurar un reloj del sistema de 50 MHz
    clock = Clock(dut.clk, 20, unit="ns")
    cocotb.start_soon(clock.start())

    # 2. Estado inicial: Aplicamos Reset global
    dut._log.info("Iniciando el chip y aplicando Reset...")
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1  # Liberamos el reset
    await ClockCycles(dut.clk, 2)

    # 3. Parametros iniciales: Umbral=8, Fuga=1, Ventana STDP=7 (Máxima sensibilidad)
    config_bits = (7 << 5) | (1 << 1)
    dut.ui_in.value = config_bits
    dut.uio_in.value = 8
    await ClockCycles(dut.clk, 2)

    dut._log.info("--- FASE 1: FORZANDO POTENCIACIÓN MÁXIMA (LTP) ---")
    # Para que el peso suba, estimulamos repetidamente simulando una entrada fuerte
    for i in range(40):
        dut.ui_in.value = config_bits | 0x01  # spike_pre = 1
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = config_bits & ~0x01 # spike_pre = 0
        await ClockCycles(dut.clk, 2)         # Intervalo óptimo para asociar pulsos

        # Lectura moderna corregida sin advertencias
        val_uo_out = dut.uo_out.value.to_unsigned()
        peso_actual = (val_uo_out >> 1) & 0x3F
        dut._log.info(f"Pulso LTP {i} -> Peso Sinaptico actual: {peso_actual}")

    dut._log.info("--- FASE 2: FORZANDO DEPRESIÓN MÁXIMA (LTD) ---")
    # Cambiamos el comportamiento bajando el umbral a 0 de golpe para que la neurona 
    # dispare sola antes de recibir los estímulos, provocando desasociación temporal
    dut.uio_in.value = 0 
    for i in range(40):
        dut.ui_in.value = config_bits | 0x01  # spike_pre = 1
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = config_bits & ~0x01 # spike_pre = 0
        await ClockCycles(dut.clk, 5)         # Retraso largo para castigar la sinapsis

        val_uo_out = dut.uo_out.value.to_unsigned()
        peso_actual = (val_uo_out >> 1) & 0x3F
        dut._log.info(f"Pulso LTD {i} -> Peso Sinaptico actual: {peso_actual}")

    dut._log.info("Simulacion dinamica completada con exito.")
