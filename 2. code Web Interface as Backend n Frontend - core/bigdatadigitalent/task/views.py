from django.shortcuts import render
import string
import random
import os
import shutil
import subprocess

import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

SPARK_BIN = 'spark-submit'
HADOOP_BIN = 'hadoop'
HADOOP_STREAMING_JAR = ''

#utils
random_name = lambda N : ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N))

# make random string
def randomString(stringLength):
    """Generate a random string with the combination of lowercase and uppercase letters """

    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def get_merge_local(file_out, dir_input):
	with open(file_out, 'wb') as outfile:
		for filename in os.listdir(dir_input):
        		if filename == file_out or filename[0] == ".":
            			continue
        		with open(dir_input+"/"+filename, 'rb') as readfile:
            			shutil.copyfileobj(readfile, outfile)

def run_process(l):
	print(' '.join(l))
	try:
		process = subprocess.Popen(l, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = [s.decode() for s in process.communicate()]
		print(stdout)
		print(stderr)
		return 0, stdout, stderr
	except subprocess.CalledProcessError as e:
		stdout, stderr = process.communicate()
		print("Program returned exitcode %d" % process.returncode)
		print(stderr)
		print(stdout)
		return process.returncode, stdout,  stderr

def parse_output(file):
	l = []
	cast = lambda x : (int(x[0]), list(map(float, x[1:])))
	for row in file:
		l.append(cast(row.replace("(", "").replace(")", "").split(",")))
	return l
# Create your views here.
def index(request):
	return render(request, 'index.html')

def function_week1(request):
	if request.method == 'POST':
		import pandas as pd
		import numpy as np
		dataset = request.FILES['inputDataset']#'E:/Pak Imam/Digitalent/dataset_dump.csv'
		persentase_data_training = 90
		banyak_fitur = int(request.POST['banyakFitur'])
		banyak_hidden_neuron = int(request.POST['banyakHiddenNeuron'])

		dataset = pd.read_csv(dataset, delimiter=';', names = ['Tanggal', 'Harga'], usecols=['Harga'])
		minimum = int(dataset.min()-10000)
		maksimum = int(dataset.max()+10000)
		new_banyak_fitur = banyak_fitur + 1
		hasil_fitur = []
		for i in range((len(dataset)-new_banyak_fitur)+1):
			kolom = []
			j = i
			while j < (i+new_banyak_fitur):
				kolom.append(dataset.values[j][0])
				j += 1
			hasil_fitur.append(kolom)
		hasil_fitur = np.array(hasil_fitur)
		data_normalisasi = (hasil_fitur - minimum)/(maksimum - minimum)

		data_training = data_normalisasi[:int(persentase_data_training*len(data_normalisasi)/100)]
		data_testing = data_normalisasi[int(persentase_data_training*len(data_normalisasi)/100):]

		#Training
		bobot = np.random.rand(banyak_hidden_neuron, banyak_fitur)
		bias = np.random.rand(banyak_hidden_neuron)
		h = 1/(1 + np.exp(-(np.dot(data_training[:, :banyak_fitur], np.transpose(bobot)) + bias)))
		h_plus = np.dot(np.linalg.inv(np.dot(np.transpose(h),h)),np.transpose(h))
		output_weight = np.dot(h_plus, data_training[:, banyak_fitur])

		#Testing
		h = 1/(1 + np.exp(-(np.dot(data_testing[:, :banyak_fitur], np.transpose(bobot)) + bias)))
		predict = np.dot(h, output_weight)
		predict = predict * (maksimum - minimum) + minimum

		#MAPE
		aktual = np.array(hasil_fitur[int(persentase_data_training*len(data_normalisasi)/100):, banyak_fitur])
		mape = np.sum(np.abs(((aktual - predict)/aktual)*100))/len(predict)
		return render(request, 'week1.html', {
		'y_aktual' : list(aktual),
		'y_prediksi' : list(predict),
		'mape' : mape
	})
	else:
		return render(request, 'week1.html')

def function_week2_task1(request):
	return render(request, 'week21.html')

def function_week2_task2(request):
	return render(request, 'week22.html')

def function_week3(request):
	# Import library request
	import requests
	apikey = '133559c63e055b23b0dd2dafc698fcfe' # --> imam, 
	# tlg masing" sign up mandiri ke https://openweathermap.org/appid
	weather_url = "http://api.openweathermap.org/data/2.5/weather" # get kondisi saat ini
	#weather_url = "http://api.openweathermap.org/data/2.5/forecast" # get untuk peramalannya
	city_name = "Malang"
	# print(weather_url)
	#r = requests.get(weather_url, params={'q': city_name, 'APPID': apikey})
	r = requests.get(weather_url, params={'q': city_name, 'APPID': apikey})
	r.url # `requests` help us encode the URL in the correct format
	r.status_code # 200 means success
	result = r.json()
	return render(request, 'week3.html', {
		'result': result,
		'celcius': result['main']['temp']-273.15
	})

def function_week4(request):
	return render(request, 'week4.html')

def function_week4_task1(request):
	if request.method == 'POST':
		cwd			= os.getcwd()
		dir_output 		= cwd+"/"+random_name(10)+"/"
		file_input		= dir_output+"input.in"
		
		#clean output
		run_process(["rm", "-r", dir_output])

		#write to file 
		run_process(["mkdir", dir_output])

		with open(file_input, "wb+", buffering=0) as file:
			file.write(memory_input)
			file.flush()
			os.fsync(file)
		del memory_input
		
		#run hadoop
		exitcode, stdout, stdin = run_process([HADOOP_BIN, 'jar', HADOOP_STREAMING_JAR,'-input', 'file://'+file_input, '-output', 'file://'+dir_output, '-mapper', 'piMapper.py', '-reducer', 'piReducer.py', '-file', 'hadoop/piMapper.py', 'hadoop/piReducer.py'])
		
		#merge file
		result_file = dir_output+"result.txt"
		get_merge_local(result_file, dir_output)

		#parse output
		result = sorted(open(mape_file, "r").read().split("\n"))
		mape = [x[2] for x in result]
		values = [x[1] for x in result]

		#delete output dir
		run_process(["rm", "-r", dir_output])
		return render(request, 'week41.html', {
		'value' : value,
		'mapes' : mape,
		'mape'	: mape[-1]
	})
	else:
		return render(request, 'week41.html')

def function_week4_task2(request):
	return render(request, 'week4.html')

def function_week5(request):
	return render(request, 'week5.html')
def function_week5_task1(request):
	if request.method == 'POST':
		cwd			= os.getcwd()
		memory_input 		= request.FILES['inputDataset'].read()
		jumlah_fitur 		= request.POST['banyakFitur']
		jumlah_hidden	 	= request.POST['banyakHiddenNeuron']
		dir_output 		= cwd+"/"+random_name(10)+"/"
		file_input		= dir_output+"input.in"
		activation_function	= request.POST['fungsiAktivasi']


		#clean output
		run_process(["rm", "-r", dir_output])

		#write to file 
		run_process(["mkdir", dir_output])
		with open(file_input, "wb", buffering=0) as file:
			file.write(memory_input)
			file.flush()
			os.fsync(file)
		del memory_input
		#upload file to hdfs (Not Supported)

		#run spark
		exitcode, stdout, stdin = run_process([SPARK_BIN, 'spark/pyspark_elm.py', jumlah_fitur, jumlah_hidden, "file://"+file_input, "file://"+dir_output, activation_function])
		
		#Return if error occured		
		if exitcode :
			return render(request, 'Error.html', {
				'exitcode'	: exitcode,
				'stdout'	: stdout,
				'stdin'		: stdin
			})

		#download file (Not Supported)

		#merge file
		output_file = dir_output+"result.txt"
		mape_file = dir_output+"mape.txt"
		get_merge_local(output_file, dir_output+"result")
		get_merge_local(mape_file, dir_output+"mape")

		#parse output
		output = sorted(parse_output(open(output_file)))
		aktual = [x[1][0] for x in output]
		prediction = [x[1][1] for x in output]
		del output
		mape = list(map(float,open(mape_file).read().replace("\n", " ").strip().split(" ")))
		
		#delete output dir
		run_process(["rm", "-r", dir_output])

		#render
		return render(request, 'week51.html', {
		'y_aktual' : aktual,
		'y_prediksi' : prediction,
		'mape' : mape[1],
		'mape_train' : mape[0]
		})
	else:
		return render(request, 'week51.html')

def function_week5_task2(request):
	if request.method == 'POST':
		cwd			= os.getcwd()
		memory_input 		= request.FILES['inputDataset'].read()
		jumlah_fitur 		= request.POST['banyakFitur']
		#jumlah_hidden	 	= request.POST['banyakHiddenNeuron']
		dir_output 		= cwd+"/"+random_name(10)+"/"
		file_input		= dir_output+"input.in"

		#clean output
		run_process(["rm", "-r", dir_output])

		#write to file 
		run_process(["mkdir", dir_output])
		with open(file_input, "wb", buffering=0) as file:
			file.write(memory_input)
			file.flush()
			os.fsync(file)
		del memory_input

		#upload file to hdfs (Not Supported)

		#run spark
		exitcode, stdout, stdin = run_process([SPARK_BIN, 'spark/pyspark_lr.py', jumlah_fitur, "file://"+file_input, "file://"+dir_output])
		
		#Return if error occured		
		if exitcode :
			return render(request, 'Error.html', {
				'exitcode'	: exitcode,
				'stdout'	: stdout,
				'stdin'		: stdin
			})

		#download file (Not Supported)

		#merge file
		output_file = dir_output+"result.txt"
		mape_file = dir_output+"mape.txt"
		get_merge_local(output_file, dir_output+"result")
		get_merge_local(mape_file, dir_output+"mape")

		#parse output
		output = sorted(parse_output(open(output_file)))
		aktual = [x[1][0] for x in output]
		prediction = [x[1][1] for x in output]
		del output
		mape = list(map(float,open(mape_file).read().replace("\n", " ").strip().split(" ")))
		
		#delete output dir
		run_process(["rm", "-r", dir_output])

		#render
		return render(request, 'week52.html', {
		'y_aktual' : aktual,
		'y_prediksi' : prediction,
		'mape' : mape[1],
		'mape_train' : mape[0]
		})
	else:
		return render(request, 'week52.html')

def function_week6(request):
	return render(request, 'week6.html')

def function_week7(request):
	return render(request, 'week7.html')

def function_week7_task_1(request):
	if request.method == 'POST':
		cetak = nb_run(request, False)

		#render
		return render(request, 'week71.html', {
		'prediction' : cetak
		})
	else:
		return render(request, 'week71.html')

def function_week7_task_2(request):
	if request.method == 'POST':
		cwd			= os.getcwd()
		memory_input 		= request.FILES['inputDataset'].read()
		jumlah_fitur 		= request.POST['banyakFitur']
		jumlah_hidden	 	= request.POST['banyakHiddenNeuron']
		dir_output 		= cwd+"/"+random_name(10)+"/"
		file_input		= dir_output+"input.in"
		activation_function	= request.POST['fungsiAktivasi']


		#clean output
		run_process(["rm", "-r", dir_output])

		#write to file 
		run_process(["mkdir", dir_output])
		with open(file_input, "wb", buffering=0) as file:
			file.write(memory_input)
			file.flush()
			os.fsync(file)
		del memory_input
		#upload file to hdfs (Not Supported)

		#run spark
		exitcode, stdout, stdin = run_process([SPARK_BIN, 'spark/pyspark_elm_2.py', jumlah_fitur, jumlah_hidden, "file://"+file_input, "file://"+dir_output, activation_function])
		
		#Return if error occured		
		if exitcode :
			return render(request, 'Error.html', {
				'exitcode'	: exitcode,
				'stdout'	: stdout,
				'stdin'		: stdin
			})

		#download file (Not Supported)

		#merge file
		output_file = dir_output+"result.txt"
		mape_file = dir_output+"mape.txt"
		get_merge_local(output_file, dir_output+"result")
		get_merge_local(mape_file, dir_output+"mape")

		#parse output
		output = sorted(parse_output(open(output_file)))
		aktual = [x[1][0] for x in output]
		prediction = [x[1][1] for x in output]
		del output
		mape = list(map(float,open(mape_file).read().replace("\n", " ").strip().split(" ")))
		
		#delete output dir
		run_process(["rm", "-r", dir_output])

		#render
		return render(request, 'week72.html', {
		'y_aktual' : aktual,
		'y_prediksi' : prediction,
		'mape' : mape[1],
		'mape_train' : mape[0]
		})
	else:
		return render(request, 'week72.html')

def company(request):
	return render(request, 'week8.html')

# other function

def nb_run(request, type_api=True):
	
	# make unique directory
	output_dir = randomString(10)
	
	if type_api:
		payload = json.loads(request.body)
		fitur_1 = payload['fitur_1']
		fitur_2 = payload['fitur_2']
		fitur_3 = payload['fitur_3']
	else:
		fitur_1 = request.POST['fitur_1']
		fitur_2 =  request.POST['fitur_2']
		fitur_3 =  request.POST['fitur_3']

	# merge input 
	dataInput = fitur_1 + "," + fitur_2 + "," + fitur_3

	#run hadoop
	exitcode, stdout, stdin = run_process([HADOOP_BIN, 'jar', 'hadoop/NBMapReduce/NBMapReduce.jar', 'NBCDriver', dataInput, '/user/ubuntu/nb-input/dataset.txt', '/user/ubuntu/nb-output/'+output_dir])

	#Return if error occured		
	if exitcode :
		cetak = exitcode
	else :
		cetak = run_process([HADOOP_BIN, 'fs', '-cat' , '/user/ubuntu/nb-output/'+output_dir+'/*'])

	#delete output dir
	run_process([HADOOP_BIN, "fs", "-rm", "-r", '/user/ubuntu/nb-output/'+output_dir])

	#return
	return cetak[1]

@csrf_exempt
def post_api(request):
    if request.method == 'POST' :
        hasil = nb_run(request)
        response = json.dumps({ 'prediksi': hasil })

    return HttpResponse(response, content_type='text/json')
