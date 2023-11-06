import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo, askyesno, showwarning
import database as db


conexao = db.conecta_bd()
db.cria_tabelas(conexao)

window = tk.Tk()
window.title('Geração de cronogramas')

style = ttk.Style(window)
style.theme_use('clam') 

def screen_center(window_width, window_height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)
    window.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')

dicionario_semestres=dict()
nomes_disciplinas=list()
def add_oferta():
    
    janela_oferta = tk.Toplevel(window)
    janela_oferta.title('Cadastro de ofertas')
    janela_oferta.resizable(False, False)        
    
    x = window.winfo_x()
    y = window.winfo_y()
    w = janela_oferta.winfo_width()
    h = janela_oferta.winfo_height()  
    janela_oferta.geometry("+%d+%d" % (x, y))

    estilo = ttk.Style()
    estilo.theme_use('clam')

    estilo.configure('TFrame', background='#F2F2F2')
    estilo.configure('TLabel', background='#F2F2F2')
    estilo.configure('TButton', font =('arial', 12), foreground = '#3D3D3D')

    def preenche_combobox_anos_semestres():
        global anos
        global dicionario_semestres
        
        semestres = db.lista_semestres(conexao)
        
        if semestres:
            # transforma o retorno do banco de dados em um dicionario    
            dicionario_semestres=dict()
            anos = []
            for ano, semestre in semestres:
                dicionario_semestres.setdefault(ano, []).append(semestre)
                anos.append(ano)
            anos = dicionario_semestres.keys()
        else:
            anos = {}
        
    preenche_combobox_anos_semestres()

    def preenche_combobox_disciplinas():
        global nomes_disciplinas

        disciplinas = db.lista_disciplinas(conexao)
        if disciplinas:
            # pega os nomes das disciplinas da lista de tuplas
            nomes_disciplinas = [disciplina[1] for disciplina in disciplinas]

        else:
            nomes_disciplinas = ['']
        return nomes_disciplinas
    
    def teste():
        global nomes_disciplinas
        global dicionario_disciplinas
    
        disciplinas = db.lista_disciplinas(conexao)
    
        if disciplinas:
            # transforma o retorno do banco de dados em um dicionario    
            dicionario_disciplinas=dict()
            nomes_disciplinas = []
            for _, nome, _, nivel in disciplinas:
                dicionario_disciplinas.setdefault(nome, []).append(nivel)
                nomes_disciplinas.append(nome)
            nomes_disciplinas = dicionario_disciplinas.keys()
        else:
            nomes_disciplinas = {}
    teste()
    #====================================================

    # labels e combobox =================================
    frame_combos = ttk.Frame(janela_oferta, style='TFrame')
    frame_combos.grid(row=0, pady=10, padx=10)

    label_ano = ttk.Label(frame_combos, text='Ano:', style='TLabel')
    label_ano.grid(row=0, column=0, padx=10, sticky=tk.W)

    combobox_ano = ttk.Combobox(frame_combos, width=6, state="readonly", values=list(anos))
    combobox_ano.grid(row=1, column=0, padx=10, sticky=tk.EW)

    def checa_se_ano_esta_vazio():
        if not anos:
            combobox_ano.set('')
            combobox_ano['state'] = 'disabled'
        else:
            combobox_ano.current(0)        
    checa_se_ano_esta_vazio()

    label_semestre = ttk.Label(frame_combos, text='Semestre:')
    label_semestre.grid(row=0, column=1, padx=10, sticky=tk.W)

    # postcommand: chama um método imediatamente antes de exibir os valores.
    #combobox_semestre = ttk.Combobox(frame_combos, width=5, state="readonly", postcommand=atualiza_semestres)
    combobox_semestre = ttk.Combobox(frame_combos, width=5, state="readonly", values=dicionario_semestres[int(combobox_ano.get())])
    combobox_semestre.grid(row=1, column=1, padx=10)
    combobox_semestre.current(0)

    def atualiza_semestres(event=None):
        combobox_semestre.config(value=dicionario_semestres[int(combobox_ano.get())])
        combobox_semestre.current(0)

    combobox_ano.bind('<<ComboboxSelected>>', atualiza_semestres)


    label_disciplina = ttk.Label(frame_combos, text='Disciplina:')
    label_disciplina.grid(row=0, column=2, padx=20, sticky=tk.W)

    combobox_disciplina = ttk.Combobox(frame_combos, state='readonly', values=list(nomes_disciplinas))
    combobox_disciplina.grid(row=1, column=2, padx=20)

    def checa_se_disciplina_esta_vazia():
        if not nomes_disciplinas:
            combobox_disciplina.set('')
            combobox_disciplina['state'] = 'disabled'
        else:
            combobox_disciplina.current(0)        
    checa_se_disciplina_esta_vazia()

    label_nivel = ttk.Label(frame_combos, text='Nível de ensino:')
    label_nivel.grid(row=0, column=3, padx=10, sticky=tk.W)

    combobox_nivel = ttk.Combobox(frame_combos, state='readonly', values=dicionario_disciplinas[combobox_disciplina.get()])
    combobox_nivel.grid(row=1, column=3, padx=10)
    combobox_nivel.current(0)

    def atualiza_niveis(event=None):
        combobox_nivel.config(value=dicionario_disciplinas[combobox_disciplina.get()])
        combobox_nivel.current(0)

    combobox_disciplina.bind('<<ComboboxSelected>>', atualiza_niveis)

    # treeview =================================
    frame_treeview = ttk.Frame(janela_oferta)
    frame_treeview.grid(row=2)

    # defininado as colunas do treeview
    colunas = ('ano', 'semestre', 'disciplina', 'nivel')

    treeview_ofertas = ttk.Treeview(frame_treeview, columns=colunas, show='headings')
    treeview_ofertas.grid(row=0, column=0, sticky=tk.EW)

    # adicionando titulos nos cabecalhos
    treeview_ofertas.heading('ano', text='Ano')
    treeview_ofertas.heading('semestre', text='Semestre')
    treeview_ofertas.heading('disciplina', text='Disciplina')
    treeview_ofertas.heading('nivel', text='Nível')

    # customizando as colunas
    treeview_ofertas.column('ano', anchor=tk.CENTER)
    treeview_ofertas.column('semestre', width=200, anchor=tk.CENTER)
    treeview_ofertas.column('disciplina', anchor=tk.CENTER)
    treeview_ofertas.column('nivel', anchor=tk.CENTER)

    # carregando dados no treeview
    def carrega_dados_treeview():
        # antes, limpa o treeview
        for item in treeview_ofertas.get_children():
            treeview_ofertas.delete(item)
        # consulta no BD as ofertas cadastradas e insere no treeview
        linhas = db.lista_ofertas(conexao)
        if linhas:
            for linha in linhas:
                treeview_ofertas.insert("", tk.END, values=(linha[1], linha[2], linha[5], linha[7]))
    carrega_dados_treeview()

    # adicionando uma barra de rolagem
    scrollbar = ttk.Scrollbar(frame_treeview, orient=tk.VERTICAL, command=treeview_ofertas.yview)
    treeview_ofertas.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')


    def excluir_oferta():
        askyesno(title='Deseja realmente excluir a oferta de disciplina', message=f'{ano_selecionado}.{semestre_selecionado} - {disciplina_selecionado} - {nivel_selecionado}')

    m = tk.Menu(janela_oferta, tearoff = 0)
    m.add_command(label ="Excluir oferta", command=excluir_oferta)
    m.add_separator()
    m.add_command(label ="Sair")
    
    def do_popup(event):
        try:
            item = treeview_ofertas.identify_row(event.y)
            info = treeview_ofertas.item(item, 'values')
            #ano, semestre, disciplina, nivel = info
            print(info)
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()
    
    # Button-2 no Mac. Unix e Windows Button-3
    treeview_ofertas.bind("<Button-2>", do_popup)

    # implementacao do CRUD
    # =============================================

    # consulta disciplina por nome e nivel
    # retorna o id da disciplina
    def pega_id_disciplina():
        dados_disciplina = db.consulta_disciplina_por_nome_e_nivel(conexao, combobox_disciplina.get(), combobox_nivel.get())
        return dados_disciplina[0]

    def cadastrar_oferta():
        if combobox_ano != '' and combobox_semestre != '' and combobox_disciplina != '' and combobox_nivel != '':
            dados_disciplina = db.consulta_disciplina_por_nome_e_nivel(conexao, combobox_disciplina.get(), combobox_nivel.get())
            for disciplina in dados_disciplina:
                id_disciplina = disciplina[0]
            linhas, erro = db.insere_oferta(conexao, combobox_ano.get(), combobox_semestre.get(), id_disciplina)
            if linhas is not None:
                showinfo(title="Sucesso", message="Oferta cadastrada com sucesso!")
            else:
                if erro == 1:
                    showwarning(title="Que pena", message="Esta disciplina já está ofertada, neste semestre")
                else:
                    showwarning(title="Que pena", message="Erro ao tentar cadastrar a Oferta!")
        else:
            showinfo('Aviso!', 'Para cadastrar uma oferta, preencha TODOS os campos: Ano, Semestre, Disciplina e Nível de ensino!')

    def captura_item_selecionado(event=None):
        global detalhes

        # pega o identificador da linha
        linha_selecionada = treeview_ofertas.focus()
        
        # pega um dicionario com os detalhes
        detalhes = treeview_ofertas.item(linha_selecionada)
        
        # pega os valores da linha
        print(detalhes.get("values"))

    treeview_ofertas.bind("<<TreeviewSelect>>", captura_item_selecionado)

    def excluir_oferta():
        global ano_selecionado, semestre_selecionado, disciplina_selecionada, nivel_selecionado

        captura_item_selecionado()
        if detalhes['values'] == '':
            showwarning('Aviso!', 'Você selecionar uma oferta, para excluir!')
        else:
            ano_selecionado, semestre_selecionado, disciplina_selecionada, nivel_selecionado = detalhes.get("values")
            dados_disciplina = db.consulta_disciplina_por_nome_e_nivel(conexao, disciplina_selecionada, nivel_selecionado)
            for disciplina in dados_disciplina:
                id_disciplina = disciplina[0]
            print('id da disciplina:', id_disciplina)
            oferta_selecionada = db.consulta_oferta_com_condicao(conexao, ano_selecionado, semestre_selecionado, id_disciplina)
            print('id da oferta:', oferta_selecionada[0][0])
            db.delete_oferta(conexao, oferta_selecionada[0][0])
            showinfo('Aí sim!', 'Oferta excluida com sucesso!')
    # botoes =================================
    frame_botoes = ttk.Frame(janela_oferta)
    frame_botoes.grid(row=3, pady=10)

    botao_salvar = ttk.Button(frame_botoes, text='Salvar', command= lambda: [cadastrar_oferta(), carrega_dados_treeview()])
    botao_salvar.grid(row=3, column=1, sticky=tk.EW, padx=5)

    botao_excluir = ttk.Button(frame_botoes, text='Excluir', command=lambda: [excluir_oferta(), carrega_dados_treeview()])
    botao_excluir.grid(row=3, column=3, sticky=tk.EW, padx=5)

    botao_cancelar = ttk.Button(frame_botoes, text='Cancelar', command=janela_oferta.destroy)
    botao_cancelar.grid(row=3, column=4, sticky=tk.EW, padx=5)



window.minsize(width=550, height=80)

window.resizable(False, False)
window.config(bg='#FFFEE1')
screen_center(550, 80)

# adicionando um menu
main_menu = tk.Menu(window)
window.config(menu=main_menu)

# itens do menu
add_menu = tk.Menu(main_menu)
main_menu.add_cascade(label='Cadastrar', menu=add_menu)
add_menu.add_command(label='Ofertas', command=add_oferta)


# criando uma barra de ferramentas
toolbar = tk.Frame(window, relief=tk.RAISED, bg='#FFFEE1', height=100)
toolbar.pack()

# para adicionar tooltip nos botoes

schedule_button_img = Image.open("./images/icon_offer.png")
schedule_button_img = schedule_button_img.resize((48, 48), Image.ANTIALIAS)
schedule_button_img_tk = ImageTk.PhotoImage(schedule_button_img)
schedule_button = tk.Button(toolbar, bd=0, padx=20, pady=5, font='Arial 12', fg='#3D3D3D',
                                text="Adicionar Oferta", compound="top", image=schedule_button_img_tk,
                                relief=tk.FLAT,
                                command=add_oferta,height=10, width=30)

schedule_button.image = schedule_button_img_tk
schedule_button.pack(side=tk.LEFT, padx=2)


content_button_img = Image.open("./images/icon_semester.png")
content_button_img = content_button_img.resize((48, 48), Image.ANTIALIAS)

content_button_img_tk = ImageTk.PhotoImage(content_button_img)
content_button = tk.Button(toolbar, padx=20, pady=5, font='Arial 12', fg='#3D3D3D',
                                text="Adicionar Semestres", compound="top", border=0,
                                image=content_button_img_tk, relief=tk.FLAT,
                                command=None)
content_button.image = content_button_img_tk
content_button.pack(side=tk.LEFT, padx=2)

report_button_img = Image.open("./images/icon_subjects.png")
report_button_img = report_button_img.resize((48, 48), Image.ANTIALIAS)

report_button_img_tk = ImageTk.PhotoImage(report_button_img)
report_button = tk.Button(toolbar, padx=20, pady=5, font='Arial 12', fg='#3D3D3D', border=0, height=100,
                            text="Adicionar Disciplinas", compound="top", image=report_button_img_tk, relief=tk.FLAT,
                            command=None)

report_button.image = report_button_img_tk
report_button.pack(side=tk.LEFT, padx=2)

semester_var = tk.IntVar()
discipline_var = tk.IntVar()

exit_button_img = Image.open("./images/icon-exit.png")
exit_button_img = exit_button_img.resize((48, 48), Image.ANTIALIAS)

exit_button_img_tk = ImageTk.PhotoImage(exit_button_img)
exit_button = tk.Button(toolbar, padx=20, pady=5, font='Arial 12', fg='#3D3D3D', border=0, height=100,
                            text="Sair", compound="top", image=exit_button_img_tk, relief=tk.FLAT,
                            command=window.quit, bd=0)

exit_button.image = exit_button_img_tk
exit_button.pack(side=tk.LEFT, padx=2)


window.mainloop()