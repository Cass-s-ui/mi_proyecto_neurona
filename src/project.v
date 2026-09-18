`default_nettype none

module tt_um_cass_s_ui_neuron_lif (
    input  wire [7:0] ui_in,    // Inputs
    output wire [7:0] uo_out,   // Outputs
    input  wire [7:0] uio_in,   // Bidirectional in
    output wire [7:0] uio_out,  // Bidirectional out
    output wire [7:0] uio_oe,   // Bidirectional enable
    input  wire       ena,      // always 1
    input  wire       clk,      // clock
    input  wire       rst_n     // reset active low
);

    // 1. Cables internos para conectar los dos módulos entre sí
    wire [5:0] current_weight;
    wire       neuron_spike;

    // 2. Mapeo de los pines físicos de entrada (ui_in)
    wire       spike_pre_input = ui_in[0];  // Pin 0: Pulso de entrada externo
    wire [3:0] config_leak     = ui_in[4:1];  // Pines 4 a 1: Configura la fuga (leak)
    wire [2:0] config_window   = ui_in[7:5];  // Pines 7 a 5: Configura la ventana STDP

    // 3. Mapeo de las entradas bidireccionales (uio_in) para parámetros extra
    wire [3:0] config_threshold = uio_in[3:0]; // Pines Bidi 3 a 0: Configura el umbral

    // 4. Instanciamos el bloque de aprendizaje STDP
    stdp_core plastic_synapse (
        .clk(clk),
        .rst_n(rst_n),
        .spike_pre(spike_pre_input),
        .spike_post(neuron_spike),
        .window_size({1'b0, config_window}), // Convertimos 3 bits a 4 bits de forma segura
        .weight(current_weight)
    );

    // 5. Instanciamos la neurona LIF (el estímulo será el peso si hay pulso previo)
    wire [5:0] dynamic_stimulus = spike_pre_input ? current_weight : 6'b0;

    neuron_lif main_neuron (
        .clk(clk),
        .rst_n(rst_n),
        .stimulus(dynamic_stimulus),
        .leak(config_leak),
        .threshold(config_threshold),
        .spike(neuron_spike)
    );

    // 6. Asignamos las salidas físicas del chip (uo_out)
    assign uo_out[0]     = neuron_spike;   // Pin de salida 0: Transmite el disparo al exterior
    assign uo_out[6:1]   = current_weight; // Pines de salida 6 a 1: Monitorea el peso en tiempo real
    assign uo_out[7]     = 1'b0;           // Pin no usado fijado a cero

    // Desactivamos las salidas de los pines bidireccionales (los usamos solo como entradas)
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

endmodule
