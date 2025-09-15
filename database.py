def atualizar_produto(conexao, cursor, titulo, preco, preco_pix,
                     valor_parcela, numero_parcelas, informacoes_tecnicas, sku):
  data = (sku, titulo, preco, preco_pix, valor_parcela, numero_parcelas, informacoes_tecnicas, sku)
  cursor.execute("UPDATE products SET sku=?, titulo=?, preco=?, preco_pix=?, valor_parcela=?, "
                 "numero_parcelas=?, informacoes_tecnicas=? WHERE sku=?;", data)
  conexao.commit()

def inserir_registro(conexao, cursor, titulo, preco, preco_pix,
                     valor_parcela, numero_parcelas, informacoes_tecnicas, sku):
  data = (sku, titulo, preco, preco_pix, valor_parcela, numero_parcelas, informacoes_tecnicas)
  cursor.execute("""
      INSERT INTO products (sku, titulo, preco, preco_pix, valor_parcela, numero_parcelas, informacoes_tecnicas) 
      VALUES (?, ?, ?, ?, ?, ?, ?);
  """, data)
  conexao.commit()

def verifica_se_o_produto_existe(cursor, sku_do_produto):
    cursor.execute("SELECT titulo, sku FROM products WHERE sku=?", (sku_do_produto,))
    sinaliza_se_existe = cursor.fetchone()
    if sinaliza_se_existe:
        return True
    return False