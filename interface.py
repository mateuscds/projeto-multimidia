##### PyQt5 IMPORTS #####
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDesktopWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStackedWidget, QLineEdit, QSpacerItem, QSizePolicy, QFileDialog
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

##### SynchroEditor IMPORT  #####
from synchroeditor import SynchroEditor

##### OS IMPORTS #####
from os import listdir
from os.path import isfile, join

##### UI ELEMENTS #####
ICON = 'images/icon.png'
LOGO = 'images/logo.jpg'
APP_NAME = 'SynchroEditor'
SLOGAN = 'Sincronize seus vídeos com música de forma simples e rápida!'
SUCCESS_MESSAGE = 'Seu vídeo já está pronto! Obrigado por escolher o SynchroEditor!'

class SynchroEditorUI(QWidget):
	def __init__(self):
		
		super().__init__()

		#configurações gerais da janela
		self.title = APP_NAME
		self.top = 100
		self.left = 100
		self.width = 830
		self.heigh = 630
		self.iconName = ICON
		self.setFixedSize(self.width, self.heigh)
		self.InitProgram()

	def InitProgram(self):

		#aplicando as configurações gerais da janela
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

		#primeira página
		self.pag1 = QWidget()
		self.pag1.setStyleSheet("background-color: #ffffff")
		self.Pag1UI()
		self.pag1.btAvancar.clicked.connect(lambda: self.BotaoAvancar(0))
		#segunda página
		self.pag2 = QWidget()
		self.pag2.setStyleSheet("background-color: #ffffff")
		self.Pag2UI()
		self.pag2.btAvancar.clicked.connect(lambda: self.BotaoAvancar(1))
		self.pag2.btVoltar.clicked.connect(lambda: self.BotaoVoltar(1))
		#terceira página
		self.pag3 = QWidget()
		self.pag3.setStyleSheet("background-color: #ffffff")
		self.Pag3UI()
		self.pag3.btVoltar.clicked.connect(lambda: self.BotaoVoltar(2))

		#adicionando as páginas
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
			#se todos os parâmetros de entrada foram definidos pelo usuário, instânciamos o SynchroEditor e avançamos a página
			if hasattr(self, 'video_folder_path') and hasattr(self, 'music_path') and hasattr(self, 'output_video_filename') and self.video_folder_path != '' and self.music_path != '' and self.output_video_filename != '':				
				
				QApplication.setOverrideCursor(Qt.WaitCursor)

				#parâmetros default
				min_interval_between_moments = 2
				method = 'onset'
				clicks = False

				#criando lista com os caminhos de todos os vídeos no diretório indicado para obter o formato de entrada correto para o editor
				onlyfiles = [f for f in listdir(self.video_folder_path) if isfile(join(self.video_folder_path + '/', f))]
				input_video_paths = []
				for path in onlyfiles:
					if path.endswith('.mp4'):
						input_video_paths.append(path)
				
				#fazendo a chamada de edição dos vídeos
				synchro_editor = SynchroEditor(self.music_path, input_video_paths, self.output_video_filename)
				synchro_editor.merge(method, clicks, min_interval_between_moments)

				QApplication.restoreOverrideCursor()
				self.stackedWidget.setCurrentIndex(id + 1) 

	def Pag1UI(self): 
		
		#configura a página 1
		
		self.pag1.vbox = QVBoxLayout() 
		self.pag1.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.pag1.vbox.addItem(self.pag1.verticalSpacer)

		#imagem
		self.pag1.imagem = QLabel(self)
		self.pag1.image_pixmap = QPixmap(LOGO)
		self.pag1.imagem.setPixmap(self.pag1.image_pixmap)

		#título
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

		self.pag1.vbox.addWidget(self.pag1.imagem, alignment = QtCore.Qt.AlignCenter) 
		self.pag1.horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.pag1.vbox.addItem(self.pag1.horizontalSpacer) 
		self.pag1.vbox.addWidget(self.pag1.titulo, alignment = QtCore.Qt.AlignCenter) 
		self.pag1.vbox.addWidget(self.pag1.slogan, alignment = QtCore.Qt.AlignCenter) 
		self.pag1.vbox.addItem(self.pag1.horizontalSpacer)

		self.AddButtons(0)
		self.pag1.vbox.addItem(self.pag1.verticalSpacer)
		self.pag1.new_widget = QWidget()
		self.pag1.new_widget.setStyleSheet("background-color: #eeeeee")
		self.pag1.new_widget.setLayout(self.pag1.hbox)
		self.pag1.vbox.addWidget(self.pag1.new_widget)
		self.pag1.vbox.setContentsMargins(0,0,0,0)

		self.pag1.setLayout(self.pag1.vbox) 

	def Pag2UI(self): 
		
		#configura a página 2

		self.pag2.vbox = QVBoxLayout()
		self.pag2.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.pag2.vbox.addItem(self.pag2.verticalSpacer)

		self.pag2.titulo = QLabel("Selecione os parâmetros de entrada:")
		self.pag2.titulo.setAlignment(QtCore.Qt.AlignCenter)
		self.pag2.titulo.setFont(QtGui.QFont("Helvetica", 15))
		self.pag2.vbox.addWidget(self.pag2.titulo, alignment = QtCore.Qt.AlignCenter)

		label = QLabel(" ")
		label.setFont(QtGui.QFont('Helvetica', 8))

		self.pag2.videos_hbox = QHBoxLayout()
		self.pag2.videos_hbox.addWidget(label)
		self.pag2.videos_label = QLabel("Selecione o diretório que contém os vídeos a serem editados:")
		self.pag2.videos_label.setFont(QtGui.QFont("Helvetica", 10))
		self.pag2.videos_lineedit = QLineEdit()
		self.pag2.videos_lineedit.setStyleSheet("background-color:  #ffffff; selection-background-color: #e7e7e3; selection-color: #000000;")
		self.pag2.videos_lineedit.setFont(QtGui.QFont("Helvetica", 8))
		self.pag2.diretorio_videos_botao = QPushButton("Selecione diretório")
		self.pag2.diretorio_videos_botao.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
		self.pag2.diretorio_videos_botao.setFont(QtGui.QFont("Helvetica", 8))
		self.pag2.diretorio_videos_botao.setToolTip("Selecione diretório que contém os vídeos a serem editados!")
		self.pag2.diretorio_videos_botao.clicked.connect(lambda: self.DiretorioDeVideos())
		self.pag2.videos_hbox.addWidget(self.pag2.videos_label)
		self.pag2.videos_hbox.addWidget(self.pag2.videos_lineedit)
		self.pag2.videos_hbox.addWidget(self.pag2.diretorio_videos_botao)
		self.pag2.videos_hbox.addWidget(label)
		
		self.pag2.musica_hbox = QHBoxLayout()
		self.pag2.musica_hbox.addWidget(label)
		self.pag2.musica_label = QLabel("Selecione a música a ser utilizada no vídeo final:")
		self.pag2.musica_label.setFont(QtGui.QFont("Helvetica", 10))
		self.pag2.musica_lineedit = QLineEdit()
		self.pag2.musica_lineedit.setStyleSheet("background-color:  #ffffff; selection-background-color: #e7e7e3; selection-color: #000000;")
		self.pag2.musica_lineedit.setFont(QtGui.QFont("Helvetica", 8))
		self.pag2.musica_botao = QPushButton("Selecione arquivo")
		self.pag2.musica_botao.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
		self.pag2.musica_botao.setFont(QtGui.QFont("Helvetica", 8))
		self.pag2.musica_botao.setToolTip("Selecione o arquivo da música a ser utilizada no vídeo final!")
		self.pag2.musica_botao.clicked.connect(lambda: self.ArquivoDeMusica())
		self.pag2.musica_hbox.addWidget(self.pag2.musica_label)
		self.pag2.musica_hbox.addWidget(self.pag2.musica_lineedit)
		self.pag2.musica_hbox.addWidget(self.pag2.musica_botao)
		self.pag2.musica_hbox.addWidget(label)

		self.pag2.output_video_hbox = QHBoxLayout()
		self.pag2.output_video_hbox.addWidget(label)
		self.pag2.output_video_label = QLabel("Selecione o nome do arquivo onde será salvo o vídeo final:")
		self.pag2.output_video_label.setFont(QtGui.QFont("Helvetica", 10))
		self.pag2.output_video_lineedit = QLineEdit()
		self.pag2.output_video_lineedit.setStyleSheet("background-color:  #ffffff; selection-background-color: #e7e7e3; selection-color: #000000;")
		self.pag2.output_video_lineedit.setFont(QtGui.QFont("Helvetica", 8))
		self.pag2.output_video_botao = QPushButton("Selecione nome do arquivo")
		self.pag2.output_video_botao.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
		self.pag2.output_video_botao.setFont(QtGui.QFont("Helvetica", 8))
		self.pag2.output_video_botao.setToolTip("Selecione o nome do videoclipe final!")
		self.pag2.output_video_botao.clicked.connect(lambda: self.ArquivoDeSaida())
		self.pag2.output_video_hbox.addWidget(self.pag2.output_video_label)
		self.pag2.output_video_hbox.addWidget(self.pag2.output_video_lineedit)
		self.pag2.output_video_hbox.addWidget(self.pag2.output_video_botao)
		self.pag2.output_video_hbox.addWidget(label)
		
		self.pag2.vbox.addLayout(self.pag2.videos_hbox)
		self.pag2.vbox.addLayout(self.pag2.musica_hbox)
		self.pag2.vbox.addLayout(self.pag2.output_video_hbox)

		self.AddButtons(1)
		self.pag2.new_widget = QWidget()
		self.pag2.new_widget.setStyleSheet("background-color: #eeeeee")
		self.pag2.new_widget.setLayout(self.pag2.hbox)
		self.pag2.vbox.addItem(self.pag2.verticalSpacer)
		self.pag2.vbox.addWidget(self.pag2.new_widget)
		self.pag2.vbox.setContentsMargins(0, 0, 0, 0)

		self.pag2.setLayout(self.pag2.vbox)

	def Pag3UI(self): 
		
		#configura a página 3
		
		self.pag3.vbox = QVBoxLayout()
		self.pag3.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.pag3.vbox.addItem(self.pag3.verticalSpacer)

		#imagem
		self.pag3.imagem = QLabel(self)
		self.pag3.image_pixmap = QPixmap(LOGO)
		self.pag3.imagem.setPixmap(self.pag3.image_pixmap)

		#título
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

		self.pag3.vbox.addWidget(self.pag3.imagem, alignment = QtCore.Qt.AlignCenter)
		self.pag3.horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.pag3.vbox.addItem(self.pag3.horizontalSpacer)
		self.pag3.vbox.addWidget(self.pag3.titulo, alignment = QtCore.Qt.AlignCenter)
		self.pag3.vbox.addWidget(self.pag3.success_message, alignment = QtCore.Qt.AlignCenter)
		self.pag3.vbox.addItem(self.pag3.horizontalSpacer) 

		self.AddButtons(2) 
		self.pag3.vbox.addItem(self.pag3.verticalSpacer)
		self.pag3.new_widget = QWidget()
		self.pag3.new_widget.setStyleSheet("background-color: #eeeeee")
		self.pag3.new_widget.setLayout(self.pag3.hbox)
		self.pag3.vbox.addWidget(self.pag3.new_widget) 
		self.pag3.vbox.setContentsMargins(0,0,0,0)

		self.pag3.setLayout(self.pag3.vbox)

	def AddButtons(self, id):
		#criando a barra de botões inferior de cada página do programa
		if id == 0:

			self.pag1.hbox = QHBoxLayout()
			self.pag1.hbox.addStretch(1)
			self.pag1.font = QtGui.QFont("Helvetica", 8)

			self.pag1.btVoltar = QPushButton("Voltar", self)
			self.pag1.btVoltar.setEnabled(0) #desativando esse botão nessa página
			self.pag1.btVoltar.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
			self.pag1.btVoltar.setFont(self.pag1.font)
			self.pag1.btVoltar.setToolTip("Volte para página anterior!")

			self.pag1.btAvancar = QPushButton("Avançar")
			self.pag1.btAvancar.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
			self.pag1.btAvancar.setFont(self.pag1.font)
			self.pag1.btAvancar.setToolTip("Avance para página seguinte!")

			self.pag1.hbox.addWidget(self.pag1.btVoltar, alignment = QtCore.Qt.AlignBottom)
			self.pag1.hbox.addWidget(self.pag1.btAvancar, alignment = QtCore.Qt.AlignBottom)

		elif id == 1:

			self.pag2.hbox = QHBoxLayout()
			self.pag2.hbox.addStretch(1)
			self.pag2.font = QtGui.QFont("Helvetica", 8)

			self.pag2.btVoltar = QPushButton("Voltar")
			self.pag2.btVoltar.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
			self.pag2.btVoltar.setFont(self.pag2.font)
			self.pag2.btVoltar.setToolTip("Voltar para página anterior!")

			self.pag2.btAvancar = QPushButton("Gerar vídeo")
			self.pag2.btAvancar.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
			self.pag2.btAvancar.setFont(self.pag2.font)
			self.pag2.btAvancar.setToolTip("Gere o novo vídeo!")

			self.pag2.hbox.addWidget(self.pag2.btVoltar, alignment = QtCore.Qt.AlignBottom)
			self.pag2.hbox.addWidget(self.pag2.btAvancar, alignment = QtCore.Qt.AlignBottom)

		elif id == 2:

			self.pag3.hbox = QHBoxLayout()
			self.pag3.hbox.addStretch(1)
			self.pag3.font = QtGui.QFont("Helvetica", 8)

			self.pag3.btVoltar = QPushButton("Voltar")
			self.pag3.btVoltar.setStyleSheet( "QPushButton { background-color: #eeeeee }" )
			self.pag3.btVoltar.setFont(self.pag3.font)
			self.pag3.btVoltar.setToolTip("Volte para página anterior!")

			self.pag3.hbox.addWidget(self.pag3.btVoltar, alignment = QtCore.Qt.AlignBottom)

	def DiretorioDeVideos(self): 
		#abrindo o popup para escolher qual o diretório em que estão os vídeos a serem editados
		self.video_folder_path = str(QFileDialog.getExistingDirectory(None, "Selecione diretório"))
		self.pag2.videos_lineedit.setText(self.video_folder_path)

	def ArquivoDeMusica(self): 
		#abrindo o popup para escolher o arquivo de música de entrada
		#aparecendo apenas arquivos mp3
		audio_formats = "*.mp3"
		filename = QFileDialog().getOpenFileName(filter = audio_formats)
		path = filename[0]
		self.music_path = str(path)
		self.pag2.musica_lineedit.setText(self.music_path)

	def ArquivoDeSaida(self): 
		#abrindo o popup para escolher o nome do arquivo de saída
		#será salvo em mp4
		video_formats = "*.mp4"
		output_filename = QFileDialog.getSaveFileName(self, 'Determine nome do arquivo de saída', filter = video_formats)
		self.output_video_filename = output_filename
		self.pag2.output_video_lineedit.setText(self.output_video_filename[0])