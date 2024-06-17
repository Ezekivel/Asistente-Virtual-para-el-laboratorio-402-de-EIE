import openai
from openai import OpenAI
import config
import typer
import requests
from rich import print
from rich.table import Table
client = OpenAI(api_key=config.api_key)

def main():
    

    # Tabla de bienvenida
    print("[bold green]Bienvenido a ChatGPT [/bold green]")
    tabla = Table("[blue]Comando[/blue]", "[blue]Descripción[/blue]")
    tabla.add_row("Salir", "Cierra el programa")
    tabla.add_row("Nuevo chat", "Crea una nueva conversación")
    tabla.add_row("Buscar", "Busca lo solicitado, pero en la web")
    print(tabla)

    # Rol a cumplir para ChatGPT
    contexto = {"role": "system",
                "content": "Eres un experto en inteligencia artificial."}
    messages = [contexto]

    while True:
        try:
            content = __prompt()

            # Si se quiere crear una nueva conversación
            if content == "Nuevo chat":
                print("[bold]¡Se creó una nueva conversación![/bold]")
                messages = [contexto]
                while True:
                    content = __prompt()
                    if content == "Nuevo chat":
                        print("[bold]¡Se creó una nueva conversación![/bold]")
                        messages = [contexto]
                    else:
                        break

            # Si se quiere realizar una búsqueda en internet
            if content.startswith("Buscar"):
                search_query = content[len("Buscar"):].strip()
                if search_query:
                    print("Realizando la búsqueda...")
                    search_results = buscar_en_internet(search_query)
                    response_content = procesar_resultados(search_results)
                    messages.append({"role": "assistant", "content": response_content})

            # Para que guarde el contexto de la pregunta
            messages.append({"role": "user", "content": content})

            # Modelo a utilizar
            response = client.chat.completions.create(model="gpt-4", messages=messages, temperature=0, max_tokens=1000)

            # Para escoger solo 1 respuesta
            response_content = response.choices[0].message.content

            # Para que guarde el contexto de la respuesta
            messages.append({"role": "assistant", "content": response_content})

            print(f"[gray]{response_content}[/gray]")

        except (requests.exceptions.RequestException, openai.APIConnectionError):
            print(f"[bold red]Lo siento, no hay conexión a internet[/bold red]")


def __prompt() -> str:
    prompt = typer.prompt("\n¡Hola! ¿Cómo puedo ayudarte?")

    if prompt == "Salir":
        print("[bold green]Espero haberte ayudado.[/bold green]")
        raise typer.Abort()
    return prompt


def buscar_en_internet(query: str) -> str:
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": config.custom_search,
        "cx": config.custom_search_cx,
        "q": query,
    }

    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f"No se pudieron obtener resultados para: {query}"


def procesar_resultados(resultados):
    # Si hubo un error en la búsqueda, devuelve el mensaje de error
    if "error" in resultados:
        return resultados["error"]

    # Si no hubo error pero tampoco se encontraron resultados
    items = resultados.get('items')
    if not items:
        return "No se encontraron resultados para tu búsqueda."

    # Si se encontraron resultados, procesa los datos
    respuestas = []
    for item in items[:5]:
        respuesta = item['title'] + ": " + item['snippet']
        if 'link' in item:
            respuesta += " Más información"
        respuestas.append(respuesta)
    return "\n".join(respuesta)

if __name__ == "__main__":
    typer.run(main)
