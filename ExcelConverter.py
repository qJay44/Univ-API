from PDFNetPython3 import *
from os.path import splitext


class Converter:

    def __init__(self, fileName) -> None:
        self.filePath = './UnivAPI/files/' + fileName
        self.filePathNew = splitext(self.filePath)[0] + '.pdf'
        self.main()

    def SimpleConvert(self, input_path, output_path):
        pdfdoc = PDFDoc()

        Convert.OfficeToPDF(pdfdoc, input_path, None)

        pdfdoc.Save(output_path, SDFDoc.e_linearized)

        print('Saved ' + output_path )


    def main(self):
        PDFNet.Initialize('demo:1665566627466:7ac5db1e03000000001e589e726c417970bf2c57366e560bb19edbf2e2')

        self.SimpleConvert(self.filePath, self.filePathNew)

        PDFNet.Terminate()

        print('Done.')

