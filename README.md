# Comparador de Preços
Projeto da matéria de C14 dedicado a criar uma aplicação web que compara preços de lojas online, mostrando ao usuário o produto mais baratos entre as lojas.

# TECNOLOGIAS E DEPENDÊNCIAS
- Backend: Python=3.13.7;
- Frontend: Streamlit;
- Versionamento: pip;
- Framework: Django;
- Tipo de aplicação: Web;

| Participante  | Matrícula / Curso | GitHub |
| ------------- | ----------------- | ------ |
| Beatriz Araújo Cardozo | 339 / GES | [beatriz-a-cardozo](https://github.com/beatriz-a-cardozo) |
| Felipe Ferreira de Carvalho Gabriel Pereira | 380 / GES | [Fefeeu](https://github.com/Fefeeu) | 
| João Paulo Fonseca Bernardo | 207 / GES | [JoaoPauloBernardo](https://github.com/JoaoPauloBernardo) |
| John Nunes Sugahara | 268 / GES | [JohnSugahara](https://github.com/JohnSugahara) |
| Marcelo Alckmin Pereira Lima | 119 / GES | [marceloalckmin](https://github.com/marceloalckmin) |
| Vinícius Carvalho Ensá | 266 / GES | [ViniciusCarvalhoEnsa](https://github.com/ViniciusCarvalhoEnsa) |

# INTRUÇÕES PARA RODAR O PROJETO
## Instalando as depedências
Para adicionar as dependências do projeto, rode o comando abaixo no terminal da raiz do projeto:
```python
pip install -r requirements.txt
```
Depois, adicione as migrações no mesmo terminal:
```python
python manage.py makemigrations
python manage.py migrate
```
## Rodar o backend
```python
python manage.py runserver
```
## Rodar o frontend
```python
cd frontend
python -m streamlit run Home.py
```