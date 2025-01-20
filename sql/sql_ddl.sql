--CRIAR TABELAS--
CREATE TABLE tbl_rfid (
	cp_id_dispositivo int PRIMARY KEY,
	ind_venda_dispositivo boolean
);

CREATE TABLE tbl_categoria (
	cp_cod_categoria int PRIMARY KEY,
	nm_categoria varchar(20)
);

CREATE TABLE tbl_cliente (
	cp_cod_cliente serial PRIMARY KEY,
	nm_cliente varchar(200),
	cpf_cliente varchar(11) UNIQUE
);

CREATE TABLE tbl_estabelecimento (
	cp_cod_estab int PRIMARY KEY,
	nm_estab varchar(60),
	cnpj_estab varchar(60) UNIQUE,
	localizacao_estab real[8],
	endereco_estab varchar(200),
	uf_estab varchar(2),
	cidade_estab varchar(5)
);

CREATE TABLE tbl_fornecedor (
	cp_cod_forn int PRIMARY KEY,
	cnpj_forn varchar(14) UNIQUE,
	nm_forn varchar(60),
	localizacao_forn real[8],
	endereco_forn int,
	uf_forn varchar(2),
	cidade_forn varchar(5)
);

CREATE TABLE tbl_produto (
	cp_id_produto serial PRIMARY KEY,
	ce_rfid int UNIQUE REFERENCES tbl_rfid(cp_id_dispositivo),
	cd_ean_prod varchar(12),
	nm_produto varchar(60),
	ce_categoria_principal int REFERENCES tbl_categoria(cp_cod_categoria),
	ce_categoria_secundaria int REFERENCES tbl_categoria(cp_cod_categoria)
);

CREATE TABLE tbl_funcionario (
	cp_cod_func int PRIMARY KEY,
	nm_func varchar(200),
	cpf_func varchar(11) UNIQUE,
	funcao_func varchar(40),
	ce_cod_estab int REFERENCES tbl_estabelecimento(cp_cod_estab)
);

CREATE TABLE tbl_pedido (
	cp_id_pedido serial PRIMARY KEY,
	ce_cod_cliente int REFERENCES tbl_cliente(cp_cod_cliente),
	data_pedido date,
	hora_pedido time,
	valor_total real
);

CREATE TABLE pedido_produto (
	cp_id_pedido int REFERENCES tbl_pedido(cp_id_pedido),
	cp_id_produto int REFERENCES tbl_produto(cp_id_produto),
	PRIMARY KEY (cp_id_pedido, cp_id_produto)
);

CREATE TABLE estab_produto (
	cp_cod_estab int REFERENCES tbl_estabelecimento(cp_cod_estab),
	cp_id_produto int REFERENCES tbl_produto(cp_id_produto),
	data_venda_estab date,
	preco_venda_estab real,
	PRIMARY KEY (cp_cod_estab, cp_id_produto)
);

CREATE TABLE forn_produto (
	cp_cod_forn int REFERENCES tbl_fornecedor(cp_cod_forn),
	cp_id_produto int REFERENCES tbl_produto(cp_id_produto),
	data_venda_forn date,
	data_vencimento date,
	preco_venda_forn real,
	PRIMARY KEY (cp_cod_forn, cp_id_produto)
);

-- Reiniciar todas as sequências para começarem em 1
ALTER SEQUENCE tbl_cliente_cp_cod_cliente_seq RESTART WITH 1;
ALTER SEQUENCE tbl_produto_cp_id_produto_seq RESTART WITH 1;
ALTER SEQUENCE tbl_pedido_cp_id_pedido_seq RESTART WITH 1;
