# Configuración del simulador para Tiny Tapeout
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

# Rutas de los archivos de hardware reales
VERILOG_SOURCES += $(PWD)/../src/project.v
VERILOG_SOURCES += $(PWD)/../src/neuron_lif.v
VERILOG_SOURCES += $(PWD)/../src/stdp_core.v

# Módulo superior y nombre de la prueba en Python
TOPLEVEL = tt_um_example
MODULE   = test_project

# Incluye las herramientas de simulación de cocotb
include $(shell cocotb-config --makefiles)/Makefile.sim
