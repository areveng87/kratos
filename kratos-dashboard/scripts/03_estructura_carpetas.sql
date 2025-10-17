/* =========================================================
   LIMPIEZA (opcionales para rehacer rápido en dev)
   ========================================================= */
IF OBJECT_ID('dbo.V_Estructuras_Raiz', 'V') IS NOT NULL DROP VIEW dbo.V_Estructuras_Raiz;
IF OBJECT_ID('dbo.V_Modulos_Asignacion', 'V') IS NOT NULL DROP VIEW dbo.V_Modulos_Asignacion;
IF OBJECT_ID('dbo.TR_ESTRUCTURA_CARPETAS_Prevent_File_With_Children', 'TR') IS NOT NULL DROP TRIGGER dbo.TR_ESTRUCTURA_CARPETAS_Prevent_File_With_Children;
IF OBJECT_ID('dbo.TR_MODULO_ESTRUCTURA_CARPETAS_ValidateRootActive', 'TR') IS NOT NULL DROP TRIGGER dbo.TR_MODULO_ESTRUCTURA_CARPETAS_ValidateRootActive;

IF OBJECT_ID('dbo.MODULO_ESTRUCTURA_CARPETAS', 'U') IS NOT NULL DROP TABLE dbo.MODULO_ESTRUCTURA_CARPETAS;
IF OBJECT_ID('dbo.ESTRUCTURA_CARPETAS', 'U') IS NOT NULL DROP TABLE dbo.ESTRUCTURA_CARPETAS;
IF OBJECT_ID('dbo.MODULOS', 'U') IS NOT NULL DROP TABLE dbo.MODULOS;
GO

/* =========================================================
   TABLA: MODULOS
   ========================================================= */
CREATE TABLE dbo.MODULOS (
    IDMODULO     INT IDENTITY(1,1)  NOT NULL CONSTRAINT PK_MODULOS PRIMARY KEY,
    DESCRIPCION  VARCHAR(100)       NULL
);

-- Evita nombres repetidos (si no usas NULLs, hazlo sin filtro)
CREATE UNIQUE INDEX UQ_MODULOS_DESCRIPCION
    ON dbo.MODULOS (DESCRIPCION)
    WHERE DESCRIPCION IS NOT NULL;
GO

/* =========================================================
   TABLA: ESTRUCTURA_CARPETAS
   - Árbol de carpetas/archivos
   - ARCHIVO = 0 (carpeta), 1 (archivo)
   ========================================================= */
CREATE TABLE dbo.ESTRUCTURA_CARPETAS (
    IDCARPETA        INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_ESTRUCTURA_CARPETAS PRIMARY KEY,
    IDCARPETAPADRE   INT               NULL,
    NOMBRE           VARCHAR(100)      NOT NULL,
    ARCHIVO          BIT               NOT NULL CONSTRAINT DF_ESTRUCTURA_CARPETAS_ARCHIVO DEFAULT(0),
    ACTIVA           BIT               NOT NULL CONSTRAINT DF_ESTRUCTURA_CARPETAS_ACTIVA DEFAULT(1),
    CONSTRAINT FK_ESTRUCTURA_CARPETAS_Padre
        FOREIGN KEY (IDCARPETAPADRE) REFERENCES dbo.ESTRUCTURA_CARPETAS(IDCARPETA)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);

-- Índice para resolver árbol por padre
CREATE INDEX IX_ESTRUCTURA_CARPETAS_Padre ON dbo.ESTRUCTURA_CARPETAS (IDCARPETAPADRE);

-- Evita nombres duplicados entre "hermanos" (mismo padre)
CREATE UNIQUE INDEX UQ_ESTRUCTURA_CARPETAS_Padre_Nombre
    ON dbo.ESTRUCTURA_CARPETAS (IDCARPETAPADRE, NOMBRE);

-- Obliga a que los nombres de estructuras raíz sean únicos
CREATE UNIQUE INDEX UQ_ESTRUCTURA_CARPETAS_Raiz_Nombre
    ON dbo.ESTRUCTURA_CARPETAS (NOMBRE)
    WHERE IDCARPETAPADRE IS NULL;
GO

/* 
   Trigger: un "archivo" no puede tener hijos.
   - Bloquea insertar hijos bajo un nodo marcado como ARCHIVO=1
   - Bloquea convertir a ARCHIVO=1 si ya tiene hijos
*/
CREATE TRIGGER dbo.TR_ESTRUCTURA_CARPETAS_Prevent_File_With_Children
ON dbo.ESTRUCTURA_CARPETAS
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Caso 1: se intentan insertar/actualizar nodos con padre que es ARCHIVO=1
    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN dbo.ESTRUCTURA_CARPETAS p ON p.IDCARPETA = i.IDCARPETAPADRE
        WHERE i.IDCARPETAPADRE IS NOT NULL
          AND p.ARCHIVO = 1
    )
    BEGIN
        RAISERROR('No se pueden crear carpetas/archivos dentro de un archivo.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END

    -- Caso 2: se marca un nodo como ARCHIVO=1 y tiene hijos
    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN dbo.ESTRUCTURA_CARPETAS c ON c.IDCARPETAPADRE = i.IDCARPETA
        WHERE i.ARCHIVO = 1
    )
    BEGIN
        RAISERROR('No se puede marcar como archivo una carpeta que ya tiene hijos.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END
END
GO

/* =========================================================
   TABLA: MODULO_ESTRUCTURA_CARPETAS
   - Relación (opcional) 1:1 entre módulo y una estructura raíz
   - Solo se puede asignar una raíz activa
   ========================================================= */
CREATE TABLE dbo.MODULO_ESTRUCTURA_CARPETAS (
    IDMODULO            INT NOT NULL 
        CONSTRAINT PK_MODULO_ESTRUCTURA_CARPETAS PRIMARY KEY
        CONSTRAINT FK_MEC_Modulo
            FOREIGN KEY REFERENCES dbo.MODULOS(IDMODULO)
            ON DELETE CASCADE ON UPDATE NO ACTION,
    IDESTRUCTURACARPETA INT NOT NULL 
        CONSTRAINT FK_MEC_Estructura
            FOREIGN KEY REFERENCES dbo.ESTRUCTURA_CARPETAS(IDCARPETA)
            ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- Un módulo solo puede tener una estructura asignada
-- y una raíz no puede estar asignada a más de un módulo
CREATE UNIQUE INDEX UQ_MEC_Estructura ON dbo.MODULO_ESTRUCTURA_CARPETAS (IDESTRUCTURACARPETA);
GO

/* 
   Trigger: solo permite asignar una ESTRUCTURA raíz y ACTIVA
   (IDCARPETAPADRE IS NULL y ACTIVA=1)
*/
CREATE TRIGGER dbo.TR_MODULO_ESTRUCTURA_CARPETAS_ValidateRootActive
ON dbo.MODULO_ESTRUCTURA_CARPETAS
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN dbo.ESTRUCTURA_CARPETAS e ON e.IDCARPETA = i.IDESTRUCTURACARPETA
        WHERE NOT (e.IDCARPETAPADRE IS NULL AND e.ACTIVA = 1)
    )
    BEGIN
        RAISERROR('Solo se pueden asignar estructuras raíz activas a los módulos.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END
END
GO

/* =========================================================
   VISTAS DE APOYO PARA LA UI
   ========================================================= */

-- Vista superior: módulos y su estructura raíz (si la hay)
CREATE VIEW dbo.V_Modulos_Asignacion AS
SELECT 
    m.IDMODULO,
    m.DESCRIPCION                AS MODULO,
    mec.IDESTRUCTURACARPETA      AS RAIZ_ID,
    e.NOMBRE                     AS RAIZ_NOMBRE,
    e.ACTIVA                     AS RAIZ_ACTIVA
FROM dbo.MODULOS m
LEFT JOIN dbo.MODULO_ESTRUCTURA_CARPETAS mec 
       ON mec.IDMODULO = m.IDMODULO
LEFT JOIN dbo.ESTRUCTURA_CARPETAS e 
       ON e.IDCARPETA = mec.IDESTRUCTURACARPETA;
GO

-- Vista inferior: estructuras raíz, su estado y a qué módulo (si alguno) están asignadas
CREATE VIEW dbo.V_Estructuras_Raiz AS
SELECT 
    e.IDCARPETA           AS RAIZ_ID,
    e.NOMBRE              AS RAIZ_NOMBRE,
    e.ACTIVA              AS RAIZ_ACTIVA,
    mec.IDMODULO,
    m.DESCRIPCION         AS MODULO_ASIGNADO
FROM dbo.ESTRUCTURA_CARPETAS e
LEFT JOIN dbo.MODULO_ESTRUCTURA_CARPETAS mec 
       ON mec.IDESTRUCTURACARPETA = e.IDCARPETA
LEFT JOIN dbo.MODULOS m 
       ON m.IDMODULO = mec.IDMODULO
WHERE e.IDCARPETAPADRE IS NULL;
GO

/* =========================================================
   ÍNDICES RECOMENDADOS
   ========================================================= */
-- Búsqueda por nombre de raíz
CREATE INDEX IX_ESTRUCTURA_CARPETAS_Nombre ON dbo.ESTRUCTURA_CARPETAS (NOMBRE);
-- Búsqueda por actividad
CREATE INDEX IX_ESTRUCTURA_CARPETAS_Activa ON dbo.ESTRUCTURA_CARPETAS (ACTIVA);
GO
