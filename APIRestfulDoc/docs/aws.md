## Deploy na AWS 

Para colocarmos nossa aplicação na aws foram feitos os seguintes passos

### 1 - Criando a primeira Role para EKS

Para criar uma nova Role selecionamos AWS Service e o serviço EKS (Elastic Kubernets Service) - Cluster. Após isso, selecionamos o AmazonEKSClusterPolicy para nossa Role e finalizamos.

### 2 - AWS CloudFormation

Criamos uma stack para as conexões do nosso projeto e deixamos os blocos de rede padrões.

### 3 - Criando EKS

Em Elastic Kubernetes Service ciramos um novo cluster e selecionamos a role que haviamos criado, após isso selecionamos o stack de conexões que havíamos criado também. 

### 4 - Instalando AWS CLI

Para iniciar nosso projeto no EKS precisamos nos comunicar com a AWS, para isso utilizei o AWS CLI windows.

### 5 - Adicionando nossos nodes

Definimos um Node group e para isso, criamos mais uma role para os worker nodes, com profiles para que possa interagir com outros serviços. Nessa role colocamos as policies AmazonEKS_CNI_Policy e AmazonEKSWorkerNodePolicy.

### 5 - Criando os arquivos deployment.yaml e service.yaml

Para finalizarmos e enviarmos o projeto para os pods, foi necessário criar os arquivos que servem como guia para a aws. Os arquivos encontram-se na pasta raíz do repositório.

### 6 - Configurando o AWS CLI e configurando pods 
- aws configure
- kubectl apply -f deployment.yaml
- kubectl apply -f service.yaml

### 7 - Visualizando se funcionou
- kubectl get pods
- kubectl get services

### 8 - Vídeo Funcionando

https://youtu.be/xMzDFUAlNfU




