===========================================================
	CARA MENJALANKAN DJANGO FRAMEWORK untuk Big Data App :D
by:
1. Imam Cholissodin (imamcs@ub.ac.id)
2. Galih Ariwanda (galihariwanda01@gmail.com)
3. Django Developer
4. Apache Hadoop, Spark, etc
5. All of My Teams

Fakultas Ilmu Komputer (Filkom), Universitas Brawijaya (UB)
Untuk Kelas A, B, C dan D, Digital Talent Big Data Analytics AWS-Kominfo 2019 
Pada Tanggal 1 Juli 2019 sampai 31 Agustus 2019 di Gedung G Filkom UB
dan Untuk Kelas B Batch 2 sampai -+ Pertengahan November 2019
=======================================================================
1. Lakukan install Django dan lainnya melalui Command Prompt (CMD) dengan perintah:
> pip install Django 
> pip install sqlparse

2. Check Django dengan perintah:
> python
>>> import django
>>> django.get_version()
'2.1.1'
>>>

3. Membuat project django menggunakan Comman Prompt (CMD) dengan perintah:
> django-admin startproject <nama_project>

4. Masuk ke directory <nama_project>, directory hasil create project django sebagai berikut:
*misal nama project adalah bigdatadigitalent
bigdatadigitalent
 |___bigdatadigitalent
 |	|___ __init__.py
 |	|___ settings.py
 |	|___ urls.py
 |	|___ wsgi.py
 |___manage.py

5. Jalankan django dengan perintah:
> python manage.py runserver

6. Buka pada browser pada url berikut -> http://127.0.0.1:8000/

7. Tambahkan apps pada django dengan perintah:
> python manage.py startapp <nama_apps>

8. Directory akan berubah menjadi:
 |___bigdatadigitalent
 |	|___ __init__.py
 |	|___ settings.py
 |	|___ urls.py
 |	|___ wsgi.py
 |___task
 |	|___ migrations
 |	|	|___ __init__.py
 |	|___ __init__.py
 |	|___ admin.py
 |	|___ apps.py
 |	|___ models.py
 |	|___ tests.py
 |	|___ views.py
 |___db.sqlite3
 |___manage.py

9. Tambahkan pada settings.py code berikut:
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

dan

ganti bagian templates menjadi:
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
] 

10. Tambahkan folder static dan templates di dalam folder project, hasil directory:
 |___bigdatadigitalent
 |	|___ __init__.py
 |	|___ settings.py
 |	|___ urls.py
 |	|___ wsgi.py
 |___static (berisi file CSS, JS, dan ASSET)
 |___task
 |	|___ migrations
 |	|	|___ __init__.py
 |	|___ __init__.py
 |	|___ admin.py
 |	|___ apps.py
 |	|___ models.py
 |	|___ tests.py
 |	|___ views.py
 |___templates (berisi file *.html)
 |___db.sqlite3
 |___manage.py

NB:
- Link Dokumentasi -> https://docs.djangoproject.com/en/2.2/
- Menampilkan hasil return dari views.py pada html menggunakan perintah: {{ nama_key }}
- Menambahkan routes url pada bagian apps di urls.py
