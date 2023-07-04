
import inspect
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

from macq import generate, extract
from macq.observation import (
    IdentityObservation,
    AtomicPartialObservation,
    ObservedTraceList,
    ActionObservation,
    NoisyPartialDisorderedParallelObservation,
)
from macq.trace import (
    Step,
    Fluent,
    Action,
    State,
    PlanningObject,
    DisorderedParallelActionsObservationLists,
)

from macq.trace.disordered_parallel_actions_observation_lists import (
    default_theta_vec,
    num_parameters_feature,
    objects_shared_feature,
)


PROBLEM_ID = 1801

PREAMBLE = """
from macq import generate, extract
from macq.observation import (
    IdentityObservation,
    AtomicPartialObservation,
    ObservedTraceList,
    ActionObservation,
    NoisyPartialDisorderedParallelObservation,
)
from macq.trace import (
    Step,
    Fluent,
    Action,
    State,
    PlanningObject,
    DisorderedParallelActionsObservationLists,
)

from macq.trace.disordered_parallel_actions_observation_lists import (
    default_theta_vec,
    num_parameters_feature,
    objects_shared_feature,
)


PROBLEM_ID = 1801"""


def observer_example():
    print("\nGenerating traces...")
    traces = generate.pddl.VanillaSampling(
        problem_id=PROBLEM_ID, plan_len=20, num_traces=100
    ).traces

    traces[0].print(view="color")

    print("\nExtracting model...")
    observations = traces.tokenize(IdentityObservation)
    model = extract.Extract(observations, extract.modes.OBSERVER)

    print("\nPrinting model...")
    model.to_pddl(
        domain_name="test", domain_filename="d.pddl", problem_filename="p.pddl"
    )

    print("\nDone!\n")


def slaf_example():
    print("\nGenerating traces...")
    traces = generate.pddl.VanillaSampling(
        problem_id=PROBLEM_ID, plan_len=15, num_traces=1
    ).traces

    traces[0].print(view="color")

    print("\nExtracting model...")
    observations = traces.tokenize(AtomicPartialObservation, percent_missing=0.25)
    model = extract.Extract(observations, extract.modes.SLAF, debug=False, sample=False)

    print("\nPrinting model...")
    model.to_pddl(
        domain_name="test", domain_filename="d.pddl", problem_filename="p.pddl"
    )

    print("\nDone!\n")


def slaf_slides_example():
    f1 = Fluent("f1", [])
    f2 = Fluent("f2", [])

    a1 = Action("a1", [])
    a2 = Action("a2", [])

    s1 = State({f1: False, f2: True})
    s2 = State({f1: True, f2: False})
    s3 = State({f1: True, f2: False})

    st1 = Step(s1, a1, 1)
    st2 = Step(s2, a2, 2)
    st3 = Step(s3, None, 3)

    o1 = AtomicPartialObservation(st1)
    o2 = AtomicPartialObservation(st2, hide={f2})
    o3 = AtomicPartialObservation(st3)

    obs = ObservedTraceList(observations=[[o1, o2, o3]])

    model = extract.Extract(obs, extract.modes.SLAF, debug=False)
    print(model.details())


def amdn_example():
    print("\nGenerating traces...")
    traces = generate.pddl.VanillaSampling(
        problem_id=PROBLEM_ID, plan_len=20, num_traces=10, observe_pres_effs=True
    ).traces

    traces[0].print(view="color")

    print("\nExtracting model...")
    features = [objects_shared_feature, num_parameters_feature]
    learned_theta = default_theta_vec(2)
    observations = traces.tokenize(
        Token=NoisyPartialDisorderedParallelObservation,
        ObsLists=DisorderedParallelActionsObservationLists,
        features=features,
        learned_theta=learned_theta,
        percent_missing=0,
        percent_noisy=0,
        replace=True,
    )
    model = extract.Extract(
        observations, extract.modes.AMDN, debug=False, occ_threshold=2
    )

    print("\nPrinting model...")
    model.to_pddl(
        domain_name="test", domain_filename="d.pddl", problem_filename="p.pddl"
    )

    print("\nDone!\n")


def locm_example():
    print("\nGenerating traces...")
    traces = generate.pddl.VanillaSampling(
        problem_id=PROBLEM_ID, plan_len=50, num_traces=1
    ).traces

    traces[0].print(view="color")

    print("\nExtracting model...")
    observations = traces.tokenize(ActionObservation)
    model = extract.Extract(observations, extract.modes.LOCM, debug=False, viz=True)

    print("\nPrinting model...")
    model.to_pddl(
        domain_name="test", domain_filename="d.pddl", problem_filename="p.pddl"
    )

    print("\nDone!\n")


def locm_slides_example():
    print("\nGenerating traces...")

    c1 = PlanningObject("", "c1")
    c2 = PlanningObject("", "c2")
    c3 = PlanningObject("", "c3")
    j1 = PlanningObject("", "j1")
    j2 = PlanningObject("", "j2")
    wr1 = PlanningObject("", "wr1")
    wr2 = PlanningObject("", "wr2")

    a1 = Action("open", [c1])
    a2 = Action("fetch-jack", [j1, c1])
    a3 = Action("fetch-wrench", [wr1, c1])
    a4 = Action("close", [c1])
    a5 = Action("open", [c2])
    a6 = Action("fetch-wrench", [wr2, c2])
    a7 = Action("fetch-jack", [j2, c2])
    a8 = Action("close", [c2])
    a9 = Action("close", [c3])
    a10 = Action("open", [c3])

    s1 = ActionObservation(Step(None, a1, 1))
    s2 = ActionObservation(Step(None, a2, 2))
    s3 = ActionObservation(Step(None, a3, 3))
    s4 = ActionObservation(Step(None, a4, 4))
    s5 = ActionObservation(Step(None, a5, 5))
    s6 = ActionObservation(Step(None, a6, 6))
    s7 = ActionObservation(Step(None, a7, 7))
    s8 = ActionObservation(Step(None, a8, 8))
    s9 = ActionObservation(Step(None, a9, 9))
    s10 = ActionObservation(Step(None, a10, 10))

    obs = ObservedTraceList(observations=[[s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]])

    model = extract.Extract(obs, extract.modes.LOCM, viz=True)

    print("\nPrinting model...")
    model.to_pddl(
        domain_name="test", domain_filename="d.pddl", problem_filename="p.pddl"
    )

    print("\nDone!\n")


def main():
    # Ask the user which example they want to run.
    print("\nWhich example would you like to see?")
    print("1. Observer")
    print("2. SLAF")
    print("3. AMDN")
    print("4. LOCM")
    inp = input("\nEnter a number: ")
    print()

    assert inp in ["1", "2", "3", "4"], "Invalid input. Exiting."

    if inp in ["2", "4"]:
        # Ask if simple or slides example.
        print("Which example would you like to run?")
        print("1. Simple")
        print("2. Slides")
        inp2 = input("\nEnter a number: ")
        print()

        assert inp2 in ["1", "2"], "Invalid input. Exiting."

    if inp == "1":
        func = observer_example
        code = inspect.getsource(observer_example) + "\n" + "observer_example()"
    elif inp == "2" and inp2 == "1":
        func = slaf_example
        code = inspect.getsource(slaf_example) + "\n" + "slaf_example()"
    elif inp == "2" and inp2 == "2":
        func = slaf_slides_example
        code = inspect.getsource(slaf_slides_example) + "\n" + "slaf_slides_example()"
    elif inp == "3":
        func = amdn_example
        code = inspect.getsource(amdn_example) + "\n" + "amdn_example()"
    elif inp == "4" and inp2 == "1":
        func = locm_example
        code = inspect.getsource(locm_example) + "\n" + "locm_example()"
    elif inp == "4" and inp2 == "2":
        func = locm_slides_example
        code = inspect.getsource(locm_slides_example) + "\n" + "locm_slides_example()"
    else:
        print("Invalid input. Exiting.")
        exit(1)


    # Prompt to see if they'd like to see the code, write it to run.py, or exit.
    print("Would you like to see the code, write it to run.py, or exit?")
    print("1. See the code")
    print("2. Write to run.py")
    print("3. Run the code")
    print("4. Exit")
    inp = input("\nEnter a number: ")

    assert inp in ["1", "2", "3", "4"], "Invalid input. Exiting."

    if inp == "1":
        print("\nCode:\n")
        highlighted_code = highlight(code, PythonLexer(), TerminalFormatter())
        print(highlighted_code)
    elif inp == "2":
        with open("run.py", "w") as f:
            f.write(PREAMBLE+"\n\n"+code)
        print("\nWrote code to run.py\n")
    elif inp == "3":
        func()
    else:
        print("\nExiting.\n")


if __name__ == "__main__":
    main()
