import os
import stat
import mimetypes
import pwd
import grp
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.prompt import Prompt, Confirm

log = print
get = input
console = Console()

meses = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
]

def permissao_para_string(permissoes):
    return ", ".join([
        "Leitura" if permissoes[0] == 'r' else "Sem leitura",
        "Escrita" if permissoes[1] == 'w' else "Sem escrita",
        "Execução" if permissoes[2] == 'x' else "Sem execução"
    ])

def formatar_data(timestamp):
    tm = time.localtime(timestamp)
    mes_completo = meses[tm.tm_mon - 1]
    return (
        f"{tm.tm_mday} de {mes_completo} de {tm.tm_year}, "
        f"{tm.tm_hour:02d}h {tm.tm_min:02d}min {tm.tm_sec:02d}s"
    )

def bool_colorido(valor, positivo="Sim", negativo="Não"):
    return f"[green]{positivo}[/green]" if valor else f"[red]{negativo}[/red]"
    
# TIPO DE ÍCONES FEATURE
def icone_tipo(caminho):
    if not os.path.exists(caminho):
        return "⚠️"
    if os.path.islink(caminho):
        return "🔗"
    if os.path.isdir(caminho):
        return "📁"

    nome = os.path.basename(caminho).lower()
    tipo, _ = mimetypes.guess_type(caminho)

    if nome.endswith(".py"):
        return "🐍"
    if nome.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp")):
        return "🖼️"
    if nome.endswith((".mp4", ".avi", ".mov", ".mkv")):
        return "📹"
    if nome.endswith((".mp3", ".wav", ".ogg", ".flac")):
        return "🎵"
    if nome.endswith((".zip", ".rar", ".tar", ".gz", ".7z")):
        return "🗃️"
    if nome.endswith((".txt", ".md", ".log")):
        return "📜"
    if nome.endswith((".csv", ".xls", ".xlsx")):
        return "📊"
    if nome.endswith((".pdf", ".doc", ".docx")):
        return "📝"
    if tipo and tipo.startswith("image/"):
        return "🖼️"
    if tipo and tipo.startswith("video/"):
        return "📹"
    if tipo and tipo.startswith("audio/"):
        return "🎵"
    if tipo and tipo.startswith("text/"):
        return "📜"

    return "📄"  # Padrão para arquivos desconhecidos
    
def mostrar_propriedades(caminho):
    if not os.path.exists(caminho):
        console.print("[red]⚠️ Arquivo ou pasta não existe.[/red]")
        return

    estat = os.stat(caminho)
    modo = estat.st_mode
    permissoes = stat.filemode(modo)
    tipo, _ = mimetypes.guess_type(caminho)

    dono_perms = permissao_para_string(permissoes[1:4])
    grupo_perms = permissao_para_string(permissoes[4:7])
    outros_perms = permissao_para_string(permissoes[7:10])

    icone = icone_tipo(caminho)
    titulo = f"{icone} {os.path.basename(caminho)}"

    console.rule(f"[bold blue]Propriedades de: {titulo}")

    console.print(Panel.fit(
        f"[bold]Caminho:[/] {os.path.abspath(caminho)}\n"
        f"[bold]Tamanho:[/] {estat.st_size} bytes\n"
        f"[bold]Tipo (MIME):[/] {tipo or 'Desconhecido'}",
        title="📦 Informações Básicas",
        style="cyan"
    ))

    console.print(Panel.fit(
        f"[bold]Dono:[/] {pwd.getpwuid(estat.st_uid).pw_name}\n"
        f"[bold]Grupo:[/] {grp.getgrgid(estat.st_gid).gr_name}\n\n"
        f"[bold]Permissões do dono:[/] {dono_perms}\n"
        f"[bold]Permissões do grupo:[/] {grupo_perms}\n"
        f"[bold]Permissões de outros:[/] {outros_perms}",
        title="🔐 Permissões e Acesso",
        style="magenta"
    ))

    console.print(Panel.fit(
        f"[bold]Criado:[/] {formatar_data(estat.st_ctime)}\n"
        f"[bold]Modificado:[/] {formatar_data(estat.st_mtime)}\n"
        f"[bold]Último acesso:[/] {formatar_data(estat.st_atime)}",
        title="⏰ Datas",
        style="yellow"
    ))

    console.print(Panel.fit(
        f"[bold]📁 É diretório:[/] {bool_colorido(os.path.isdir(caminho))}\n"
        f"[bold]🔗 É link simbólico:[/] {bool_colorido(os.path.islink(caminho))}\n"
        f"[bold]📄 É arquivo:[/] {bool_colorido(os.path.isfile(caminho))}",
        title="🧭 Tipo de Objeto",
        style="green"
    ))
    
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
import os

console = Console()

EXTENSOES_VISUALIZAVEIS = {
    '.txt': 'text',
    '.md': 'markdown',
    '.json': 'json',
    '.log': 'text',
    '.ini': 'ini',
    '.csv': 'text',
    '.py': 'python'
}

def visualizar_conteudo(caminho):
    _, ext = os.path.splitext(caminho)
    linguagem = EXTENSOES_VISUALIZAVEIS.get(ext)

    if not linguagem:
        console.print(f"[yellow]⚠️ Visualização não suportada para essa extensão: {ext}[/yellow]")
        return

    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        syntax = Syntax(conteudo, linguagem, theme="monokai", line_numbers=True)

        painel = Panel(
            syntax,
            title=f"[bold cyan]Visualizando: {os.path.basename(caminho)}[/bold cyan]",
            border_style="bold magenta",
            padding=(1, 2)
        )

        console.print(painel)

    except Exception as e:
        console.print(f"[red]❌ Erro ao ler o arquivo:[/red] {e}")
        
##############################   
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
import time
import datetime

class DeslumbranteLogger(FileSystemEventHandler):
    
    def __init__(self, log_path):
        self.log_path = log_path

    def registrar_log(self, mensagem_pura):
        
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(mensagem_pura + "\n")

    def on_any_event(self, event):
        tipo = event.event_type.upper()
        cor = "blue" if tipo == "MODIFIED" else "green" if tipo == "CREATED" else "red"
        caminho = event.src_path

        mensagem_visual = f"[{tipo}] {caminho}"
        mensagem_pura = f"{datetime.datetime.now().isoformat()} [{tipo}] {caminho}"

        painel = Panel(Text(mensagem_visual, style=f"bold {cor}"), title="[bold magenta]LOG MONITORAMENTO[/bold magenta]", border_style=cor)
        console.print(painel)

        self.registrar_log(mensagem_pura)

##############################

def iniciar_monitoramento(caminho):
    
    salvar = Confirm.ask("[cyan]Deseja salvar os logs em arquivo?[/cyan]", default=True)
    log_path = None

    if salvar:
        sugestao_nome = f"monitor_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        sugestao_path = os.path.join(os.path.expanduser("~"), sugestao_nome)
        
		#LOG_PATH INPUT VAR
        caminho_log = Prompt.ask(
            "[cyan]Digite o caminho completo do arquivo ou pressione Enter para usar o padrão[/cyan]",
            default=sugestao_path
        ).strip()

        dir_log = os.path.dirname(caminho_log)
        if not os.path.isdir(dir_log):
            console.print(f"[red]⚠️ Diretório '{dir_log}' não existe. Criando automaticamente...[/red]")
            try:
                os.makedirs(dir_log, exist_ok=True)
                console.print(f"[green]✔ Diretório '{dir_log}' criado com sucesso.[/green]")
            except Exception as e:
                console.print(f"[red]❌ Erro ao criar diretório: {e}[/red]")
                return

        log_path = caminho_log
        
	#OBSERVER HANDLER SETTINGS
    event_handler = DeslumbranteLogger(log_path=log_path)
    
    #OBSERVER LAUCHING
    observer = Observer()
    observer.schedule(event_handler, path=caminho, recursive=True)
    observer.start()

    console.print(f"[bold green]✔ Monitorando mudanças em:[/bold green] {caminho}")
    if log_path:
        console.print(f"[white]Logs sendo salvos em: [bold yellow]{log_path}[/bold yellow][/white]")
    else:
        console.print("[bold yellow]Logs visíveis apenas no console.[/bold yellow]")

##############################

def explorar_diretorio(pasta_inicial):
    atual = os.path.abspath(pasta_inicial)
    iniciar_monitoramento(atual)

    while True:
        try:
            itens = os.listdir(atual)
        except Exception as e:
            console.print(f"[red]⚠️ Erro ao acessar o diretório: {e}[/red]")
            return None

        aplicar_filtros = Confirm.ask("\n[bold cyan]Deseja aplicar filtros personalizados antes de exibir os arquivos?[/bold cyan]", default=True)

        filtro_nome = ""
        filtro_extensao = ""
        tamanho_min_mb = 0.0

        if aplicar_filtros:
            filtro_nome = Prompt.ask("\n[cyan]Filtro por nome (Enter para ignorar)[/cyan]", default="").strip().lower()
            filtro_extensao = Prompt.ask("[cyan]Filtro por extensão, ex: .py (Enter para ignorar)[/cyan]", default="").strip().lower()
            filtro_tamanho = Prompt.ask("[cyan]Filtro por tamanho mínimo em MB (Enter para ignorar)[/cyan]", default="").strip()
            try:
                tamanho_min_mb = float(filtro_tamanho) if filtro_tamanho else 0.0
            except ValueError:
                console.print("[red]⚠️ Tamanho inválido, ignorando filtro de tamanho.[/red]")
                tamanho_min_mb = 0.0

        itens_filtrados = []
        for nome in itens:
            caminho = os.path.join(atual, nome)
            if not os.path.exists(caminho): continue

            nome_lower = nome.lower()
            tamanho_mb = os.path.getsize(caminho) / (1024 * 1024)

            if filtro_nome and filtro_nome not in nome_lower:
                continue
            if filtro_extensao and not nome_lower.endswith(filtro_extensao):
                continue
            if tamanho_mb < tamanho_min_mb:
                continue

            itens_filtrados.append(nome)

        itens_filtrados.sort()
        table = Table(title=f"[bold]Conteúdo de {atual}", header_style="bold blue")
        table.add_column("Índice", justify="right")
        table.add_column("Nome", justify="left")
        table.add_column("Tipo", justify="center")

        table.add_row("0", "[..] Voltar", "📁 Pasta")

        for i, nome in enumerate(itens_filtrados, start=1):
            caminho_completo = os.path.join(atual, nome)
            tipo = icone_tipo(caminho_completo)
            table.add_row(str(i), nome, tipo)

        if not itens_filtrados:
            console.print("[yellow]Nenhum item corresponde aos filtros aplicados.[/yellow]")
            continue

        console.print(table)

        try:
            escolha = Prompt.ask("\nEscolha um índice ou [bold magenta]Enter[/bold magenta] para cancelar", default="")
            if escolha.strip() == "":
                return None

            idx = int(escolha)
            if idx == 0:
                novo = os.path.dirname(atual)
                if novo != atual:
                    atual = novo
            elif 1 <= idx <= len(itens_filtrados):
                selecionado = os.path.join(atual, itens_filtrados[idx - 1])
                if os.path.isdir(selecionado):
                    atual = selecionado
                else:
                    acao = Prompt.ask(
                        "\n[cyan]Deseja[/cyan] [bold green](V)[/bold green]isualizar propriedades, [bold yellow](A)[/bold yellow]brir arquivo ou [bold red](C)[/bold red]ancelar?",
                        choices=["V", "A", "C"], default="V"
                    ).upper()

                    if acao == "V":
                        return selecionado
                    elif acao == "A":
                        visualizar_conteudo(selecionado)
                    else:
                        console.print("[yellow]Ação cancelada.[/yellow]")
            else:
                console.print("[red]⚠️ Índice inválido[/red]")
        except Exception as e:
            console.print(f"[red]⚠️ Erro: {e}[/red]")
                        
# Execução principal
if __name__ == "__main__":
    
    console.print("[bold cyan]Navegue até o arquivo ou pasta que deseja inspecionar, (.) para o actual:[/bold cyan]")
    
    caminho0 = get(":")
    caminho = explorar_diretorio(caminho0)
    if caminho:
        mostrar_propriedades(caminho)
    else:
        console.print("[yellow]Nenhum item selecionado.[/yellow]")