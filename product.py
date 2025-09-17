from datetime import datetime


class Product:
    def __init__(self, sku, titulo, preco, preco_pix, valor_parcela, numero_parcelas, informacoes_tecnicas):
        self.sku = sku
        self.titulo = titulo
        self.preco = preco
        self.preco_pix = preco_pix
        self.valor_parcela = valor_parcela
        self.numero_parcelas = numero_parcelas
        self.informacoes_tecnicas = informacoes_tecnicas
        self.data_criacao = datetime.now()

    @property
    def sku(self):
        return self._sku

    @property
    def titulo(self):
        return self._titulo

    @property
    def preco(self):
        return self._preco

    @property
    def preco_pix(self):
        return self._preco_pix

    @property
    def valor_parcela(self):
        return self._valor_parcela

    @property
    def numero_parcelas(self):
        return self._numero_parcelas

    @property
    def informacoes_tecnicas(self):
        return self._informacoes_tecnicas

    @property
    def data_criacao(self):
        return self._data_criacao

    @sku.setter
    def sku(self, new):
            self._sku = new

    @titulo.setter
    def titulo(self, new):
            self._titulo = new


    @preco.setter
    def preco(self, new):
            self._preco = new


    @preco_pix.setter
    def preco_pix(self, new):
            self._preco_pix = new


    @valor_parcela.setter
    def valor_parcela(self, new):
            self._valor_parcela = new


    @numero_parcelas.setter
    def numero_parcelas(self, new):
            self._numero_parcelas = new


    @informacoes_tecnicas.setter
    def informacoes_tecnicas(self, new):
            self._informacoes_tecnicas = new

    @data_criacao.setter
    def data_criacao(self, new):
        self._data_criacao = new