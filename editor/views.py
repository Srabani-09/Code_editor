from django.shortcuts import render
import subprocess, os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import docker
import uuid
import tempfile, sys
# Create your views here.
class RunCode(APIView):
    def post(self, request):
        code = request.data.get("code",'')
        user_input = request.data.get("input",'')
        language = request.data.get("language",'').lower()
        if not code or not language: 
            return Response({"error":"Unsupported language"}, status=400)
        filename_map = {
            "python":"main.py",
            "c":"main.c",
            "cpp":"main.cpp",
            "java":"Main.java" ,
            "javascript":"main.js",
            "php": "main.php"
        }
        compile_commands = {
            'c': 'gcc main,c -o main && ./main',
            'cpp': 'g++ main.cpp -o main && ./main',
            'java': 'javac Main.java && java Main',
            'python': 'python3 main.py',
            'php': 'php main.php',
            'javascript': 'node main.js'
        }
        docker_image = {
            'python': 'python:3.13-slim',
            'c': 'gcc:latest',
            'cpp':'gcc:latest',
            'java':'openjdk:latest',
            'php': 'php:cli',
            'javascript': 'node:alpine'
        }
        filename = filename_map[language]
        run_command = compile_commands[language]
        docker_image = docker_image[language]
        client = docker.from_env()
        temp_dir = f"/tmp/{uuid.uuid4()}"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, filename)
        with open(file_path, 'w') as f:
            f.write(code)
        try:
            with open(file_path, 'rb') as f:
                container = client.containers.run(image=docker_image, command=f"sh -c \"echo '{user_input}'|{run_command}\"",
                                                  volumes={temp_dir:{'bind':'/usr/src/app', 'mode':'rw'}},
                                                  working_dir='/usr/src/app',
                                                  stdin_open=True,
                                                  stdout=True,
                                                  stderr=True,
                                                  remove=True
                                                  )
                output = container.decode('utf-8')
                return Response({'output':output})
        except Exception as e:
            return Response({'error':str(e)}, status=500)
        finally:
            try:
                os.remove(file_path)
                os.rmdir(temp_dir)
            except:
                pass
        
        
        # filename, cmd = lang_config[language]
        # with tempfile.TemporaryDirectory() as tempdir:
        #     file_path = os.path.join(tempdir, filename)
        #     with open(file_path, "w") as f:
        #         f.write(code)
        #         try:
        #             if "&&" in cmd:
        #                 script = "&&".join(cmd)
        #                 result = subprocess.run(input=user_input.encode(), shell=True, cwd=tempdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        #             else:
        #                 result = subprocess.run(cmd, input=user_input.encode(), cwd=tempdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        #             return Response({"output":result.stdout.decode(), "error":result.stderr.decode()})
        #         except subprocess.TimeoutExpired:
        #             return Response({"error":"Execution timed out"})                

        # with tempfile.NamedTemporaryFile(mode='w+',suffix=".py",delete=False) as temp_code:
        #     temp_code.write(code)
        #     temp_code.flush()
        #     try:
        #         # result = subprocess.run(['python3', temp_code.name], input=stdin.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        #         result = subprocess.run([sys.executable, temp_code.name],input=stdin.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        #         output = result.stdout.decode()
        #         error = result.stderr.decode()
        #         return Response({"output": output, "error": error})
        #     except subprocess.TimeoutExpired:
        #         return Response({"error": "Code execution timed out"}, status=400)
            