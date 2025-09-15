def criar_tabela(conexao, cursor):
  cursor.execute(
  "CREATE TABLE IF NOT EXISTS products (sku INTEGER PRIMARY KEY, titulo "
  "VARCHAR(100), preco REAL, preco_pix REAL, valor_parcela REAL, "
  "numero_parcelas INTEGER, informacoes_tecnicas VARCHAR(250))"
  )
  conexao.commit()

