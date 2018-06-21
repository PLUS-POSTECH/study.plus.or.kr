from functools import reduce
import json
from typing import Dict, List, NamedTuple, Optional

from django.contrib.auth import get_user_model
from django.utils import timezone

from problem.models import ProblemInstance, ProblemAuthLog

User = get_user_model()


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


class ProblemState(NamedTuple):
    solve_count: int
    first_solve: Optional[User]


class UserState(NamedTuple):
    solved_problems: List[ProblemInstance]
    last_auth: Optional[timezone.datetime]


class ReplayState(NamedTuple):
    datetime: Optional[timezone.datetime]
    user_states: Dict[User, UserState]
    problem_states: Dict[ProblemInstance, ProblemState]


class AuthReplay:
    def __init__(self, problem_list, crunch_timedelta):
        self.problem_list = problem_list
        self.problem_instances = ProblemInstance.objects.filter(problem_list=problem_list)
        self.state = ReplayState(
            datetime=None,
            user_states={},
            problem_states={}
        )
        self.crunch_timedelta = crunch_timedelta

    def process_crunch(self, logs, datetime):
        problem_states = self.state.problem_states
        user_states = self.state.user_states
        solved_log_queries = []
        for problem_instance in self.problem_instances.all():
            correct_auth_key = problem_instance.problem.auth_key
            solve_logs = logs.filter(problem_instance=problem_instance, auth_key=correct_auth_key)
            solved_log_queries.append(solve_logs)

            first_solve_log = solve_logs.first() if solve_logs.exists() else None
            solve_count = solve_logs.count()

            first_solve_user = first_solve_log.user if first_solve_log is not None else None

            previous_state = problem_states.get(problem_instance, ProblemState(0, None))
            new_state = \
                ProblemState(
                    solve_count=previous_state.solve_count + solve_count,
                    first_solve=first_solve_user if previous_state.first_solve is None else previous_state.first_solve
                )

            problem_states[problem_instance] = new_state

        solve_logs = reduce(lambda x, y: x | y, solved_log_queries).order_by('datetime')
        users_with_logs = solve_logs.values_list('user', flat=True)

        for user in users_with_logs:
            previous_state = user_states.get(user, UserState([], None))
            user_solve_logs = solve_logs.filter(user=user)
            solved_problems = user_solve_logs.values_list('problem_instance', flat=True)
            last_auth = user_solve_logs.last().datetime

            user_states[user] = UserState(
                solved_problems=previous_state.solved_problems + solved_problems,
                last_auth=last_auth
            )

        self.state = ReplayState(
            datetime=datetime,
            user_states=user_states,
            problem_states=problem_states
        )

    def crunch(self):
        datetime_std = timezone.now() - self.crunch_timedelta
        logs = ProblemAuthLog.objects \
            .filter(problem_instance__in=self.problem_instances.all(), datetime_lte=datetime_std) \
            .order_by('datetime')

        if self.state.datetime is not None:
            logs = logs.filter(datetime__gt=self.state.datetime)

        self.process_crunch(logs, datetime_std)

    def calc_problem_points(self, problem_instance, state_diffs):
        problem_state = self.state.problem_states[problem_instance]
        problem_state_diff = state_diffs.get(problem_instance, None)
        solve_count = problem_state.solve_count
        first_solver = problem_state.first_solve

        if problem_state_diff is not None:
            solve_count += problem_state_diff.solve_count
            if first_solver is None:
                first_solver = problem_state_diff.first_solve

        if solve_count == 0:
            return

        default_points = problem_instance.points
        distributed_points = problem_instance.distributed_points / solve_count
        breakthrough_points = problem_instance.breakthrough_points

        return default_points + int(distributed_points), (first_solver, breakthrough_points)

    def calc_user_problem_points(self, user, problem_instance, problem_points, state_diffs):
        all_solved_problems = self.state.user_states[user].solved_problems + state_diffs[user].solved_problems
        if problem_instance not in all_solved_problems:
            return 0

        basic, (first_solver, breakthrough) = problem_points[problem_instance]
        return (basic + breakthrough) if (user == first_solver) else basic

    def get_statistic_data(self):
        if self.state.datetime is None:
            return [], []

        problem_state_diffs = {}
        user_state_diffs = {}

        problem_points = {}
        user_points = {}

        for problem_instance in self.state.problem_states:
            problem_points[problem_instance] = self.calc_problem_points(problem_instance, problem_state_diffs)

        for user, state in self.state.user_states.items():
            user_points[user] = \
                sum(map(
                    lambda x: self.calc_user_problem_points(user, x, problem_points, user_state_diffs),
                    state.solved_problems))

        crunched_datetime: timezone.datetime = self.state.datetime
        logs_to_replay = ProblemAuthLog.objects \
            .filter(
                problem_instance__in=self.problem_instances.all(),
                datetime__gt=crunched_datetime) \
            .order_by('datetime')

        def append_chart(timestamp):
            for chart_user, points in user_points.items():
                entry = chart_data.get(chart_user.username, [])
                entry.append({'x': timestamp.isoformat(), 'y': points})
                chart_data[chart_user.username] = entry

        chart_data = {}
        append_chart(crunched_datetime)

        for log in logs_to_replay:
            for user in user_points:
                user_points[user] -= self.calc_user_problem_points(
                    user, log.problem_instance, problem_points, user_state_diffs)

            prev_problem_state = problem_state_diffs.get(log.problem_instance, ProblemState(0, None))
            problem_state_diffs[log.problem_instance] = \
                ProblemState(
                    solve_count=prev_problem_state.solve_count + 1,
                    first_solve=prev_problem_state.first_solve
                    if prev_problem_state.first_solve is not None else
                    log.user
                )
            problem_points[log.problem_instance] = self.calc_problem_points(log.problem_instance, problem_state_diffs)

            for user in user_points:
                user_points[user] += self.calc_user_problem_points(
                    user, log.problem_instance, problem_points, user_state_diffs)

            prev_user_state = user_state_diffs.get(log.user, UserState([], None))
            user_state_diffs[log.user] = \
                UserState(
                    solved_problems=prev_user_state.solved_problems + [log.problem_instance],
                    last_auth=log.datetime
                )
            prev_point = user_points.get(log.user, 0)
            user_points[log.user] = prev_point + self.calc_user_problem_points(
                log.user, log.problem_instance, problem_points, user_state_diffs)

            append_chart(log.datetime)

        append_chart(timezone.now())

        def get_user_last_auth(rank_user):
            user_state_diff = user_state_diffs.get(rank_user, None)
            return self.state.user_states[rank_user].last_auth \
                if user_state_diff is None else \
                user_state_diff.last_auth

        rank_raw = list(map(lambda x: (x[0].username, x[1], get_user_last_auth(x[0])), user_points.items()))
        top10_rank = sorted(rank_raw, key=lambda x: (-x[1], x[2]))[:10]
        top10_users = list(map(lambda x: x[0], top10_rank))
        top10_chart_data = \
            map(lambda x: (x[0], json.dumps(x[1])),
                filter(lambda x: x[0] in top10_users, chart_data.items()))

        return top10_chart_data, top10_rank