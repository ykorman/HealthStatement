# -*- coding: utf-8 -*-

import pdfrw
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from bidi.algorithm import get_display

pdfmetrics.registerFont(TTFont('Hebrew', 'Alef-Regular.ttf'))

def create_overlay(form):
	"""
	Create the data that will be overlayed on top
	of the form that we want to fill
	"""
	c = canvas.Canvas('form_overlay.pdf')

	c.setFont("Hebrew", 12)
	c.setFillColor(HexColor('#0033cc'))
	# child_name
	c.drawCentredString(400, 612, get_display(form['child_name']))
	# child id
	c.drawCentredString(260, 612, form['child_id'])
	# birth date
	c.drawCentredString(100, 612, form['child_birthdate'])
	# school name
	c.drawCentredString(180, 589, get_display(form['school_name']))
	# school manager
	c.drawCentredString(180, 564, get_display(form['school_manager']))
	# parent name
	c.drawCentredString(410, 374, get_display(form['parent_name']))
	# parent phone
	c.drawCentredString(250, 374, form['parent_phone'])
	# parent id
	c.drawCentredString(100, 374, form['parent_id'])
	# date
	c.drawCentredString(340, 326, form['date'])
	# signature
	c.drawCentredString(180, 326, get_display(form['signature']))

	c.save()

def merge_pdfs(form_pdf, overlay_pdf, output):
	"""
	Merge the specified fillable form PDF with the 
	overlay PDF and save the output
	"""
	form = pdfrw.PdfReader(form_pdf)
	olay = pdfrw.PdfReader(overlay_pdf)
	
	for form_page, overlay_page in zip(form.pages, olay.pages):
		merge_obj = pdfrw.PageMerge()
		overlay = merge_obj.add(overlay_page)[0]
		pdfrw.PageMerge(form_page).add(overlay).render()
		
	writer = pdfrw.PdfWriter()
	writer.write(output, form)

def gen_filled_form(form, form_name):
	create_overlay(form)
	merge_pdfs('form.pdf', 'form_overlay.pdf', form_name)
	
if __name__ == '__main__':
	form = dict()
	form['child_name'] = u'משה כץ המלך'
	form['child_id'] = '123456789'
	form['child_birthdate'] = '01/11/19'
	form['school_name'] = u'גן פיטר פן, אלכסנדר 3, לוד'
	form['school_manager'] = u'לרה'
	form['parent_name'] = u'אהרון כץ הגדול'
	form['parent_phone'] = '054-1234567'
	form['parent_id'] = '123456789'
	form['date'] = '20/09/20'
	form['signature'] = form['parent_name']
	gen_filled_form(form, 'form_merged.pdf')