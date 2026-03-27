import customtkinter as ctk
import os
import json

ctk.set_appearance_mode("dark")

class AppCaixa(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- CONFIGURAÇÃO E DADOS ---
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        
        self.carrinho = []
        self.total = 0.0
        self.ficheiro_pedidos = "pedidos.txt"
        self.ficheiro_produtos = "produtos.json"
        self.num_pedido = self.obter_ultimo_numero_pedido()
        
        self.carregar_produtos()

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- 1. MONITOR DE TOPO ---
        self.frame_monitor = ctk.CTkFrame(self, fg_color="#000", height=200, corner_radius=0)
        self.frame_monitor.grid(row=0, column=0, sticky="ew")
        
        # Botão Configurações (Discreto no canto)
        self.btn_cfg = ctk.CTkButton(self.frame_monitor, text="⚙️", width=60, height=60, font=("Arial", 35), fg_color="#222", command=self.abrir_configuracoes)
        self.btn_cfg.pack(side="left", anchor="n", padx=15, pady=15)

        self.label_total = ctk.CTkLabel(self.frame_monitor, text="0.00€", font=("Arial", 90, "bold"), text_color="#50fa7b")
        self.label_total.pack(side="right", padx=60)
        
        self.txt_lista = ctk.CTkTextbox(self.frame_monitor, font=("Monospace", 28), fg_color="transparent", width=600, height=180)
        self.txt_lista.pack(side="left", padx=30, pady=10)
        self.txt_lista.configure(state="disabled")

        # --- 2. ÁREA DE PRODUTOS ---
        self.scroll_produtos = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.scroll_produtos.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.desenhar_botoes_produtos()

        # --- 3. BARRA INFERIOR ---
        self.footer = ctk.CTkFrame(self, fg_color="#1a1a1a", height=220, corner_radius=0)
        self.footer.grid(row=2, column=0, sticky="ew")

        # Controlos
        self.f_edit = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.f_edit.pack(side="left", padx=15)
        ctk.CTkButton(self.f_edit, text="REMOVER ÚLTIMO", fg_color="#333", width=180, height=70, font=("Arial", 18, "bold"), command=self.remover_ultimo).pack(pady=5)
        ctk.CTkButton(self.f_edit, text="LIMPAR TUDO", fg_color="#600", width=180, height=70, font=("Arial", 18, "bold"), command=self.limpar_pedido).pack(pady=5)

        # Extra
        self.f_extra = ctk.CTkFrame(self.footer, fg_color="#252525", corner_radius=10)
        self.f_extra.pack(side="left", padx=15, pady=10)
        self.entry_extra_n = ctk.CTkEntry(self.f_extra, placeholder_text="Extra...", width=180, height=45, font=("Arial", 20))
        self.entry_extra_n.grid(row=0, column=0, padx=5, pady=5)
        self.entry_extra_p = ctk.CTkEntry(self.f_extra, placeholder_text="€", width=80, height=45, font=("Arial", 20))
        self.entry_extra_p.grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(self.f_extra, text="ADD EXTRA", fg_color="#1f538d", height=45, font=("Arial", 18, "bold"), command=self.add_manual).grid(row=1, column=0, columnspan=2, pady=5)

        # Pagamento
        self.f_pagar = ctk.CTkFrame(self.footer, fg_color="transparent")
        self.f_pagar.pack(side="left", padx=20)
        f_notas = ctk.CTkFrame(self.f_pagar, fg_color="transparent")
        f_notas.pack()
        for v in [5, 10, 20, 50]:
            ctk.CTkButton(f_notas, text=f"{v}€", width=90, height=65, font=("Arial", 24, "bold"), command=lambda val=v: self.set_pago(val)).pack(side="left", padx=5)
        self.entry_pago = ctk.CTkEntry(self.f_pagar, placeholder_text="Recebido (€)", font=("Arial", 30), width=320, height=65)
        self.entry_pago.pack(pady=10)

        # Enviar
        self.btn_enviar = ctk.CTkButton(self.footer, text="ENVIAR\nPEDIDO", fg_color="#ff5555", font=("Arial", 35, "bold"), width=300, height=160, command=self.finalizar_pedido)
        self.btn_enviar.pack(side="right", padx=20, pady=20)
        
        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 28, "bold"))
        self.label_feedback.place(relx=0.5, rely=0.94, anchor="center")

    # --- GESTÃO DO NÚMERO DO PEDIDO ---
    def obter_ultimo_numero_pedido(self):
        if os.path.exists(self.ficheiro_pedidos):
            try:
                with open(self.ficheiro_pedidos, "r", encoding="utf-8") as f:
                    linhas = [linha for linha in f.readlines() if linha.strip()]
                    if linhas:
                        ultima_linha = linhas[-1]
                        if ultima_linha.startswith("#"):
                            numero = ultima_linha.split(maxsplit=1)[0][1:] # Pega no "15" de "#15"
                            return int(numero)
            except Exception:
                pass
        return 0

    # --- GESTÃO DE PRODUTOS ---
    def carregar_produtos(self):
        if os.path.exists(self.ficheiro_produtos):
            with open(self.ficheiro_produtos, "r", encoding="utf-8") as f:
                self.menu_produtos = json.load(f)
        else:
            self.menu_produtos = [{"nome": "🍺 Fino", "preco": 2.0}, {"nome": "🍔 Hamb.", "preco": 5.0}]
            self.guardar_produtos()

    def guardar_produtos(self):
        with open(self.ficheiro_produtos, "w", encoding="utf-8") as f:
            json.dump(self.menu_produtos, f, indent=4, ensure_ascii=False)

    def desenhar_botoes_produtos(self):
        for widget in self.scroll_produtos.winfo_children():
            widget.destroy()
        
        for i in range(5): self.scroll_produtos.grid_columnconfigure(i, weight=1)
        
        r, c = 0, 0
        for item in self.menu_produtos:
            nome, preco = item['nome'], item['preco']
            btn = ctk.CTkButton(self.scroll_produtos, text=f"{nome}\n{preco:.2f}€", 
                               font=("Arial", 26, "bold"), height=150, fg_color="#2c2c2c",
                               command=lambda n=nome, p=preco: self.add_item(n, p))
            btn.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")
            c += 1
            if c > 4: r += 1; c = 0

    # --- JANELA DE CONFIGURAÇÕES ---
    def abrir_configuracoes(self):
        self.janela_cfg = ctk.CTkToplevel(self)
        self.janela_cfg.title("Configurações de Menu")
        self.janela_cfg.geometry("600x700")
        self.janela_cfg.attributes("-topmost", True)
        
        ctk.CTkLabel(self.janela_cfg, text="ADICIONAR NOVO PRODUTO", font=("Arial", 22, "bold")).pack(pady=15)
        
        self.new_n = ctk.CTkEntry(self.janela_cfg, placeholder_text="Nome (ex: 🥤 Cola)", font=("Arial", 20), height=45, width=300)
        self.new_n.pack(pady=10)
        self.new_p = ctk.CTkEntry(self.janela_cfg, placeholder_text="Preço (ex: 1.50)", font=("Arial", 20), height=45, width=300)
        self.new_p.pack(pady=10)
        
        ctk.CTkButton(self.janela_cfg, text="GRAVAR NO MENU", fg_color="green", font=("Arial", 18, "bold"), height=50, command=self.adicionar_ao_menu).pack(pady=15)
        
        ctk.CTkLabel(self.janela_cfg, text="PRODUTOS ATUAIS (Clique para apagar)", font=("Arial", 16)).pack(pady=10)
        
        self.scroll_lista_cfg = ctk.CTkScrollableFrame(self.janela_cfg, height=300)
        self.scroll_lista_cfg.pack(fill="both", expand=True, padx=20, pady=10)
        self.atualizar_lista_config()

    def adicionar_ao_menu(self):
        try:
            nome = self.new_n.get()
            preco = float(self.new_p.get().replace(',', '.'))
            if nome:
                self.menu_produtos.append({"nome": nome, "preco": preco})
                self.guardar_produtos()
                self.desenhar_botoes_produtos()
                self.atualizar_lista_config()
                self.new_n.delete(0, 'end'); self.new_p.delete(0, 'end')
        except: pass

    def remover_do_menu(self, index):
        self.menu_produtos.pop(index)
        self.guardar_produtos()
        self.desenhar_botoes_produtos()
        self.atualizar_lista_config()

    def atualizar_lista_config(self):
        for widget in self.scroll_lista_cfg.winfo_children(): widget.destroy()
        for idx, item in enumerate(self.menu_produtos):
            btn = ctk.CTkButton(self.scroll_lista_cfg, text=f"Remover: {item['nome']}", fg_color="#444", 
                               font=("Arial", 18), height=45, hover_color="red", command=lambda i=idx: self.remover_do_menu(i))
            btn.pack(fill="x", pady=5)

    # --- LÓGICA DE VENDAS (IGUAL À ANTERIOR) ---
    def set_pago(self, valor):
        self.entry_pago.delete(0, 'end'); self.entry_pago.insert(0, str(valor))

    def add_item(self, nome, preco):
        self.carrinho.append({"nome": nome, "preco": preco})
        self.total += preco
        self.atualizar_ui()

    def add_manual(self):
        try:
            n, p = self.entry_extra_n.get(), float(self.entry_extra_p.get().replace(',', '.'))
            self.add_item(f"⭐ {n}", p)
            self.entry_extra_n.delete(0, 'end'); self.entry_extra_p.delete(0, 'end')
        except: pass

    def remover_ultimo(self):
        if self.carrinho:
            item = self.carrinho.pop()
            self.total -= item['preco']
            self.atualizar_ui()

    def limpar_pedido(self):
        self.carrinho = []; self.total = 0.0; self.atualizar_ui()
        self.entry_pago.delete(0, 'end'); self.label_feedback.configure(text="")

    def atualizar_ui(self):
        self.label_total.configure(text=f"{self.total:.2f}€")
        self.txt_lista.configure(state="normal")
        self.txt_lista.delete("1.0", "end")
        if not self.carrinho:
            self.txt_lista.insert("1.0", "Aguardando itens...")
        else:
            contagem = {}
            for item in self.carrinho: contagem[item['nome']] = contagem.get(item['nome'], 0) + 1
            for nome, qtd in contagem.items(): self.txt_lista.insert("end", f" {qtd}x {nome}\n")
        self.txt_lista.configure(state="disabled")

    def finalizar_pedido(self):
        if not self.carrinho: return
        try:
            pago = float(self.entry_pago.get().replace(',', '.') or self.total)
            if pago < self.total:
                self.label_feedback.configure(text="VALOR INSUFICIENTE!", text_color="red")
                return
            self.num_pedido += 1
            contagem = {}
            for item in self.carrinho:
                nome = item['nome'].replace("🍺 ", "").replace("🍔 ", "").replace("🥤 ", "").replace("⭐ ", "")
                contagem[nome] = contagem.get(nome, 0) + 1
            resumo = " + ".join([f"{q}x {n}" if q > 1 else n for n, q in contagem.items()])
            with open(self.ficheiro_pedidos, "a", encoding="utf-8") as f:
                f.write(f"#{self.num_pedido}   {resumo.lower()}\n")
            self.label_feedback.configure(text=f"PEDIDO #{self.num_pedido} OK! TROCO: {(pago-self.total):.2f}€", text_color="#50fa7b")
            self.limpar_pedido()
        except: pass

if __name__ == "__main__":
    AppCaixa().mainloop()