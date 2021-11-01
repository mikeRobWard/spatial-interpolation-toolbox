# GUI imports
from windows.main_window import Ui_sp_int_tbox
from windows.aw_widget import Ui_Areal_Weight
from windows.binary_widget import Ui_Binary_Method
from windows.expert_widget import Ui_Expert_Method
from windows.lv_widget import Ui_Limiting_Variable_Method
from windows.nclass_widget import Ui_N_Class_Method
from windows.parcel_widget import Ui_Parcel_Method

# PyQt imports
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui

# interpolation imports
from modules.sp_interpolate import arealwt, binary_vector, parcel_method, expert_system, lim_var, n_class

# Functional imports
import geopandas as gpd
import sys

#############################################################################################
class projectWidget(qtw.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_sp_int_tbox()        
        self.ui.setupUi(self)      
        self.ui.buttonOpenmethod.clicked.connect(self.open_intp_method)
        title = "Spatial Interpolation Toolbox"
        self.setWindowTitle(title)
        self.ui.label_3.setOpenExternalLinks(True)
        
    # function to handle which method to open
    def open_intp_method(self):
        index = self.ui.boxSelectmethod.currentIndex() # get current index of combo box
        if index == 0:
            self.aw = aw()
            self.aw.show()
        elif index == 1:
            self.bm = bm()
            self.bm.show()
        elif index == 2:
            self.lv = lv()
            self.lv.show()
        elif index == 3:
            self.nc = nc()
            self.nc.show()
        elif index == 4:
            self.pm = pm()
            self.pm.show()
        elif index == 5:
            self.em = em()
            self.em.show()
   
################################################################################################            
class aw_Worker(qtc.QObject):
    finished = qtc.pyqtSignal() # finished signal
    nono = qtc.pyqtSignal() # main function error
    src_error = qtc.pyqtSignal() # source shapefile error
    target_error = qtc.pyqtSignal() # target shapefile error
    countChanged = qtc.pyqtSignal(int) # update progbar signal
    
    @qtc.pyqtSlot(str,str,list,str,str) # decorator to allow arguments
    def worker_func(self, src, target, intp, suffix, save):
        count = 0
        try:
            print("analyzing source shapefile")
            src = gpd.read_file(src)
            count += 10
            self.countChanged.emit(count)
        except:
            self.src_error.emit()
            return
        try:
            print("analyzing target shapefile")
            target = gpd.read_file(target)
            count += 10
            self.countChanged.emit(count)
        except:
            self.target_error.emit()
            return
        try:
            outp = arealwt(src, target, intp, suffix)
            count += 75
            self.countChanged.emit(count)
            print("saving results")
            outp.to_file(save)
            count += 5
            self.countChanged.emit(count)
            self.finished.emit()
        except:
            self.nono.emit()
            return
            
class aw(qtw.QWidget):
    worker_requested = qtc.pyqtSignal(str,str,list,str,str) # emits signal to worker
    def __init__(self):
        super().__init__()
        self.ui = Ui_Areal_Weight()
        self.ui.setupUi(self)
        self.ui.aw_source_browse.clicked.connect(self.source_browser) 
        self.ui.aw_target_browse.clicked.connect(self.target_browser)
        self.ui.aw_save_browse.clicked.connect(self.save_browser)
        self.ui.aw_run_prog.clicked.connect(self.run_aw)
        self.ui.aw_cancel_prog.clicked.connect(self.close_aw)
        title = "Areal Weighting Method"
        self.setWindowTitle(title)        
    def source_browser(self):
        self.filename = QFileDialog.getOpenFileName()
        self.ui.aw_source_lineedit.setText(self.filename[0])  
    def target_browser(self):
        self.filename = QFileDialog.getOpenFileName()
        self.ui.aw_target_lineedit.setText(self.filename[0])    
    def save_browser(self):
        self.filename = QFileDialog.getSaveFileName()
        self.ui.aw_save_lineedit.setText(self.filename[0])          
    def run_aw(self):
        # get data from gui
        src = self.ui.aw_source_lineedit.text()
        target = self.ui.aw_target_lineedit.text()
        intp = self.ui.aw_intp_fields.text()
        intp = intp.split()
        suffix = self.ui.aw_output_suffix.text()
        save = self.ui.aw_save_lineedit.text()        
        # create thread
        self.thread = qtc.QThread()
        # create worker
        self.worker = aw_Worker()        
        # move worker to thread
        self.worker.moveToThread(self.thread)          
        # connect signals and slots 
        self.worker_requested.connect(self.worker.worker_func) # connects aw signal to worker slot      
        self.worker.finished.connect(self.thread.quit) # quits threead when worker is done
        self.worker.finished.connect(self.success) # success popup when done
        self.worker.nono.connect(self.fail) # error popup when fail
        self.worker.nono.connect(self.thread.quit) # quit thread on fail
        self.worker.src_error.connect(self.src_fail) # error popup on shapefile error
        self.worker.src_error.connect(self.thread.quit) # quit thread on shapefile error
        self.worker.target_error.connect(self.src_fail) # error popup on shapefile error
        self.worker.target_error.connect(self.thread.quit) # quit thread on shapefile error
        self.worker.countChanged.connect(self.onCountChanged) # connect count change signal to progressbar   
        # start thread
        self.thread.start()        
        # send data to worker
        self.worker_requested.emit(src,target,intp,suffix,save)        
        # enable or disable button based on events
        self.ui.aw_run_prog.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.ui.aw_run_prog.setEnabled(True)
        )
        self.worker.nono.connect(
            lambda: self.ui.aw_run_prog.setEnabled(True)
        )
        self.worker.src_error.connect(
            lambda: self.ui.aw_run_prog.setEnabled(True)
        )        
        self.worker.target_error.connect(
            lambda: self.ui.aw_run_prog.setEnabled(True)
        )
    def onCountChanged(self,value):
        # this function updates progressbar
        self.ui.aw_progressBar.setValue(value)
    # following functions control info popups and closing windows      
    def fail(self):
        qtw.QMessageBox.critical(self, 'Error', 'Interpolation Failed')
    def src_fail(self):
        qtw.QMessageBox.critical(self, 'Error', 'Source Shapefile is invalid')
    def target_fail(self):
        qtw.QMessageBox.critical(self, 'Error', 'Target Shapefile is invalid')
    def success(self):
        qtw.QMessageBox.information(self, 'Success', 'Interpolation Complete')
    def close_aw(self):
        self.close() 
  
##########################################################################################################   
class bm_Worker(qtc.QObject):
    finished = qtc.pyqtSignal() # finished signal
    nono = qtc.pyqtSignal() # main function error
    src_error = qtc.pyqtSignal() # source shapefile error
    target_error = qtc.pyqtSignal() # target shapefile error
    countChanged = qtc.pyqtSignal(int) # update progbar signal
    
    @qtc.pyqtSlot(str,str,str,list,str,list,str) # decorator to allow arguments
    def worker_func(self, src, target, exclude, exclude_val, suffix, intp, save):
        count = 0
        try:
            print("analyzing source shapefile")
            src = gpd.read_file(src)
            count += 10
            self.countChanged.emit(count)
        except:
            self.src_error.emit()
            return
        try:
            print("analyzing ancillary shapefile")
            target = gpd.read_file(target)
            count += 10
            self.countChanged.emit(count)
        except:
            self.target_error.emit()
            return
        try:
            if any(char.isalpha() for string in exclude_val for char in string): 
                outp = binary_vector(src, target, exclude, exclude_val, suffix, intp)
                count += 75
                self.countChanged.emit(count)
                print("saving results")
                outp.to_file(save)
                count += 5
                self.countChanged.emit(count)
                self.finished.emit()  
            else:
                exclude_val = list(map(int,exclude_val)) #turns values in list to ints
                outp = binary_vector(src, target, exclude, exclude_val, suffix, intp)
                count += 75
                self.countChanged.emit(count)
                print("saving results")
                outp.to_file(save)
                count += 5
                self.countChanged.emit(count)
                self.finished.emit()
        except:
            self.nono.emit()
            return
        
class bm(qtw.QWidget):
        worker_requested = qtc.pyqtSignal(str,str,str,list,str,list,str) # emits signal to worker
        def __init__(self):
            super().__init__()
            self.ui = Ui_Binary_Method()
            self.ui.setupUi(self)
            self.ui.binary_source_browse.clicked.connect(self.source_browser)
            self.ui.binary_anc_browse.clicked.connect(self.target_browser)
            self.ui.binary_save_browse.clicked.connect(self.save_browser)
            self.ui.binary_run_prog.clicked.connect(self.run_bm)
            self.ui.binary_cancel_prog.clicked.connect(self.close_bm)
            title = "Binary Method"
            self.setWindowTitle(title)
        def source_browser(self):
            self.filename = QFileDialog.getOpenFileName()
            self.ui.binary_source_lineedit.setText(self.filename[0])  
        def target_browser(self):
            self.filename = QFileDialog.getOpenFileName()
            self.ui.binary_anc_lineedit.setText(self.filename[0])    
        def save_browser(self):
            self.filename = QFileDialog.getSaveFileName()
            self.ui.binary_save_lineedit.setText(self.filename[0])              
        def run_bm(self):
            src = self.ui.binary_source_lineedit.text()
            target = self.ui.binary_anc_lineedit.text()
            intp = self.ui.binary_intp_fields.text()
            intp = intp.split()
            suffix = self.ui.binary_output_suffix.text()
            save = self.ui.binary_save_lineedit.text()        
            exclude = self.ui.binary_exclude_field.text()
            exclude_val = self.ui.binary_exclude_vals.text()
            exclude_val = exclude_val.split()           
             # create thread
            self.thread = qtc.QThread()
            # create worker
            self.worker = bm_Worker()        
            # move worker to thread
            self.worker.moveToThread(self.thread)          
            # connect signals and slots 
            self.worker_requested.connect(self.worker.worker_func) # connects aw signal to worker slot      
            self.worker.finished.connect(self.thread.quit) # quits threead when worker is done
            self.worker.finished.connect(self.success) # success popup when done
            self.worker.nono.connect(self.fail) # error popup when fail
            self.worker.nono.connect(self.thread.quit) # quit thread on fail
            self.worker.src_error.connect(self.src_fail) # error popup on shapefile error
            self.worker.src_error.connect(self.thread.quit) # quit thread on shapefile error
            self.worker.target_error.connect(self.src_fail) # error popup on shapefile error
            self.worker.target_error.connect(self.thread.quit) # quit thread on shapefile error
            self.worker.countChanged.connect(self.onCountChanged) # connect count change signal to progressbar       
            # start thread
            self.thread.start()        
            # send data to worker
            self.worker_requested.emit(src,target,exclude,exclude_val,suffix,intp,save)        
            # enable or disable button based on events
            self.ui.binary_run_prog.setEnabled(False)
            self.thread.finished.connect(
                lambda: self.ui.binary_run_prog.setEnabled(True)
            )
            self.worker.nono.connect(
                lambda: self.ui.binary_run_prog.setEnabled(True)
            )
            self.worker.src_error.connect(
                lambda: self.ui.binary_run_prog.setEnabled(True)
            )        
            self.worker.target_error.connect(
                lambda: self.ui.binary_run_prog.setEnabled(True)
            )          
        def onCountChanged(self,value):
            # this function updates progressbar
            self.ui.binary_progressBar.setValue(value)
        # following functions control info popups and closing windows      
        def fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Interpolation Failed')
        def src_fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Source Shapefile is invalid')
        def target_fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Target Shapefile is invalid')
        def success(self):
            qtw.QMessageBox.information(self, 'Success', 'Interpolation Complete')
        def close_bm(self):
            self.close()

#####################################################################################################
class lv_Worker(qtc.QObject):
    finished = qtc.pyqtSignal() # finished signal
    nono = qtc.pyqtSignal() # main function error
    src_error = qtc.pyqtSignal() # source shapefile error
    target_error = qtc.pyqtSignal() # target shapefile error
    countChanged = qtc.pyqtSignal(int) # update progbar signal
    
    @qtc.pyqtSlot(str,str,str,str,list,str,str,str) # decorator to allow arguments
    def worker_func(self, src, target, cls, clsdict, intp, srcid, suffix, save):
        count = 0
        try:
            print("analyzing source shapefile")
            src = gpd.read_file(src)
            count += 10
            self.countChanged.emit(count)
        except:
            self.src_error.emit()
            return
        try:
            print("analyzing ancillary shapefile")
            target = gpd.read_file(target)
            count += 10
            self.countChanged.emit(count)
        except:
            self.target_error.emit()
            return
        try:
            print("converting inputs to dictionary")
            # read keypairs into dict splitting the strings on commas and colons
            new_dict = {}
            for keyval in clsdict.split(","):
                (key, val) = keyval.split(":",1)
                new_dict[key] = int(val)
            count += 10
            self.countChanged.emit(count)
            # convert keys to ints if there are no alphabet chars in keys
            if any(char.isalpha() for key in new_dict for char in key):
                count += 10
                self.countChanged.emit(count)
                pass
            else:
                new_dict = {int(key):val for key,val in new_dict.items()}
                count += 10
                self.countChanged.emit(count)
            outp = lim_var(src, target, cls, new_dict, intp, srcid, suffix)
            count += 55
            self.countChanged.emit(count)
            print("saving results")
            outp.to_file(save)
            count += 5
            self.countChanged.emit(count)
            self.finished.emit()
        except:
            self.nono.emit()
            return

class lv(qtw.QWidget):
        worker_requested = qtc.pyqtSignal(str,str,str,str,list,str,str,str)    
        def __init__(self):
            super().__init__()
            self.ui = Ui_Limiting_Variable_Method()
            self.ui.setupUi(self)
            self.ui.lv_source_browse.clicked.connect(self.source_browser)
            self.ui.lv_anc_browse.clicked.connect(self.target_browser)
            self.ui.lv_save_browse.clicked.connect(self.save_browser)
            self.ui.lv_run_prog.clicked.connect(self.run_lv)
            self.ui.lv_cancel_prog.clicked.connect(self.close_lv)
            title = "Limiting Variable Method"
            self.setWindowTitle(title)
        def source_browser(self):
            self.filename = QFileDialog.getOpenFileName()
            self.ui.lv_source_lineedit.setText(self.filename[0])  
        def target_browser(self):
            self.filename = QFileDialog.getOpenFileName()
            self.ui.lv_anc_lineedit.setText(self.filename[0])    
        def save_browser(self):
            self.filename = QFileDialog.getSaveFileName()
            self.ui.lv_save_lineedit.setText(self.filename[0])              
        def run_lv(self):
            src = self.ui.lv_source_lineedit.text()
            target = self.ui.lv_anc_lineedit.text()
            cls = self.ui.lv_class_lineedit.text()
            # get dictionary keypairs in string form
            clsdict = self.ui.lv_dict_lineedit.text()
            intp = self.ui.lv_intp.text()
            intp = intp.split()
            suffix = self.ui.lv_suffix_lineedit.text()
            save = self.ui.lv_save_lineedit.text()   
            srcid = self.ui.lv_sourceid_lineedit.text()
            # create thread
            self.thread = qtc.QThread()
            # create worker
            self.worker = lv_Worker()        
            # move worker to thread
            self.worker.moveToThread(self.thread)          
            # connect signals and slots 
            self.worker_requested.connect(self.worker.worker_func) # connects aw signal to worker slot      
            self.worker.finished.connect(self.thread.quit) # quits threead when worker is done
            self.worker.finished.connect(self.success) # success popup when done
            self.worker.nono.connect(self.fail) # error popup when fail
            self.worker.nono.connect(self.thread.quit) # quit thread on fail
            self.worker.src_error.connect(self.src_fail) # error popup on shapefile error
            self.worker.src_error.connect(self.thread.quit) # quit thread on shapefile error
            self.worker.target_error.connect(self.src_fail) # error popup on shapefile error
            self.worker.target_error.connect(self.thread.quit) # quit thread on shapefile error
            self.worker.countChanged.connect(self.onCountChanged) # connect count change signal to progressbar       
            # start thread
            self.thread.start()        
            # send data to worker
            self.worker_requested.emit(src,target,cls,clsdict,intp,srcid,suffix,save)        
            # enable or disable button based on events
            self.ui.lv_run_prog.setEnabled(False)
            self.thread.finished.connect(
                lambda: self.ui.lv_run_prog.setEnabled(True)
            )
            self.worker.nono.connect(
                lambda: self.ui.lv_run_prog.setEnabled(True)
            )
            self.worker.src_error.connect(
                lambda: self.ui.lv_run_prog.setEnabled(True)
            )        
            self.worker.target_error.connect(
                lambda: self.ui.lv_run_prog.setEnabled(True)
            )           
        def onCountChanged(self,value):
            # this function updates progressbar
            self.ui.lv_progressBar.setValue(value)
        # following functions control info popups and closing windows      
        def fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Interpolation Failed')
        def src_fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Source Shapefile is invalid')
        def target_fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Target Shapefile is invalid')
        def success(self):
            qtw.QMessageBox.information(self, 'Success', 'Interpolation Complete')
        def close_lv(self):
            self.close()
 
#############################################################################################            
class nc_Worker(qtc.QObject):
    finished = qtc.pyqtSignal() # finished signal
    nono = qtc.pyqtSignal() # main function error
    src_error = qtc.pyqtSignal() # source shapefile error
    target_error = qtc.pyqtSignal() # target shapefile error
    countChanged = qtc.pyqtSignal(int) # update progbar signal
    
    @qtc.pyqtSlot(str,str,str,str,list,str,str,str) # decorator to allow arguments
    def worker_func(self, src, target, cls, clsdict, intp, srcid, suffix, save):
        count = 0
        try:
            print("analyzing source shapefile")
            src = gpd.read_file(src)
            count += 10
            self.countChanged.emit(count)
        except:
            self.src_error.emit()
            return
        try:
            print("analyzing ancillary shapefile")
            target = gpd.read_file(target)
            count += 10
            self.countChanged.emit(count)
        except:
            self.target_error.emit()
            return
        try:
            print("converting inputs to dictionary")
            # read keypairs into dict splitting the strings on commas and colons
            new_dict = {}
            for keyval in clsdict.split(","):
                (key, val) = keyval.split(":",1)
                new_dict[key] = float(val)
            count += 10
            self.countChanged.emit(count)
            # convert keys to ints if there are no alphabet chars in keys    
            if any(char.isalpha() for key in new_dict for char in key): 
                count += 10
                self.countChanged.emit(count)
                pass
            else:
                new_dict = {int(key):val for key,val in new_dict.items()}
                count += 10
                self.countChanged.emit(count)
            outp = n_class(src, target, cls, new_dict, intp, srcid, suffix)
            count += 55
            self.countChanged.emit(count)
            print("saving results")
            outp.to_file(save)
            count += 5
            self.countChanged.emit(count)
            self.finished.emit()                    
        except:
            self.nono.emit()  
            return
            
class nc(qtw.QWidget):
        worker_requested = qtc.pyqtSignal(str,str,str,str,list,str,str,str) 
        def __init__(self):
            super().__init__()
            self.ui = Ui_N_Class_Method()
            self.ui.setupUi(self)
            self.ui.n_source_browse.clicked.connect(self.source_browser)
            self.ui.n_anc_browse.clicked.connect(self.target_browser)
            self.ui.n_save_browse.clicked.connect(self.save_browser)
            self.ui.n_run_prog.clicked.connect(self.run_nc)
            self.ui.n_cancel_prog.clicked.connect(self.close_nc)
            title = "N-Class Method"
            self.setWindowTitle(title)
        def source_browser(self):
            self.filename = QFileDialog.getOpenFileName()
            self.ui.n_source_lineedit.setText(self.filename[0])  
        def target_browser(self):
            self.filename = QFileDialog.getOpenFileName()
            self.ui.n_anc_lineedit.setText(self.filename[0])    
        def save_browser(self):
            self.filename = QFileDialog.getSaveFileName()
            self.ui.n_save_lineedit.setText(self.filename[0])              
        def run_nc(self):
            src = self.ui.n_source_lineedit.text()
            target = self.ui.n_anc_lineedit.text()
            cls = self.ui.n_field_lineedit.text()
            # get dictionary keypairs in string form
            clsdict = self.ui.n_dict_lineedit.text()
            srcid = self.ui.n_sourceid_lineedit.text()
            intp = self.ui.n_intp.text()
            intp = intp.split()
            suffix = self.ui.n_suffix_lineedit.text()
            save = self.ui.n_save_lineedit.text()        
            # create thread
            self.thread = qtc.QThread()
            # create worker
            self.worker = nc_Worker()        
            # move worker to thread
            self.worker.moveToThread(self.thread)          
            # connect signals and slots 
            self.worker_requested.connect(self.worker.worker_func) # connects aw signal to worker slot      
            self.worker.finished.connect(self.thread.quit) # quits threead when worker is done
            self.worker.finished.connect(self.success) # success popup when done
            self.worker.nono.connect(self.fail) # error popup when fail
            self.worker.nono.connect(self.thread.quit) # quit thread on fail
            self.worker.src_error.connect(self.src_fail) # error popup on shapefile error
            self.worker.src_error.connect(self.thread.quit) # quit thread on shapefile error
            self.worker.target_error.connect(self.src_fail) # error popup on shapefile error
            self.worker.target_error.connect(self.thread.quit) # quit thread on shapefile error
            self.worker.countChanged.connect(self.onCountChanged) # connect count change signal to progressbar       
            # start thread
            self.thread.start()        
            # send data to worker
            self.worker_requested.emit(src,target,cls,clsdict,intp,srcid,suffix,save)        
            # enable or disable button based on events
            self.ui.n_run_prog.setEnabled(False)
            self.thread.finished.connect(
                lambda: self.ui.n_run_prog.setEnabled(True)
            )
            self.worker.nono.connect(
                lambda: self.ui.n_run_prog.setEnabled(True)
            )
            self.worker.src_error.connect(
                lambda: self.ui.n_run_prog.setEnabled(True)
            )        
            self.worker.target_error.connect(
                lambda: self.ui.n_run_prog.setEnabled(True)
            )           
        def onCountChanged(self,value):
            # this function updates progressbar
            self.ui.n_progressBar.setValue(value)
        # following functions control info popups and closing windows      
        def fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Interpolation Failed')
        def src_fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Source Shapefile is invalid')
        def target_fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Target Shapefile is invalid')
        def success(self):
            qtw.QMessageBox.information(self, 'Success', 'Interpolation Complete')
        def close_nc(self):
            self.close()

##############################################################################################
class pm_Worker(qtc.QObject):
    finished = qtc.pyqtSignal() # finished signal
    nono = qtc.pyqtSignal() # main function error
    src_error = qtc.pyqtSignal() # source shapefile error
    target_error = qtc.pyqtSignal() # target shapefile error
    countChanged = qtc.pyqtSignal(int) # update progbar signal
    
    @qtc.pyqtSlot(str,str,str,str,str,str,list,str) # decorator to allow arguments
    def worker_func(self, src, target, tu, ru, ba, ra, intp, save):
        count = 0
        try:
            print("analyzing source shapefile")
            src = gpd.read_file(src)
            count += 10
            self.countChanged.emit(count)
        except:
            self.src_error.emit()
            return
        try:
            print("analyzing parcel shapefile")
            target = gpd.read_file(target)
            count += 10
            self.countChanged.emit(count)
        except:
            self.target_error.emit()
            return
        try:
            outp = parcel_method(src, target, tu, ru, ba, ra, intp)
            count += 75
            self.countChanged.emit(count)
            print("saving results")
            outp.to_file(save)
            count += 5
            self.countChanged.emit(count)
            self.finished.emit()
        except:
            self.nono.emit()
            return
        
class pm(qtw.QWidget):
        worker_requested = qtc.pyqtSignal(str,str,str,str,str,str,list,str)     
        def __init__(self):
            super().__init__()
            self.ui = Ui_Parcel_Method()
            self.ui.setupUi(self)
            self.ui.parcel_source_browse.clicked.connect(self.source_browser)
            self.ui.parcel_anc_browse.clicked.connect(self.target_browser)
            self.ui.parcel_save_browse.clicked.connect(self.save_browser)
            self.ui.parcel_run_prog.clicked.connect(self.run_pm)
            self.ui.parcel_cancel_prog.clicked.connect(self.close_pm)
            title = "Parcel Method"
            self.setWindowTitle(title)
        def source_browser(self):
            self.filename = QFileDialog.getOpenFileName()
            self.ui.parcel_source_lineedit.setText(self.filename[0])  
        def target_browser(self):
            self.filename = QFileDialog.getOpenFileName()
            self.ui.parcel_anc_lineedit.setText(self.filename[0])    
        def save_browser(self):
            self.filename = QFileDialog.getSaveFileName()
            self.ui.parcel_save_lineedit.setText(self.filename[0])              
        def run_pm(self):
            src = self.ui.parcel_source_lineedit.text()
            target = self.ui.parcel_anc_lineedit.text()
            tu = self.ui.parcel_tu.text()
            ru = self.ui.parcel_ru.text()
            ba = self.ui.parcel_ba.text()
            ra = self.ui.parcel_ra.text()            
            intp = self.ui.parcel_intp.text()
            intp = intp.split()
            save = self.ui.parcel_save_lineedit.text()        
            # create thread
            self.thread = qtc.QThread()
            # create worker
            self.worker = pm_Worker()        
            # move worker to thread
            self.worker.moveToThread(self.thread)          
            # connect signals and slots 
            self.worker_requested.connect(self.worker.worker_func) # connects aw signal to worker slot      
            self.worker.finished.connect(self.thread.quit) # quits threead when worker is done
            self.worker.finished.connect(self.success) # success popup when done
            self.worker.nono.connect(self.fail) # error popup when fail
            self.worker.nono.connect(self.thread.quit) # quit thread on fail
            self.worker.src_error.connect(self.src_fail) # error popup on shapefile error
            self.worker.src_error.connect(self.thread.quit) # quit thread on shapefile error
            self.worker.target_error.connect(self.src_fail) # error popup on shapefile error
            self.worker.target_error.connect(self.thread.quit) # quit thread on shapefile error
            self.worker.countChanged.connect(self.onCountChanged) # connect count change signal to progressbar       
            # start thread
            self.thread.start()        
            # send data to worker
            self.worker_requested.emit(src,target,tu,ru,ba,ra,intp,save)        
            # enable or disable button based on events
            self.ui.parcel_run_prog.setEnabled(False)
            self.thread.finished.connect(
                lambda: self.ui.parcel_run_prog.setEnabled(True)
            )
            self.worker.nono.connect(
                lambda: self.ui.parcel_run_prog.setEnabled(True)
            )
            self.worker.src_error.connect(
                lambda: self.ui.parcel_run_prog.setEnabled(True)
            )        
            self.worker.target_error.connect(
                lambda: self.ui.parcel_run_prog.setEnabled(True)
            )           
        def onCountChanged(self,value):
            # this function updates progressbar
            self.ui.parcel_progressBar.setValue(value)
        # following functions control info popups and closing windows      
        def fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Interpolation Failed')
        def src_fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Source Shapefile is invalid')
        def target_fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Target Shapefile is invalid')
        def success(self):
            qtw.QMessageBox.information(self, 'Success', 'Interpolation Complete')
        def close_pm(self):
            self.close()          

##############################################################################################
class em_Worker(qtc.QObject):
    finished = qtc.pyqtSignal() # finished signal
    nono = qtc.pyqtSignal() # main function error
    src_error = qtc.pyqtSignal() # source shapefile error
    target_error = qtc.pyqtSignal() # target shapefile error
    nest_error = qtc.pyqtSignal() # nested shapefile error
    countChanged = qtc.pyqtSignal(int) # update progbar signal
    
    @qtc.pyqtSlot(str, str, str, str, str, str, str, str, str) # decorator to allow arguments
    def worker_func(self, src, nest, parcel, tu, ru, ba, ra, intp, save):
        count = 0
        try:
            print("analyzing source shapefile")
            src = gpd.read_file(src)
            count += 10
            self.countChanged.emit(count)
        except:
            self.src_error.emit()
            return
        try:
            print("analyzing nested shapefile")
            nest = gpd.read_file(nest)
            count += 10
            self.countChanged.emit(count)
        except:
            self.target_error.emit()
            return
        try:
            print("analyzing parcel shapefile")
            parcel = gpd.read_file(parcel)
            count += 10
            self.countChanged.emit(count)
        except:
            self.target_error.emit()
            return   
        try:
            outp = expert_system(src, nest, parcel, tu, ru, ba, ra, intp)
            count += 65
            self.countChanged.emit(count)
            print("saving results")
            outp.to_file(save)
            count += 5
            self.countChanged.emit(count)
            self.finished.emit()                        
        except:
            self.nono.emit()
            return
            
class em(qtw.QWidget): 
        worker_requested = qtc.pyqtSignal(str, str, str, str, str, str, str, str, str) 
        def __init__(self):
            super().__init__()
            self.ui = Ui_Expert_Method()
            self.ui.setupUi(self)   
            self.ui.expert_source_browse.clicked.connect(self.source_browser)
            self.ui.expert_nest_browse.clicked.connect(self.target_browser)
            self.ui.expert_parcel_browse.clicked.connect(self.parcel_browser)
            self.ui.expert_save_browse.clicked.connect(self.save_browser)
            self.ui.expert_run_prog.clicked.connect(self.run_em)
            self.ui.expert_cancel_prog.clicked.connect(self.close_em)
            title = "Expert Method"
            self.setWindowTitle(title)
        def source_browser(self):
            self.filename = QFileDialog.getOpenFileName()
            self.ui.expert_source_lineedit.setText(self.filename[0])  
        def target_browser(self):
            self.filename = QFileDialog.getOpenFileName()
            self.ui.expert_nest_lineedit.setText(self.filename[0])
        def parcel_browser(self):
            self.filename = QFileDialog.getOpenFileName()
            self.ui.expert_parcel_lineedit.setText(self.filename[0])  
        def save_browser(self):
            self.filename = QFileDialog.getSaveFileName()
            self.ui.expert_save_lineedit.setText(self.filename[0])              
        def run_em(self):
            src = self.ui.expert_source_lineedit.text()
            nest = self.ui.expert_nest_lineedit.text()
            parcel = self.ui.expert_parcel_lineedit.text()
            tu = self.ui.expert_tu.text()
            ru = self.ui.expert_ru.text()
            ba = self.ui.expert_ba.text()
            ra = self.ui.expert_ra.text()            
            intp = self.ui.expert_intp.text()
            save = self.ui.expert_save_lineedit.text()        
            # create thread
            self.thread = qtc.QThread()
            # create worker
            self.worker = em_Worker()        
            # move worker to thread
            self.worker.moveToThread(self.thread)          
            # connect signals and slots 
            self.worker_requested.connect(self.worker.worker_func) # connects aw signal to worker slot      
            self.worker.finished.connect(self.thread.quit) # quits threead when worker is done
            self.worker.finished.connect(self.success) # success popup when done
            self.worker.nono.connect(self.fail) # error popup when fail
            self.worker.nono.connect(self.thread.quit) # quit thread on fail
            self.worker.src_error.connect(self.src_fail) # error popup on shapefile error
            self.worker.src_error.connect(self.thread.quit) # quit thread on shapefile error
            self.worker.target_error.connect(self.src_fail) # error popup on shapefile error
            self.worker.target_error.connect(self.thread.quit) # quit thread on shapefile error
            self.worker.nest_error.connect(self.nest_fail) # error popup for nest shapefile
            self.worker.nest_error.connect(self.thread.quit) # quit thread on nest error
            self.worker.countChanged.connect(self.onCountChanged) # connect count change signal to progressbar       
            # start thread
            self.thread.start()        
            # send data to worker
            self.worker_requested.emit(src, nest, parcel, tu, ru, ba, ra, intp, save)        
            # enable or disable button based on events
            self.ui.expert_run_prog.setEnabled(False)
            self.thread.finished.connect(
                lambda: self.ui.expert_run_prog.setEnabled(True)
            )
            self.worker.nono.connect(
                lambda: self.ui.expert_run_prog.setEnabled(True)
            )
            self.worker.src_error.connect(
                lambda: self.ui.expert_run_prog.setEnabled(True)
            )        
            self.worker.target_error.connect(
                lambda: self.ui.expert_run_prog.setEnabled(True)
            )           
        def onCountChanged(self,value):
            # this function updates progressbar
            self.ui.expert_progressBar.setValue(value)
        # following functions control info popups and closing windows      
        def fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Interpolation Failed')
        def src_fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Source Shapefile is invalid')
        def target_fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Target Shapefile is invalid')
        def nest_fail(self):
            qtw.QMessageBox.critical(self, 'Error', 'Nested Shapefile is invalid')
        def success(self):
            qtw.QMessageBox.information(self, 'Success', 'Interpolation Complete')            
        def close_em(self):
            self.close()

###################################################################################################
stylesheet = """
.QWidget {
    background-color: #f0f8fc;
    }
#Limiting_Variable_Method {
    background-color: #f0f8fc;
}
#Areal_Weight {
    background-color: #f0f8fc;
}
#Binary_Method {
    background-color: #f0f8fc;
}
#Expert_Method {
    background-color: #f0f8fc;
}
#N_Class_Method {
    background-color: #f0f8fc;
}
#Parcel_Method {
    background-color: #f0f8fc;
}                   
"""

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    app.setWindowIcon(QtGui.QIcon('assets/map.png'))
    widget = projectWidget()
    widget.show()
    sys.exit(app.exec_())        
