# APIRestful




# Inicializando




## Comandos utilizados para publicação no Docker Hub

Logando no Docker Hub

&nbsp;&nbsp;&nbsp;&nbsp;```docker login```

### Dockerfile da api <br/>
Entrando na pasta api:  <br/>
&nbsp;&nbsp;&nbsp;&nbsp;```cd api```  <br/>
Construindo a imagem:  <br/>
&nbsp;&nbsp;&nbsp;&nbsp;```docker build -t yanorck/api-apirestful_myanimelist:v1.0 .```  <br/>
Publicando imagem no Docker Hub:  <br/>
&nbsp;&nbsp;&nbsp;&nbsp;```docker push yanorck/api-apirestful_myanimelist:v1.0```  <br/>

### Dockerfile do web <br/>
Entrando na pasta web: <br/>
&nbsp;&nbsp;&nbsp;&nbsp;```cd web``` <br/>
Construindo a imagem: <br/>
&nbsp;&nbsp;&nbsp;&nbsp;```docker build -t yanorck/web-apirestful_myanimelist:v1.0 .``` <br/>
    Publicando imagem no Docker Hub: <br/>
&nbsp;&nbsp;&nbsp;&nbsp;```docker push yanorck/web-apirestful_myanimelist:v1.0``` <br/>



