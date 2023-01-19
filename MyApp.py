import sys, os, re, cv2
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon

from modules import instantsave as iss
from modules import textprocess as tpr


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        # get system path
        self.inpath = str(os.getcwd())

        self.initUI()
    
    # This is main UI.
    def initUI(self):

        self.setWindowTitle("My app")
        self.setWindowIcon(QIcon(self.inpath + "/icons/app_icon.jpg"))
        self.setGeometry(300, 300, 600, 300)

        self.main_tab = QTabWidget()

        self.tab_link_manager = self.link_manager()
        self.tab_file_manager = self.file_manager()
        self.tab_image_manager = self.image_manager()

        self.main_tab.addTab(self.tab_link_manager, "Link")
        self.main_tab.addTab(self.tab_file_manager, "File")
        self.main_tab.addTab(self.tab_image_manager, "Image")

        mainbox = QVBoxLayout()
        mainbox.addWidget(self.main_tab)
        self.setLayout(mainbox)
        self.show()

        self.update_link_manager()
    
    # Main>Tab>Link UI
    def link_manager(self):
        main_widget = QWidget(self)

        self.search_box = QLineEdit()
        self.search_box.returnPressed.connect(self.searchLabels)

        grid = QGridLayout()

        mainwin_group_links = QGroupBox("Recently Links")
        mainwin_group_labels = QGroupBox("Recently Labels")

        vbox_links = QVBoxLayout()
        recently_link_1 = QLabel("None", self)
        recently_link_2 = QLabel("None", self)
        recently_link_3 = QLabel("None", self)
        recently_link_4 = QLabel("None", self)
        recently_link_5 = QLabel("None", self)
        self.recently_links_list = [recently_link_1, recently_link_2, recently_link_3, recently_link_4, recently_link_5]
        for r in self.recently_links_list:
            vbox_links.addWidget(r)
        
        mainwin_group_links.setLayout(vbox_links)

        vbox_labels = QVBoxLayout()
        recently_label_1 = QLabel("None", self)
        recently_label_2 = QLabel("None", self)
        recently_label_3 = QLabel("None", self)
        recently_label_4 = QLabel("None", self)
        recently_label_5 = QLabel("None", self)
        self.recently_labels_list = [recently_label_1, recently_label_2, recently_label_3, recently_label_4, recently_label_5]
        for r in self.recently_labels_list:
            vbox_labels.addWidget(r)

        mainwin_group_labels.setLayout(vbox_labels)

        grid.addWidget(mainwin_group_links, 0, 0)
        grid.addWidget(mainwin_group_labels, 0, 1)

        buttons_bar = QHBoxLayout()

        self.add_label = QPushButton("Label+")
        self.add_label.setMaximumSize(50, 50)
        self.add_label.clicked.connect(self.append_label)

        self.del_label = QPushButton("Label-")
        self.del_label.setMaximumSize(50, 50)
        self.del_label.clicked.connect(self.delete_label)

        self.add_link = QPushButton("Link+")
        self.add_link.setMaximumSize(50, 50)
        self.add_link.clicked.connect(self.append_link)

        self.del_link = QPushButton("Link-")
        self.del_link.setMaximumSize(50, 50)
        self.del_link.clicked.connect(self.delete_link)

        self.open_trash = QPushButton("Trash")
        self.open_trash.setMaximumSize(50, 50)

        self.setting = QPushButton("setting")
        self.setting.setMaximumSize(50, 50)

        buttons_bar.addWidget(self.add_label)
        buttons_bar.addWidget(self.del_label)
        buttons_bar.addWidget(self.add_link)
        buttons_bar.addWidget(self.del_link)
        buttons_bar.addWidget(self.open_trash)
        buttons_bar.addWidget(self.setting)

        vbox_main = QVBoxLayout()
        vbox_main.addWidget(self.search_box)
        vbox_main.addLayout(grid)
        vbox_main.addLayout(buttons_bar)

        main_widget.setLayout(vbox_main)
        
        return main_widget
    
    # Main>Tab>Link&update Func
    def update_link_manager(self):
        read_recently_links = open(self.inpath+"/file_tab/docs/recently_log/recently_links.txt", 'r')
        recently_links = read_recently_links.readlines()
        try:
            n = 0
            for l in recently_links:
                r = self.recently_links_list[n]
                show_l = tpr.link_short(l)
                
                r.setText(show_l+" "+"<a href=\"{}\">Go</a>".format(l))
                r.setTextFormat(Qt.RichText)
                r.setOpenExternalLinks(True)
                n += 1
        except:
            print("Error --update recently links")
        
        read_recently_labels = open(self.inpath+"/file_tab/docs/recently_log/recently_labels.txt", 'r')
        recently_labels = read_recently_labels.readlines()
        try:
            n = 0
            for l in recently_labels:
                l = tpr.text_short(l)
                r = self.recently_labels_list[n]
                
                r.setText(l)
                n += 1
        except:
            print("Error --update recently labels")
    
    # Main>Tab>File UI
    def file_manager(self):
        main_widget = QWidget(self)

        return main_widget
    
    def image_manager(self):
        main_widget = QWidget(self)

        
        return main_widget
    
    # search Labels in Links
    def searchLabels(self):
        keyword = self.search_box.text()
        self.search_box.clear()

        labels = self.readLabels()
        links = list(self.readLinks(labels).values())
        search_key = re.compile(keyword)

        result_labels = []
        for l in labels:
            if re.findall(search_key, str(l)):
                result_labels.append(l)
            else:
                pass
        
        result_links = []
        for link in links:
            for l in link:
                #print(l)
                if re.findall(search_key, str(l)):
                    result_links.append(l)
                else:
                    pass
        
        if result_labels or result_links:
            print("find:", result_labels, result_links)
            result_links_process = set(result_links)
            result_links = list(result_links_process)
            result_links.sort()
            self.searchresult = [result_labels, result_links]
            if result_labels is None: result_labels = ""
            if result_links is None: result_links = ""
            
            iss.save_recently(self.inpath, 0, result_labels)
            iss.save_recently(self.inpath, 1, result_links)
            self.update_link_manager()

            self.createResultWindow()
        else:
            reply = QMessageBox.question(self, "Error", "There are no results.")
    
    def append_label(self):
        label, ok = QInputDialog.getText(self, "QWindow", "Enter your label name")
        if ok:
            added = self.addLabels(str(label))
        else:
            added = 1
        if added:
            pass
        else:
            reply = QMessageBox.question(self, "Error", "This label already exists.")
    
    def delete_label(self):
        labels = self.readLabels()
        label, ok = QInputDialog.getItem(self, "QWindow", "Choose label you want to delete.", labels)

        if ok:
            deleted = self.delLabels(str(label))
    
    def append_link(self):
        labels = self.readLabels()
        labels_new = []
        for l in labels:
            l.replace(" ", "_")
            labels_new.append(l)
        labels = labels_new.copy()

        vbox = QVBoxLayout()

        self.dialog_append = QDialog(self)
        self.dialog_append.resize(200, 200)
        
        self.combobox = QComboBox(self)
        for l in labels:
            self.combobox.addItem(str(l))
        
        self.combobox.activated[str].connect(self.combobox_connection_append)
        self.append_link_in = "major_site"
        
        self.append_link_list = []
        self.lineedit = QLineEdit(self)
        self.lineedit.returnPressed.connect(self.lineedit_connection)

        self.button_temp = QPushButton("+")
        self.button_temp.setMaximumSize(50, 50)
        self.button_ok = QPushButton("OK")
        self.button_ok.clicked.connect(self.dialog_ok_append)
        self.button_ok.setChecked(False)
        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.dialog_cancel_append)
        self.button_cancel.setChecked(False)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button_temp)
        hbox.addWidget(self.button_ok)
        hbox.addWidget(self.button_cancel)

        vbox.addWidget(self.combobox)
        vbox.addWidget(self.lineedit)
        vbox.addLayout(hbox)

        self.dialog_append.setLayout(vbox)
        self.dialog_append.show()
    
    def dialog_ok_append(self):
        self.dialog_append.close()
        label = [self.append_link_in]
        links = self.append_link_list

        add, added = self.addLinks(label, links)
        print(add, added)
    
    def dialog_cancel_append(self):
        self.dialog_append.close()

    def combobox_connection_append(self, label):
        self.append_link_in = label
    
    def lineedit_connection(self):
        self.append_link_list.append(self.lineedit.text())
        self.lineedit.clear()
    
    def createResultWindow(self):
        self.resultwindow = ResultWindow(self.searchresult)
        self.resultwindow.show()
    
    def delete_link(self):
        labels = self.readLabels()
        labels_new = []
        for l in labels:
            l.replace(" ", "_")
            labels_new.append(l)
        labels = labels_new.copy()

        self.vbox = QVBoxLayout()
        self.checks = QVBoxLayout()
        self.now_checked = []

        self.dialog_delete = QDialog(self)
        self.dialog_delete.resize(200, 200)

        self.combobox = QComboBox(self)
        for l in labels:
            self.combobox.addItem(str(l))
        
        self.combobox.activated[str].connect(self.combobox_connection_delete)
        self.append_link_in = "major_site"

        self.button_ok = QPushButton("OK")
        self.button_ok.clicked.connect(self.dialog_ok_delete)
        self.button_ok.setChecked(False)
        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.dialog_cancel_delete)
        self.button_cancel.setChecked(False)

        hbox = QHBoxLayout()
        hbox.addWidget(self.button_ok)
        hbox.addWidget(self.button_cancel)

        self.vbox.addWidget(self.combobox)
        self.vbox.addLayout(self.checks)
        self.vbox.addLayout(hbox)

        self.dialog_delete.setLayout(self.vbox)
        self.dialog_delete.show()
    
    def dialog_ok_delete(self):
        self.dialog_delete.close()
        label = self.delete_link_in
        links = []
        for n in self.now_checked:
            links.append(self.var_list_row[n])

        b = self.delLinks(list([label]), links)
        print(b[0], b[1])
    
    def dialog_cancel_delete(self):
        self.dialog_delete.close()
    
    def combobox_connection_delete(self, label):
        self.combobox.setEnabled(False)

        self.checks = QVBoxLayout()
        self.delete_link_in = label

        links = self.readLinks(list([self.delete_link_in]))
        links = list(links.values())[0]

        self.var_list_process = []
        self.var_list_row = []

        for l in links:
            self.var_list_row.append(l)
            name = l[:]
            ban = ["+", "-", "*", "/", "$", "@", "&", "%", ".", ":", "\d"]
            for b in ban:
                name = name.replace(b, "_")
            
            if len(name) >= 45:
                self.var_list_process.append("self.v_"+str(name[5:45]))
                name = name[5:45]
            else:
                self.var_list_process.append("self.v_"+str(name))
                name = name
            command = f"""self.v_{name} = QCheckBox('{l}', self);self.v_{name}.stateChanged.connect(self.check_status);self.checks.addWidget(self.v_{name})"""

            exec(command)
        
        self.vbox.addLayout(self.checks)

        self.dialog_delete.update()
    
    def check_status(self, check):
        active = []
        for v in self.var_list_process:
            command = f"if "+str(v)+".isChecked(): num = self.var_list_process.index('"+str(v)+"'); active.append(num)"
            exec(command)
        
        self.now_checked = active
        
    # read labels file in {inpath} + "labels.txt"
    def readLabels(self):
        get_Labels = open(self.inpath+"/file_tab/docs/labels.txt", 'r')
        labels = get_Labels.read()
        labels = labels.split("\n")
        get_Labels.close()

        return labels
    
    # add labels file in {inpath} + "labels.txt"
    def addLabels(self, input_label: str):
        in_labels = self.readLabels()
        if input_label in in_labels:
            return False

        open_Labels = open(self.inpath+"/file_tab/docs/labels.txt", 'a')
        open_Labels.write("\n" + input_label)
        open_Labels.close()

        return True
    
    # delete labels file in {inpath} + "labels.txt"
    def delLabels(self, input_label: str):
        open_Labels = open(self.inpath+"/file_tab/docs/labels.txt", 'r')
        labels_origin = open_Labels.read()
        labels_origin = labels_origin.split('\n')
        labels_edited = labels_origin.copy()
        deleted = False
        for l in labels_origin:
            if l == input_label:
                labels_edited.remove(l)
                deleted = True
        open_Labels.close()
        
        rewrite_Labels = open(self.inpath+"/file_tab/docs/labels.txt", 'w')
        for l in labels_edited:
            #print("l:", l)
            if (labels_edited.index(l) + 1) == len(labels_edited):
                end = ""
            else:
                end = "\n"
            rewrite_Labels.write(l + end)
        
        # copy rewrite labels 
        rewrite_Labels.close()
        
        contents = self.readLinks(list([input_label]))
        contents = list(contents.values())[0]
        input_label = input_label.replace(" ", "_")
        write_temp = open(self.inpath+"/file_tab/docs/temp_file_memory/"+input_label+"_temp.txt", 'w')
        for c in contents:
            if (contents.index(c) + 1) == len(contents):
                end = ""
            else:
                end = "\n"
            write_temp.write(c + end)
        
        write_temp.close()

        return deleted
    
    # read links file in {inpath} + "~.txt"
    def readLinks(self, labels: list):
        new_list = []
        for l in labels:
            if l not in new_list:
                new_list.append(l)
        labels = new_list.copy()
        
        links_dict = {}
        for label in labels:
            if re.match(".+\s.+", str(label)):
                # filename: " " --> "_" / labelname in file(labels.txt): " " --> " "
                label = label.replace(" ", "_")
            try:
                get_Links = open(self.inpath+"/file_tab/docs/link_files/"+str(label)+".txt", 'r')
            except:
                continue
            get = get_Links.read()
            #print("get:\n", get, "\n", type(get))
            links = get.split('\n')
            new_links = []

            try:
                for l in links:
                    # expression: http(s)://(domain)/
                    forming = re.match("(?P<matching>(https:[/][/])?(www[.])?.+[.].+[/]?)", l)
                    new_links.append(str(forming.group('matching')))
            except:
                print("Error (no links) --readLinks")
            finally:
                get_Links.close()
            
            links = new_links.copy()
            links_dict[str(label)] = links
            
        return links_dict
    
    # add links file in {inpath} + "~.txt"
    def addLinks(self, labels: list, links: list):
        in_links = self.readLinks(labels)
        added = 0
        not_added = 0
        for label in labels:
            for l in links:
                if l in in_links[label]:
                    links.remove(l)
                    not_added += 1
                else:
                    added += 1

        open_Links = open(self.inpath+"/file_tab/docs/link_files/"+str(labels[0])+".txt", 'a')
        new_links = []

        try:
            for l in links:
                # expression: http(s)://(domain)/
                forming = re.match("(?P<matching>(https:[/][/])?www[.].+[.].+[/]?)", l)
                new_links.append(str(forming.group('matching')))
        except:
            print("Error (no links) --addLinks")

        for l in links:
            open_Links.write("\n" + l)
        
        open_Links.close()

        return True, [added, not_added]
    
    # delete links file in {inpath} + "~.txt"
    def delLinks(self, labels: list, input_links: list):
        open_Links = open(self.inpath+"/file_tab/docs/link_files/"+str(labels[0].replace(" ", "_"))+".txt", 'r')
        links_origin = open_Links.read()
        links_origin = links_origin.split('\n')
        links_edited = links_origin.copy()
        processing = links_edited + input_links
        #print(processing, type(processing))
        elements = links_origin.copy()

        deleted = 0
        not_deleted = 0

        for e in elements:
            if processing.count(e) >= 2:
                links_edited.remove(e)
                deleted += 1
            else:
                not_deleted += 1
        open_Links.close()

        rewrite_Links = open(self.inpath+"/file_tab/docs/link_files/"+str(labels[0].replace(" ", "_"))+".txt", 'w')

        for l in links_edited:
            #print("l:", l)
            if (links_edited.index(l) + 1) == len(links_edited):
                end = ""
            else:
                end = "\n"
            rewrite_Links.write(l + end)
        rewrite_Links.close()

        return [deleted, not_deleted]

class ResultWindow(QWidget):

    def __init__(self, result):
        super().__init__()

        self.setWindowTitle("Search Results")
        #self.setWindowIcon(QIcon(self.inpath + "/icons/app_icon.jpg"))
        self.setGeometry(400, 300, 300, 300)

        self.results_labels = result[0]
        self.results_links = result[1]

        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        results_labels = QGroupBox("Labels")

        vbox_label = QVBoxLayout()
        
        try:
            n = 0
            for l in self.results_labels:
                label = QLabel(l)
                vbox_label.addWidget(label)
                if n >= 4:
                    label_so_on = QLabel("...")
                    vbox_label.addWidget(label_so_on)
                    break
                n += 1
        except:
            pass
        if self.results_labels:
            pass
        else:
            label_none = QLabel("None")
            vbox_label.addWidget(label_none)

        results_labels.setLayout(vbox_label)
        
        results_links = QGroupBox("Links")

        vbox_link = QVBoxLayout()
        
        try:
            n = 0
            for l in self.results_links:
                self.show_l = tpr.link_short(l)
                link = QLabel(self.show_l+" "+"<a href=\"{}\">Go</a>".format(l))
                link.setOpenExternalLinks(True)
                vbox_link.addWidget(link)
                if n >= 4:
                    label_so_on = QLabel("...")
                    vbox_link.addWidget(label_so_on)
                    break
        except:
            pass
        if self.results_links:
            pass
        else:
            label_none = QLabel("None")
            vbox_link.addWidget(label_none)

        results_links.setLayout(vbox_link)

        button_plus_label = QPushButton("+", self)
        button_plus_label.setMaximumSize(50, 50)
        button_plus_label.clicked.connect(self.createExpansionWin_label)

        button_plus_link = QPushButton("+", self)
        button_plus_link.setMaximumSize(50, 50)
        button_plus_link.clicked.connect(self.createExpansionWin_link)

        grid.addWidget(results_labels, 0, 0)
        grid.addWidget(results_links, 1, 0)
        grid.addWidget(button_plus_label, 0, 1)
        grid.addWidget(button_plus_link, 1, 1)

        self.setLayout(grid)
    
    def createExpansionWin_label(self):
        self.expansionwindow = ExpansionWindow(self.results_labels, 0)
        self.expansionwindow.show()
    
    def createExpansionWin_link(self):
        self.expansionwindow = ExpansionWindow(self.results_links, 1)
        self.expansionwindow.show()

class ExpansionWindow(QWidget):

    def __init__(self, contents, what):
        super().__init__()

        self.setWindowTitle("Expansion Results")
        #self.setWindowIcon(QIcon(self.inpath + "/icons/app_icon.jpg"))
        self.setGeometry(600, 300, 300, 500)
        self.gets = contents
        self.what = what

        self.initUI()

    def initUI(self):
        main_widget = QWidget(self)

        vbox = QVBoxLayout()
        for g in self.gets:
            label = QLabel()
            if self.what == 0:
                label.setText(g)
            elif self.what == 1:
                self.show_g = tpr.link_short(g)
                label.setText(self.show_g+" "+"<a href=\"{}\">Go</a>".format(g))
                label.setTextFormat(Qt.RichText)
                label.setOpenExternalLinks(True)
            else:
                label.setText("Error")
            vbox.addWidget(label)
        
        main_widget.setLayout(vbox)
        
        scroll = QScrollArea()
        scroll.setWidget(main_widget)
        scroll.setWidgetResizable(True)

        show_layout = QVBoxLayout()
        show_layout.addWidget(scroll)
        self.setLayout(show_layout)



# start program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    
    win.show()
    app.exec()