# 📊 Dashboard Preditivo COVID-19  

Dashboard interativo para análise de sintomas e comorbidades relacionadas à COVID-19 no Brasil. Utiliza **inteligência artificial** para prever a probabilidade de infecção e identificar padrões regionais e demográficos com base em dados nacionais de síndromes gripais.  

---

## 🚀 Pré-requisitos  

Antes de executar o projeto, certifique-se de ter instalado:  

- **Python 3.8+**  
- **pip** (gerenciador de pacotes do Python)  

---

## 📥 Instalação  

1. **Clone o repositório**:  
   ```sh
   git clone https://github.com/Kaioguilherme1/Dashboard-covid19.git
   cd covid-dashboard-ai
   ```  

2. **Instale as dependências**:  
   ```sh
   pip install dash pandas plotly scikit-learn 
   ```  

---

## 📦 Bibliotecas Utilizadas  

As principais bibliotecas utilizadas no projeto são:  

- **Dash** → Framework para construção de dashboards interativos  
- **Pandas** → Manipulação e análise de dados  
- **Plotly** → Visualização gráfica avançada  
- **Scikit-learn** → Modelos de machine learning  

---

## 📊 Conjuntos de Dados  

# processamento Pesado e expanção dos datasets

O conjunto de dados relacionado à COVID-19 no Brasil passou por um processo abrangente de limpeza, unificação e transformação. Durante esse processo, a coluna 'diagnosticoCOVID' foi criada para categorizar os casos como confirmados (1) e não confirmados (0), enquanto a coluna 'evolucaoCaso' foi mapeada com valores numéricos para representar os desfechos clínicos, como cura, internação e óbito. Além disso, a variável 'profissionalSeguranca' foi codificada em formato binário, facilitando a análise dessa categoria profissional.

Na criação de novas variáveis, foi aplicada uma técnica de transformação das listas de sintomas e condições em variáveis binárias, utilizando filtros específicos definidos para cada coluna. Esses filtros foram configurados por meio de percentuais personalizados para garantir que apenas os sintomas e condições mais relevantes, de acordo com sua frequência de ocorrência no dataset, fossem selecionados. A configuração dos percentuais personalizados foi estabelecida da seguinte forma:

Esses filtros permitiram selecionar os valores mais representativos, otimizando a criação de colunas e garantindo que o modelo de IA tivesse um conjunto de features mais informativo e eficiente. A abordagem visa melhorar a capacidade do modelo de identificar padrões e correlacionar sintomas e desfechos clínicos, maximizando a performance preditiva.

Devido ao tamanho do dataset e à quantidade de sintomas e condições a serem processados, o procedimento foi realizado fora do Google Colab. O código utilizado encontra-se disponível no repositório [GitHub: Expandir_dataset.py](https://github.com/Kaioguilherme1/Dashboard-covid19/blob/main/Expandir_dataset.py), juntamente com os novos datasets já processados.

---

## ▶️ Executando a Aplicação  

Para iniciar o servidor e acessar o dashboard, execute:  
```sh
python3 dashboard/dashboard.py
```  

Após iniciar, acesse o dashboard no navegador:  
🔗 **http://127.0.0.1:8050/**  

---

## 📂 Estrutura do Projeto  

```
📦 Dashboard-covid19
│── 📁 dashboard/        # Código principal do dashboard
│── 📁 IA_Models/        # Modelos de IA para previsão
│── 📁 datasets/         # Conjuntos de dados (baixar e adicionar aqui)
│── README.md           # Documentação do projeto
```

---

## 🎯 Como Usar  

- **Dashboard** → Explore dados sobre COVID-19 no Brasil.  
- **IA Preditiva** → Insira sintomas do paciente e obtenha previsões sobre a infecção.  

---


