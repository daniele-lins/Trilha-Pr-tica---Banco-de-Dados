--tbl_rfid
DO $$
BEGIN
	FOR i IN 1..200 LOOP
    	INSERT INTO tbl_rfid (cp_id_dispositivo, ind_venda_dispositivo)
    	VALUES (i, 0::boolean);
	END LOOP;
END $$;

--tbl_categoria
DO $$
DECLARE
	v_nome_categoria varchar(20);
BEGIN
	FOR i IN 1..200 LOOP
    	v_nome_categoria := 'Categoria ' || i;
   	 
    	INSERT INTO tbl_categoria (cp_cod_categoria, nm_categoria)
    	VALUES (i, v_nome_categoria);
	END LOOP;
END $$;

--tbl_cliente
DO $$
DECLARE
	v_nome_cliente varchar(200);
	v_cpf_cliente varchar(11);
BEGIN
	FOR i IN 1..200 LOOP
    	v_nome_cliente := 'Cliente ' || i;
    	v_cpf_cliente := LPAD(i::text, 11, '0');  -- Gerando um CPF sequencial (00000000001, 00000000002, etc.)
   	 
    	INSERT INTO tbl_cliente (nm_cliente, cpf_cliente)
    	VALUES (v_nome_cliente, v_cpf_cliente);
	END LOOP;
END $$;

--tbl_estabelecimento
DO $$
DECLARE
	v_nome_estab varchar(60);
	v_cnpj_estab varchar(60);
	v_localizacao_estab real[8];
	v_endereco_estab varchar(200);
	v_uf_estab varchar(2);
	v_cidade_estab varchar(5);
BEGIN
	FOR i IN 1..200 LOOP
    	v_nome_estab := 'Estabelecimento ' || i;
    	v_cnpj_estab := LPAD(i::text, 14, '0') || '0001';  -- Gerando um CNPJ fictício com 14 dígitos
    	v_localizacao_estab := ARRAY[
        	random(), random(), random(), random(), random(), random(), random(), random()
    	];  -- Gerando 8 números reais aleatórios para a localização
    	v_endereco_estab := 'Endereço ' || i;
    	v_uf_estab := 'UF';
    	v_cidade_estab := 'CDD';

    	INSERT INTO tbl_estabelecimento (
        	cp_cod_estab, nm_estab, cnpj_estab, localizacao_estab, endereco_estab, uf_estab, cidade_estab
    	)
    	VALUES (i, v_nome_estab, v_cnpj_estab, v_localizacao_estab, v_endereco_estab, v_uf_estab, v_cidade_estab);
	END LOOP;
END $$;

--tbl_fornecedor
DO $$
DECLARE
	v_nome_forn varchar(60);
	v_cnpj_forn varchar(14);
	v_localizacao_forn real[8];
	v_endereco_forn int;
	v_uf_forn varchar(2);
	v_cidade_forn varchar(5);
BEGIN
	FOR i IN 1..200 LOOP
    	v_nome_forn := 'Fornecedor ' || i;
    	v_cnpj_forn := LPAD(i::text, 14, '0');  -- Gerando um CNPJ fictício com 14 dígitos
    	v_localizacao_forn := ARRAY[
        	random(), random(), random(), random(), random(), random(), random(), random()
    	];  -- Gerando 8 números reais aleatórios para a localização
    	v_endereco_forn := i * 1000;  -- Gerando um número inteiro para o endereço
    	v_uf_forn := 'UF';
    	v_cidade_forn := 'CDD';

    	INSERT INTO tbl_fornecedor (
        	cp_cod_forn, cnpj_forn, nm_forn, localizacao_forn, endereco_forn, uf_forn, cidade_forn
    	)
    	VALUES (i, v_cnpj_forn, v_nome_forn, v_localizacao_forn, v_endereco_forn, v_uf_forn, v_cidade_forn);
	END LOOP;
END $$;

--tbl_produto
DO $$
DECLARE
	v_nome_produto varchar(60);
	v_cd_ean_prod varchar(12);
	v_ce_rfid int;
BEGIN
	FOR i IN 1..200 LOOP
    	v_nome_produto := 'Produto ' || i;
    	v_cd_ean_prod := LPAD(i::text, 12, '0');  -- Gerando um EAN fictício de 12 dígitos
    	v_ce_rfid := i;  -- Atribuindo o cp_id_dispositivo da tbl_rfid como ce_rfid

    	INSERT INTO tbl_produto (
        	ce_rfid, cd_ean_prod, nm_produto, ce_categoria_principal, ce_categoria_secundaria
    	)
    	VALUES (v_ce_rfid, v_cd_ean_prod, v_nome_produto, 1, 2);  -- Categoria principal = 1, Secundária = 2
	END LOOP;
END $$;

--tbl_funcionario
DO $$
DECLARE
	v_nome_func varchar(200);
	v_cpf_func varchar(11);
	v_funcao_func varchar(40);
	v_ce_cod_estab int;
BEGIN
	FOR i IN 1..200 LOOP
    	v_nome_func := 'Funcionário ' || i;
    	v_cpf_func := LPAD(i::text, 11, '0');  -- Gerando um CPF fictício com 11 dígitos
    	v_funcao_func := 'Função ' || i;  -- Função genérica como "Função 1", "Função 2", etc.
    	v_ce_cod_estab := 1;  -- Associando a um estabelecimento existente (usando o id de 1 a 200)

    	INSERT INTO tbl_funcionario (
        	cp_cod_func, nm_func, cpf_func, funcao_func, ce_cod_estab
    	)
    	VALUES (i, v_nome_func, v_cpf_func, v_funcao_func, v_ce_cod_estab);
	END LOOP;
END $$;

--tbl_pedido
DO $$
DECLARE
	v_data_pedido date;
	v_hora_pedido time;
	v_valor_total real;
	v_ce_cod_cliente int;
BEGIN
	v_data_pedido := '2025-01-18';  -- Data fixa para todos os pedidos
	v_hora_pedido := '12:00:00';	-- Hora fixa para todos os pedidos
	v_valor_total := 0;          	-- Valor total fixo igual a 0

	FOR i IN 1..200 LOOP
    	v_ce_cod_cliente := i;  -- Atribuindo o código do cliente sequencial

    	INSERT INTO tbl_pedido (
        	cp_id_pedido, ce_cod_cliente, data_pedido, hora_pedido, valor_total
    	)
    	VALUES (i, v_ce_cod_cliente, v_data_pedido, v_hora_pedido, v_valor_total);
	END LOOP;
END $$;

--pedido_produto
DO $$
DECLARE
	v_cp_id_pedido int;
	v_cp_id_produto int;
BEGIN
	FOR i IN 1..200 LOOP
    	v_cp_id_pedido := i; 	-- Referenciando o pedido com o id igual à iteração
    	v_cp_id_produto := i;	-- Referenciando o produto com o id igual à iteração

    	INSERT INTO pedido_produto (
        	cp_id_pedido, cp_id_produto
    	)
    	VALUES (v_cp_id_pedido, v_cp_id_produto);
	END LOOP;
END $$;

--estab_produto
DO $$
DECLARE
	v_data_venda_estab date;
	v_preco_venda_estab real;
	v_cp_id_produto int;
BEGIN
	v_data_venda_estab := '2025-01-18';  -- Data fixa para todas as vendas
	v_preco_venda_estab := 2.50;    	-- Preço de venda fixo para todos os produtos

	FOR i IN 1..200 LOOP
    	v_cp_id_produto := i;  -- Atribui o código do produto sequencial

    	INSERT INTO estab_produto (
        	cp_cod_estab, cp_id_produto, data_venda_estab, preco_venda_estab
    	)
    	VALUES (1, v_cp_id_produto, v_data_venda_estab, v_preco_venda_estab);
	END LOOP;
END $$;

--forn_produto
DO $$
DECLARE
	v_data_venda_forn date;
	v_data_vencimento date;
	v_preco_venda_forn real;
	v_cp_id_produto int;
BEGIN
	v_data_venda_forn := '2025-01-18';   -- Data fixa para todas as vendas
	v_data_vencimento := '2025-12-31';   -- Data fixa para o vencimento de todos os produtos
	v_preco_venda_forn := 2.00;      	-- Preço fixo de venda para todos os produtos

	FOR i IN 1..200 LOOP
    	v_cp_id_produto := i;  -- Atribui o código do produto sequencial

    	INSERT INTO forn_produto (
        	cp_cod_forn, cp_id_produto, data_venda_forn, data_vencimento, preco_venda_forn
    	)
    	VALUES (1, v_cp_id_produto, v_data_venda_forn, v_data_vencimento, v_preco_venda_forn);
	END LOOP;
END $$;
