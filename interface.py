from PyQt5.QtWidgets import QApplication, QRadioButton, QWidget, QLabel, QDesktopWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStackedWidget, QLineEdit, QGridLayout, QComboBox, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem, QStyledItemDelegate, QFrame, QMessageBox, QFileDialog, QHeaderView, QScrollArea, QGraphicsOpacityEffect, QTableView
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap, QIcon, QStandardItemModel
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import Qt
from editor import Editor
from os import listdir
from os.path import isfile, join

ICON = 'icon.png'
LOGO = 'logo.png'
APP_NAME = 'Videoclip\nMaker'
SLOGAN = 'Sincronize seus vídeos com música\ncom facilidade.'
SUCCESS_MESSAGE = 'Seu videoclipe já está pronto!'

class VideoclipMaker(QWidget):
	def __init__(self):
		super().__init__()

		#definindo os dados da janela "pai"
		self.title = APP_NAME #nome do programa
		self.top = 100 #dado que será ignorado, pois a tela será centralizada
		self.left = 100 #dado que será ignorado, pois a tela será centralizada
		self.width = 830 #largura da janela ao abrir 830
		self.heigh = 630 #altura da janela ao abrir 630
		self.iconName = ICON #endereço do icon da janela
		self.setFixedSize(self.width, self.heigh) #tornando a janela não resizable
		self.output_video_filename = ""
		self.InitProgram()

	def InitProgram(self):

		self.setWindowIcon(QtGui.QIcon(self.iconName))
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.heigh)

		#centralizando a janela
		qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())

		#configurando a cor de fundo da janela
		self.setStyleSheet("background-color: #ffffff")

		#configurando a primeira página
		self.pag1 = QWidget()
		self.pag1.setStyleSheet("background-color: #ffffff")
		self.Pag1UI()
		self.pag1.btAvancar.clicked.connect(lambda: self.BotaoAvancar(0))
		
		#configurando a segunda página
		self.pag2 = QWidget()
		self.pag2.setStyleSheet("background-color: #ffffff")
		self.Pag2UI()
		self.pag2.btAvancar.clicked.connect(lambda: self.BotaoAvancar(1))
		self.pag2.btVoltar.clicked.connect(lambda: self.BotaoVoltar(1))
		
		#configurando a terceira página
		self.pag3 = QWidget()
		self.pag3.setStyleSheet("background-color: #ffffff")
		self.Pag3UI()
		self.pag3.btVoltar.clicked.connect(lambda: self.BotaoVoltar(2))

		#adicionando as quatro páginas
		self.stackedWidget = QStackedWidget()
		self.stackedWidget.addWidget(self.pag1)
		self.stackedWidget.addWidget(self.pag2)
		self.stackedWidget.addWidget(self.pag3)

		#adicionando a stackedwidget ao layout da página
		self.vbox = QVBoxLayout()
		self.vbox.addWidget(self.stackedWidget)
		self.vbox.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.vbox)

		#impedindo da janela ser maximizada
		self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)
		self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)

		#mostrando a janela
		self.show()

	def BotaoVoltar(self, id):
		self.stackedWidget.setCurrentIndex(id - 1) #apenas volta uma página

	def BotaoAvancar(self, id):
		if id == 0: #página 1 indo para a página 2
			self.stackedWidget.setCurrentIndex(id + 1) 
		elif id == 1: #página 2 indo para página 3
			QApplication.setOverrideCursor(Qt.WaitCursor)

			onlyfiles = [f for f in listdir(self.video_folder_path) if isfile(join(self.video_folder_path + '/', f))]
			input_video_paths = []
			for path in onlyfiles:
				if path.endswith('.mp4'):
					input_video_paths.append(self.video_folder_path+'/'+path)
			
			#default que definimos
			min_interval_between_moments = 2
			method = 'onset'
			clicks = False

			editor = Editor(self.music_path, input_video_paths, self.output_video_filename[0])
			editor.merge(method, clicks, min_interval_between_moments)

			#import time 
			#time. sleep(5)
			
			QApplication.restoreOverrideCursor()
			self.stackedWidget.setCurrentIndex(id + 1) 

	def Pag1UI(self): #configura o layout da página 1
		
		self.pag1.vbox = QVBoxLayout() #layout que contém a informação da página e a barra inferior de botões
		self.pag1.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.pag1.vbox.addItem(self.pag1.verticalSpacer) #adicionando um espaço no topo da página

		self.pag1.tophbox = QHBoxLayout() #contem logo, título e slogan

		#imagem
		self.pag1.imagem = QLabel(self)
		self.pag1.image_pixmap = QPixmap(LOGO)
		self.pag1.imagem.setPixmap(self.pag1.image_pixmap)

		#título da página
		self.pag1.titulo = QLabel(APP_NAME)
		self.pag1.titulo.setAlignment(QtCore.Qt.AlignCenter)
		titleFont = QtGui.QFont("Helvetica", 20)
		self.pag1.titulo.setFont(titleFont)
		self.pag1.titulo.setStyleSheet("color: #000000")

		#slogan
		self.pag1.slogan = QLabel(SLOGAN)
		self.pag1.slogan.setAlignment(QtCore.Qt.AlignCenter)
		sloganFont = QtGui.QFont("Helvetica", 10)
		self.pag1.slogan.setFont(sloganFont)
		self.pag1.slogan.setStyleSheet("color: #000000")
		self.pag1.slogan.resize(10, 10)

		self.pag1.tophbox.addWidget(self.pag1.imagem) #adicionando imagem
		self.pag1.horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.pag1.tophbox.addItem(self.pag1.horizontalSpacer) #adicionando espaço horizontal entre a imagem e o título

		self.pag1.topvbox = QVBoxLayout()
		self.pag1.topvbox.addWidget(self.pag1.titulo, alignment = QtCore.Qt.AlignCenter) #adicionando título
		self.pag1.topvbox.addWidget(self.pag1.slogan, alignment = QtCore.Qt.AlignCenter) #adicionando slogan

		self.pag1.tophbox.addLayout(self.pag1.topvbox) #adicionando titulo e slogan
		self.pag1.tophbox.addItem(self.pag1.horizontalSpacer) #adicionando espaço horizontal do lado direito do layout horizontal

		self.AddButtons(0) #criando botões

		self.pag1.vbox.addLayout(self.pag1.tophbox) #adicionando o layout exclusivo da página
		self.pag1.vbox.addItem(self.pag1.verticalSpacer) #adicionando spacer no meio

		#configurando barra inferior dos botões
		self.pag1.new_widget = QWidget()
		self.pag1.new_widget.setStyleSheet("background-color: #eeeeee")
		self.pag1.new_widget.setLayout(self.pag1.hbox)

		self.pag1.vbox.addWidget(self.pag1.new_widget) #adicionando barra inferior dos botões
		self.pag1.vbox.setContentsMargins(0,0,0,0) #removendo as margens

		self.pag1.setLayout(self.pag1.vbox) #setando o layout da página inteira

	def Pag2UI(self): #configura o layout da página 2

		self.pag2.vbox = QVBoxLayout() #layout que contém a informação da página e a barra inferior de botões

		self.pag2.hbox2 = QHBoxLayout() #contém o título e o conjunto de parâmetros

		self.pag2.vbox_in = QVBoxLayout() #contém o conjunto de parâmetros
		self.pag2.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.pag2.vbox_in.addItem(self.pag2.verticalSpacer) #adicionando spacer

		#título da página
		self.pag2.titulo = QLabel("Selecione os parâmetros:")
		self.pag2.titulo.setAlignment(QtCore.Qt.AlignCenter)
		self.pag2.titulo.setFont(QtGui.QFont("Helvetica", 15))
		self.pag2.vbox_in.addWidget(self.pag2.titulo, alignment = QtCore.Qt.AlignCenter) #adicionando título

		self.pag2.videos_hbox = QHBoxLayout() #QHBoxLayout que contém titulo e botão do diretório dos vídeos
		self.pag2.videos_label = QLabel("Selecione o diretório que contém os vídeos a serem editados:")
		self.pag2.videos_label.setFont(QtGui.QFont("Helvetica", 10))
		
		self.pag2.videos_lineedit = QLineEdit()
		self.pag2.videos_lineedit.setStyleSheet("background-color:  #ffffff; selection-background-color: #e7e7e3; selection-color: #000000;")
		self.pag2.videos_lineedit.setFont(QtGui.QFont("Helvetica", 8))
		#combobox

		#botão para selecionar diretório que contém os vídeos
		self.pag2.diretorio_videos_botao = QPushButton("Selecione diretório")
		self.pag2.diretorio_videos_botao.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
		self.pag2.diretorio_videos_botao.setFont(QtGui.QFont("Helvetica", 8))
		self.pag2.diretorio_videos_botao.setToolTip("Selecione diretório que contém os vídeos a serem editados!")
		self.pag2.diretorio_videos_botao.clicked.connect(lambda: self.EscolherVideos())

		#adicionando ao layout horizontal
		self.pag2.videos_hbox.addWidget(self.pag2.videos_label)
		self.pag2.videos_hbox.addWidget(self.pag2.videos_lineedit)
		self.pag2.videos_hbox.addWidget(self.pag2.diretorio_videos_botao)
		
		self.pag2.vbox_in.addItem(self.pag2.verticalSpacer) #adicionando spacer
		self.pag2.vbox_in.addLayout(self.pag2.videos_hbox) #adicionando o layout do comprimento

		self.pag2.musica_hbox = QHBoxLayout() #QHBoxLayout que contém título, line edit e botão da música
		#titulo
		self.pag2.musica_label = QLabel("Selecione a música a ser utilizada nos vídeos:")
		self.pag2.musica_label.setFont(QtGui.QFont("Helvetica", 10))
		#lineedit
		self.pag2.musica_lineedit = QLineEdit()
		self.pag2.musica_lineedit.setStyleSheet("background-color:  #ffffff; selection-background-color: #e7e7e3; selection-color: #000000;")
		self.pag2.musica_lineedit.setFont(QtGui.QFont("Helvetica", 8))
		#botão para selecionar arquivo a ser lido
		self.pag2.musica_botao = QPushButton("Selecione arquivo")
		self.pag2.musica_botao.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
		self.pag2.musica_botao.setFont(QtGui.QFont("Helvetica", 8))
		self.pag2.musica_botao.setToolTip("Selecionar arquivo da música a ser utilizada no videoclipe.")
		self.pag2.musica_botao.clicked.connect(lambda: self.EscolherArquivo())

		#adicionando ao layout horizontal
		self.pag2.musica_hbox.addWidget(self.pag2.musica_label)
		self.pag2.musica_hbox.addWidget(self.pag2.musica_lineedit)
		self.pag2.musica_hbox.addWidget(self.pag2.musica_botao)

		self.pag2.vbox_in.addLayout(self.pag2.musica_hbox) #adicionando o layout do diametro externo

		self.pag2.output_video_hbox = QHBoxLayout() #QHBoxLayout que contém título, line edit e botão
		self.pag2.output_video_label = QLabel("Selecione o nome do arquivo onde será salvo o videoclipe finalizado:")
		self.pag2.output_video_label.setFont(QtGui.QFont("Helvetica", 10))
		#lineedit
		self.pag2.output_video_lineedit = QLineEdit()
		self.pag2.output_video_lineedit.setStyleSheet("background-color:  #ffffff; selection-background-color: #e7e7e3; selection-color: #000000;")
		self.pag2.output_video_lineedit.setFont(QtGui.QFont("Helvetica", 8))
		#botão para selecionar arquivo a ser lido
		self.pag2.output_video_botao = QPushButton("Selecione nome do arquivo")
		self.pag2.output_video_botao.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
		self.pag2.output_video_botao.setFont(QtGui.QFont("Helvetica", 8))
		self.pag2.output_video_botao.setToolTip("Determine o nome do videoclipe final.")
		self.pag2.output_video_botao.clicked.connect(lambda: self.EscolherArquivo2())

		#adicionando ao layout horizontal
		self.pag2.output_video_hbox.addWidget(self.pag2.output_video_label)
		self.pag2.output_video_hbox.addWidget(self.pag2.output_video_lineedit)
		self.pag2.output_video_hbox.addWidget(self.pag2.output_video_botao)

		self.pag2.vbox_in.addLayout(self.pag2.output_video_hbox) #adicionando o layout da espessura

		self.pag2.vbox_in.addItem(self.pag2.verticalSpacer) #adicionando spacer

		self.AddButtons(1) #criando botões inferiores

		self.pag2.horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.pag2.hbox2.addItem(self.pag2.horizontalSpacer) 
		self.pag2.hbox2.addLayout(self.pag2.vbox_in) #adicionando título e informações do duto no layout específico da página
		self.pag2.hbox2.addItem(self.pag2.horizontalSpacer)

		self.pag2.vbox.addItem(self.pag2.verticalSpacer) #adicionando spacer
		self.pag2.vbox.addLayout(self.pag2.hbox2) #adicionando o layout específico da página no layout geral da página

		self.pag2.new_widget = QWidget()
		self.pag2.new_widget.setStyleSheet("background-color: #eeeeee")
		self.pag2.new_widget.setLayout(self.pag2.hbox)
		
		self.pag2.vbox.addItem(self.pag2.verticalSpacer)
		self.pag2.vbox.addWidget(self.pag2.new_widget) #adicionando barra inferior de botoões
		self.pag2.vbox.setContentsMargins(0,0,0,0) #removendo as margens

		self.pag2.setLayout(self.pag2.vbox) #adicionando ao layout da página

	def Pag3UI(self): #configura o layout da página 3
		
		self.pag3.vbox = QVBoxLayout() #layout que contém a informação da página e a barra inferior de botões
		self.pag3.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.pag3.vbox.addItem(self.pag3.verticalSpacer) #adicionando um espaço no topo da página

		self.pag3.tophbox = QHBoxLayout() #contem logo, título e slogan

		#imagem
		self.pag3.imagem = QLabel(self)
		self.pag3.image_pixmap = QPixmap(LOGO)
		self.pag3.imagem.setPixmap(self.pag3.image_pixmap)

		#título da página
		self.pag3.titulo = QLabel(APP_NAME)
		self.pag3.titulo.setAlignment(QtCore.Qt.AlignCenter)
		titleFont = QtGui.QFont("Helvetica", 20)
		self.pag3.titulo.setFont(titleFont)
		self.pag3.titulo.setStyleSheet("color: #000000")

		#slogan
		self.pag3.success_message = QLabel(SUCCESS_MESSAGE)
		self.pag3.success_message.setAlignment(QtCore.Qt.AlignCenter)
		success_message_font = QtGui.QFont("Helvetica", 10)
		self.pag3.success_message.setFont(success_message_font)
		self.pag3.success_message.setStyleSheet("color: #000000")
		self.pag3.success_message.resize(10, 10)

		self.pag3.tophbox.addWidget(self.pag3.imagem) #adicionando imagem
		self.pag3.horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.pag3.tophbox.addItem(self.pag3.horizontalSpacer) #adicionando espaço horizontal entre a imagem e o título

		self.pag3.topvbox = QVBoxLayout()
		self.pag3.topvbox.addWidget(self.pag3.titulo, alignment = QtCore.Qt.AlignCenter) #adicionando título
		self.pag3.topvbox.addWidget(self.pag3.success_message, alignment = QtCore.Qt.AlignCenter) #adicionando slogan

		self.pag3.tophbox.addLayout(self.pag3.topvbox) #adicionando titulo e slogan
		self.pag3.tophbox.addItem(self.pag3.horizontalSpacer) #adicionando espaço horizontal do lado direito do layout horizontal

		self.AddButtons(2) #criando botões

		self.pag3.vbox.addLayout(self.pag3.tophbox) #adicionando o layout exclusivo da página
		self.pag3.vbox.addItem(self.pag3.verticalSpacer) #adicionando spacer no meio

		#configurando barra inferior dos botões
		self.pag3.new_widget = QWidget()
		self.pag3.new_widget.setStyleSheet("background-color: #eeeeee")
		self.pag3.new_widget.setLayout(self.pag3.hbox)

		self.pag3.vbox.addWidget(self.pag3.new_widget) #adicionando barra inferior dos botões
		self.pag3.vbox.setContentsMargins(0,0,0,0) #removendo as margens

		self.pag3.setLayout(self.pag3.vbox) #setando o layout da página inteira		

	def AddButtons(self, id):
		#criando a barra de botões inferior de cada página do programa
		if id == 0:
			#hboxlauout que contém os botões
			self.pag1.hbox = QHBoxLayout()
			self.pag1.hbox.addStretch(1)
			self.pag1.font = QtGui.QFont("Helvetica", 8)

			self.pag1.btVoltar = QPushButton("Voltar", self)
			self.pag1.btVoltar.setEnabled(0) #desativando esse botão nessa página
			self.pag1.btVoltar.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
			self.pag1.btVoltar.setFont(self.pag1.font)
			self.pag1.btVoltar.setToolTip("Voltar para página anterior!")

			self.pag1.btAvancar = QPushButton("Avançar")
			self.pag1.btAvancar.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
			self.pag1.btAvancar.setFont(self.pag1.font)
			self.pag1.btAvancar.setToolTip("Avançar para página seguinte!")

			self.pag1.hbox.addWidget(self.pag1.btVoltar, alignment = QtCore.Qt.AlignBottom) #centralizando botões no layout
			self.pag1.hbox.addWidget(self.pag1.btAvancar, alignment = QtCore.Qt.AlignBottom)

		elif id == 1:
			self.pag2.hbox = QHBoxLayout()
			self.pag2.hbox.addStretch(1)
			self.pag2.font = QtGui.QFont("Helvetica", 8)

			self.pag2.btVoltar = QPushButton("Voltar")
			self.pag2.btVoltar.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
			self.pag2.btVoltar.setFont(self.pag2.font)
			self.pag2.btVoltar.setToolTip("Voltar para página anterior!")

			self.pag2.btAvancar = QPushButton("Gerar videoclipe")
			self.pag2.btAvancar.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
			self.pag2.btAvancar.setFont(self.pag2.font)
			self.pag2.btAvancar.setToolTip("Crie o novo videoclipe!")

			self.pag2.hbox.addWidget(self.pag2.btVoltar, alignment = QtCore.Qt.AlignBottom)
			self.pag2.hbox.addWidget(self.pag2.btAvancar, alignment = QtCore.Qt.AlignBottom)

		elif id == 2:
			self.pag3.hbox = QHBoxLayout()
			self.pag3.hbox.addStretch(1)
			self.pag3.font = QtGui.QFont("Helvetica", 8)

			self.pag3.btVoltar = QPushButton("Voltar")
			self.pag3.btVoltar.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
			self.pag3.btVoltar.setFont(self.pag3.font)
			self.pag3.btVoltar.setToolTip("Voltar para página anterior!")

			self.pag3.hbox.addWidget(self.pag3.btVoltar, alignment = QtCore.Qt.AlignBottom)

	def EscolherVideos(self): #abrindo o diálogo para escolher qual arquivo diretório em que estão os vídeos
		self.video_folder_path = str(QFileDialog.getExistingDirectory(None, "Selecione diretório"))
		self.pag2.videos_lineedit.setText(self.video_folder_path)

	def EscolherArquivo(self): #abrindo o diálogo para escolher o arquivo de música
		#aparecendo apenas arquivos do mp3
		audio_formats = "*.mp3 *.wav *.ogg *.wma *.flac"
		filename = QFileDialog().getOpenFileName(filter = audio_formats)
		path = filename[0]
		self.music_path = str(path)
		self.pag2.musica_lineedit.setText(self.music_path)

	def EscolherArquivo2(self): #abrindo o diálogo para escolher o arquivo de saída
		video_formats = "*.mp4"
		output_filename = QFileDialog.getSaveFileName(self, 'Determine nome do arquivo de saída', filter = video_formats)
		self.output_video_filename = output_filename
		self.pag2.output_video_lineedit.setText(self.output_video_filename[0])
		
if __name__ == "__main__":
	app = QApplication([])
	window = VideoclipMaker()
	app.exec()