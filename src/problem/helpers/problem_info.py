from typing import NamedTuple, Optional

from django.contrib.auth import get_user_model

from problem.models import ProblemInstance
from .score import calculate_problem_score

User = get_user_model()


class UserProblemInfo(NamedTuple):
    user: User
    problem_instance: ProblemInstance
    solved: bool
    first_solver: Optional[User]
    solver_count: int
    solver_list: list
    effective_points: int

    def display_first_solve(self):
        return self.first_solver is None or self.user == self.first_solver


def get_user_problem_info(user, problem_instance):
    solved_log = problem_instance.problemauthlog_set \
        .filter(auth_key=problem_instance.problem.auth_key) \
        .order_by('datetime')

    first_solver = solved_log.first().user if solved_log.exists() else None
    solved = solved_log.filter(user=user).exists()
    solve_count = solved_log.count()
    solve_user_list = list(map(lambda x: x.user.username, solved_log))
    effective_solve_count = solve_count + (0 if solved else 1)
    first_blood = first_solver is None or user == first_solver
    points = calculate_problem_score(problem_instance, effective_solve_count, first_blood)

    return UserProblemInfo(user, problem_instance, solved, first_solver, solve_count, solve_user_list, points)


def get_problem_list_user_info(problem_list, user):
    problem_instances = problem_list.probleminstance_set.order_by('points', 'problem__title')
    problem_info = []
    user_score = 0
    for problem_instance in problem_instances:
        info = get_user_problem_info(user, problem_instance)
        if info.solved:
            user_score += info.effective_points
        problem_info.append(info)

    return problem_info, user_score


def get_problem_instance_score(problem_instance, fixed=False):  # no first blood points in account
    if fixed:
        return problem_instance.points

    solved_log = problem_instance.problemauthlog_set \
        .filter(auth_key=problem_instance.problem.auth_key) \
        .order_by('datetime')
    solve_count = solved_log.count()
    return calculate_problem_score(problem_instance, solve_count, False)


def get_problem_list_user_score(problem_list, user, fixed=False):
    problem_instances = problem_list.probleminstance_set.order_by('points', 'problem__title')
    user_score = 0
    for problem_instance in problem_instances:
        solved = problem_instance.problemauthlog_set.filter(user=user, auth_key=problem_instance.problem.auth_key).exists()
        if solved:
            user_score += get_problem_instance_score(problem_instance, fixed)

    return user_score

def get_problem_list_total_score(problem_list, fixed=False):  # no first blood points in account
    problem_instances = problem_list.probleminstance_set.all()
    total = 0
    for problem_instance in problem_instances:
        total += get_problem_instance_score(problem_instance, fixed)
    return total
