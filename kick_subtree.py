# Imports do repositório da UTBots
import py_trees

from Behaviour_tree import commom_behaviours as cb
from Behaviour_tree.bob_manager import BobManager
from Behaviour_tree.commom_behaviours import actions as action_nodes
from Behaviour_tree.commom_behaviours import condition as condition_nodes
from Behaviour_tree.robot.bob import Bob

def get_kick_subtree(robot: Bob) -> py_trees.behaviour.Behaviour:
    # Nós de condição para efetuar o chute ao gol
    posse_da_bola = cb.condition.HasBall(robot) # Se tem a bola
    is_in_goalkeeper_area = cb.condition.Is_in_prohibited_area(robot)   # Está em área proibida
    visibilidade_gol = cb.condition.Goal_visibility(robot)  # Tem visibilidade para o gol
    ball_safety = cb.condition.BolaSegura(robot)    # A bola está segura (não corre o risco de ser roubada)
    distancia_gol = cb.condition.Goal_distance(robot)   # Está a uma certa distância predeterminada do gol

    # Nós de ação
    calculate_angular_position = cb.actions.Calculate_angular_target(robot) # Calcula a posição angular para o chute
    calculate_linear_position = cb.actions.Calculate_linear_target(robot)   # Calcula a posição angular para o chute
    alinhamento_angular = cb.actions.Angular_align(robot)   # Alinha o robô angularmente com o alvo
    alinhamento_linear = cb.actions.Move_node(robot)    # Move o robô para a posição linear calculada
    chutar_gol = cb.actions.Shoot_to_goal(robot)    # Chuta
    kick_subtree = py_trees.composites.Sequence(
        "chutar no gol",
        True,
        children=[  # Desenha a árvore
            posse_da_bola,
            is_in_goalkeeper_area,
            ball_safety,
            visibilidade_gol,
            distancia_gol,
            calculate_linear_position,
            alinhamento_linear,
            calculate_angular_position,
            alinhamento_angular,
            chutar_gol,
        ],
    )

    # kick_root = py_trees.trees.BehaviourTree(kick_subtree)
    # kick_root.setup()
    kick_subtree.setup()
    return kick_subtree
