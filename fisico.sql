CREATE TABLE clientes {
    id_cliente NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- es autoincremental y clave primaria
    id_nacional NUMBER NOT NULL UNIQUE, --unique es para que no se repita
    nombre VARCHAR2(50) NOT NULL,
    apellido VARCHAR2(50) NOT NULL,
    email VARCHAR2(100) NOT NULL UNIQUE,
    telefono VARCHAR2(20) NOT NULL,
    activo VARCHAR2(5) DEFAULT 'TRUE' CHECK ( Activo IN( 'TRUE', 'FALSE' ) ) NOT NULL,
    correo_confirmado VARCHAR2(5) DEFAULT 'TRUE' CHECK ( Correo_confirmado IN( 'TRUE', 'FALSE' ) ) NOT NULL,
    contrasena VARCHAR2(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
};

CREATE TABLE direcciones {
    id_direccion NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- es autoincremental y clave primaria
    id_cliente NUMBER NOT NULL,
    direccion VARCHAR2(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_direccion_clientes FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente) ON DELETE CASCADE -- si se elimina un cliente se eliminan todas sus direcciones
};

CREATE TABLE metodos_pago {
    id_metodo_pago NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- es autoincremental y clave primaria
    id_cliente NUMBER NOT NULL,
    metodo_pago VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_metodo_pagos_clientes FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente) ON DELETE CASCADE -- si se elimina un cliente se eliminan todos sus metodos de pago
};

CREATE TABLE categorias {
    id_categoria NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- es autoincremental y clave primaria
    nombre VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
};

CREATE TABLE departamentos {
    id_departamento NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- es autoincremental y clave primaria
    nombre VARCHAR2(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
};

CREATE TABLE productos{
    id_producto NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_categoria NUMBER NOT NULL,
    sku VARCHAR2(50) NOT NULL,
    nombre VARCHAR2(100) NOT NULL,
    descripcion VARCHAR2(255) NOT NULL,
    precio NUMBER NOT NULL,
    slug VARCHAR2(100) NOT NULL,
    activo VARCHAR2(5) DEFAULT 'TRUE' CHECK ( Activo IN( 'TRUE', 'FALSE' ) ) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_producto_categoria FOREIGN KEY (id_categoria) REFERENCES categorias (id_categoria) ON DELETE CASCADE 
};

CREATE TABLE imagenes{
    id_imagen NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_producto NUMBER NOT NULL,
    ruta_imagen VARCHAR2(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_imagen_producto FOREIGN KEY (id_producto) REFERENCES productos (id_producto) ON DELETE CASCADE 
};


CREATE TABLE sedes{
    id_sede NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name_sede VARCHAR2(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
};


CREATE TABLE trabajadores{
    id_trabajador NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    id_sede NUMBER NOT NULL,
    id_departamento NUMBER NOT NULL,
    id_nacional NUMBER NOT NULL UNIQUE,
    nombre VARCHAR2(50) NOT NULL,
    apellido VARCHAR2(50) NOT NULL,
    cargo VARCHAR2(50) NOT NULL,
    telefono VARCHAR2(20) NOT NULL,
    email VARCHAR2(100) NOT NULL UNIQUE,
    activo VARCHAR2(5) DEFAULT 'TRUE' CHECK ( Activo IN( 'TRUE', 'FALSE' ) ) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_trabajador_sede FOREIGN KEY (id_sede) REFERENCES sedes (id_sede) ON DELETE CASCADE,
    CONSTRAINT fk_trabajador_departamento FOREIGN KEY (id_departamento) REFERENCES departamentos (id_departamento) ON DELETE CASCADE
};


CREATE TABLE inventarios{
    id_inventario NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_sede NUMBER NOT NULL,
    id_producto NUMBER NOT NULL, 
    stock NUMBER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_inventario_sede FOREIGN KEY (id_sede) REFERENCES sedes (id_sede) ON DELETE CASCADE,
    CONSTRAINT fk_inventario_producto FOREIGN KEY (id_producto) REFERENCES productos (id_producto) ON DELETE CASCADE
};



CREATE TABLE traslados_internos{
    id_traslado_interno NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha_movimiento TIMESTAMP NOT NULL,
    id_almacen_origen NUMBER NOT NULL,
    id_almacen_destino NUMBER NOT NULL,
    estado VARCHAR2(50) NOT NULL,
    fecha_estimada_llegada TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_traslado_interno_sede_origen FOREIGN KEY (id_almacen_origen) REFERENCES sedes (id_sede) ON DELETE CASCADE,
    CONSTRAINT fk_traslado_interno_sede_destino FOREIGN KEY (id_almacen_destino) REFERENCES sedes (id_sede) ON DELETE CASCADE
};



CREATE TABLE listas_prod_tras_int{
    id_lista_prod_tras_int NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_traslado_interno NUMBER NOT NULL,
    id_producto NUMBER NOT NULL,
    cantidad NUMBER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_lista_prod_tras_int_traslado_interno FOREIGN KEY (id_traslado_interno) REFERENCES traslados_internos (id_traslado_interno) ON DELETE CASCADE,
    CONSTRAINT fk_lista_prod_tras_int_producto FOREIGN KEY (id_producto) REFERENCES productos (id_producto) ON DELETE CASCADE
};



CREATE TABLE orden_compras{
    id_orden_compra NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cliente NUMBER NOT NULL,
    id_sede NUMBER NOT NULL,
    fecha_creacion TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_orden_compra_cliente FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente) ON DELETE CASCADE,
    CONSTRAINT fk_orden_compra_sede FOREIGN KEY (id_sede) REFERENCES sedes (id_sede) ON DELETE CASCADE
};



CREATE TABLE orden_listas{
    id_orden_lista NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_orden_compra NUMBER NOT NULL,
    id_producto NUMBER NOT NULL,
    cantidad NUMBER NOT NULL,
    precio_unitario NUMBER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_orden_lista_orden_compra FOREIGN KEY (id_orden_compra) REFERENCES orden_compras (id_orden_compra) ON DELETE CASCADE,
    CONSTRAINT fk_orden_lista_producto FOREIGN KEY (id_producto) REFERENCES productos (id_producto) ON DELETE CASCADE
};



CREATE TABLE envios {
    id_envio NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_orden_compra NUMBER NOT NULL,
    fecha_despacho TIMESTAMP NOT NULL,
    direccion_entrega VARCHAR2(255) NOT NULL,
    empresa_transporte VARCHAR2(150) NOT NULL,
    numero_seguimiento VARCHAR2(50) NOT NULL,
    estado VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_envio_orden_compra FOREIGN KEY (id_orden_compra) REFERENCES orden_compras (id_orden_compra) ON DELETE CASCADE
};


CREATE TABLE pagos{
    id_pago NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_orden_compra NUMBER NOT NULL,
    metodo_pago VARCHAR2(50) NOT NULL,
    fecha_transaccion TIMESTAMP NOT NULL,
    monto_total NUMBER NOT NULL,
    estado VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_pago_orden_compra FOREIGN KEY (id_orden_compra) REFERENCES orden_compras (id_orden_compra) ON DELETE CASCADE
};



CREATE TABLE devoluciones{
    id_devolucion NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_orden_compra NUMBER NOT NULL,
    fecha_solicitud TIMESTAMP NOT NULL,
    motivo VARCHAR2(255) NOT NULL,
    estado VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_devolucion_orden_compra FOREIGN KEY (id_orden_compra) REFERENCES orden_compras (id_orden_compra) ON DELETE CASCADE
};