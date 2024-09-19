import streamlit as st
import pandas as pd
import random
import os

# Nome do arquivo CSV para armazenar os dados
DATA_FILE = "tbr_list.csv"

# Função para carregar os dados da planilha
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["Title", "Genre", "Pages", "Hype"])
    return df

# Função para salvar os dados no CSV
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Função para adicionar um novo livro
def add_book(title, genre, pages, hype):
    df = load_data()
    new_row = pd.DataFrame({
        "Title": [title],
        "Genre": [genre],
        "Pages": [pages],
        "Hype": [hype]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)

# Função para sortear um livro aleatoriamente
def pick_random_book():
    df = load_data()
    if not df.empty:
        book = df.sample().iloc[0]
        return book
    else:
        return None

# Função para recomendar um livro baseado em preferências
def recommend_book(preferred_genre, min_hype):
    df = load_data()
    if not df.empty:
        filtered = df[(df["Genre"] == preferred_genre) & (df["Hype"] >= min_hype)]
        if not filtered.empty:
            book = filtered.sample().iloc[0]
            return book
    return None

# Configurações iniciais do Streamlit
st.set_page_config(page_title="TBR Manager", layout="centered")

st.title("📚 TBR Manager")
st.markdown("Gerencie sua lista de livros para ler, sorteie aleatoriamente ou receba recomendações personalizadas.")

# Seção para adicionar um novo livro
st.header("Adicionar um Livro à Sua Lista TBR")
with st.form(key="add_book_form"):
    title = st.text_input("Título do Livro")
    genre = st.selectbox("Gênero", ["Ficção", "Fantasia", "Suspense", "Romance", "Não-ficção", "Biografia", "Sci-Fi", "Outros"])
    pages = st.number_input("Número de Páginas", min_value=1, step=1)
    hype = st.slider("Nível de Hype (1 a 5)", min_value=1, max_value=5, value=3)
    submit_button = st.form_submit_button(label="Adicionar à Lista")

if submit_button:
    if title.strip() == "":
        st.error("Por favor, insira o título do livro.")
    else:
        add_book(title, genre, pages, hype)
        st.success(f"📖 **{title}** adicionado com sucesso à sua lista TBR!")

st.markdown("---")

# Seção para sortear um livro
st.header("Sortear um Livro Aleatoriamente")
if st.button("🔀 Sortear Livro"):
    book = pick_random_book()
    if book is not None:
        st.success(f"📖 **{book['Title']}** por *{book['Genre']}* foi sorteado!")
        st.write(f"**Gênero:** {book['Genre']}")
        st.write(f"**Número de Páginas:** {book['Pages']}")
        st.write(f"**Hype:** {book['Hype']} ⭐️")
    else:
        st.warning("Sua lista TBR está vazia. Adicione alguns livros para sortear.")

st.markdown("---")

# Seção para recomendar um livro
st.header("Recomendar um Livro Baseado nas Suas Preferências")
with st.form(key="recommend_form"):
    preferred_genre = st.selectbox("Selecione o Gênero Desejado", ["Ficção", "Fantasia", "Suspense", "Romance", "Não-ficção", "Biografia", "Sci-Fi", "Outros"])
    min_hype = st.slider("Selecione o Nível Mínimo de Hype", min_value=1, max_value=5, value=3)
    recommend_button = st.form_submit_button(label="Recomendar Livro")

if recommend_button:
    book = recommend_book(preferred_genre, min_hype)
    if book is not None:
        st.success(f"📚 **Recomendação:** *{book['Title']}* por {book['Genre']}")
        st.write(f"**Gênero:** {book['Genre']}")
        st.write(f"**Número de Páginas:** {book['Pages']}")
        st.write(f"**Hype:** {book['Hype']} ⭐️")
    else:
        st.warning("Nenhum livro encontrado com os critérios selecionados.")

st.markdown("---")

# Seção para exibir a lista atual de livros
st.header("Sua Lista TBR Atual")
df = load_data()
if not df.empty:
    st.dataframe(df)
else:
    st.info("Sua lista TBR está vazia. Adicione alguns livros para começar.")
