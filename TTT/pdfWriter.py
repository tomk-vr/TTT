from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class pdfWriter(object):
    """description of class"""

    doc = None
    def __init__(self, fpath, **kwargs):
        super().__init__()
        if not 'rightMargin' in kwargs:
            kwargs['rightMargin'] = 30
        if not 'leftMargin' in kwargs:
            kwargs['leftMargin'] = 30    
        if not 'topMargin' in kwargs:
            kwargs['topMargin'] = 30
        if not 'bottomMargin' in kwargs:
            kwargs['bottomMargin'] = 18
        self.doc = SimpleDocTemplate(fpath, **kwargs)
        self.doc.pagesize = portrait(A4)

    def write_table(self, data):
        t=Table(data)
        #t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),colors.gray),
        #                       ('TEXTCOLOR',(0,0),(1,-1),colors.red)]))        t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),colors.lightgrey),                               ('BACKGROUND',(0,0),(-1,0),colors.lightgrey)]))        elements = []
        elements.append(t)
        self.doc.build(elements)
