PGDMP     '                     }           logistica_rutas    15.13    15.13 8    A           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            B           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            C           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            D           1262    16398    logistica_rutas    DATABASE     �   CREATE DATABASE logistica_rutas WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Spain.1252';
    DROP DATABASE logistica_rutas;
                postgres    false            �            1259    16453    cabecera_albaran_ruta    TABLE     3  CREATE TABLE public.cabecera_albaran_ruta (
    id integer NOT NULL,
    fecha date NOT NULL,
    transportista_id integer NOT NULL,
    ruta_id integer NOT NULL,
    base_imponible numeric(18,2) NOT NULL,
    importe_liquido numeric(18,2) NOT NULL,
    importe_transporte numeric(18,2),
    beneficio numeric(18,2),
    beneficio_post_log numeric(18,2),
    porcentaje_ben_real numeric(7,4),
    lineas_pedido integer,
    porcentaje_pactado numeric(5,2),
    usuario_id integer NOT NULL,
    fecha_registro timestamp without time zone DEFAULT now() NOT NULL
);
 )   DROP TABLE public.cabecera_albaran_ruta;
       public         heap    postgres    false            �            1259    16452    cabecera_albaran_ruta_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cabecera_albaran_ruta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.cabecera_albaran_ruta_id_seq;
       public          postgres    false    223            E           0    0    cabecera_albaran_ruta_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.cabecera_albaran_ruta_id_seq OWNED BY public.cabecera_albaran_ruta.id;
          public          postgres    false    222            �            1259    16477    lineas_albaran_ruta    TABLE     �  CREATE TABLE public.lineas_albaran_ruta (
    id integer NOT NULL,
    cabecera_id integer NOT NULL,
    numero_albaran text NOT NULL,
    nombre_cliente text,
    codigo_cliente text,
    municipio_envio text,
    importe numeric(18,2),
    descuento_pronto_pago numeric(5,2),
    firma_recibe text,
    beneficio numeric(18,2),
    importe_liquido_linea numeric(18,2),
    porcentaje numeric(7,4),
    conductor text,
    ilpa numeric(18,2),
    beneficio_menos_log numeric(18,2),
    beneficio_real numeric(18,2),
    deuda_cliente numeric(18,2),
    lineas integer,
    fecha_registro timestamp without time zone DEFAULT now() NOT NULL,
    fecha_albaran date
);
 '   DROP TABLE public.lineas_albaran_ruta;
       public         heap    postgres    false            �            1259    16476    lineas_albaran_ruta_id_seq    SEQUENCE     �   CREATE SEQUENCE public.lineas_albaran_ruta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.lineas_albaran_ruta_id_seq;
       public          postgres    false    225            F           0    0    lineas_albaran_ruta_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.lineas_albaran_ruta_id_seq OWNED BY public.lineas_albaran_ruta.id;
          public          postgres    false    224            �            1259    16438    portes    TABLE     �   CREATE TABLE public.portes (
    id integer NOT NULL,
    transportista_id integer NOT NULL,
    porcentaje numeric(5,2) NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date,
    descripcion text
);
    DROP TABLE public.portes;
       public         heap    postgres    false            �            1259    16437    portes_id_seq    SEQUENCE     �   CREATE SEQUENCE public.portes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.portes_id_seq;
       public          postgres    false    221            G           0    0    portes_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.portes_id_seq OWNED BY public.portes.id;
          public          postgres    false    220            �            1259    16414    rutas    TABLE     �   CREATE TABLE public.rutas (
    id integer NOT NULL,
    codigo_ruta text NOT NULL,
    nombre_ruta text NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT now() NOT NULL,
    activo boolean DEFAULT true NOT NULL
);
    DROP TABLE public.rutas;
       public         heap    postgres    false            �            1259    16413    rutas_id_seq    SEQUENCE     �   CREATE SEQUENCE public.rutas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.rutas_id_seq;
       public          postgres    false    217            H           0    0    rutas_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.rutas_id_seq OWNED BY public.rutas.id;
          public          postgres    false    216            �            1259    16427    transportistas    TABLE     P  CREATE TABLE public.transportistas (
    id integer NOT NULL,
    nombres text NOT NULL,
    apellidos text NOT NULL,
    telefono text,
    direccion text,
    email text,
    documento_cif text,
    codigo_postal text,
    fecha_registro timestamp without time zone DEFAULT now() NOT NULL,
    activo boolean DEFAULT true NOT NULL
);
 "   DROP TABLE public.transportistas;
       public         heap    postgres    false            �            1259    16426    transportistas_id_seq    SEQUENCE     �   CREATE SEQUENCE public.transportistas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.transportistas_id_seq;
       public          postgres    false    219            I           0    0    transportistas_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.transportistas_id_seq OWNED BY public.transportistas.id;
          public          postgres    false    218            �            1259    16400    usuarios    TABLE     �  CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nombres text NOT NULL,
    apellidos text NOT NULL,
    nickname text NOT NULL,
    password_hash text NOT NULL,
    fecha_registro timestamp without time zone DEFAULT now() NOT NULL,
    requiere_cambio_pw boolean DEFAULT true NOT NULL,
    email text,
    rol text,
    last_login timestamp without time zone,
    activo boolean DEFAULT true NOT NULL
);
    DROP TABLE public.usuarios;
       public         heap    postgres    false            �            1259    16399    usuarios_id_seq    SEQUENCE     �   CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.usuarios_id_seq;
       public          postgres    false    215            J           0    0    usuarios_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;
          public          postgres    false    214            �           2604    16456    cabecera_albaran_ruta id    DEFAULT     �   ALTER TABLE ONLY public.cabecera_albaran_ruta ALTER COLUMN id SET DEFAULT nextval('public.cabecera_albaran_ruta_id_seq'::regclass);
 G   ALTER TABLE public.cabecera_albaran_ruta ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    222    223    223            �           2604    16480    lineas_albaran_ruta id    DEFAULT     �   ALTER TABLE ONLY public.lineas_albaran_ruta ALTER COLUMN id SET DEFAULT nextval('public.lineas_albaran_ruta_id_seq'::regclass);
 E   ALTER TABLE public.lineas_albaran_ruta ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    224    225    225            �           2604    16441 	   portes id    DEFAULT     f   ALTER TABLE ONLY public.portes ALTER COLUMN id SET DEFAULT nextval('public.portes_id_seq'::regclass);
 8   ALTER TABLE public.portes ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    221    221            �           2604    16417    rutas id    DEFAULT     d   ALTER TABLE ONLY public.rutas ALTER COLUMN id SET DEFAULT nextval('public.rutas_id_seq'::regclass);
 7   ALTER TABLE public.rutas ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    217    217            �           2604    16430    transportistas id    DEFAULT     v   ALTER TABLE ONLY public.transportistas ALTER COLUMN id SET DEFAULT nextval('public.transportistas_id_seq'::regclass);
 @   ALTER TABLE public.transportistas ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    219    219            ~           2604    16403    usuarios id    DEFAULT     j   ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);
 :   ALTER TABLE public.usuarios ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    214    215    215            <          0    16453    cabecera_albaran_ruta 
   TABLE DATA           �   COPY public.cabecera_albaran_ruta (id, fecha, transportista_id, ruta_id, base_imponible, importe_liquido, importe_transporte, beneficio, beneficio_post_log, porcentaje_ben_real, lineas_pedido, porcentaje_pactado, usuario_id, fecha_registro) FROM stdin;
    public          postgres    false    223   I       >          0    16477    lineas_albaran_ruta 
   TABLE DATA           G  COPY public.lineas_albaran_ruta (id, cabecera_id, numero_albaran, nombre_cliente, codigo_cliente, municipio_envio, importe, descuento_pronto_pago, firma_recibe, beneficio, importe_liquido_linea, porcentaje, conductor, ilpa, beneficio_menos_log, beneficio_real, deuda_cliente, lineas, fecha_registro, fecha_albaran) FROM stdin;
    public          postgres    false    225   �I       :          0    16438    portes 
   TABLE DATA           h   COPY public.portes (id, transportista_id, porcentaje, fecha_inicio, fecha_fin, descripcion) FROM stdin;
    public          postgres    false    221   �I       6          0    16414    rutas 
   TABLE DATA           U   COPY public.rutas (id, codigo_ruta, nombre_ruta, fecha_creacion, activo) FROM stdin;
    public          postgres    false    217   �I       8          0    16427    transportistas 
   TABLE DATA           �   COPY public.transportistas (id, nombres, apellidos, telefono, direccion, email, documento_cif, codigo_postal, fecha_registro, activo) FROM stdin;
    public          postgres    false    219   �I       4          0    16400    usuarios 
   TABLE DATA           �   COPY public.usuarios (id, nombres, apellidos, nickname, password_hash, fecha_registro, requiere_cambio_pw, email, rol, last_login, activo) FROM stdin;
    public          postgres    false    215   J       K           0    0    cabecera_albaran_ruta_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.cabecera_albaran_ruta_id_seq', 1, false);
          public          postgres    false    222            L           0    0    lineas_albaran_ruta_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.lineas_albaran_ruta_id_seq', 1, false);
          public          postgres    false    224            M           0    0    portes_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.portes_id_seq', 1, false);
          public          postgres    false    220            N           0    0    rutas_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.rutas_id_seq', 1, false);
          public          postgres    false    216            O           0    0    transportistas_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.transportistas_id_seq', 1, false);
          public          postgres    false    218            P           0    0    usuarios_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.usuarios_id_seq', 1, false);
          public          postgres    false    214            �           2606    16459 0   cabecera_albaran_ruta cabecera_albaran_ruta_pkey 
   CONSTRAINT     n   ALTER TABLE ONLY public.cabecera_albaran_ruta
    ADD CONSTRAINT cabecera_albaran_ruta_pkey PRIMARY KEY (id);
 Z   ALTER TABLE ONLY public.cabecera_albaran_ruta DROP CONSTRAINT cabecera_albaran_ruta_pkey;
       public            postgres    false    223            �           2606    16485 ,   lineas_albaran_ruta lineas_albaran_ruta_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.lineas_albaran_ruta
    ADD CONSTRAINT lineas_albaran_ruta_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.lineas_albaran_ruta DROP CONSTRAINT lineas_albaran_ruta_pkey;
       public            postgres    false    225            �           2606    16445    portes portes_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.portes
    ADD CONSTRAINT portes_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.portes DROP CONSTRAINT portes_pkey;
       public            postgres    false    221            �           2606    16425    rutas rutas_codigo_ruta_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public.rutas
    ADD CONSTRAINT rutas_codigo_ruta_key UNIQUE (codigo_ruta);
 E   ALTER TABLE ONLY public.rutas DROP CONSTRAINT rutas_codigo_ruta_key;
       public            postgres    false    217            �           2606    16423    rutas rutas_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.rutas
    ADD CONSTRAINT rutas_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.rutas DROP CONSTRAINT rutas_pkey;
       public            postgres    false    217            �           2606    16436 "   transportistas transportistas_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.transportistas
    ADD CONSTRAINT transportistas_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.transportistas DROP CONSTRAINT transportistas_pkey;
       public            postgres    false    219            �           2606    16412    usuarios usuarios_nickname_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_nickname_key UNIQUE (nickname);
 H   ALTER TABLE ONLY public.usuarios DROP CONSTRAINT usuarios_nickname_key;
       public            postgres    false    215            �           2606    16410    usuarios usuarios_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.usuarios DROP CONSTRAINT usuarios_pkey;
       public            postgres    false    215            �           1259    16475    idx_cabecera_fecha    INDEX     Z   CREATE INDEX idx_cabecera_fecha ON public.cabecera_albaran_ruta USING btree (fecha DESC);
 &   DROP INDEX public.idx_cabecera_fecha;
       public            postgres    false    223            �           1259    16491    idx_lineas_numero_albaran    INDEX     c   CREATE INDEX idx_lineas_numero_albaran ON public.lineas_albaran_ruta USING btree (numero_albaran);
 -   DROP INDEX public.idx_lineas_numero_albaran;
       public            postgres    false    225            �           1259    16451    idx_portes_transportista_fecha    INDEX     p   CREATE INDEX idx_portes_transportista_fecha ON public.portes USING btree (transportista_id, fecha_inicio DESC);
 2   DROP INDEX public.idx_portes_transportista_fecha;
       public            postgres    false    221    221            �           2606    16465 8   cabecera_albaran_ruta cabecera_albaran_ruta_ruta_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.cabecera_albaran_ruta
    ADD CONSTRAINT cabecera_albaran_ruta_ruta_id_fkey FOREIGN KEY (ruta_id) REFERENCES public.rutas(id);
 b   ALTER TABLE ONLY public.cabecera_albaran_ruta DROP CONSTRAINT cabecera_albaran_ruta_ruta_id_fkey;
       public          postgres    false    3220    223    217            �           2606    16460 A   cabecera_albaran_ruta cabecera_albaran_ruta_transportista_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.cabecera_albaran_ruta
    ADD CONSTRAINT cabecera_albaran_ruta_transportista_id_fkey FOREIGN KEY (transportista_id) REFERENCES public.transportistas(id);
 k   ALTER TABLE ONLY public.cabecera_albaran_ruta DROP CONSTRAINT cabecera_albaran_ruta_transportista_id_fkey;
       public          postgres    false    223    3222    219            �           2606    16470 ;   cabecera_albaran_ruta cabecera_albaran_ruta_usuario_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.cabecera_albaran_ruta
    ADD CONSTRAINT cabecera_albaran_ruta_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);
 e   ALTER TABLE ONLY public.cabecera_albaran_ruta DROP CONSTRAINT cabecera_albaran_ruta_usuario_id_fkey;
       public          postgres    false    215    3216    223            �           2606    16486 8   lineas_albaran_ruta lineas_albaran_ruta_cabecera_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.lineas_albaran_ruta
    ADD CONSTRAINT lineas_albaran_ruta_cabecera_id_fkey FOREIGN KEY (cabecera_id) REFERENCES public.cabecera_albaran_ruta(id);
 b   ALTER TABLE ONLY public.lineas_albaran_ruta DROP CONSTRAINT lineas_albaran_ruta_cabecera_id_fkey;
       public          postgres    false    225    3227    223            �           2606    16446 #   portes portes_transportista_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.portes
    ADD CONSTRAINT portes_transportista_id_fkey FOREIGN KEY (transportista_id) REFERENCES public.transportistas(id);
 M   ALTER TABLE ONLY public.portes DROP CONSTRAINT portes_transportista_id_fkey;
       public          postgres    false    3222    219    221            <      x������ � �      >      x������ � �      :      x������ � �      6      x������ � �      8      x������ � �      4      x������ � �     