from macq import generate, extract
from macq.observation import IdentityObservation

traces = generate.pddl.VanillaSampling(problem_id=4398, plan_len=20, num_traces=10).traces

print(dir(traces[0]))
traces[0].print(view="color")

observations = traces.tokenize(IdentityObservation)
model = extract.Extract(observations, extract.modes.OBSERVER)

# print(model.details())
