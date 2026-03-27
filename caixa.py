import customtkinter as ctk
import os

ctk.set_appearance_mode("dark") 

class AppCaixa(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- CONFIGURAÇÃO FULL SCREEN ---
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False)) # Esc para sair
        
        self.carrinho = []
        self.total = 0.0
        self.num_pedido = 10200
        self.ficheiro = "pedidos.txt"

        # Configurar grelha principal (Layout Responsivo)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Onde ficam os produtos

        # --- BARRA SUPERIOR (Título e Sair) ---
        self.header = ctk.CTkFrame(self, fg_color="#1a1a1a", height=60)
        self.header.grid(row=0, column=0, sticky="ew")
        
        ctk.CTkLabel(self.header, text="SISTEMA DE VENDAS ROULOTE", font=("Arial", 30, "bold")).pack(side="left", padx=30, pady=10)
        ctk.CTkButton(self.header, text="SAIR (ESC)", fg_color="#444", width=100, command=self.destroy).pack(side="right", padx=20)

        # --- ZONA DO MONITOR (Carrinho e Total) ---
        self.frame_monitor = ctk.CTkFrame(self, fg_color="#000", border_width=2, border_color="#333")
        self.frame_monitor.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.frame_monitor.grid_columnconfigure(0, weight=3)
        self.frame_monitor.grid_columnconfigure(1, weight=1)

        self.txt_carrinho = ctk.CTkTextbox(self.frame_monitor, font=("Monospace", 25), fg_color="transparent", height=200)
        self.txt_carrinho.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.txt_carrinho.insert("1.0", "Aguardando pedido...")
        self.txt_carrinho.configure(state="disabled")

        self.label_total = ctk.CTkLabel(self.frame_monitor, text="0.00€", font=("Arial", 80, "bold"), text_color="#50fa7b")
        self.label_total.grid(row=0, column=1, sticky="e", padx=40)

        # --- ZONA DE PRODUTOS (Grelha Gigante) ---
        self.scroll_produtos = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_produtos.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        
        # Configurar colunas da grelha de produtos (4 colunas)
        for i in range(4): self.scroll_produtos.grid_columnconfigure(i, weight=1)

        produtos = [
            ("🍺 Fino", 2.00), ("🍺 Caneca", 3.50), ("🍔 Hamb.", 5.50), 
            ("🌭 Cachorro", 4.50), ("🥖 Pão com Chouriço", 3.00), ("🍟 Batatas", 2.50),
            ("🥤 Cola", 1.50), ("🥤 Água", 1.00), ("☕ Café", 0.70), ("🍷 Vinho", 1.50)
        ]
        
        r, c = 0, 0
        for nome, preco in produtos:
            btn = ctk.CTkButton(self.scroll_produtos, text=f"{nome}\n{preco:.2f}€", 
                               font=("Arial", 22, "bold"), height=120,
                               fg_color="#2c2c2c", hover_color="#3d3d3d",
                               command=lambda n=nome, p=preco: self.add_item(n, p))
            btn.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
            c += 1
            if c > 3: r += 1; c = 0

        # --- ZONA DE RODAPÉ (Pagamento e Extras) ---
        self.footer = ctk.CTkFrame(self, fg_color="#1a1a1a", height=250)
        self.footer.grid(row=3, column=0, sticky="ew", padx=0, pady=0)

        # Item Extra (Esquerda)
        self.f_extra = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.f_extra.pack(side="left", padx=40, pady=20)
        self.entry_nome_extra = ctk.CTkEntry(self.f_extra, placeholder_text="Produto Especial", width=250, font=("Arial", 18))
        self.entry_nome_extra.pack(side="left", padx=5)
        self.entry_preco_extra = ctk.CTkEntry(self.f_extra, placeholder_text="0.00€", width=100, font=("Arial", 18))
        self.entry_preco_extra.pack(side="left", padx=5)
        ctk.CTkButton(self.f_extra, text="+", width=50, command=self.add_item_personalizado).pack(side="left")

        # Pagamento e Botão Enviar (Direita)
        self.f_pago = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.f_pago.pack(side="right", padx=40)
        
        self.entry_pago = ctk.CTkEntry(self.f_pago, placeholder_text="Recebido", font=("Arial", 30), width=200, height=60)
        self.entry_pago.pack(side="left", padx=10)

        self.btn_finalizar = ctk.CTkButton(self.f_pago, text="ENVIAR PEDIDO", fg_color="#ff5555", 
                                          hover_color="#ff4444", font=("Arial", 30, "bold"),
                                          width=350, height=100, command=self.finalizar_pedido)
        self.btn_finalizar.pack(side="left", padx=10)

        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 20))
        self.label_feedback.place(relx=0.5, rely=0.95, anchor="center")

    def add_item_personalizado(self):
        nome = self.entry_nome_extra.get()
        preco = self.entry_preco_extra.get().replace(',', '.')
        if nome and preco:
            try:
                self.add_item(f"⭐ {nome}", float(preco))
                self.entry_nome_extra.delete(0, 'end'); self.entry_preco_extra.delete(0, 'end')
            except: pass

    def update_carrinho_display(self):
        self.txt_carrinho.configure(state="normal")
        self.txt_carrinho.delete("1.0", "end")
        resumo = {}
        for item in self.carrinho: resumo[item['nome']] = resumo.get(item['nome'], 0) + 1
        for nome, qtd in resumo.items():
            self.txt_carrinho.insert("end", f" • {qtd}x {nome}\n")
        self.txt_carrinho.configure(state="disabled")
        self.label_total.configure(text=f"{self.total:.2f}€")

    def add_item(self, nome, preco):
        self.carrinho.append({"nome": nome, "preco": preco})
        self.total += preco
        self.update_carrinho_display()

    def finalizar_pedido(self):
        if not self.carrinho: return
        try:
            pago = float(self.entry_pago.get().replace(',', '.') or self.total)
            troco = pago - self.total
            if troco < 0: return
            
            self.num_pedido += 1
            nomes = [i['nome'].split()[-1].lower() for i in self.carrinho] # simplifica nomes
            with open(self.ficheiro, "a", encoding="utf-8") as f:
                f.write(f"#{self.num_pedido}   {' + '.join(nomes)}\n")

            self.label_feedback.configure(text=f"PEDIDO #{self.num_pedido} ENVIADO! TROCO: {troco:.2f}€", text_color="#50fa7b")
            self.carrinho = []; self.total = 0.0
            self.update_carrinho_display()
            self.entry_pago.delete(0, 'end')
        except: pass

if __name__ == "__main__":
    app = AppCaixa()
    app.mainloop()