from problem.models import ProblemInstance, ProblemAuthLog


def get_problem_list_info(problem_list, user):
    problem_instances = ProblemInstance.objects.filter(problem_list=problem_list)
    problem_info = []
    user_score = 0
    for problem_instance in problem_instances:
        solved_log = ProblemAuthLog.objects \
            .filter(problem_instance=problem_instance, auth_key=problem_instance.problem.auth_key) \
            .order_by('datetime')

        first_solved_log = solved_log.first() if solved_log.exists() else None
        solved = solved_log.filter(user=user).exists()
        solved_count = solved_log.count()
        first_blood = first_solved_log is None or user == first_solved_log.user
        points = problem_instance.points
        points += problem_instance.distributed_points / (solved_count + (0 if solved else 1))
        points += problem_instance.breakthrough_points if first_blood else 0
        if solved:
            user_score += points
        problem_info.append((problem_instance, int(points), solved, first_blood))

    return problem_info, int(user_score)
