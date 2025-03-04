CREATE TABLE clientes (
    client_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    national_document NUMBER NOT NULL UNIQUE,
    name VARCHAR2(50) NOT NULL,
    lastname VARCHAR2(50) NOT NULL,
    phone VARCHAR2(35) NOT NULL,
    email VARCHAR2(100) NOT NULL UNIQUE,
    active VARCHAR2(5) DEFAULT 'FALSE' NOT NULL,
    confirmed_email VARCHAR2(5) DEFAULT 'FALSE' NOT NULL,
    password VARCHAR2(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);



CREATE TABLE direcciones (
    id_direccion NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    client_id NUMBER NOT NULL,
    address VARCHAR2(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_direccion_clientes FOREIGN KEY (client_id) REFERENCES clientes (client_id) ON DELETE CASCADE
);



CREATE TABLE metodos_pago (
    id_metodo_pago NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    client_id NUMBER NOT NULL,
    payment_method VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_metodo_pagos_clientes FOREIGN KEY (client_id) REFERENCES clientes (client_id) ON DELETE CASCADE
);



CREATE TABLE categorias (
    id_categoria NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);



CREATE TABLE departamentos (
    id_departamento NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);



CREATE TABLE productos (
    id_producto NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_id NUMBER NOT NULL,
    sku VARCHAR2(50) NOT NULL,
    name VARCHAR2(100) NOT NULL,
    description VARCHAR2(255) NOT NULL,
    price NUMBER NOT NULL,
    slug VARCHAR2(100) NOT NULL,
    active VARCHAR2(5) DEFAULT 'FALSE' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_producto_categoria FOREIGN KEY (category_id) REFERENCES categorias (id_categoria) ON DELETE CASCADE
);



CREATE TABLE imagenes(
    id_imagen NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_producto NUMBER NOT NULL,
    ruta_imagen VARCHAR2(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_imagen_producto FOREIGN KEY (id_producto) REFERENCES productos (id_producto) ON DELETE CASCADE 
);



CREATE TABLE sedes (
    id_sede NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);



CREATE TABLE trabajadores (
    id_trabajador NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    location_id NUMBER NOT NULL,
    department_id NUMBER NOT NULL,
    id_nacional NUMBER NOT NULL UNIQUE,
    name VARCHAR2(50) NOT NULL,
    lastname VARCHAR2(50) NOT NULL,
    job VARCHAR2(50) NOT NULL,
    phone VARCHAR2(20) NOT NULL,
    email VARCHAR2(100) NOT NULL UNIQUE,
    active VARCHAR2(5) DEFAULT 'FALSE' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_trabajador_sede FOREIGN KEY (location_id) REFERENCES sedes (id_sede) ON DELETE CASCADE,
    CONSTRAINT fk_trabajador_departamento FOREIGN KEY (department_id) REFERENCES departamentos (id_departamento) ON DELETE CASCADE
);



CREATE TABLE inventarios (
    id_inventario NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    location_id NUMBER NOT NULL,
    product_id NUMBER NOT NULL, 
    quantity NUMBER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_inventario_sede FOREIGN KEY (location_id) REFERENCES sedes (id_sede) ON DELETE CASCADE,
    CONSTRAINT fk_inventario_producto FOREIGN KEY (product_id) REFERENCES productos (id_producto) ON DELETE CASCADE
);



CREATE TABLE traslados_internos (
    id_traslado_interno NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha_movimiento TIMESTAMP NOT NULL,
    location_origin_id NUMBER NOT NULL,
    location_dest_id NUMBER NOT NULL,
    estado VARCHAR2(50) NOT NULL,
    fecha_estimada_llegada TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_traslado_interno_sede_origen FOREIGN KEY (location_origin_id) REFERENCES sedes (id_sede) ON DELETE CASCADE,
    CONSTRAINT fk_traslado_interno_sede_destino FOREIGN KEY (location_dest_id) REFERENCES sedes (id_sede) ON DELETE CASCADE
);



CREATE TABLE listas_prod_tras_int (
    id_lista_prod_tras_int NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    movement_id NUMBER NOT NULL,
    product_id NUMBER NOT NULL,
    quantity NUMBER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_lista_prod_tras_int_traslado_interno FOREIGN KEY (movement_id) REFERENCES traslados_internos (id_traslado_interno) ON DELETE CASCADE,
    CONSTRAINT fk_lista_prod_tras_int_producto FOREIGN KEY (product_id) REFERENCES productos (id_producto) ON DELETE CASCADE
);



CREATE TABLE orden_compras (
    id_orden_compra NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    client_id NUMBER NOT NULL,
    location_id NUMBER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_orden_compra_cliente FOREIGN KEY (client_id) REFERENCES clientes (client_id) ON DELETE CASCADE,
    CONSTRAINT fk_orden_compra_sede FOREIGN KEY (location_id) REFERENCES sedes (id_sede) ON DELETE CASCADE
);



CREATE TABLE orden_detalles(
    id_orden_detalles NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id NUMBER NOT NULL,
    product_id NUMBER NOT NULL,
    quantity NUMBER NOT NULL,
    price NUMBER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_orden_lista_orden_compra FOREIGN KEY (order_id) REFERENCES orden_compras (id_orden_compra) ON DELETE CASCADE,
    CONSTRAINT fk_orden_lista_producto FOREIGN KEY (product_id) REFERENCES productos (id_producto) ON DELETE CASCADE
);



CREATE TABLE envios (
    id_envios NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id NUMBER NOT NULL,
    company VARCHAR2(150) NOT NULL,
    address VARCHAR2(255) NOT NULL,
    number_company_guide VARCHAR2(50) NOT NULL,
    status VARCHAR2(50) NOT NULL,
    delivered_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_envio_orden_compra FOREIGN KEY (order_id) REFERENCES orden_compras (id_orden_compra) ON DELETE CASCADE
);



CREATE TABLE pagos(
    id_pago NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id NUMBER NOT NULL,
    payment_method VARCHAR2(50) NOT NULL,
    status VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_pago_orden_compra FOREIGN KEY (order_id) REFERENCES orden_compras (id_orden_compra) ON DELETE CASCADE
);


CREATE TABLE devoluciones(
    id_devolucion NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id NUMBER NOT NULL,
    description VARCHAR2(255) NOT NULL,
    status VARCHAR2(50) NOT NULL,
    requested_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_devolucion_orden_compra FOREIGN KEY (order_id) REFERENCES orden_compras (id_orden_compra) ON DELETE CASCADE
);