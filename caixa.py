import customtkinter as ctk
import os

ctk.set_appearance_mode("dark") 

class AppCaixa(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- CONFIGURAÇÃO FULL SCREEN ---
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        
        self.carrinho = [] # Lista de dicionários {'nome': str, 'preco': float}
        self.total = 0.0
        self.num_pedido = 10200
        self.ficheiro = "pedidos.txt"

        # Layout Principal (3 Linhas: Topo, Centro, Rodapé)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) 

        # --- 1. MONITOR DE TOPO (LISTA EM COLUNAS) ---
        self.frame_monitor = ctk.CTkFrame(self, fg_color="#000", height=200, corner_radius=0, border_width=1, border_color="#333")
        self.frame_monitor.grid(row=0, column=0, sticky="ew")
        
        # Preço Gigante à Direita
        self.label_total = ctk.CTkLabel(self.frame_monitor, text="0.00€", font=("Arial", 90, "bold"), text_color="#50fa7b")
        self.label_total.pack(side="right", padx=60)
        
        # Lista Vertical à Esquerda (Scrollable para não fugir do ecrã)
        self.txt_lista = ctk.CTkTextbox(self.frame_monitor, font=("Monospace", 24), fg_color="transparent", width=600, height=180)
        self.txt_lista.pack(side="left", padx=30, pady=10)
        self.txt_lista.insert("1.0", "Aguardando itens...")
        self.txt_lista.configure(state="disabled")

        # --- 2. ÁREA CENTRAL: GRELHA DE PRODUTOS ---
        self.scroll_produtos = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.scroll_produtos.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        for i in range(5): self.scroll_produtos.grid_columnconfigure(i, weight=1)

        # Menu de Produtos
        produtos = [
            ("🍺 Fino", 2.00), ("🍺 Caneca", 3.50), ("🍷 Vinho", 1.50), ("🥤 Cola", 1.50),
            ("🥤 Água", 1.00), ("🥤 Sumol", 1.50), ("☕ Café", 0.70), ("🍔 Hamb. Simp.", 5.00),
            ("🍔 Hamb. Tudo", 7.00), ("🌭 Cachorro", 4.50), ("🥖 Bifana", 3.50), ("🍟 Batatas", 2.50),
            ("🥪 Tosta", 3.00), ("🥗 Salada", 4.00), ("🍩 Donut", 1.50), ("🧊 Gelo", 0.50)
        ]
        
        r, c = 0, 0
        for nome, preco in produtos:
            btn = ctk.CTkButton(self.scroll_produtos, text=f"{nome}\n{preco:.2f}€", 
                               font=("Arial", 22, "bold"), height=130, 
                               fg_color="#2c2c2c", hover_color="#444",
                               command=lambda n=nome, p=preco: self.add_item(n, p))
            btn.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")
            c += 1
            if c > 4: r += 1; c = 0

        # --- 3. BARRA INFERIOR (PAGAMENTO, EXTRAS E CONTROLOS) ---
        self.footer = ctk.CTkFrame(self, fg_color="#1a1a1a", height=220, corner_radius=0)
        self.footer.grid(row=2, column=0, sticky="ew")

        # Coluna 1: Edição
        self.f_edit = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.f_edit.pack(side="left", padx=15)
        ctk.CTkButton(self.f_edit, text="REMOVER ÚLTIMO", fg_color="#333", width=160, height=60, command=self.remover_ultimo).pack(pady=5)
        ctk.CTkButton(self.f_edit, text="LIMPAR TUDO", fg_color="#600", width=160, height=60, command=self.limpar_pedido).pack(pady=5)

        # Coluna 2: ITEM EXTRA (REPOSTO)
        self.f_extra = ctk.CTkFrame(self.footer, fg_color="#252525", corner_radius=10)
        self.f_extra.pack(side="left", padx=15, pady=10)
        ctk.CTkLabel(self.f_extra, text="ITEM PERSONALIZADO", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        self.entry_extra_n = ctk.CTkEntry(self.f_extra, placeholder_text="Nome...", width=140)
        self.entry_extra_n.grid(row=1, column=0, padx=5, pady=5)
        self.entry_extra_p = ctk.CTkEntry(self.f_extra, placeholder_text="€", width=60)
        self.entry_extra_p.grid(row=1, column=1, padx=5, pady=5)
        ctk.CTkButton(self.f_extra, text="ADICIONAR EXTRA", fg_color="#1f538d", command=self.add_manual).grid(row=2, column=0, columnspan=2, pady=5, padx=5)

        # Coluna 3: PAGAMENTO RÁPIDO (ATALHOS)
        self.f_pagar = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.f_pagar.pack(side="left", padx=20)
        ctk.CTkLabel(self.f_pagar, text="PAGAMENTO RÁPIDO", font=("Arial", 12, "bold")).pack()
        f_notas = ctk.CTkFrame(self.f_pagar, fg_color="transparent")
        f_notas.pack()
        for v in [5, 10, 20, 50]:
            ctk.CTkButton(f_notas, text=f"{v}€", width=65, height=50, font=("Arial", 16, "bold"), command=lambda val=v: self.set_pago(val)).pack(side="left", padx=2)
        self.entry_pago = ctk.CTkEntry(self.f_pagar, placeholder_text="Recebido (€)", font=("Arial", 24), width=280, height=50)
        self.entry_pago.pack(pady=10)

        # Coluna 4: ENVIAR GIGANTE
        self.btn_enviar = ctk.CTkButton(self.footer, text="ENVIAR\nPEDIDO", fg_color="#ff5555", 
                                       hover_color="#ff4444", font=("Arial", 35, "bold"), 
                                       width=300, height=160, command=self.finalizar_pedido)
        self.btn_enviar.pack(side="right", padx=20, pady=20)
        
        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 22, "bold"))
        self.label_feedback.place(relx=0.5, rely=0.94, anchor="center")

    # --- LÓGICA DE FUNCIONAMENTO ---
    def set_pago(self, valor):
        self.entry_pago.delete(0, 'end')
        self.entry_pago.insert(0, str(valor))

    def add_item(self, nome, preco):
        self.carrinho.append({"nome": nome, "preco": preco})
        self.total += preco
        self.atualizar_ui()

    def add_manual(self):
        n = self.entry_extra_n.get()
        p = self.entry_extra_p.get().replace(',', '.')
        if n and p:
            try:
                self.add_item(f"⭐ {n}", float(p))
                self.entry_extra_n.delete(0, 'end'); self.entry_extra_p.delete(0, 'end')
            except: pass

    def remover_ultimo(self):
        if self.carrinho:
            item = self.carrinho.pop()
            self.total -= item['preco']
            self.atualizar_ui()

    def limpar_pedido(self):
        self.carrinho = []; self.total = 0.0
        self.atualizar_ui()
        self.entry_pago.delete(0, 'end')
        self.label_feedback.configure(text="")

    def atualizar_ui(self):
        self.label_total.configure(text=f"{self.total:.2f}€")
        self.txt_lista.configure(state="normal")
        self.txt_lista.delete("1.0", "end")
        
        if not self.carrinho:
            self.txt_lista.insert("1.0", "Aguardando itens...")
        else:
            # LÓGICA DE AGRUPAMENTO (Ex: 2x Fino)
            contagem = {}
            for item in self.carrinho:
                nome = item['nome']
                contagem[nome] = contagem.get(nome, 0) + 1
            
            texto_lista = ""
            for nome, qtd in contagem.items():
                texto_lista += f" {qtd}x {nome}\n"
            self.txt_lista.insert("1.0", texto_lista)
            
        self.txt_lista.configure(state="disabled")

    def finalizar_pedido(self):
        if not self.carrinho: return
        try:
            val_pago = self.entry_pago.get().replace(',', '.')
            pago = float(val_pago if val_pago else self.total)
            if pago < self.total:
                self.label_feedback.configure(text="VALOR INSUFICIENTE!", text_color="red")
                return

            troco = pago - self.total
            self.num_pedido += 1
            
            # Formato para a cozinha (Agrupado)
            contagem = {}
            for item in self.carrinho:
                nome = item['nome'].replace("🍺 ", "").replace("🍔 ", "").replace("🥖 ", "").replace("🍟 ", "").replace("⭐ ", "")
                contagem[nome] = contagem.get(nome, 0) + 1
            
            resumo_cozinha = " + ".join([f"{q}x {n}" if q > 1 else n for n, q in contagem.items()])
            
            with open(self.ficheiro, "a", encoding="utf-8") as f:
                f.write(f"#{self.num_pedido}   {resumo_cozinha.lower()}\n")

            self.label_feedback.configure(text=f"PEDIDO #{self.num_pedido} OK! TROCO: {troco:.2f}€", text_color="#50fa7b")
            self.limpar_pedido()
        except:
            self.label_feedback.configure(text="ERRO NO VALOR!", text_color="orange")

if __name__ == "__main__":
    AppCaixa().mainloop()