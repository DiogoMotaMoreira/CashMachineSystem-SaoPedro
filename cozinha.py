import customtkinter as ctk
import os

class AppCozinha(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SISTEMA KDS - PREPARAÇÃO")
        
        # Configurar para ecrã inteiro ou janela grande
        self.geometry("1100x850")
        self.configure(fg_color="#0f0f0f") # Fundo quase preto para contraste total

        # Título Superior
        self.label_titulo = ctk.CTkLabel(self, text="PEDIDOS ATIVOS", 
                                       font=("Arial", 40, "bold"), 
                                       text_color="#00FF7F") # Verde Primavera
        self.label_titulo.pack(pady=15)

        # Container principal com scroll para muitos pedidos
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=1050, height=750, 
                                                  fg_color="transparent")
        self.scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.last_content = ""
        self.update_pedidos()

    def criar_card_pedido(self, texto_pedido):
        # Divide o texto para separar o número do conteúdo
        # Exemplo: "#10209 fino + hambúrguer"
        partes = texto_pedido.split("   ", 1)
        numero = partes[0] if len(partes) > 0 else "#???"
        itens = partes[1].upper() if len(partes) > 1 else ""

        # Criar o Card (Frame)
        card = ctk.CTkFrame(self.scroll_frame, fg_color="#1e1e2e", 
                           border_width=2, border_color="#313244")
        card.pack(pady=10, padx=10, fill="x")

        # Número do Pedido (Destaque Esquerdo)
        lbl_num = ctk.CTkLabel(card, text=numero, font=("Monospace", 45, "bold"), 
                              text_color="#f9e2af", width=200)
        lbl_num.pack(side="left", padx=20, pady=20)

        # Itens do Pedido (Destaque Direito)
        lbl_itens = ctk.CTkLabel(card, text=itens, font=("Arial", 35, "bold"), 
                                text_color="#cdd6f4", wraplength=700, justify="left")
        lbl_itens.pack(side="left", padx=20, fill="x")

    def update_pedidos(self):
        if os.path.exists("pedidos.txt"):
            with open("pedidos.txt", "r", encoding="utf-8") as f:
                linhas = f.readlines()
                # Consideramos apenas os últimos 10 pedidos
                pedidos_atuais = [l.strip() for l in linhas[-10:] if l.strip()]
                
                # Só redesenha se houver novos pedidos
                if str(pedidos_atuais) != self.last_content:
                    # Limpar frames antigos
                    for widget in self.scroll_frame.winfo_children():
                        widget.destroy()
                    
                    # Criar novos cards (os mais recentes aparecem primeiro)
                    for p in reversed(pedidos_atuais):
                        self.criar_card_pedido(p)
                        
                    self.last_content = str(pedidos_atuais)
        
        # Verifica a cada 1 segundo
        self.after(1000, self.update_pedidos)

if __name__ == "__main__":
    # Otimização para Linux/Archcraft
    app = AppCozinha()
    app.mainloop()