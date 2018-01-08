Przygotowanie nowej witryny
===========================

## Wymagane pakiety:
 * nginx
 * Python3
 * Git
 * pip
 * virtualenv

Na przykład w systemie ubuntu należy wydać polecenia:
    sudo yum install nginx git python36 python36-pip
    sudo pip3 install virtualenv

## Konfiguracja wirtualnych hostów w Nginx

 * Zobacz plik nginx.template.conf
 * SITENAME należy zastąpić odpowiednią nazwą, na przykład staging.my-domain.com

## Zadanie upstart

 * Zobacz plik gunicorn-upstart.template.conf
 * SITENAME należy zastąpić odpowiednią nazwą, na przykład staging.my-domain.com

## Struktura katalogów:
Przyjmujemy założenie o istnieniu konta uzytkownika w postaci /home/użytkownik.

/home/użytkownik
  sites
    SITENAME
      database
      source
      static
      virtualenv
