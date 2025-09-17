def criar_tabela(conexao, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            sku TEXT PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            preco REAL NOT NULL,
            preco_pix REAL,
            valor_parcela REAL,
            numero_parcelas INTEGER,
            informacoes_tecnicas TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conexao.commit()

