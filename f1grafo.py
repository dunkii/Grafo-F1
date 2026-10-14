import math
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

#1) CRIAÇÃO DO GRAFO

grafo = {}


def adicionar_setor(nome):
    #Todo setor começa sem nenhum trecho saindo dele
    grafo[nome] = {}


def adicionar_trecho(origem, destino, custo):
    #Destino com o custo em segundos
    grafo[origem][destino] = custo


#Posição (x, y) de cada setor
posicoes = {
    "Largada": (70, 320),
    "Reta dos Boxes": (200, 320),
    "Box": (330, 430),
    "Senna S": (300, 200),
    "Curva do Sol": (470, 130),
    "Reta Oposta": (650, 110),
    "Descida do Lago": (540, 290),
    "Caixa de Brita": (730, 260),
    "Laranjinha": (640, 420),
    "Mergulho": (520, 540),
    "Junção": (330, 570),
    "Bandeirada": (110, 500),
}

for nome_setor in posicoes:
    adicionar_setor(nome_setor)

adicionar_trecho("Largada", "Reta dos Boxes", 2)
adicionar_trecho("Reta dos Boxes", "Senna S", 3)
adicionar_trecho("Reta dos Boxes", "Box", 2)
adicionar_trecho("Box", "Senna S", 2)
adicionar_trecho("Senna S", "Curva do Sol", 3)
adicionar_trecho("Curva do Sol", "Reta Oposta", 3)
adicionar_trecho("Curva do Sol", "Descida do Lago", 2)
adicionar_trecho("Reta Oposta", "Descida do Lago", 2)
adicionar_trecho("Reta Oposta", "Caixa de Brita", 1)
adicionar_trecho("Descida do Lago", "Laranjinha", 3)
adicionar_trecho("Laranjinha", "Mergulho", 3)
adicionar_trecho("Laranjinha", "Junção", 5)
adicionar_trecho("Mergulho", "Junção", 2)
adicionar_trecho("Junção", "Reta dos Boxes", 2)
adicionar_trecho("Junção", "Bandeirada", 3)
adicionar_trecho("Bandeirada", "Reta dos Boxes", 2)

#2) DADOS DO JOGO

RAIO = 26

COR_FUNDO = "#14161c"
COR_PAINEL = "#1d2029"
COR_TEXTO = "#e8e8e8"
COR_VERMELHO = "#e10600"
COR_AMARELO = "#ffd43b"
COR_VERDE = "#35e05a"

descricoes = {
    "Largada": "É dada a largada!! Começa o GP de Interlagos",
    "Reta dos Boxes": "A longa reta principal. Atenção aos boxes",
    "Box": "Pit lane! A equipe está pronta para o pit stop.",
    "Senna S": "Os pilotos entram no S do Senna",
    "Curva do Sol": "Grande oportunidade de ultrapassagem, atenção agora!!",
    "Reta Oposta": "Reta longa. Quem erra a frenagem acaba na brita!",
    "Descida do Lago": "Cuidado com a curva aqui. ",
    "Caixa de Brita": "Escapou... o carro atolou na brita e não sai mais...",
    "Laranjinha": "Curva fechada, exige frenagem forte.",
    "Mergulho": "Arriscou a ultrapassagem, será que vai dar??",
    "Junção": "Última curva antes da chegada.",
    "Bandeirada": "Vem no capricho...",
}

#Opções de risco
obstaculos_iniciais = {
    "Senna S": ("Acidente na pista!",
                "Você desviou dos carros batidos.",
                "Você bateu de raspão e perdeu 4 segundos.", 4, 10),
    "Descida do Lago": ("Chuva forte!",
                        "Você controlou o carro no molhado.",
                        "Você derrapou e perdeu 5 segundos.", 5, 11),
    "Mergulho": ("Carro quebrado na pista!",
                 "Você passou pelo lado sem problemas.",
                 "Você freou forte e perdeu 6 segundos.", 6, 12),
}

itens_iniciais = {
    "Box": "Pit stop obrigatório",
    "Curva do Sol": "Kit aerodinâmico",
}

#3) JANELA DO JOGO

class JogoF1:

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Grande Prêmio de Interlagos - Grafos")
        self.janela.configure(bg=COR_FUNDO)
        self.janela.resizable(False, False)

        self.nome_piloto = "Piloto"
        self.montar_interface()

        nome = simpledialog.askstring("Piloto", "Digite o nome do seu piloto:",
                                      parent=self.janela)
        if nome:
            self.nome_piloto = nome

        self.novo_jogo()

    # Montagem da interface

    def montar_interface(self):
        #Zona do grafo
        self.canvas = tk.Canvas(self.janela, width=800, height=640,
                                bg=COR_FUNDO, highlightthickness=0)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self.clicar)

        #Painel da direita
        painel = tk.Frame(self.janela, bg=COR_PAINEL, width=360, height=640)
        painel.grid(row=0, column=1)
        painel.pack_propagate(False)

        fonte = ("Segoe UI", 10)

        tk.Label(painel, text="GRANDE PRÊMIO DE INTERLAGOS - GRAFOS", bg=COR_PAINEL,
                 fg=COR_VERMELHO, font=("Segoe UI", 13, "bold")
                 ).pack(pady=(10, 6))

        self.lbl_piloto = tk.Label(painel, bg=COR_PAINEL, fg=COR_TEXTO, font=fonte)
        self.lbl_piloto.pack(anchor="w", padx=12)

        self.lbl_local = tk.Label(painel, bg=COR_PAINEL, fg=COR_TEXTO, font=fonte)
        self.lbl_local.pack(anchor="w", padx=12)

        self.lbl_tempo = tk.Label(painel, bg=COR_PAINEL, fg=COR_TEXTO, font=fonte)
        self.lbl_tempo.pack(anchor="w", padx=12)

        self.lbl_pit = tk.Label(painel, bg=COR_PAINEL, fg=COR_TEXTO, font=fonte)
        self.lbl_pit.pack(anchor="w", padx=12)

        tk.Button(painel, text="Novo jogo", width=20,
                  command=self.novo_jogo).pack(pady=10)

        #Lista de adjacências
        tk.Label(painel, text="Lista de adjacências (setor -> destinos e custos)",
                 bg=COR_PAINEL, fg=COR_TEXTO, font=("Segoe UI", 9, "bold")
                 ).pack(anchor="w", padx=12)
        self.txt_adj = tk.Text(painel, width=46, height=14, bg="#0d0e12",
                               fg=COR_TEXTO, font=("Consolas", 8),
                               highlightthickness=0, wrap="word")
        self.txt_adj.pack(padx=12, pady=2)
        self.txt_adj.tag_configure("atual", background="#7a1410")

        #Registro de eventos
        tk.Label(painel, text="Rádio / Eventos", bg=COR_PAINEL, fg=COR_TEXTO,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=12, pady=(8, 0))
        self.log = tk.Text(painel, width=44, height=9, bg="#0d0e12",
                           fg=COR_TEXTO, font=("Consolas", 9),
                           highlightthickness=0, wrap="word", state="disabled")
        self.log.pack(padx=12, pady=(2, 8))

    #Controle do jogo

    def novo_jogo(self):
        self.setor = "Largada"
        self.tempo = 0
        self.bonus = 0
        self.pit_feito = False
        self.fim = False
        self.itens = dict(itens_iniciais)
        self.obstaculos = dict(obstaculos_iniciais)
        self.visitados = []

        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

        self.registrar("Bem-vindo, " + self.nome_piloto + "! Chegue à Bandeirada,")
        self.registrar("mas passe no Box para o pit stop obrigatório.")
        self.registrar("Clique num círculo vizinho para dirigir até ele.")

        self.entrar_no_setor("Largada")

    def registrar(self, texto):
        self.log.configure(state="normal")
        self.log.insert("end", texto + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def fim_de_jogo(self, mensagem, vitoria=False):
        self.fim = True
        self.registrar(mensagem)
        self.atualizar_painel()
        self.desenhar()
        if vitoria:
            messagebox.showinfo("Bandeira quadriculada!", mensagem)
        else:
            messagebox.showerror("Abandono (DNF)", mensagem)

    #Movimento e eventos

    def clicar(self, evento):
        if self.fim:
            return
        for setor in posicoes:
            x, y = posicoes[setor]
            if math.hypot(evento.x - x, evento.y - y) <= RAIO + 4:
                self.mover(setor)
                return

    def mover(self, destino):
        if destino == self.setor:
            return

        if destino not in grafo[self.setor]:
            self.registrar("Não há pista direta de " + self.setor + " para "
                           + destino + ". Siga o sentido das setas!")
            return

        custo = grafo[self.setor][destino]
        self.tempo = self.tempo + custo
        self.registrar("-> " + destino + " (+" + str(custo) + " s)")
        self.entrar_no_setor(destino)

    def entrar_no_setor(self, setor):
        self.setor = setor
        if setor not in self.visitados:
            self.visitados.append(setor)
        self.registrar(descricoes[setor])
        self.atualizar_painel()
        self.desenhar()
        self.janela.update()

        if setor in self.obstaculos:
            self.enfrentar_obstaculo(setor)

        if setor in self.itens:
            self.pegar_item(setor)

        if setor == "Bandeirada":
            self.cruzar_linha()
        elif len(grafo[setor]) == 0:
            self.fim_de_jogo("Você ficou atolado em " + setor + ". Abandono!")

        self.atualizar_painel()
        self.desenhar()

    def enfrentar_obstaculo(self, setor):
        aviso, texto_ok, texto_falha, segundos, dificuldade = self.obstaculos[setor]

        #Dado é rolado para decisão de evento
        dado = random.randint(1, 20) + self.bonus

        if dado >= dificuldade:
            resultado = texto_ok
        else:
            resultado = texto_falha
            self.tempo = self.tempo + segundos

        del self.obstaculos[setor]
        self.registrar(aviso + " " + resultado)
        messagebox.showinfo(aviso, resultado)

    def pegar_item(self, setor):
        item = self.itens[setor]

        if item == "Pit stop obrigatório":
            self.pit_feito = True
            self.tempo = self.tempo + 3
            self.registrar("PIT STOP feito! Foram 3 segundos parado.")
        elif item == "Kit aerodinâmico":
            self.bonus = self.bonus + 3
            self.registrar("Kit aerodinâmico instalado! O carro está mais estável.")

        del self.itens[setor]

    def cruzar_linha(self):
        if self.pit_feito:
            self.fim_de_jogo("VITÓRIA, " + self.nome_piloto + "! Tempo total: "
                             + str(self.tempo) + " segundos.", vitoria=True)
        else:
            self.registrar("Você cruzou a linha SEM o pit stop obrigatório!")
            messagebox.showwarning(
                "Pit stop obrigatório",
                "Você cruzou a linha sem fazer o pit stop obrigatório.\n"
                "Dê mais uma volta passando pelo Box!")

    #Painel e desenho
    def atualizar_painel(self):
        self.lbl_piloto.configure(text="Piloto: " + self.nome_piloto)
        self.lbl_local.configure(text="Local: " + self.setor)
        self.lbl_tempo.configure(text="Tempo de corrida: " + str(self.tempo) + " s")

        if self.pit_feito:
            self.lbl_pit.configure(text="Pit stop obrigatório: FEITO", fg=COR_VERDE)
        else:
            self.lbl_pit.configure(text="Pit stop obrigatório: PENDENTE",
                                   fg=COR_AMARELO)

        #Lista de adjacências
        self.txt_adj.configure(state="normal")
        self.txt_adj.delete("1.0", "end")
        numero_linha = 1
        for setor in grafo:
            partes = []
            for destino in grafo[setor]:
                partes.append(destino + "(" + str(grafo[setor][destino]) + ")")
            linha = setor + " -> " + ", ".join(partes)
            if len(partes) == 0:
                linha = setor + " -> (sem saída)"
            self.txt_adj.insert("end", linha + "\n")
            if setor == self.setor:
                self.txt_adj.tag_add("atual", str(numero_linha) + ".0",
                                     str(numero_linha) + ".end")
            numero_linha = numero_linha + 1
        self.txt_adj.configure(state="disabled")

    def desenhar(self):
        c = self.canvas
        c.delete("all")

        c.create_text(14, 16, anchor="w", fill=COR_TEXTO, font=("Segoe UI", 9),
                      text="Círculo vermelho = seu carro   |   Losango amarelo = item"
                           "   |   Triângulo laranja = perigo")
        c.create_text(14, 36, anchor="w", fill=COR_TEXTO, font=("Segoe UI", 9),
                      text="Seta = sentido da pista (mão única)   |   Número na seta"
                           " = custo em segundos")

        self.desenhar_arestas()
        for setor in posicoes:
            self.desenhar_vertice(setor)

    def desenhar_arestas(self):
        c = self.canvas

        for origem in grafo:
            for destino in grafo[origem]:
                x1, y1 = posicoes[origem]
                x2, y2 = posicoes[destino]

                dx = x2 - x1
                dy = y2 - y1
                distancia = math.hypot(dx, dy)
                ux = dx / distancia
                uy = dy / distancia

                c.create_line(x1 + ux * RAIO, y1 + uy * RAIO,
                              x2 - ux * (RAIO + 3), y2 - uy * (RAIO + 3),
                              fill="#8a8f98", width=2, arrow=tk.LAST,
                              arrowshape=(13, 15, 5))

                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2
                c.create_rectangle(mx - 11, my - 9, mx + 11, my + 9,
                                   fill=COR_FUNDO, outline="#8a8f98")
                c.create_text(mx, my, text=str(grafo[origem][destino]),
                              fill="white", font=("Segoe UI", 9, "bold"))

    def cor_do_setor(self, setor):
        if setor == "Box":
            return "#1f5fbf"
        if setor == "Caixa de Brita":
            return "#b8995a"
        if setor == "Largada":
            return "#2f8f4e"
        return "#3a4052"

    def desenhar_vertice(self, setor):
        c = self.canvas
        x, y = posicoes[setor]

        if not self.fim and setor in grafo[self.setor]:
            c.create_oval(x - RAIO - 6, y - RAIO - 6, x + RAIO + 6, y + RAIO + 6,
                          outline=COR_AMARELO, width=2, dash=(4, 3))

        contorno = "#9aa0ac"
        if setor in self.visitados:
            contorno = "#8be9fd"

        if setor == self.setor:
            c.create_oval(x - RAIO, y - RAIO, x + RAIO, y + RAIO,
                          fill=COR_VERMELHO, outline="white", width=3)
            self.desenhar_carro(x, y)
        elif setor == "Bandeirada":
            caixa = (x - RAIO, y - RAIO, x + RAIO, y + RAIO)
            c.create_oval(*caixa, fill="white", outline=contorno, width=2)
            c.create_arc(*caixa, start=0, extent=90, fill="black", outline="")
            c.create_arc(*caixa, start=180, extent=90, fill="black", outline="")
        else:
            c.create_oval(x - RAIO, y - RAIO, x + RAIO, y + RAIO,
                          fill=self.cor_do_setor(setor), outline=contorno, width=2)

        c.create_text(x, y + RAIO + 12, text=setor, fill="white",
                      font=("Segoe UI", 9, "bold"))

        if setor in self.itens:
            ix = x + RAIO - 2
            iy = y - RAIO + 2
            c.create_polygon(ix, iy - 9, ix + 9, iy, ix, iy + 9, ix - 9, iy,
                             fill=COR_AMARELO, outline="black")

        if setor in self.obstaculos:
            px = x - RAIO + 2
            py = y - RAIO + 2
            c.create_polygon(px, py - 10, px + 10, py + 8, px - 10, py + 8,
                             fill="#ff7b00", outline="black")
            c.create_text(px, py + 2, text="!", font=("Segoe UI", 8, "bold"))

    def desenhar_carro(self, x, y):
        c = self.canvas
        c.create_rectangle(x - 16, y - 4, x + 14, y + 4, fill="white", outline="")
        c.create_polygon(x + 14, y - 3, x + 22, y, x + 14, y + 3,
                         fill="white", outline="")
        c.create_rectangle(x - 19, y - 8, x - 15, y + 8, fill="white", outline="")
        c.create_rectangle(x + 17, y - 8, x + 20, y + 8, fill="white", outline="")
        c.create_rectangle(x - 12, y - 9, x - 4, y - 5, fill="black", outline="")
        c.create_rectangle(x - 12, y + 5, x - 4, y + 9, fill="black", outline="")
        c.create_rectangle(x + 4, y - 9, x + 12, y - 5, fill="black", outline="")
        c.create_rectangle(x + 4, y + 5, x + 12, y + 9, fill="black", outline="")


def main():
    janela = tk.Tk()
    JogoF1(janela)
    janela.mainloop()


if __name__ == "__main__":
    main()