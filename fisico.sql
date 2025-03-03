CREATE TABLE clientes {
    id_cliente NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- es autoincremental y clave primaria
    id_nacional NUMBER NOT NULL UNIQUE, --unique es para que no se repita
    nombre VARCHAR2(50) NOT NULL,
    apellido VARCHAR2(50) NOT NULL,
    email VARCHAR2(100) NOT NULL,
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
    metodo_pago VARCHAR2(25) NOT NULL,
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













CREATE TABLE envios {
    id_envio NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    fecha_despacho TIMESTAMP NOT NULL,
    direccion_entrega VARCHAR2(255) NOT NULL,
    empresa_transporte VARCHAR2(150) NOT NULL,
    numero_seguimiento VARCHAR2(50) NOT NULL,
    estado VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
};




































CREATE TABLE trabajadores{
    id_trabajador NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 

    id_nacional NUMBER NOT NULL UNIQUE,
    nombre VARCHAR2(50) NOT NULL,
    apellido VARCHAR2(50) NOT NULL,
    cargo VARCHAR2(50) NOT NULL,
    telefono VARCHAR2(20) NOT NULL,
    email VARCHAR2(100) NOT NULL,
    activo VARCHAR2(5) DEFAULT 'TRUE' CHECK ( Activo IN( 'TRUE', 'FALSE' ) ) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
};
