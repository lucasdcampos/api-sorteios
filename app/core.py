import random
from app.db import SupabaseDB
from app.models import SorteioRequest, VagaUnidadeAtribuida

db = SupabaseDB()

def realizar_sorteio(request: SorteioRequest):
    """
    Função principal que executa o sorteio.
    1. Busca as vagas e unidades do condomínio.
    2. Remove as que já foram atribuídas.
    3. Realiza o sorteio com base nas regras de compatibilidade por torre.
    4. Retorna a lista de atribuições sorteadas.
    """

    todas_vagas = db.get_vagas(request.condominio_id)
    todas_unidades = db.get_unidades(request.condominio_id)

    vagas_disponiveis = filtrar_vagas_disponiveis(todas_vagas, request.vagas_atribuidas)
    unidades_disponiveis = filtrar_unidades_disponiveis(todas_unidades, request.vagas_atribuidas)

    return sortear_vagas_para_unidades(vagas_disponiveis, unidades_disponiveis)

def sortear_vagas_para_unidades(vagas, unidades):
    """
    Associa vagas disponíveis a unidades disponíveis de forma aleatória.
    - Considera a compatibilidade entre vaga e unidade com base na torre (id_torre).
    - Garante que cada unidade seja sorteada apenas uma vez.
    - Retorna uma lista de objetos VagaUnidadeAtribuida.
    """

    random.shuffle(vagas)
    random.shuffle(unidades)

    unidades_restantes = unidades.copy()
    sorteios = []

    for vaga in vagas:
        unidade_compativel = selecionar_unidade_compativel(vaga, unidades_restantes)

        if not unidade_compativel:
            continue

        sorteio = VagaUnidadeAtribuida(
            vaga_id=vaga["vaga_id"],
            unidade_id=unidade_compativel["unid_id"]
        )
        sorteios.append(sorteio)

        # Remove a unidade sorteada
        unidades_restantes = [u for u in unidades_restantes if u["unid_id"] != unidade_compativel["unid_id"]]

    return sorteios


def selecionar_unidade_compativel(vaga, unidades):
    """
    Seleciona uma unidade compatível com a vaga:
    - Se a vaga tem um id_torre definido, seleciona apenas unidades com o mesmo id_torre.
    - Se a vaga não tem torre, qualquer unidade disponível pode ser escolhida.
    - Retorna uma unidade aleatória compatível, ou None se não houver compatíveis.
    """

    if vaga.get("id_torre") is not None:
        candidatas = [u for u in unidades if u.get("id_torre") == vaga.get("id_torre")]
    else:
        candidatas = unidades

    if not candidatas:
        return None

    return random.choice(candidatas)

def filtrar_vagas_disponiveis(vagas, vagas_atribuidas):
    """
    Remove da lista de vagas todas aquelas que já foram atribuídas previamente.
    - Compara os IDs das vagas com a lista de vagas_atribuidas.
    - Retorna a lista de vagas disponíveis para sorteio.
    """

    vagas_atribuidas_ids = {v.vaga_id for v in vagas_atribuidas}
    return [vaga for vaga in vagas if vaga["vaga_id"] not in vagas_atribuidas_ids]


def filtrar_unidades_disponiveis(unidades, vagas_atribuidas):
    """
    Remove da lista de unidades todas aquelas que já receberam uma vaga previamente.
    - Compara os IDs das unidades com a lista de vagas_atribuidas.
    - Retorna a lista de unidades disponíveis para sorteio.
    """

    unidades_atribuidas_ids = {v.unidade_id for v in vagas_atribuidas}
    return [unidade for unidade in unidades if unidade["unid_id"] not in unidades_atribuidas_ids]
