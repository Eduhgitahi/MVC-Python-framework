from __future__ import absolute_import ,unicode_literals
from freelance.models import Document,Writer,client_cost,circle
import django_tables2 as tables
from django.utils.html import format_html
from django_tables2.utils import A
from django.urls import reverse
#class CheckBoxColumnWithName(tables.CheckBoxColumn):
 #   @property
  #  def header(self):
   #     return self.verbose_name

class DocumentTable(tables.Table):
	edit = tables.LinkColumn('accept',args=[A('pk')],verbose_name="Action",orderable=False,empty_values=())
	#editable =  CheckBoxColumnWithName(verbose_name="Select", accessor="pk")

	def render_edit(self,record):
		if Document.objects.values_list('status',flat=True).get(order_number=record.pk)==False:
			return format_html('<a href='+reverse("accept", args=[record.pk])+'><button type="button" class="btn-danger">Accept</button></a>')

	class Meta:
		model = Document
		fields = ('Title','due_date','writer_email','attachment','cost','Message','created_at','urlhash','status')


class WriterTable(tables.Table):
	editw = tables.LinkColumn('approve',args=[A('pk')],verbose_name="Action",orderable=False,empty_values=())
	def render_editw(self,record):
		if Writer.objects.values_list('status',flat=True).get(order_number=record.pk)==False:
			return format_html('<a href='+reverse("approve", args=[record.pk])+'><button type="button" class="btn-danger">Approve</button></a>')

	class Meta:
		model = Writer
		fields = ('Title','client_email','user_id','urlhash','Number_of_pages','attachment','description','status')

class DocumentTable1(tables.Table):
	class Meta:
		model = Document
		fields = ('Title','due_date','writer_email','attachment','cost','Message','created_at','urlhash','status')

class WriterTable1(tables.Table):
	class Meta:
		model = Writer
		fields = ('Title','client_email','user_id','urlhash','Number_of_pages','attachment','description','status')

class CostTable(tables.Table):
	class Meta:
		model = client_cost
		fields = ('Username','writer_email','total','paid','Balance','created_at')
class CostTable1(tables.Table):
	class Meta:
		model = client_cost
		fields = ('Username','client_id','total','paid','Balance','created_at')

class CircleTable(tables.Table):
	stat = tables.LinkColumn('approve',args=[A('pk')],verbose_name="Accepted Status ",orderable=False,empty_values=())
	wstatus = tables.LinkColumn('c_accept',args=[A('pk')],verbose_name="Action ",orderable=False,empty_values=())

	def render_stat(self,record):
		if circle.objects.values_list('status',flat=True).get(id=record.pk)==False:
			return format_html('<i class="fa fa-user-times"></i>')
		else:
			return format_html('<i class="fa fa-user"></i>')
	def render_wstatus(self,record):
		if circle.objects.values_list('cstatus',flat=True).get(id=record.pk)==False:
			return format_html('<a href='+reverse("c_accept", args=[record.pk])+'><button type="button" class="btn-success">Accept request</button></a>')
		if circle.objects.values_list('status',flat=True).get(id=record.pk)==True:
			return format_html('<p>This writer is in your circle.</p>')
		else:
			return format_html('<p>Waiting for writer to join.</p>')
	class Meta:
		model = circle
		fields = ('Username','created_at')

class CircleTable1(tables.Table):
	stat = tables.LinkColumn('approve',args=[A('pk')],verbose_name="Accepted Status ",orderable=False,empty_values=())
	cstatus = tables.LinkColumn('w_accept',args=[A('pk')],verbose_name="Action ",orderable=False,empty_values=())

	def render_stat(self,record):
		if circle.objects.values_list('status',flat=True).get(id=record.pk)==False:
			return format_html('<i class="fa fa-user-times"></i>')
		else:
			return format_html('<i class="fa fa-user"></i>')

	def render_cstatus(self,record):
		if circle.objects.values_list('wstatus',flat=True).get(id=record.pk)==False:
			return format_html('<a href='+reverse("w_accept", args=[record.pk])+'><button type="button" class="btn-success">Accept request</button></a>')
		if circle.objects.values_list('status',flat=True).get(id=record.pk)==True:
			return format_html('<p>This client is in your circle.</p>')
		else:
			return format_html('<p>Waiting for client to accept.</p>')


	class Meta:
		model = circle
		fields = ('client_id','created_at')