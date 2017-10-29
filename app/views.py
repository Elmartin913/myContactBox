from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import *
from pprint import pprint
from django.views.decorators.csrf import csrf_exempt

# Create your views here
# .

@csrf_exempt
def new(request):
    if request.method == 'GET':
        html='''</html>
                  <body>
                    <form action="/new" method="POST">
                      <fieldset>
                        <legend>Dodaj nowy kontakt:</legend>
                        Podaj imię: <br><input type="text" name="name" value=""><br>
                        Podaj nazwisko: <br> <input type="text" name="surname" value=""><br>
                        Kilka słów opisu: <br><input type="text" name="description" value=""><br>
                        <button type="submit">Wyślij</button>
                      </fieldset>
                    </form>
                  </body>
                </html>'''

        return HttpResponse(html)
    else:
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        description = request.POST.get('description')
        new_p=Person.objects.create(name=name,
                                    surname=surname,
                                    description=description)
        return HttpResponseRedirect('/adress/')

@csrf_exempt
def modify(request, id):
    if request.method == 'GET':
        id = int(id)

        a_all = Adress.objects.filter(person__pk=id)
        t_all = Phone.objects.filter(person__pk=id)
        m_all = Email.objects.filter(person__pk=id)

        adr = ''
        for a in a_all:
            adr += '''<tr><td>{}</td><td>{}</td>
                      <tr><td>{}</td><td>{}</td>
                      <td><a href="/modify/{}"> Edytuj </a></td>
                      <td><a href="/delete/{}"> Usuń </a></td></tr>
                      '''.format(a.city, a.street,
                                 a.home_number, a.flat_number,
                                 a.id, a.id)

        tel=''
        for t in t_all:
            tel += '''<tr><td>{}</td><td>{}</td></tr>
                      <td><a href="/modify/{}"> Edytuj </a></td>
                      <td><a href="/delete/{}"> Usuń </a></td></tr>
                      '''.format(t.number, t.typ_phone, t.id, t.id)

        em=''
        for m in m_all:
            tel += '''<tr><td>{}</td><td>{}</td></tr>
                      <td><a href="/modify/{}"> Edytuj </a></td>
                      <td><a href="/delete/{}"> Usuń </a></td></tr>
                      '''.format(m.email, m.typ_email, m.id, m.id)


def delete(request,id):
    if request.method == 'GET':
        id = int(id)
        pd =  Person.objects.get(pk=id)
        #pprint(vars(pers_d))
        pd.delete()
        return HttpResponseRedirect('/adress/')


def adress(request):
    all_p = Person.objects.all().order_by('name')

    html ='''
        </html>
            <body>
                <h3> Skrzynka kontaktowa </h3>
                <table>
                        {}
                    <tr>
                        <td><a href="/new/"> Dodaj nowe </a></td>
                    </tr>
                </table>
            </body>
        </html>'''

    html2 = ''
    count = 0
    for p in all_p:
        count+=1
        html2 += '''
                <tr>
                    <td>{} | {}</td>
                    <td><a href="/show/{}"> {} </a></td>
                    <td><a href="/modify/{}"> Edytuj </a></td>
                    <td><a href="/delete/{}"> Usuń </a></td>
                 </tr>'''.format(str(count), p.id, p.id,p.name+' '+p.surname, p.id, p.id)

    return HttpResponse(html.format(html2))


def show(request, id):
    if request.method == 'GET':
        id = int(id)
        try:
            p =  Person.objects.get(pk=id)
        except:
            return HttpResponse('Nie ma osoby o podanym id')

        try:
            a_all = Adress.objects.filter(person__pk=id)
            t_all = Phone.objects.filter(person__pk=id)
            m_all = Email.objects.filter(person__pk=id)
        except:
            return HttpResponse('W adresie nie ma osoby o podanym id')

        adr = ''
        for a in a_all:
            adr += '''<tr><td>{}</td><td>ul.{} {}/{}</td></tr>
                      '''.format(a.city, a.street, a.home_number, a.flat_number)

        tel=''
        for t in t_all:
            tel += '''<tr><td>tel.{}: </td><td>{}</td></tr>
                      '''.format(t.typ_phone, t.number)

        em=''
        for m in m_all:
            tel += '''<tr><td>email {}: </td><td>{}</td></tr>
                      '''.format(m.typ_email, m.email)

        html='''
                <html>
                  <body>
                    <table>
                      <th>Dane osobowe:</th>
                      <tr><td>Imię: </td><td>{}</td></tr>
                      <tr><td>Nazwisko: </td><td>{}</td></tr>
                      <tr><td>Opis: </td><td>{}</td></tr>
                    </table>
                    <table>
                      <th>Dane adresowe:</th>
                            {}
                    </table>
                    <table>
                      <th>Dane kontaktowe:</th>
                            {}  
                            {}
                    </table>
                    <a href="/modify/{}">Edytuj</a>
                  </body>
                </html>
                '''.format(p.name, p.surname, p.description, adr, tel, em, id)

        return HttpResponse(html)

@csrf_exempt
def modify_adr(request, id):
    if request.method == 'GET':
        id = int(id)
        try:
            p = Person.objects.get(pk=id)
        except:
            return HttpResponse('Nie ma osoby o podanym id')

        try:
            a_all = Adress.objects.filter(person__pk=id)
            t_all = Phone.objects.filter(person__pk=id)
            m_all = Email.objects.filter(person__pk=id)
        except:
            return HttpResponse('W adresie nie ma osoby o podanym id')

        adr = ''
        for a in a_all:
            adr += '''<tr><td>{}</td><td>ul.{} {}/{}</td>
                      <td><a href="/{}/delete_address/{}"> Usuń </a></td></tr>
                      '''.format(a.city, a.street, a.home_number,
                                 a.flat_number, a.id, id, a.id)
        adr += ''' <tr><td><a href="/{}/addAddress"> Dodaj adres </a>
                    </td></tr>'''.format(str(id))

        tel=''
        for t in t_all:
            tel += '''<tr><td>tel.{}: </td><td>{}</td>
                      <td><a href="/{}/delete_phone/{}"> Usuń </a></td></tr>
                      '''.format(t.typ_phone, t.number, t.id, id, t.id)
        tel += '''<tr><td><a href="/{}/addPhone"> Dodaj telefon </a></td></tr>
                '''.format(str(id))

        em=''
        for m in m_all:
            tel += '''<tr><td>email {}: </td><td>{}</td>
                      <td><a href="/{}/delete_email/{}"> Usuń </a></td></tr>
                      '''.format(m.typ_email, m.email, m.id, id, m.id)
        em += '''<tr><td><a href="/{}/addEmail"> Dodaj email </a></td></tr>
                '''.format(str(id))

        html='''
                <html>
                  <body>
                    <table>
                      <th>Dane osobowe:</th>
                      <tr><td>Imię: </td><td>{}</td></tr>
                      <tr><td>Nazwisko: </td><td>{}</td></tr>
                      <tr><td>Opis: </td><td>{}</td></tr>
                      <tr><td><a href="/modify_person/{}"> Modyfikuj </a></td></tr>
                    </table>
                    <table>
                      <th>Dane adresowe:</th>
                            {}
                    </table>
                    <table>
                    <th>Dane teleadresowe:</th>
                            {}  
                            {}
                    </table>
                    <p></p>
                    <a href="/adress/"> << Skrzynka kontaktowa </a>
                  </body>
                </html>
                '''.format(p.name, p.surname, p.description, id, adr, tel, em)

        return HttpResponse(html)

@csrf_exempt
def add_address(request,id):
    if request.method == 'GET':
        html='''</html>
                  <body>
                    <form action="#" method="POST">
                      <fieldset>
                        <legend>Dodaj nowy adress:</legend>
                        Miasto: <br><input type="text" name="city" value=""><br>
                        Ulica: <br> <input type="text" name="street" value=""><br>
                        Nr domu: <br><input type="text" name="home_number" value=""><br>
                        Nr mieszkania: <br><input type="text" name="flat_number" value="0"><br>
                        <button type="submit">Wyślij</button>
                      </fieldset>
                    </form>
                  </body>
                </html>'''
        return HttpResponse(html)
    else:

        pd = Person.objects.get(pk=int(id))

        city = request.POST.get('city')
        street = request.POST.get('street')
        home_number = request.POST.get('home_number')
        flat_number = request.POST.get('flat_number')
        a1 = Adress.objects.create(city=city, street=street,home_number=home_number,
                                       flat_number=flat_number, person=pd)
        return HttpResponseRedirect('/modify/{}'.format(str(id)))


@csrf_exempt
def add_phone(request,id):
    if request.method == 'GET':
        html='''</html>
                  <body>
                    <form action="#" method="POST">
                      <fieldset>
                        <legend>Dodaj nowy telefon:</legend>
                        Numer: <br><input type="text" name="number" value=""><br>
                        Typ: <br> <input type="text" name="typ_phone" value="1"><br>
                        <button type="submit">Wyślij</button>
                      </fieldset>
                    </form>
                  </body>
                </html>'''
        return HttpResponse(html)
    else:
        pd = Person.objects.get(pk=int(id))
        number = request.POST.get('number')
        typ_phone = request.POST.get('typ_phone')
        t1 = Phone.objects.create(number=number, typ_phone=int(typ_phone), person=pd)
        return HttpResponseRedirect('/modify/{}'.format(str(id)))


@csrf_exempt
def add_email(request,id):
    if request.method == 'GET':
        html='''</html>
                  <body>
                    <form action="#" method="POST">
                      <fieldset>
                        <legend>Dodaj nowy email:</legend>
                        email: <br><input type="text" name="email" value=""><br>
                        typ: <br> <input type="text" name="typ_email" value=""><br>
                        <button type="submit">Wyślij</button>
                      </fieldset>
                    </form>
                  </body>
                </html>'''
        return HttpResponse(html)
    else:
        pd = Person.objects.get(pk=int(id))
        email = request.POST.get('email')
        typ_email = request.POST.get('typ_email')
        m1 = Adress.objects.create(email=email, typ_email=int(typ_email), person=pd)
        return HttpResponseRedirect('/modify/{}'.format(str(id)))


def delete_address(request,id, idp):
    if request.method == 'GET':
        idp = int(idp)
        a = Adress.objects.filter(pk=idp)
        a.delete()
        return HttpResponseRedirect('/modify/{}'.format(id))


def delete_phone(request,id, idp):
    if request.method == 'GET':
        idp = int(idp)
        t = Phone.objects.filter(pk=idp)
        t.delete()
        return HttpResponseRedirect('/modify/{}'.format(id))


def delete_email(request,id, idp):
    if request.method == 'GET':
        idp = int(idp)
        m = Email.objects.filter(pk=idp)
        m.delete()
        return HttpResponseRedirect('/modify/{}'.format(id))


@csrf_exempt
def modify_person(request, id):
    id = int(id)
    if request.method == 'GET':
        p = Person.objects.get(pk=id)
        html = '''
                </html>
                  <body>
                    <form action="#" method="POST">
                      <fieldset>
                        <legend>Modyfikuj dane:</legend>
                        Imie: <br><input type="text" name="new_name" value="{}"><br>
                        Nazwisko: <br> <input type="text" name="new_surname" value="{}"><br>
                        Opis: <br><input type="text" name="new_des" value="{}"><br>
                        <button type="submit">Wyślij</button>
                      </fieldset>
                    </form>
                  </body>
                </html>'''.format(p.name, p.surname, p.description)
        return HttpResponse(html)
    else:
        p1 = Person.objects.get(pk=id)
        new_name = request.POST.get('new_name')
        new_surname = request.POST.get('new_surname')
        new_des = request.POST.get('new_des')
        if new_name is not None:
            p1.name = new_name
            p1.save()

        if new_surname is not None:
            p1.surname = new_surname
            p1.save()

        if new_des is not None:
            p1.description = new_des
            p1.save()

        return HttpResponseRedirect('/modify/{}'.format(str(id)))