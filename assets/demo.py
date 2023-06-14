from macq import generate, extract
from macq.observation import IdentityObservation

# print("\nGenerating traces...")
# traces = generate.pddl.VanillaSampling(problem_id=4398,
#                                        plan_len=20,
#                                        num_traces=10).traces

# print(dir(traces[0]))
# traces[0].print(view="color")

# print("\nExtracting model...")
# observations = traces.tokenize(IdentityObservation)
# model = extract.Extract(observations, extract.modes.OBSERVER)

# print("\nPrinting model...")
# model.to_pddl(domain_name="test-blocks", domain_filename="d.pddl", problem_filename="p.pddl")

# print("\nDone!\n")

from macq.observation import AtomicPartialObservation, ObservedTraceList
from macq.trace import Step, Fluent, Action, State

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

model = extract.Extract(obs, extract.modes.SLAF, debug=True)
print(model.details())
