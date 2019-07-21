from reportlab.lib import  colors
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import mm

class pdfWriter(object):
    """description of class"""

    doc = None
    elements = []
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

    def write_header(self, textTitle, styleStr='', alignment='', firstLineIndent=57):
    #        styles['title'] = ParagraphStyle(
    #    'title',
    #    parent=styles['default'],
    #    fontName='Helvetica-Bold',
    #    fontSize=24,
    #    leading=42,
    #    alignment=TA_CENTER,
    #    textColor=purple,
    #)
        if styleStr == '':
            styleStr = 'Heading1'

        styles = getSampleStyleSheet()        style = styles[styleStr]        if alignment == '':            style_right = ParagraphStyle(name='li', parent=style, firstLineIndent=firstLineIndent)        elif alignment == 'c':            style_right = ParagraphStyle(name='li', parent=style, alignment=TA_CENTER)        elif alignment == 'l':            style_right = ParagraphStyle(name='li', parent=style, alignment=TA_LEFT)        elif alignment == 'r':            style_right = ParagraphStyle(name='li', parent=style, alignment=TA_RIGHT)        elif alignment == 'j':            style_right = ParagraphStyle(name='li', parent=style, alignment=TA_JUSTIFY)

        ph = Paragraph(textTitle, style_right);
        self.elements.append(ph)

    def write_table(self, data, report=True):
        
        if report:
            t=Table(data)
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),colors.lightgrey),                                   ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),                                   ('BACKGROUND',(0,-2),(-1,-2),colors.green),                                   ('GRID', (0,0), (-1,-1), 0.25, colors.black)]))        else:
            t=Table(data, colWidths=(None, 86*mm, None, None))
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),colors.ghostwhite),                                   ('BACKGROUND',(0,0),(-1,0),colors.beige),                                   ('BACKGROUND',(0,-1),(-1,-1),colors.beige),                                   ('ALIGN', (3,1), (3,-1), 'DECIMAL'),                                   ('RIGHTPADDING', (3,1), (3,-1), 15)]))
        self.elements.append(t)

    def build(self):
        self.doc.build(self.elements)
