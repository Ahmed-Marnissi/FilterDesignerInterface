import sys
from PyQt5 import QtWidgets
import harold
import string

class FilterDesigner(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a label and a line edit for the filter order
        orderLabel = QtWidgets.QLabel("Filter Type:", self)
        self.orderEdit = QtWidgets.QLineEdit(self)

        # Create a label and a line edit for the cutoff frequency
        cutoffLabel = QtWidgets.QLabel("Cutoff Frequency:", self)
        self.cutoffEdit = QtWidgets.QLineEdit(self)
         # Create a label and a line edit for the Sampling Time
        SamplingTimeLabel = QtWidgets.QLabel("Sampling Time:", self)
        self.SamplingTimeEdit = QtWidgets.QLineEdit(self)

        # Create a design button
        designButton = QtWidgets.QPushButton("Design Filter", self)
        designButton.clicked.connect(self.designFilter)

        # Create a layout and add the widgets to it
        layout = QtWidgets.QGridLayout()
        layout.addWidget(orderLabel, 0, 0)
        layout.addWidget(self.orderEdit, 0, 1)
        layout.addWidget(cutoffLabel, 1, 0)
        layout.addWidget(self.cutoffEdit, 1, 1)
        layout.addWidget(SamplingTimeLabel, 2, 0)
        layout.addWidget(self.SamplingTimeEdit, 2, 1)
        layout.addWidget(designButton, 3, 1, 2, 3)

        # Set the layout for the main window
        self.setLayout(layout)
    

    

     
    def designFilter(self):
        # Get the filter order and cutoff frequency from the line edits
       

        # Design the filter using the provided parameters
        # TODO: Implement filter design algorithm here
        Type = (self.orderEdit.text())
        Tau = (float(self.cutoffEdit.text()))
        Te=float(self.SamplingTimeEdit.text())
        print(Type)
        if(Type=="LOWPASS"):
            G = harold.Transfer( [1], [Tau , 1])
        elif(Type=="HIGHPASS"):
            G = harold.Transfer( [Tau , 0], [Tau , 1])
        else :  
            QtWidgets.QMessageBox.information(self, "Error", "error in filter Type")     

        
        H_zoh= harold.discretize(G, dt=Te, method='zoh')
        Den=H_zoh.den
        Num=H_zoh.num 

        

        ch=""
        for i in range(len ( Den[0] )):
            if i== 0:
                
                ch=ch+ str(Den[0][i]) + "*Y[n]"

            elif i== len ( Den[0] )-1:
                print(Den[0][i],'*Y[n +',i,']  ',end="")
                ch=ch+ str(Den[0][i]) + "*Y[n +" +str(i)+ "]"
            else  :

                print(Den[0][i],'*Y[n +',i,'] + ',end="")
                ch=ch+ str(Den[0][i]) + "*Y[n +" +str(i)+ "] + "
         



        
        ch=ch + "="
        for j in range(len(Num[0])):

            if j==0 :
                ch=ch +str(Num[0][j]) + "*U[n]"

            elif j== len ( Num[0] )-1:
              print(Num[0][j],'*U[n +',j,']  ',end="")
              ch=ch +str(Num[0][j]) + "*U[n +" +str(j)+ "]"
            else  :
              print(Num[0][j],'*U[n +',j,'] + ',end="")
              ch=ch +str(Num[0][j]) + "*U[n +" +str(j)+ "]"
         

        
        # Display the filter equation in a message box
        print(ch)
        QtWidgets.QMessageBox.information(self, "Filter equation", "Recurrence relation: " + str(ch))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    designer = FilterDesigner()
    designer.show()
    sys.exit(app.exec_())


