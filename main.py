import os
import psycopg2
import dotenv
import PySimpleGUI as sg

dotenv.load_dotenv()

class app:
    def __init__(self):
        self.conexao = psycopg2.connect(user=os.environ['FDB_user'],
                                  password=os.environ['FDB_password'],
                                  host=os.environ['FDB_host'],
                                  port=os.environ['FDB_port'],
                                  database=os.environ['FDB_database'])
        self.cursor = self.conexao.cursor()
        self.cursor.execute("SELECT * FROM Clientes")
        self.lista = self.cursor.fetchall()



    def AddCliente(self,nome,idade,cpf,email):
        self.cursor.execute(f"INSERT INTO Clientes(nome_cliente,idade_cliente,cpf_cliente,email_cliente) VALUES('{nome}',{idade},'{cpf}','{email}')")
        self.conexao.commit()
        self.cursor.execute("SELECT * FROM Clientes")
        self.lista = self.cursor.fetchall()

    def RemoverCliente(self,nome):

        self.cursor.execute(f"DELETE FROM Clientes WHERE nome_cliente='{nome}'")
        self.conexao.commit()
        self.cursor.execute("SELECT * FROM Clientes")
        self.lista = self.cursor.fetchall()


    def TelaVisualizarCliente(self):
        sg.theme('Reddit')
        layout = [
            [sg.Text('Cliente:')],
            [sg.Text('Nome:',size=(5,1)),sg.Text(f'{self.values["lista"][0][0]}')],
            [sg.Text('Idade:',size=(5,1)), sg.Text(f'{self.values["lista"][0][1]}')],
            [sg.Text('Cpf:',size=(5,1)), sg.Text(f'{self.values["lista"][0][2]}')],
            [sg.Text('Email:',size=(5,1)), sg.Text(f'{self.values["lista"][0][3]}')],
            [sg.Button('Ok')]
        ]
        return sg.Window('Visualizar Cliente',layout,finalize=True,size=(300,200))

    def TelaInicial(self):
        sg.theme('Reddit')
        layout = [
            [sg.Text('Clientes Registrados')],
            [sg.Listbox(self.lista,size=(100,20),key='lista')],
            [sg.Button('Novo Cliente',size=(20,1)),sg.Button('Excluir Cliente',size=(20,1)),sg.Button('Visualizar Cliente',size=(20,1)),sg.Button('Sair',size=(20,1))]
        ]

        return sg.Window('App Clientes',layout=layout,finalize=True)


    def TelaNovoCliente(self):
        sg.theme('Reddit')
        layout = [
            [sg.Text('Nome',size=(5,1)),sg.InputText('',key='nome')],
            [sg.Text('Idade',size=(5,1)), sg.Input('', key='idade')],
            [sg.Text('Cpf',size=(5,1)), sg.Input('', key='cpf')],
            [sg.Text('Email',size=(5,1)), sg.InputText('', key='email')],
            [sg.Button('Enviar')]
        ]
        return sg.Window('Adicionar Novo Cliente',layout=layout,finalize=True)

    def ChamarTelas(self):
        self.janelaum, self.janeladois, self.janelatres = self.TelaInicial(), None, None
        while True:
            window , event, self.values = sg.read_all_windows()
            if window == self.janelaum and event == sg.WINDOW_CLOSED:
                break
            elif window == self.janelaum and event == 'Sair':
                break
            elif window == self.janelaum and event == 'Novo Cliente':
                self.janelaum.close()
                self.janeladois = self.TelaNovoCliente()
            if window == self.janeladois and event == sg.WINDOW_CLOSED:
                self.janeladois.close()
                self.janelaum = self.TelaInicial()
            elif window == self.janeladois and event == 'Enviar':
                if self.values['nome'] == '' or self.values['idade'] == '' or self.values['cpf'] == '' or self.values['email'] == '':
                    sg.popup_auto_close('Preencha todos os campos corretamente!',auto_close_duration=3)
                else:
                    try:
                        self.AddCliente(self.values['nome'],self.values['idade'],self.values['cpf'],self.values['email'])
                    except pyodbc.ProgrammingError:
                        sg.popup_auto_close('Um dos campos foi preenchido incorretamente!',auto_close_duration=3)
                    else:
                        self.janelaum['lista'].update()
                        self.janeladois.close()
                        self.janelaum = self.TelaInicial()
            elif window == self.janelaum and event == 'Excluir Cliente':
                if self.values['lista'] == []:
                    sg.popup_auto_close('Escolha um cliente para Excluir!',auto_close_duration=3)
                else:
                    remove = self.values['lista'][0][0]
                    self.RemoverCliente(remove)
                    self.janelaum['lista'].update()
                    self.janelaum.close()
                    self.janelaum = self.TelaInicial()
            elif window == self.janelaum and event == 'Visualizar Cliente':
                if self.values['lista'] == []:
                    sg.popup_auto_close('Escolha um cliente para visualizar!',auto_close_duration=3)
                else:
                    self.janelaum.close()
                    self.janelatres = self.TelaVisualizarCliente()
            if window == self.janelatres and event == sg.WINDOW_CLOSED:
                self.janelatres.close()
                self.janelaum = self.TelaInicial()
            elif window == self.janelatres and event == 'Ok':
                self.janelatres.close()
                self.janelaum = self.TelaInicial()




app = app()
app.ChamarTelas()