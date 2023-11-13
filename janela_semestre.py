import tkinter as tk 
from tkinter import ttk
import database as db
import re
from tkinter import messagebox

conexao = db.conecta_bd()

def draw_window():
    janela_semestre = tk.Toplevel()
    janela_semestre.title('Cadastro de semestres')
    janela_semestre.resizable(False, False)
    janela_semestre.grab_set()

    def limpa_campos():
        entry_ano.delete(0, tk.END)
        combobox_semestre.delete(0, tk.END)
        entry_ano.focus()

    # carregando dados no treeview
    def carrega_dados_treeview():
        # antes, limpa o treeview
        for item in treeview_semestres.get_children():
            treeview_semestres.delete(item)
        # consulta no BD as ofertas cadastradas e insere no treeview
        linhas = db.lista_semestres(conexao)
        if linhas:
            for linha in linhas:
                treeview_semestres.insert("", tk.END, values=(linha[0], linha[1]))

    def item_selecionado_treeview(event):
        botao_excluir['state'] = tk.NORMAL
        entry_ano['state'] = tk.NORMAL
        entry_ano.delete(0, tk.END)
        combobox_semestre.delete(0, tk.END)

        for linha in treeview_semestres.selection():
            ano, semestre = treeview_semestres.item(linha, 'values')
            entry_ano.insert(tk.END, ano)
            combobox_semestre.set(semestre)

    def excluir_semestre():
        selecionado = treeview_semestres.focus()
        ano = treeview_semestres.item(selecionado, 'value')[0]
        semestre = treeview_semestres.item(selecionado, 'value')[1]

        resposta = messagebox.askokcancel('Confirmação', 'Deseja realmente exlcuir este semestre?', parent=janela_semestre)

        if resposta:
            linhas = db.deleta_semestre(conexao, ano, semestre)

            if linhas is not None:
                messagebox.showinfo(title="Sucesso", message="Semestre excluido com sucesso!", parent=janela_semestre)
            else:
                messagebox.showwarning(title="Que pena!", message="Não foi possível excluir o semestre, pois existe oferta cadastrada!", parent=janela_semestre)
        limpa_campos()
        botao_excluir['state'] = tk.DISABLED
        carrega_dados_treeview()

    def cadastra_semestre():
        # o modulo re ajuda a digitar os anos apenas no formato: 2022
        if re.findall('^2[0-9]{3}$', entry_ano.get()):
            linhas, erro = db.insere_semestre(conexao, entry_ano.get(), combobox_semestre.get())
            if linhas is not None:
                messagebox.showinfo(title="Sucesso", message="Semestre cadastrado com sucesso!", parent=janela_semestre)
                limpa_campos()
                carrega_dados_treeview()
            else:
                if erro == 1:
                    messagebox.showwarning(title="Que pena", message="Semestre não foi cadastrado! \n "
                                                                        "Chave primária duplicada", parent=janela_semestre)
                    entry_ano.focus()
                else:
                    messagebox.showwarning(title="Que pena", message="Erro ao tentar cadastrar o semestre!", parent=janela_semestre)
                    entry_ano.focus()
        else:
            messagebox.showerror(title="Eita", message="Ano deve ser inserido com 4 digitos.Ex. 2022", parent=janela_semestre)
            entry_ano.focus()

    
    frame_fields = tk.Frame(janela_semestre)
    frame_fields.grid(row=0, padx=10, pady=10)

    label_ano = tk.Label(frame_fields, text='Digite o ano')
    label_ano.grid(row=0, column=0, padx=5, sticky=tk.W)

    entry_ano = tk.Entry(frame_fields)
    entry_ano.grid(row=0, column=1, padx=2, sticky=tk.W)
    entry_ano.focus()

    label_semestre = tk.Label(frame_fields, text='Selecione o semestre')
    label_semestre.grid(row=0, column=2, padx=10, sticky=tk.W)

    combobox_semestre = ttk.Combobox(frame_fields, width=5, state="readonly", values=[1,2])
    combobox_semestre.grid(row=0, column=3, padx=10)
    combobox_semestre.current(0)

    # treeview =================================
    frame_treeview = ttk.Frame(janela_semestre)
    frame_treeview.grid(row=2)

    # defininado as colunas do treeview
    colunas = ('ano', 'semestre')

    treeview_semestres = ttk.Treeview(frame_treeview, columns=colunas, show='headings')
    treeview_semestres.grid(row=0, column=0)

    # adicionando titulos nos cabecalhos
    treeview_semestres.heading('ano', text='Ano')
    treeview_semestres.heading('semestre', text='Semestre')

    # customizando as colunas
    treeview_semestres.column('ano', anchor=tk.CENTER, width=330)
    treeview_semestres.column('semestre', width=300, anchor=tk.CENTER)

    carrega_dados_treeview()

    # criar um evento para capturar a linha selecionada
    treeview_semestres.bind("<<TreeviewSelect>>", item_selecionado_treeview)
    
    # adicionando uma barra de rolagem
    scrollbar = ttk.Scrollbar(frame_treeview, orient=tk.VERTICAL, command=treeview_semestres.yview)
    treeview_semestres.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    # botoes =================================
    frame_botoes = ttk.Frame(janela_semestre)
    frame_botoes.grid(row=3, pady=10)

    botao_salvar = ttk.Button(frame_botoes, text='Salvar', command=cadastra_semestre)
    botao_salvar.grid(row=3, column=1, sticky=tk.EW, padx=5)

    botao_excluir = ttk.Button(frame_botoes, text='Excluir', command=excluir_semestre, state=tk.DISABLED)
    botao_excluir.grid(row=3, column=3, sticky=tk.EW, padx=5)

    botao_cancelar = ttk.Button(frame_botoes, text='Cancelar', command=janela_semestre.destroy)
    botao_cancelar.grid(row=3, column=4, sticky=tk.EW, padx=5)


