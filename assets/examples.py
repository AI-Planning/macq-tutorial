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
    DisorderedParallelActionsObservationLists,
)

from macq.trace.disordered_parallel_actions_observation_lists import (
    default_theta_vec,
    num_parameters_feature,
    objects_shared_feature,
)


PROBLEM_ID = 1801


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
        domain_name="test-blocks", domain_filename="d.pddl", problem_filename="p.pddl"
    )

    print("\nDone!\n")


def slaf_example():
    print("\nGenerating traces...")
    traces = generate.pddl.VanillaSampling(
        problem_id=PROBLEM_ID, plan_len=20, num_traces=1
    ).traces

    traces[0].print(view="color")

    print("\nExtracting model...")
    observations = traces.tokenize(AtomicPartialObservation, percent_missing=0.25)
    model = extract.Extract(observations, extract.modes.SLAF)

    print("\nPrinting model...")
    model.to_pddl(
        domain_name="test-blocks", domain_filename="d.pddl", problem_filename="p.pddl"
    )

    print("\nDone!\n")


def slaf_simple_example():
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
        problem_id=PROBLEM_ID, plan_len=20, num_traces=10
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
        domain_name="test-blocks", domain_filename="d.pddl", problem_filename="p.pddl"
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
    model = extract.Extract(observations, extract.modes.LOCM, debug=True)

    print("\nPrinting model...")
    model.to_pddl(
        domain_name="test-blocks", domain_filename="d.pddl", problem_filename="p.pddl"
    )

    print("\nDone!\n")


def main():
    # Ask the user which example they want to run.
    print("Which example would you like to run?")
    print("1. Observer")
    print("2. SLAF")
    print("3. AMDN")
    print("4. LOCM")
    inp = input("\nEnter a number: ")
    print()

    if inp == "1":
        observer_example()
    elif inp == "2":
        slaf_example()
    elif inp == "3":
        amdn_example()
    elif inp == "4":
        locm_example()
    else:
        print("Invalid input. Exiting.")
        exit(1)


if __name__ == "__main__":
    main()
