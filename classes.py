from datetime import datetime


class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.favoritos = []
        self.reservas = []

    def adicionar_favorito(self, propriedade):
        if propriedade not in self.favoritos:
            self.favoritos.append(propriedade)

    def remover_favorito(self, propriedade):
        if propriedade in self.favoritos:
            self.favoritos.remove(propriedade)

    def fazer_reserva(self, propriedade, data_inicio, data_fim):
        reserva = Reserva(self, propriedade, data_inicio, data_fim)
        self.reservas.append(reserva)
        propriedade.reservas.append(reserva)
        return reserva


class Propriedade:
    def __init__(self, nome, localizacao, capacidade, anfitriao):
        self.nome = nome
        self.localizacao = localizacao
        self.capacidade = capacidade
        self.anfitriao = anfitriao
        self.reservas = []
        self.avaliacoes = []
        self.duvidas = []

    def esta_disponivel(self, data_inicio, data_fim):
        for reserva in self.reservas:
            if not (data_fim <= reserva.data_inicio or data_inicio >= reserva.data_fim):
                return False
        return True

    def adicionar_avaliacao(self, avaliacao):
        self.avaliacoes.append(avaliacao)

    def media_avaliacoes(self):
        if not self.avaliacoes:
            return 0
        return sum(a.nota for a in self.avaliacoes) / len(self.avaliacoes)

    def adicionar_duvida(self, pergunta, resposta):
        self.duvidas.append({"pergunta": pergunta, "resposta": resposta})


class Reserva:
    def __init__(self, usuario, propriedade, data_inicio, data_fim):
        self.usuario = usuario
        self.propriedade = propriedade
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.status = "ativa"

    def concluir(self):
        self.status = "concluída"



class Avaliacao:
    def __init__(self, usuario, nota, comentario):
        self.usuario = usuario
        self.nota = nota  # estrelas (1 a 5)
        self.comentario = comentario


class Mensagem:
    def __init__(self, remetente, texto):
        self.remetente = remetente
        self.texto = texto
        self.data = datetime.now()


class Chat:
    def __init__(self, usuario, anfitriao):
        self.usuario = usuario
        self.anfitriao = anfitriao
        self.mensagens = []

    def enviar_mensagem(self, remetente, texto):
        msg = Mensagem(remetente, texto)
        self.mensagens.append(msg)


class Sistema:
    def __init__(self):
        self.usuarios = []
        self.propriedades = []

    def cadastrar_usuario(self, nome, email, senha):
        user = Usuario(nome, email, senha)
        self.usuarios.append(user)
        return user

    def anunciar_propriedade(self, nome, localizacao, capacidade, anfitriao):
        prop = Propriedade(nome, localizacao, capacidade, anfitriao)
        self.propriedades.append(prop)
        return prop

    def buscar(self, localizacao, capacidade, data_inicio, data_fim):
        resultados = []
        for prop in self.propriedades:
            if (
                prop.localizacao == localizacao
                and prop.capacidade >= capacidade
                and prop.esta_disponivel(data_inicio, data_fim)
            ):
                resultados.append(prop)
        return resultados