import psycopg2
import time
import pandas as pd

# Conexão com o banco de dados
conn = psycopg2.connect(
    dbname="teste",
    user="postgres",
    password="a",
    host="localhost",
    port="5432"
)

# Lista de queries
queries = [
"SELECT * FROM tbl_rfid;",
"SELECT * FROM tbl_categoria;",
"SELECT * FROM tbl_cliente;",
"SELECT * FROM tbl_estabelecimento;",
"SELECT * FROM tbl_fornecedor;",
"SELECT * FROM tbl_produto;",
"SELECT * FROM tbl_funcionario;",
"SELECT * FROM tbl_pedido;",
"SELECT * FROM pedido_produto WHERE cp_id_pedido = 1;",
"SELECT * FROM estab_produto WHERE cp_cod_estab = 1;",
"SELECT * FROM forn_produto WHERE cp_cod_forn = 1;",
"SELECT * FROM tbl_cliente WHERE cp_cod_cliente = 1;",
"SELECT * FROM tbl_produto WHERE cp_id_produto = 1;",
"SELECT * FROM tbl_pedido WHERE ce_cod_cliente = 1;",
"SELECT * FROM tbl_produto WHERE ce_categoria_principal = 1;",
"SELECT * FROM estab_produto WHERE data_venda_estab = '2025-01-18';",
"SELECT * FROM tbl_estabelecimento WHERE cidade_estab = 'CDD';",
"SELECT * FROM estab_produto WHERE preco_venda_estab > 2.00;",
"SELECT * FROM tbl_funcionario WHERE ce_cod_estab = 1;",
"SELECT * FROM tbl_produto WHERE cd_ean_prod = '000000000001';"
"SELECT p.cp_id_pedido, p.data_pedido, p.hora_pedido, p.valor_total, c.nm_cliente FROM tbl_pedido p JOIN tbl_cliente c ON p.ce_cod_cliente = c.cp_cod_cliente;",
"SELECT pr.cp_id_produto, pr.nm_produto, c.nm_categoria FROM tbl_produto pr JOIN tbl_categoria c ON pr.ce_categoria_principal = c.cp_cod_categoria;",
"SELECT f.nm_forn, pr.nm_produto FROM forn_produto fp JOIN tbl_produto pr ON fp.cp_id_produto = pr.cp_id_produto JOIN tbl_fornecedor f ON fp.cp_cod_forn = f.cp_cod_forn;",
"SELECT e.nm_estab, pr.nm_produto FROM estab_produto ep JOIN tbl_produto pr ON ep.cp_id_produto = pr.cp_id_produto JOIN tbl_estabelecimento e ON ep.cp_cod_estab = e.cp_cod_estab;",
"SELECT p.cp_id_pedido, pr.nm_produto FROM pedido_produto pp JOIN tbl_produto pr ON pp.cp_id_produto = pr.cp_id_produto JOIN tbl_pedido p ON pp.cp_id_pedido = p.cp_id_pedido;",
"SELECT f.nm_func, e.nm_estab FROM tbl_funcionario f JOIN tbl_estabelecimento e ON f.ce_cod_estab = e.cp_cod_estab;",
"SELECT p.cp_id_pedido, p.valor_total, c.nm_cliente FROM tbl_pedido p JOIN tbl_cliente c ON p.ce_cod_cliente = c.cp_cod_cliente;",
"SELECT c.nm_categoria, pr.nm_produto FROM tbl_produto pr JOIN tbl_categoria c ON pr.ce_categoria_secundaria = c.cp_cod_categoria;",
"SELECT f.nm_forn, pr.nm_produto, fp.preco_venda_forn FROM forn_produto fp JOIN tbl_produto pr ON fp.cp_id_produto = pr.cp_id_produto JOIN tbl_fornecedor f ON fp.cp_cod_forn = f.cp_cod_forn;",
"SELECT pr.nm_produto, e.nm_estab, ep.preco_venda_estab FROM estab_produto ep JOIN tbl_produto pr ON ep.cp_id_produto = pr.cp_id_produto JOIN tbl_estabelecimento e ON ep.cp_cod_estab = e.cp_cod_estab;",
"SELECT pr.nm_produto, f.nm_forn, fp.preco_venda_forn, fp.data_vencimento FROM forn_produto fp JOIN tbl_produto pr ON fp.cp_id_produto = pr.cp_id_produto JOIN tbl_fornecedor f ON fp.cp_cod_forn = f.cp_cod_forn;",
"SELECT f.nm_func, e.nm_estab, e.cidade_estab FROM tbl_funcionario f JOIN tbl_estabelecimento e ON f.ce_cod_estab = e.cp_cod_estab;",
"SELECT f.nm_forn, pr.nm_produto, e.nm_estab FROM forn_produto fp JOIN tbl_produto pr ON fp.cp_id_produto = pr.cp_id_produto JOIN tbl_fornecedor f ON fp.cp_cod_forn = f.cp_cod_forn JOIN estab_produto ep ON pr.cp_id_produto = ep.cp_id_produto JOIN tbl_estabelecimento e ON ep.cp_cod_estab = e.cp_cod_estab;",
"SELECT e.nm_estab, e.localizacao_estab, f.nm_forn, f.localizacao_forn FROM tbl_estabelecimento e JOIN forn_produto fp ON e.cp_cod_estab = fp.cp_cod_forn JOIN tbl_fornecedor f ON fp.cp_cod_forn = f.cp_cod_forn;",
"SELECT p.cp_id_pedido, c.nm_cliente, p.data_pedido, p.hora_pedido FROM tbl_pedido p JOIN tbl_cliente c ON p.ce_cod_cliente = c.cp_cod_cliente;"
"WITH produto_vendido_estab AS (SELECT p.cp_id_produto, SUM(e.preco_venda_estab) AS total_vendas_estab FROM estab_produto e JOIN tbl_produto p ON e.cp_id_produto = p.cp_id_produto GROUP BY p.cp_id_produto), produto_vendido_forn AS (SELECT f.cp_id_produto, SUM(f.preco_venda_forn) AS total_vendas_forn FROM forn_produto f GROUP BY f.cp_id_produto), produto_union_vendas AS (SELECT cp_id_produto, total_vendas_estab AS total_vendas FROM produto_vendido_estab UNION ALL SELECT cp_id_produto, total_vendas_forn AS total_vendas FROM produto_vendido_forn) SELECT p.cp_id_produto, p.nm_produto, c.nm_categoria, SUM(u.total_vendas) OVER (PARTITION BY p.ce_categoria_principal) AS total_vendas_categoria, u.total_vendas FROM produto_union_vendas u JOIN tbl_produto p ON u.cp_id_produto = p.cp_id_produto LEFT JOIN tbl_categoria c ON p.ce_categoria_principal = c.cp_cod_categoria WHERE u.total_vendas > (SELECT AVG(total_vendas) FROM produto_union_vendas) ORDER BY total_vendas_categoria DESC, u.total_vendas DESC;",
"WITH vendas_por_estabelecimento AS (SELECT e.cp_cod_estab, e.cp_id_produto, SUM(e.preco_venda_estab) AS total_vendas_estab FROM estab_produto e GROUP BY e.cp_cod_estab, e.cp_id_produto), vendas_por_fornecedor AS (SELECT f.cp_cod_forn AS cp_cod_estab, f.cp_id_produto, SUM(f.preco_venda_forn) AS total_vendas_forn FROM forn_produto f GROUP BY f.cp_cod_forn, f.cp_id_produto), vendas_combinadas AS (SELECT cp_cod_estab, cp_id_produto, total_vendas_estab AS total_vendas FROM vendas_por_estabelecimento UNION ALL SELECT cp_cod_estab, cp_id_produto, total_vendas_forn AS total_vendas FROM vendas_por_fornecedor) SELECT e.nm_estab, c.nm_categoria, p.nm_produto, v.total_vendas, RANK() OVER (PARTITION BY e.nm_estab ORDER BY v.total_vendas DESC) AS ranking_por_estab FROM vendas_combinadas v JOIN tbl_estabelecimento e ON v.cp_cod_estab = e.cp_cod_estab JOIN tbl_produto p ON v.cp_id_produto = p.cp_id_produto JOIN tbl_categoria c ON p.ce_categoria_principal = c.cp_cod_categoria WHERE v.total_vendas > (SELECT AVG(total_vendas) FROM vendas_combinadas) GROUP BY e.nm_estab, c.nm_categoria, p.nm_produto, v.total_vendas ORDER BY e.nm_estab, ranking_por_estab;",
"WITH vendas_por_produto AS (SELECT p.cp_id_produto, SUM(e.preco_venda_estab) AS total_vendas_estab, SUM(f.preco_venda_forn) AS total_vendas_forn FROM tbl_produto p LEFT JOIN estab_produto e ON p.cp_id_produto = e.cp_id_produto LEFT JOIN forn_produto f ON p.cp_id_produto = f.cp_id_produto GROUP BY p.cp_id_produto), total_vendas_comb AS (SELECT cp_id_produto, COALESCE(total_vendas_estab, 0) + COALESCE(total_vendas_forn, 0) AS total_vendas FROM vendas_por_produto), vendas_totais_sistema AS (SELECT SUM(total_vendas) AS vendas_totais_sistema FROM total_vendas_comb) SELECT c.nm_categoria, COUNT(DISTINCT p.cp_id_produto) AS qtd_produtos, AVG(t.total_vendas) AS media_vendas_categoria, (SELECT vendas_totais_sistema FROM vendas_totais_sistema) AS vendas_totais_sistema FROM total_vendas_comb t JOIN tbl_produto p ON t.cp_id_produto = p.cp_id_produto JOIN tbl_categoria c ON p.ce_categoria_principal = c.cp_cod_categoria WHERE t.total_vendas > (SELECT AVG(total_vendas) FROM total_vendas_comb) GROUP BY c.nm_categoria ORDER BY media_vendas_categoria DESC;",
"WITH vendas_por_estabelecimento AS (SELECT e.cp_cod_estab, e.cp_id_produto, SUM(e.preco_venda_estab) AS total_vendas_estab FROM estab_produto e GROUP BY e.cp_cod_estab, e.cp_id_produto), vendas_por_fornecedor AS (SELECT f.cp_cod_forn AS cp_cod_estab, f.cp_id_produto, SUM(f.preco_venda_forn) AS total_vendas_forn FROM forn_produto f GROUP BY f.cp_cod_forn, f.cp_id_produto), vendas_combinadas AS (SELECT cp_cod_estab, cp_id_produto, total_vendas_estab AS total_vendas FROM vendas_por_estabelecimento UNION ALL SELECT cp_cod_estab, cp_id_produto, total_vendas_forn AS total_vendas FROM vendas_por_fornecedor), vendas_por_uf AS (SELECT e.uf_estab, SUM(v.total_vendas) AS total_vendas_uf FROM vendas_combinadas v JOIN tbl_estabelecimento e ON v.cp_cod_estab = e.cp_cod_estab GROUP BY e.uf_estab) SELECT e.uf_estab, e.cidade_estab, COUNT(DISTINCT v.cp_id_produto) AS qtd_produtos_vendidos, SUM(v.total_vendas) AS total_vendas_cidade, RANK() OVER (PARTITION BY e.uf_estab ORDER BY SUM(v.total_vendas) DESC) AS ranking_cidade_uf FROM vendas_combinadas v JOIN tbl_estabelecimento e ON v.cp_cod_estab = e.cp_cod_estab WHERE v.total_vendas > (SELECT AVG(total_vendas) FROM vendas_combinadas) GROUP BY e.uf_estab, e.cidade_estab ORDER BY e.uf_estab, ranking_cidade_uf;",
"WITH vendas_estab AS (SELECT e.cp_id_produto, SUM(e.preco_venda_estab) AS total_vendas_estab FROM estab_produto e GROUP BY e.cp_id_produto), vendas_forn AS (SELECT f.cp_id_produto, SUM(f.preco_venda_forn) AS total_vendas_forn FROM forn_produto f GROUP BY f.cp_id_produto), vendas_comb AS (SELECT cp_id_produto, COALESCE(total_vendas_estab, 0) + COALESCE(total_vendas_forn, 0) AS total_vendas FROM vendas_estab FULL OUTER JOIN vendas_forn USING (cp_id_produto)), categorias_vendas AS (SELECT c.nm_categoria, COUNT(p.cp_id_produto) AS qtd_produtos, SUM(v.total_vendas) AS total_vendas_categoria FROM tbl_produto p JOIN vendas_comb v ON p.cp_id_produto = v.cp_id_produto JOIN tbl_categoria c ON p.ce_categoria_principal = c.cp_cod_categoria GROUP BY c.nm_categoria), categoria_ranked AS (SELECT nm_categoria, qtd_produtos, total_vendas_categoria, RANK() OVER (ORDER BY total_vendas_categoria DESC) AS rank_vendas FROM categorias_vendas) SELECT cr.nm_categoria, cr.qtd_produtos, cr.total_vendas_categoria, cr.rank_vendas, AVG(v.total_vendas) AS media_vendas_produtos_categoria FROM categoria_ranked cr JOIN tbl_produto p ON p.ce_categoria_principal = (SELECT cp_cod_categoria FROM tbl_categoria WHERE nm_categoria = cr.nm_categoria LIMIT 1) JOIN vendas_comb v ON p.cp_id_produto = v.cp_id_produto WHERE cr.rank_vendas <= 3 GROUP BY cr.nm_categoria, cr.qtd_produtos, cr.total_vendas_categoria, cr.rank_vendas ORDER BY cr.rank_vendas;",
"WITH vendas_por_estabelecimento AS (SELECT p.cp_id_produto, e.cp_cod_estab, SUM(e.preco_venda_estab) AS total_vendas_estab FROM estab_produto e JOIN tbl_produto p ON e.cp_id_produto = p.cp_id_produto GROUP BY p.cp_id_produto, e.cp_cod_estab), vendas_por_fornecedor AS (SELECT p.cp_id_produto, f.cp_cod_forn, SUM(f.preco_venda_forn) AS total_vendas_forn FROM forn_produto f JOIN tbl_produto p ON f.cp_id_produto = p.cp_id_produto GROUP BY p.cp_id_produto, f.cp_cod_forn), vendas_combinadas AS (SELECT cp_id_produto, cp_cod_estab AS origem, total_vendas_estab AS total_vendas FROM vendas_por_estabelecimento UNION ALL SELECT cp_id_produto, cp_cod_forn AS origem, total_vendas_forn AS total_vendas FROM vendas_por_fornecedor), produtos_vendas_totais AS (SELECT p.cp_id_produto, p.nm_produto, c.nm_categoria, SUM(vc.total_vendas) AS total_vendas_produto, COUNT(DISTINCT vc.origem) AS qtd_origens FROM vendas_combinadas vc JOIN tbl_produto p ON vc.cp_id_produto = p.cp_id_produto JOIN tbl_categoria c ON p.ce_categoria_principal = c.cp_cod_categoria GROUP BY p.cp_id_produto, p.nm_produto, c.nm_categoria), ranking_produtos AS (SELECT nm_produto, nm_categoria, total_vendas_produto, qtd_origens, RANK() OVER (PARTITION BY nm_categoria ORDER BY total_vendas_produto DESC) AS rank_categoria FROM produtos_vendas_totais) SELECT rp.nm_produto, rp.nm_categoria, rp.total_vendas_produto, rp.qtd_origens, rp.rank_categoria, AVG(rp.total_vendas_produto) OVER () AS media_vendas_geral FROM ranking_produtos rp WHERE rp.rank_categoria <= 5 ORDER BY rp.nm_categoria, rp.rank_categoria;",
"WITH vendas_estabelecimentos AS (SELECT e.cp_cod_estab, e.cp_id_produto, SUM(e.preco_venda_estab) AS total_vendas_estab FROM estab_produto e GROUP BY e.cp_cod_estab, e.cp_id_produto), vendas_fornecedores AS (SELECT f.cp_cod_forn, f.cp_id_produto, SUM(f.preco_venda_forn) AS total_vendas_forn FROM forn_produto f GROUP BY f.cp_cod_forn, f.cp_id_produto), vendas_combinadas AS (SELECT p.cp_id_produto, COALESCE(e.cp_cod_estab, f.cp_cod_forn) AS origem, COALESCE(e.total_vendas_estab, 0) + COALESCE(f.total_vendas_forn, 0) AS total_vendas FROM vendas_estabelecimentos e FULL OUTER JOIN vendas_fornecedores f USING (cp_id_produto) JOIN tbl_produto p ON p.cp_id_produto = COALESCE(e.cp_id_produto, f.cp_id_produto)), vendas_por_estado AS (SELECT COALESCE(e.uf_estab, f.uf_forn) AS uf, vc.cp_id_produto, SUM(vc.total_vendas) AS total_vendas_estado FROM vendas_combinadas vc LEFT JOIN tbl_estabelecimento e ON vc.origem = e.cp_cod_estab LEFT JOIN tbl_fornecedor f ON vc.origem = f.cp_cod_forn GROUP BY COALESCE(e.uf_estab, f.uf_forn), vc.cp_id_produto), ranking_produtos_estado AS (SELECT vp.uf, p.nm_produto, SUM(vp.total_vendas_estado) AS vendas_produto_estado, RANK() OVER (PARTITION BY vp.uf ORDER BY SUM(vp.total_vendas_estado) DESC) AS rank_produto_estado FROM vendas_por_estado vp JOIN tbl_produto p ON vp.cp_id_produto = p.cp_id_produto GROUP BY vp.uf, p.nm_produto) SELECT rpe.uf, rpe.nm_produto, rpe.vendas_produto_estado, rpe.rank_produto_estado, (SELECT AVG(vendas_produto_estado) FROM ranking_produtos_estado) AS media_vendas_geral FROM ranking_produtos_estado rpe WHERE rpe.rank_produto_estado <= 3 ORDER BY rpe.uf, rpe.rank_produto_estado;",
"WITH vendas_estabelecimentos AS (SELECT e.cp_cod_estab AS origem, p.ce_categoria_principal AS categoria, COUNT(DISTINCT e.cp_id_produto) AS qtd_produtos_estab, SUM(e.preco_venda_estab) AS total_vendas_estab FROM estab_produto e JOIN tbl_produto p ON e.cp_id_produto = p.cp_id_produto GROUP BY e.cp_cod_estab, p.ce_categoria_principal), vendas_fornecedores AS (SELECT f.cp_cod_forn AS origem, p.ce_categoria_principal AS categoria, COUNT(DISTINCT f.cp_id_produto) AS qtd_produtos_forn, SUM(f.preco_venda_forn) AS total_vendas_forn FROM forn_produto f JOIN tbl_produto p ON f.cp_id_produto = p.cp_id_produto GROUP BY f.cp_cod_forn, p.ce_categoria_principal), vendas_combinadas AS (SELECT origem, categoria, COALESCE(qtd_produtos_estab, 0) + COALESCE(qtd_produtos_forn, 0) AS qtd_produtos, COALESCE(total_vendas_estab, 0) + COALESCE(total_vendas_forn, 0) AS total_vendas FROM vendas_estabelecimentos FULL OUTER JOIN vendas_fornecedores USING (origem, categoria)), ranking_categorias AS (SELECT vc.categoria, c.nm_categoria, vc.origem, vc.qtd_produtos, vc.total_vendas, RANK() OVER (PARTITION BY vc.categoria ORDER BY vc.total_vendas DESC) AS rank_vendas_categoria FROM vendas_combinadas vc JOIN tbl_categoria c ON vc.categoria = c.cp_cod_categoria) SELECT r.nm_categoria, r.origem, r.qtd_produtos, r.total_vendas, r.rank_vendas_categoria, (SELECT AVG(total_vendas) FROM ranking_categorias) AS media_vendas_geral FROM ranking_categorias r WHERE r.rank_vendas_categoria <= 3 ORDER BY r.nm_categoria, r.rank_vendas_categoria;",
"WITH preco_produto_fornecedor AS (SELECT f.nm_forn, p.nm_produto, e.preco_venda_estab, f.cp_cod_forn, p.cp_id_produto, ROW_NUMBER() OVER (PARTITION BY p.cp_id_produto ORDER BY e.preco_venda_estab DESC) AS rank_produto FROM estab_produto e JOIN tbl_produto p ON e.cp_id_produto = p.cp_id_produto JOIN tbl_fornecedor f ON e.cp_cod_estab = f.cp_cod_forn), produtos_vendidos_comparacao AS (SELECT ppf.nm_forn, ppf.nm_produto, ppf.preco_venda_estab, (SELECT AVG(preco_venda_estab) FROM estab_produto WHERE cp_id_produto = ppf.cp_id_produto) AS preco_medio_produto FROM preco_produto_fornecedor ppf WHERE ppf.rank_produto = 1), vendas_comparadas AS (SELECT nm_forn, nm_produto, preco_venda_estab, preco_medio_produto, (preco_venda_estab - preco_medio_produto) AS diferenca_preco FROM produtos_vendidos_comparacao) SELECT nm_forn, nm_produto, preco_venda_estab, preco_medio_produto, diferenca_preco, COUNT(*) OVER (PARTITION BY nm_forn) AS quantidade_fornecimentos FROM vendas_comparadas ORDER BY diferenca_preco DESC;",
"SELECT p.cp_id_pedido, p.ce_cod_cliente, p.data_pedido, p.hora_pedido, p.valor_total, SUM(ep.preco_venda_estab) AS preco_venda_total, ROW_NUMBER() OVER (PARTITION BY p.ce_cod_cliente ORDER BY p.data_pedido DESC) AS rank_pedido FROM tbl_pedido p JOIN pedido_produto pp ON pp.cp_id_pedido = p.cp_id_pedido JOIN estab_produto ep ON ep.cp_id_produto = pp.cp_id_produto WHERE p.data_pedido BETWEEN '2025-01-01' AND '2025-12-31' GROUP BY p.cp_id_pedido, p.ce_cod_cliente, p.data_pedido, p.hora_pedido, p.valor_total UNION SELECT p.cp_id_pedido, p.ce_cod_cliente, p.data_pedido, p.hora_pedido, p.valor_total, 0 AS preco_venda_total, NULL AS rank_pedido FROM tbl_pedido p WHERE p.ce_cod_cliente IN (SELECT cp_cod_cliente FROM tbl_cliente WHERE cpf_cliente = '12345678901') ORDER BY data_pedido DESC;"
]

# Dicionário para armazenar os tempos de execução
execution_times_indexed = {query: [] for query in queries}

# Executar as queries 50 vezes
for _ in range(50):
    for query in queries:
        start_time = time.time()
        with conn.cursor() as cursor:
            cursor.execute(query)
        end_time = time.time()
        execution_times_indexed[query].append(end_time - start_time)

# Fechar a conexão
conn.close()

# Criar um DataFrame com os tempos de execução após a indexação
df_indexed = pd.DataFrame(execution_times_indexed)
df_indexed.to_csv("indexed.csv", index=False)

# Carregar a baseline
df_baseline = pd.read_csv("baseline.csv")

# Calcular o speedup
speedup = df_baseline.mean() / df_indexed.mean()

# Criar um DataFrame com os resultados
df_speedup = pd.DataFrame({
    'Query': queries,
    'Baseline Time': df_baseline.mean(),
    'Indexed Time': df_indexed.mean(),
    'Speedup': speedup
})

# Salvar a planilha de melhoria de desempenho
df_speedup.to_csv("performance_improvement.csv", index=False)