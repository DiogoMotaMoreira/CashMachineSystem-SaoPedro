import customtkinter as ctk
import os

ctk.set_appearance_mode("dark") 

class AppCaixa(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- CONFIGURAÇÃO FULL SCREEN ---
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        
        self.carrinho = []
        self.total = 0.0
        self.num_pedido = 10200
        self.ficheiro = "pedidos.txt"

        # Grid Principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) 

        # --- BARRA SUPERIOR ---
        self.header = ctk.CTkFrame(self, fg_color="#1a1a1a", height=60)
        self.header.grid(row=0, column=0, sticky="ew")
        
        ctk.CTkLabel(self.header, text="SISTEMA POS - ROULOTE", font=("Arial", 25, "bold")).pack(side="left", padx=20)
        ctk.CTkButton(self.header, text="FECHAR (ESC)", fg_color="#444", width=100, command=self.destroy).pack(side="right", padx=20)

        # --- MONITOR (Carrinho e Preço) ---
        self.frame_monitor = ctk.CTkFrame(self, fg_color="#000", border_width=2, border_color="#333")
        self.frame_monitor.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.frame_monitor.grid_columnconfigure(0, weight=3)
        self.frame_monitor.grid_columnconfigure(1, weight=1)

        self.txt_carrinho = ctk.CTkTextbox(self.frame_monitor, font=("Monospace", 22), fg_color="transparent", height=150)
        self.txt_carrinho.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.txt_carrinho.configure(state="disabled")

        self.label_total = ctk.CTkLabel(self.frame_monitor, text="0.00€", font=("Arial", 70, "bold"), text_color="#50fa7b")
        self.label_total.grid(row=0, column=1, sticky="e", padx=40)

        # --- ZONA CENTRAL: PRODUTOS + BOTÕES DE APAGAR ---
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=2, column=0, sticky="nsew", padx=20)
        self.main_area.grid_columnconfigure(0, weight=4) # Produtos
        self.main_area.grid_columnconfigure(1, weight=1) # Botões de edição

        # Grelha de Produtos
        self.scroll_produtos = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        self.scroll_produtos.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        for i in range(3): self.scroll_produtos.grid_columnconfigure(i, weight=1)

        produtos = [
            ("🍺 Fino", 2.00), ("🍔 Hamb.", 5.50), ("🌭 Cachorro", 4.50), 
            ("🥖 Pão Chour.", 3.00), ("🍟 Batatas", 2.50), ("🥤 Cola", 1.50), 
            ("🥤 Água", 1.00), ("☕ Café", 0.70)
        ]
        
        r, c = 0, 0
        for nome, preco in produtos:
            btn = ctk.CTkButton(self.scroll_produtos, text=f"{nome}\n{preco:.2f}€", 
                               font=("Arial", 20, "bold"), height=100,
                               command=lambda n=nome, p=preco: self.add_item(n, p))
            btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
            c += 1
            if c > 2: r += 1; c = 0

        # Botões de Correção (Lado Direito dos Produtos)
        self.frame_edicao = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.frame_edicao.grid(row=0, column=1, sticky="nsew")

        ctk.CTkButton(self.frame_edicao, text="❌ REMOVER ÚLTIMO", font=("Arial", 16, "bold"),
                     fg_color="#333", hover_color="#555", height=100,
                     command=self.remover_ultimo).pack(fill="x", pady=5)

        ctk.CTkButton(self.frame_edicao, text="🗑️ LIMPAR TUDO", font=("Arial", 16, "bold"),
                     fg_color="#800", hover_color="#a00", height=100,
                     command=self.limpar_pedido).pack(fill="x", pady=5)

        # --- RODAPÉ (Pagamento e Enviar) ---
        self.footer = ctk.CTkFrame(self, fg_color="#1a1a1a", height=180)
        self.footer.grid(row=3, column=0, sticky="ew")

        # Item Extra (Canto inferior esquerdo)
        self.f_extra = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.f_extra.pack(side="left", padx=20)
        self.entry_nome_extra = ctk.CTkEntry(self.f_extra, placeholder_text="Extra...", width=150)
        self.entry_nome_extra.pack(side="left", padx=2)
        self.entry_preco_extra = ctk.CTkEntry(self.f_extra, placeholder_text="€", width=60)
        self.entry_preco_extra.pack(side="left", padx=2)
        ctk.CTkButton(self.f_extra, text="+", width=40, command=self.add_item_personalizado).pack(side="left")

        # Enviar (Direita)
        self.f_final = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.f_final.pack(side="right", padx=20, pady=20)

        self.entry_pago = ctk.CTkEntry(self.f_final, placeholder_text="Recebido", font=("Arial", 25), width=150, height=60)
        self.entry_pago.pack(side="left", padx=10)

        self.btn_finalizar = ctk.CTkButton(self.f_final, text="ENVIAR PEDIDO", fg_color="#ff5555", 
                                          font=("Arial", 25, "bold"), width=300, height=80, 
                                          command=self.finalizar_pedido)
        self.btn_finalizar.pack(side="left")

        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 20))
        self.label_feedback.place(relx=0.5, rely=0.96, anchor="center")

    def update_carrinho_display(self):
        self.txt_carrinho.configure(state="normal")
        self.txt_carrinho.delete("1.0", "end")
        if not self.carrinho:
            self.txt_carrinho.insert("1.0", "Carrinho vazio.")
        else:
            for item in self.carrinho:
                self.txt_carrinho.insert("end", f" • {item['nome']} ({item['preco']:.2f}€)\n")
        self.txt_carrinho.configure(state="disabled")
        self.label_total.configure(text=f"{self.total:.2f}€")

    def add_item(self, nome, preco):
        self.carrinho.append({"nome": nome, "preco": preco})
        self.total += preco
        self.update_carrinho_display()
        self.label_feedback.configure(text="")

    def remover_ultimo(self):
        if self.carrinho:
            item = self.carrinho.pop()
            self.total -= item['preco']
            self.update_carrinho_display()

    def limpar_pedido(self):
        self.carrinho = []; self.total = 0.0
        self.update_carrinho_display()
        self.entry_pago.delete(0, 'end')

    def add_item_personalizado(self):
        nome = self.entry_nome_extra.get()
        preco = self.entry_preco_extra.get().replace(',', '.')
        if nome and preco:
            try:
                self.add_item(f"⭐ {nome}", float(preco))
                self.entry_nome_extra.delete(0, 'end'); self.entry_preco_extra.delete(0, 'end')
            except: pass

    def finalizar_pedido(self):
        if not self.carrinho: return
        try:
            pago = float(self.entry_pago.get().replace(',', '.') or self.total)
            troco = pago - self.total
            if troco < 0: return
            
            self.num_pedido += 1
            resumo = " + ".join([i['nome'].split()[-1].lower() for i in self.carrinho])
            with open(self.ficheiro, "a", encoding="utf-8") as f:
                f.write(f"#{self.num_pedido}   {resumo}\n")

            self.label_feedback.configure(text=f"ENVIADO! TROCO: {troco:.2f}€", text_color="#50fa7b")
            self.limpar_pedido()
        except: pass

if __name__ == "__main__":
    app = AppCaixa()
    app.mainloop()