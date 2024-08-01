from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from .services import MonobankAPI
from .models import Invoice
from django.views.decorators.csrf import csrf_exempt  # Импортируем csrf_exempt
import json
import pdfkit  # Убедитесь, что у вас установлен pdfkit и wkhtmltopdf

from shop.views import *
def create_payment(request):
    cart_items = get_cart(request)
    amount = sum(item.product.price * item.quantity for item in cart_items)
    redirect_url = request.build_absolute_uri('/payment-success/')
    monobank_api = MonobankAPI()
    try:
        invoice_data = monobank_api.create_invoice(amount, redirect_url)
        if 'pageUrl' in invoice_data:
            invoice = Invoice(
                invoice_id=invoice_data['invoiceId'],
                amount=amount,
                currency=980,
                reference='your_reference_id',
                destination='Payment for services',
                status='pending'
            )
            invoice.save()
            payment_url = invoice_data['pageUrl']
            return redirect(payment_url)
        else:
            return JsonResponse(invoice_data, status=400)  # Вернуть ответ с ошибкой
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    return render(request, 'monobank/payment_form.html')

def payment_success(request):
    invoice_id = request.GET.get('invoice_id')
    if invoice_id:
        monobank_api = MonobankAPI()
        status = monobank_api.check_payment_status(invoice_id)
        if status['status'] == 'success':
            return render(request, 'monobank/payment_success.html')
        else:
            return render(request, 'monobank/payment_failed.html')
    return render(request, 'monobank/payment_failed.html')

def check_payment(request, invoice_id):
    monobank_api = MonobankAPI()
    try:
        status = monobank_api.check_payment_status(invoice_id)
        if status['status'] == 'success':
            invoice = Invoice.objects.get(invoice_id=invoice_id)
            invoice.status = 'paid'
            invoice.save()
        return JsonResponse(status)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt  # Используем декоратор csrf_exempt
def webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            invoice = Invoice.objects.get(invoice_id=data['invoiceId'])
            invoice.status = data['status']
            invoice.save()
            return JsonResponse({'status': 'received'})
        except Invoice.DoesNotExist:
            return JsonResponse({'error': 'Invoice not found'}, status=404)
    return JsonResponse({'error': 'Invalid method'}, status=405)

def generate_receipt(request, invoice_id):
    try:
        invoice = Invoice.objects.get(invoice_id=invoice_id)
        context = {
            'invoice': invoice
        }
        html = render_to_string('monobank/receipt.html', context)
        pdf = pdfkit.from_string(html, False)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="receipt_{invoice_id}.pdf"'
        return response
    except Invoice.DoesNotExist:
        return JsonResponse({'error': 'Invoice not found'}, status=404)
