# -*- coding: utf-8 -*-
import os
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.http import HttpResponse
from apps.siteblocks.models import Settings
from django.template.loader import get_template
from django.template import Context
from decimal import Decimal
import xhtml2pdf.pisa as pisa
import settings

def moneyfmt(value, places=2, curr='', sep=' ', dp='.',
             pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'

    """
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    result = ''.join(reversed(result))
    try:
        if result.split(dp)[1] == u'00':
            return result.split(dp)[0]
        else:
            return result
    except:
        return result


def url_spliter(url,cut_count):
    url = url.split('/')
    current = ''
    counter = 0
    if len(url)>1:
        for part in url[1:]:
            counter = counter + 1
            if cut_count==False:
                current = '%s/%s' % (current,part)
            else:
                if counter <= cut_count:
                    current = '%s/%s' % (current,part)
                else:
                    pass
    else:
        current = u'/'

    if not current.startswith('/'):
        current = '/%s' % current
    if not current.endswith('/'):
        current = '%s/' % current
    current = current.replace('//,', '/')

    return current

def random_key(length=6, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
    from random import choice

    return ''.join([choice(allowed_chars) for i in range(length)])


def send_order_email(subject, html_content, email_list, file):
    current_site = Site.objects.get_current()

    email_from = u'«3DX Moscow Open» <reply@%s>' % current_site.domain
    text_content = u''

    if email_list:
        msg = EmailMultiAlternatives(subject, text_content, email_from, email_list)
        msg.attach_alternative(html_content, "text/html")
        msg.attach_file(file, mimetype="application/pdf")
        msg.send()


def render_to_pdf(template_src, id_guest, context_dict):
    from cStringIO import StringIO

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO()

    file_name = 'guest_%s.pdf' % id_guest
    path_name = settings.MEDIA_ROOT + 'uploads/files/guests/' + file_name
    destination = open(path_name, 'wb+')

    pdf = pisa.pisaDocument(StringIO(html.encode("utf-8")), result, show_error_as_pdf=True, encoding='utf-8', )

    destination.write(result.getvalue())
    destination.close()
    return u'%s' % path_name


def send_emails(m, file):
    admin_email = Settings.objects.get(name='email_notification').value
    email_list = [u'%s' % admin_email, ]
    subject = u'Новый зарегистрированный гость'
    html_content = u'''
        <p style="font-size: 12px;">Здравствуйте.<br /><br />Новый зарегистрированный гость.</p>
        <p style="padding-left: 10px; font-style: italic; font-size: 12px;
        border-left: 2px solid #666;">
        <b>Номер п/п:</b> %s<br />
        <b>ФИО:</b> %s<br />
        <b>E-mail:</b> %s<br />
        <b>Телефон:</b> %s<br />
        <b>Уникальный ключ:</b> %s</p>
        <p><a href="http://3dxopen.ru/admin/members/guests/%s/">перейти к просмотру</a></p>''' %\
                   (m.id, m.name, m.email, m.phone, m.key, m.id)

    send_order_email(subject, html_content, email_list, file)

    email_list = [u'%s' % m.email, ]
    subject = u'Приглашение на 3DX Moscow Open'
    html_content = u'''
        <p style="font-size: 12px;">Здравствуйте.<br /><br />Пропуск успешно выписан(см. прикрепления).</p>
        <p style="padding-left: 10px; font-style: italic; font-size: 12px;
        border-left: 2px solid #666;">
        <b>Номер п/п:</b> %s<br />
        <b>ФИО:</b> %s<br />
        <b>E-mail:</b> %s<br />
        <b>Телефон:</b> %s<br /></p>''' %\
                   (m.id, m.name, m.email, m.phone)

    send_order_email(subject, html_content, email_list, file)


def crop_image(post, original_img, output_size):
    import settings

    try:
        from PIL import Image
    except ImportError:
        import Image
    x1 = int(post['x1'])
    y1 = int(post['y1'])
    x2 = int(post['x2'])
    y2 = int(post['y2'])
    box = (x1, y1, x2, y2)
    infile = settings.ROOT_PATH + original_img.image.url
    file, ext = os.path.splitext(infile)
    im = Image.open(infile)
    ms = im.crop(box)
    name = file + "_crop.jpg"
    ms.save(name, "JPEG")
    image = Image.open(name)
    m_width = float(output_size[0])
    m_height = float(output_size[1])
    w_k = image.size[0] / m_width
    h_k = image.size[1] / m_height
    if output_size < image.size:
        if w_k > h_k:
            new_size = (int(m_width), int(image.size[1] / w_k))
        else:
            new_size = (int(image.size[0] / h_k), int(m_height))
    else:
        new_size = image.size
    image = image.resize(new_size, Image.ANTIALIAS)
    image.save(name, "JPEG", quality=100)
    return True